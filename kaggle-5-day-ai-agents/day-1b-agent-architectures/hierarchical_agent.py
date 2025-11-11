# hierarchical_agent.py
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
orchestrator = Agent(name="orchestrator", model="gemini-2.5-pro",
                     description="Top-level orchestrator to assign managers.",
                     instruction="You are the Orchestrator. Split a user goal into two managerial tasks and assign them.")

manager = Agent(name="manager", model="gemini-2.5-pro",
                description="Manager: splits tasks to workers and aggregates.",
                instruction="You are a Manager. Given your assigned task, produce two worker tasks and how to aggregate results.")

worker = Agent(name="worker", model="gemini-2.5-pro",
               description="Worker: performs a focused subtask.",
               instruction="You are a Worker. Perform the small task and return a short result.")

# Runners
r_orch = InMemoryRunner(agent=orchestrator, app_name="agents")
r_mgr = InMemoryRunner(agent=manager, app_name="agents")
r_worker = InMemoryRunner(agent=worker, app_name="agents")

async def run_hierarchy(goal):
    print("Orchestrator gets goal:", goal)
    orch_resp = await r_orch.run_debug(f"User goal: {goal}\nSplit into two manager-level tasks.")
    # we expect two manager tasks in text form
    mgr_tasks = []
    if isinstance(orch_resp, (list,tuple)):
        mgr_tasks = [extract_text_from_obj(orch_resp[0])]
    else:
        mgr_tasks = [extract_text_from_obj(orch_resp)]
    print("Manager tasks:", mgr_tasks)

    all_worker_results = []
    # For each manager, ask manager to create worker tasks then run two workers
    for i, mt in enumerate(mgr_tasks, start=1):
        print(f"\nManager {i} assigned:", mt)
        mgr_resp = await r_mgr.run_debug(f"Manager task: {mt}\nProduce 2 worker tasks (one line each).")
        # parse two worker tasks (we'll treat each response as a single task)
        worker_tasks = []
        if isinstance(mgr_resp, (list,tuple)):
            worker_tasks.append(extract_text_from_obj(mgr_resp[0]))
        else:
            worker_tasks.append(extract_text_from_obj(mgr_resp))
        # run workers (1 or more)
        for wt in worker_tasks:
            print(" - Worker performing:", wt)
            w_resp = await r_worker.run_debug(f"Worker task: {wt}\nPerform task and return a short summary.")
            await handle_resp(w_resp)
            all_worker_results.append(extract_text_from_obj(w_resp))
    print("\nHierarchy complete. Aggregated results:", all_worker_results)

if __name__ == "__main__":
    asyncio.run(run_hierarchy("Create a small experiment to test UI tweaks increasing engagement."))