DAY 1B - AGENT ARCHITECTURES
=============================

Purpose:
This section demonstrates how to build multiple agent architectures 
using the Google Agent Development Kit (ADK):
 - Sequential Agent
 - Parallel Agent
 - Hierarchical Agent
 - Multi-Agent Negotiation System

Each architecture is implemented in its own Python file.

----------------------------------------------------------------------
HOW TO RUN
----------------------------------------------------------------------

1. Open your terminal:
   cd /path/to/KAGGLE-5-DAY-AI-AGENTS

2. Activate your virtual environment:
   - macOS/Linux: source .venv/bin/activate
   - Windows: .venv\Scripts\activate

3. Navigate to this directory:
   cd day-1b-agent-architectures

4. Run any of the architecture demos:
   python sequential_agent.py
   python parallel_agent.py
   python hierarchical_agent.py
   python multi_agent_negotiation.py

----------------------------------------------------------------------
ARCHITECTURE DESCRIPTIONS
----------------------------------------------------------------------

1. Sequential Agent
   - Executes tasks in order.
   - Output from one agent becomes input for the next.

2. Parallel Agent
   - Runs multiple agents simultaneously.
   - Each agent handles independent subtasks in parallel.

3. Hierarchical Agent
   - One “manager” agent delegates subtasks to multiple “worker” agents.
   - Combines structured orchestration and autonomous execution.

4. Multi-Agent Negotiation
   - Multiple agents debate or negotiate to reach a consensus.
   - Useful for tasks requiring judgment, comparison, or evaluation.

----------------------------------------------------------------------
FILES
----------------------------------------------------------------------

sequential_agent.py          - Sequential execution example
parallel_agent.py            - Parallel execution example
hierarchical_agent.py        - Manager/worker orchestration
multi_agent_negotiation.py   - Negotiation and consensus example
readme.txt                   - This file (instructions)

----------------------------------------------------------------------
TROUBLESHOOTING
----------------------------------------------------------------------

- "API key not valid":
    -> Regenerate the key at https://aistudio.google.com/app/apikey
- "ModuleNotFoundError: google.adk":
    -> Run pip install -r requirements.txt inside your virtual environment.
- Execution too fast with no output:
    -> Add print statements or async awaits for debugging; some agents may finish instantly.

----------------------------------------------------------------------
NEXT STEP
----------------------------------------------------------------------

Move on to Day 2A - Agent Tools, where we extend agents with 
custom function tools and Google Search integration.