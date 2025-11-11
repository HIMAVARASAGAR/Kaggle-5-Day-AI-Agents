# main.py (robust consumer for runner.run_debug)
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please add it to your .env file.")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

print("✅ API key loaded successfully!\n")

# ADK imports
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

# Create agent + runner (set app_name to silence mismatch warning if desired)
root_agent = Agent(
    name="search_assistant",
    model="gemini-2.5-pro",
    description="An academic-grade assistant leveraging Gemini 2.5 Pro to analyze, cross-reference, and articulate knowledge from verified online sources.",
    instruction="You are an academic research assistant. Provide structured, well-cited, and context-aware responses. When searching the web, prioritize credible sources and synthesize findings clearly.",
    tools=[google_search],
)

# Option: give runner the same app_name as the agent package to avoid warning
runner = InMemoryRunner(agent=root_agent, app_name="agents")
print("✅ Agent and runner ready!\n")

# Helper: try to extract human text from typical ADK event/response shapes
def extract_text_from_obj(obj):
    # try several common fields / shapes
    candidates = []
    try:
        # plain string
        if isinstance(obj, str):
            return obj
        # dict-like
        if isinstance(obj, dict):
            # common keys to check
            for k in ("text", "content", "message", "output"):
                if k in obj and obj[k]:
                    return str(obj[k])
            # fallback: dump a small repr
            return repr(obj)[:1000]
        # object with attributes
        for attr in ("message", "text", "content", "output"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                # some objects wrap content in lists/dicts
                if isinstance(val, (str, int, float)):
                    return str(val)
                try:
                    # if val is a list/dict, try first element
                    if isinstance(val, (list, tuple)) and len(val) > 0:
                        first = val[0]
                        if isinstance(first, str):
                            return first
                        if isinstance(first, dict):
                            for k in ("text","content","message","output"):
                                if k in first:
                                    return str(first[k])
                        return repr(first)[:1000]
                except Exception:
                    pass
        # last resort: repr
        return repr(obj)[:1000]
    except Exception as e:
        return f"<extract error: {e}>"

async def handle_response(resp):
    """
    resp may be:
      - an async generator (stream)
      - a list of events
      - a single event/dict/object
    """
    # Case A: async generator / async iterable
    if hasattr(resp, "__aiter__"):
        print("🟢 Detected async iterable (streaming).")
        async for ev in resp:
            print("--- stream event ---")
            print(extract_text_from_obj(ev))
        return

    # Case B: regular iterable (list/tuple)
    if isinstance(resp, (list, tuple)):
        print("🟡 Detected list/tuple of events.")
        for ev in resp:
            print("--- event ---")
            print(extract_text_from_obj(ev))
        return

    # Case C: single object
    print("🔵 Single response object:")
    print(extract_text_from_obj(resp))

async def main():
    query = "what is the proper way to follow when one is trying to create a project or publishing the project?"
    print(f"🧠 Query: {query}\n")
    try:
        # NOTE: await the coroutine to get back the actual response object (could be generator/list/dict)
        resp = await runner.run_debug(query)

        # handle the response flexibly
        await handle_response(resp)

    except Exception as e:
        print("⚠️ Error while running agent:", repr(e))

if __name__ == "__main__":
    asyncio.run(main())