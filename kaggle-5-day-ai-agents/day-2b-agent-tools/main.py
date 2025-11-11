
# day-2b-agent-tools/main.py
"""
Day 2B - Agent Tools: Best Practices

Demonstrates:
 - tool chaining (search -> extract -> function tool -> summarize)
 - input validation for function tools
 - retry config and run_config usage
 - basic caching and error handling
 - safe extraction of model/tool outputs
"""

import os
import asyncio
import logging
import time
from typing import Any, Dict
from dotenv import load_dotenv

# ADK imports
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.adk.tools.function_tool import FunctionTool
from google.genai import types

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# --- Load env & validate key ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env. Create .env from .env.example")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

logging.info("✅ API key loaded, ADK environment ready.")

# --- Small utility helpers ---
def safe_str(val: Any) -> str:
    try:
        return str(val)
    except Exception:
        return ""

def extract_text(obj: Any) -> str:
    # ADK responses can be many shapes; this is conservative
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        for k in ("text", "content", "message", "output"):
            if k in obj and obj[k]:
                return safe_str(obj[k])
        # fall back to repr
        return repr(obj)[:1000]
    if hasattr(obj, "content"):
        cont = getattr(obj, "content")
        if hasattr(cont, "parts") and cont.parts:
            p = cont.parts[0]
            if hasattr(p, "text"):
                return safe_str(p.text)
    return safe_str(obj)

# --- Simple cache to avoid repeated expensive calls (demo) ---
SIMPLE_CACHE: Dict[str, Any] = {}

def cache_get(key: str):
    return SIMPLE_CACHE.get(key)

def cache_set(key: str, value: Any, ttl: int = 300):
    SIMPLE_CACHE[key] = value
    # TTL omitted for brevity in demo; production would track expiry.

# --- Function tools with validation & safe execution ---
def safe_add(a, b):
    # validate numeric inputs
    try:
        a_f = float(a)
        b_f = float(b)
    except Exception:
        raise ValueError("safe_add: inputs must be numeric.")
    return a_f + b_f

def safe_extract_number(text: str):
    # simple parser to extract first number in text; demo-level only
    import re
    m = re.search(r"([-+]?\d*\.?\d+)", safe_str(text))
    if not m:
        raise ValueError("safe_extract_number: no numeric value found")
    return float(m.group(1))

# Wrap them as FunctionTool instances
add_tool = FunctionTool(safe_add)
extract_number_tool = FunctionTool(safe_extract_number)

# --- Retry / run config ---
retry_options = types.HttpRetryOptions(
    attempts=5,
    exp_base=3,
    initial_delay=1,
    http_status_codes=[429, 500, 502, 503, 504],
)
run_config = types.RunConfig(retry_options=retry_options, timeout=30)

# --- Agent definition ---
root_agent = Agent(
    name="best_practices_agent",
    model="gemini-2.5-flash-lite",
    description="Agent demonstrating safe tool chaining, validation, retries, and caching.",
    instruction=(
        "You are a careful AI assistant. When calling tools, validate inputs, "
        "prefer cached results when available, and always return structured summaries."
    ),
    tools=[add_tool, extract_number_tool, google_search],
)

runner = InMemoryRunner(agent=root_agent, app_name="agents", run_config=run_config)
logging.info("✅ Agent and runner created with retry config.")

# --- Higher-level helper to run with safety & extract text ---
async def run_and_extract(prompt: str):
    key = f"resp:{prompt}"
    cached = cache_get(key)
    if cached:
        logging.info("→ returning cached result")
        return cached

    try:
        raw = await runner.run_debug(prompt, run_config=run_config)
        # attempt to extract meaningful text
        if hasattr(raw, "__aiter__"):
            parts = []
            async for ev in raw:
                txt = extract_text(ev)
                if txt:
                    parts.append(txt)
            result = "\n".join(parts).strip()
        elif isinstance(raw, (list, tuple)):
            parts = [extract_text(r) for r in raw if extract_text(r)]
            result = "\n".join(parts).strip()
        else:
            result = extract_text(raw)
        cache_set(key, result)
        return result
    except Exception as e:
        logging.error("Agent run error: %s", e)
        raise

# --- Example workflow: chained tools ---
async def chained_workflow(query: str):
    logging.info("Running chained workflow for query: %s", query)

    # 1) Attempt to get a cached search summary
    cache_key = "search:" + query
    cached = cache_get(cache_key)
    if cached:
        logging.info("Using cached search result")
        search_summary = cached
    else:
        # 2) Run a guided search via the agent (agent may choose to use google_search tool)
        prompt = (
            f"Search the web for the latest concise summary about: {query}\n"
            "Return a short 3-sentence summary with bullet points if possible."
        )
        search_summary = await run_and_extract(prompt)
        cache_set(cache_key, search_summary)

    logging.info("Search summary:\n%s", search_summary or "<empty>")

    # 3) Ask agent to extract a numeric metric from the summary (use function tool chaining)
    try:
        extract_prompt = (
            f"From the following text, extract the first numeric value you can find, and return it only:\n\n{search_summary}"
        )
        extracted_text = await run_and_extract(extract_prompt)
        # try to parse number using the extract_number tool directly via the agent (function tool)
        logging.info("Agent extracted (raw): %s", extracted_text)
        # use the extract tool via runner (explicit tool call by sending prompt that triggers tool)
        # For demo, call runner with instruction to call the function tool
        num_prompt = f"Extract number from: {extracted_text}"
        num_resp = await run_and_extract(num_prompt)
        logging.info("Number parsing result: %s", num_resp)
    except Exception as e:
        logging.warning("Failed to extract numeric metric: %s", e)
        num_resp = None

    # 4) Summarize final answer
    final_prompt = (
        "You are an assistant that synthesizes findings. Based on the search summary and extracted metric, "
        f"produce a short, structured final answer for the user.\n\nSEARCH SUMMARY:\n{search_summary}\n\nEXTRACTED_METRIC:\n{num_resp}"
    )
    final = await run_and_extract(final_prompt)
    logging.info("Final answer:\n%s", final)
    return final

# --- Demo runner ---
async def demo():
    queries = [
        "2024 Nobel Prize in Physics winners summary",
        "recent advances in multi-agent systems",
    ]
    for q in queries:
        logging.info("=== DEMO QUERY: %s ===", q)
        try:
            out = await chained_workflow(q)
            print("\n--- FINAL OUTPUT ---\n")
            print(out)
            print("\n--------------------\n")
            # gentle pause to avoid hitting rate limits during demo
            time.sleep(1.0)
        except Exception as e:
            logging.error("Demo workflow failed for '%s': %s", q, e)

if __name__ == "__main__":
    asyncio.run(demo())