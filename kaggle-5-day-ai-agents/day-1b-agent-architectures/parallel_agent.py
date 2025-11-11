# parallel_agent.py
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

async def handle_resp(resp):
    if hasattr(resp, "__aiter__"):
        async for ev in resp: print(extract_text_from_obj(ev))
        return
    if isinstance(resp, (list,tuple)):
        for ev in resp: print(extract_text_from_obj(ev))
        return
    print(extract_text_from_obj(resp))

# Agents
researcher = Agent(name="researcher", model="gemini-2.5-pro",
                   description="Researcher agent for parallel exploration.",
                   instruction="Propose one hypothesis for the provided goal and a 1-line rationale.")

engineer = Agent(name="engineer", model="gemini-2.5-pro",
                 description="Engineer converts hypothesis to runnable plan.",
                 instruction="Given a hypothesis, produce a tiny plan in steps.")

# Runners
r_research = InMemoryRunner(agent=researcher, app_name="agents")
r_engineer = InMemoryRunner(agent=engineer, app_name="agents")

async def pipeline_instance(goal, seed):
    # step A: researcher propose hypothesis
    h_resp = await r_research.run_debug(f"Goal: {goal}\nSeed: {seed}\nPropose one hypothesis.")
    # extract text quickly
    h_text = ""
    if isinstance(h_resp, (list,tuple)):
        h_text = extract_text_from_obj(h_resp[0])
    else:
        h_text = extract_text_from_obj(h_resp)
    print(f"\n[Pipeline {seed}] Hypothesis:", h_text)

    # step B: engineer creates plan for that hypothesis
    e_resp = await r_engineer.run_debug(f"Hypothesis: {h_text}\nProduce 2-step plan.")
    await handle_resp(e_resp)
    return (seed, h_text)

async def main():
    goal = "Reduce time-to-first-success for new tutorial users."
    # spawn 3 pipelines in parallel
    tasks = [pipeline_instance(goal, i) for i in range(1,4)]
    results = await asyncio.gather(*tasks)
    print("\nAll pipelines done. Collected hypotheses:", results)

if __name__ == "__main__":
    asyncio.run(main())