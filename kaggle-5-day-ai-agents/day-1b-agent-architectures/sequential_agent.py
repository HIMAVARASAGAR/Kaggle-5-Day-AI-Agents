# sequential_agent.py
import os, asyncio
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Add GOOGLE_API_KEY to .env before running.")
os.environ["GOOGLE_API_KEY"] = API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI","FALSE")

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

# Helpers
def extract_text_from_obj(obj):
    try:
        if isinstance(obj, str): return obj
        if isinstance(obj, dict):
            for k in ("text","content","message","output"):
                if k in obj and obj[k]: return str(obj[k])
            return repr(obj)[:1000]
        if hasattr(obj, "content"):
            cont = getattr(obj, "content")
            if hasattr(cont, "parts") and cont.parts:
                first = cont.parts[0]
                if hasattr(first, "text"): return first.text
        return repr(obj)[:1000]
    except Exception as e:
        return f"<extract error: {e}>"

async def handle_response(resp):
    if hasattr(resp, "__aiter__"):
        async for ev in resp:
            txt = extract_text_from_obj(ev)
            if txt: print(txt)
        return
    if isinstance(resp, (list,tuple)):
        for ev in resp:
            txt = extract_text_from_obj(ev)
            if txt: print(txt)
        return
    print(extract_text_from_obj(resp))

# Create three agents with different roles (simple prompt-based role separation)
researcher = Agent(
    name="researcher",
    model="gemini-2.5-pro",
    description="Researcher: reads prompt & proposes 2 hypotheses.",
    instruction="You are a Researcher. Propose 2 concise hypotheses for the user goal, ranked by feasibility."
)

engineer = Agent(
    name="engineer",
    model="gemini-2.5-pro",
    description="Engineer: turns chosen hypothesis into a small experiment plan.",
    instruction="You are an Engineer. Given hypothesis, produce a 3-step experimental plan in runnable pseudocode."
)

evaluator = Agent(
    name="evaluator",
    model="gemini-2.5-pro",
    description="Evaluator: evaluates results and gives verdict.",
    instruction="You are an Evaluator. Given results summary, state whether hypothesis is supported and why."
)

# Runners (one per agent)
r_research = InMemoryRunner(agent=researcher, app_name="agents")
r_engineer = InMemoryRunner(agent=engineer, app_name="agents")
r_eval = InMemoryRunner(agent=evaluator, app_name="agents")

async def sequential_pipeline(goal):
    print("=== Orchestrator: Start sequential pipeline ===")
    print("Goal:", goal, "\n")

    # Step 1: research
    print("-> Researcher: propose hypotheses")
    resp1 = await r_research.run_debug(f"User goal: {goal}\nPropose 2 hypotheses, rank by feasibility.")
    await handle_response(resp1)

    # Step 2: engineer (choose hypothesis 1 by convention)
    print("\n-> Engineer: plan for hypothesis 1")
    resp2 = await r_engineer.run_debug(f"Hypothesis: [choose #1]. Create 3-step experiment plan (pseudocode).")
    await handle_response(resp2)

    # Step 3: evaluator (pretend we ran experiment and got 'result: small positive effect')
    print("\n-> Evaluator: evaluate results")
    resp3 = await r_eval.run_debug("Results summary: small positive effect observed. Judge whether hypothesis supported and why.")
    await handle_response(resp3)

    print("\n=== Pipeline complete ===")

if __name__ == "__main__":
    asyncio.run(sequential_pipeline("Test whether providing example prompts increases user completion rates on a tutorial site."))