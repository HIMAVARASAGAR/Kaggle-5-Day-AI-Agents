# multi_agent_negotiation.py
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

# Define three proposer agents and one judge agent
proposers = [
    Agent(name=f"proposer_{i}", model="gemini-2.5-pro",
          description=f"Proposer agent {i}", instruction="Propose one concise solution for the prompt with a one-line rationale.")
    for i in range(1,4)
]

judge = Agent(name="judge", model="gemini-2.5-pro",
              description="Judge: ranks and picks best proposal",
              instruction="You are a Judge. Rank the provided proposals (1-3) and choose the best with a short justification.")

# runners for each
runners = [InMemoryRunner(agent=p, app_name="agents") for p in proposers]
r_judge = InMemoryRunner(agent=judge, app_name="agents")

async def negotiation_flow(prompt):
    print("Prompt for proposers:", prompt)
    # collect proposals in parallel
    tasks = [r.run_debug(f"Prompt: {prompt}\nPropose one candidate solution.") for r in runners]
    # await all (some return lists/streams; we await and handle each result)
    gathered = await asyncio.gather(*tasks)
    proposals = []
    print("\n--- Proposals ---")
    for resp in gathered:
        # extract first text
        if isinstance(resp, (list,tuple)):
            prop = extract_text_from_obj(resp[0])
        else:
            prop = extract_text_from_obj(resp)
        proposals.append(prop)
        print(prop)
    # give proposals to judge
    judge_prompt = "Rank these proposals and pick the best. Proposals:\n" + "\n".join(f"{i+1}. {p}" for i,p in enumerate(proposals))
    jresp = await r_judge.run_debug(judge_prompt)
    print("\n--- Judge decision ---")
    await handle_resp(jresp)

if __name__ == "__main__":
    asyncio.run(negotiation_flow("How can we improve first-time user activation on a learning platform?"))