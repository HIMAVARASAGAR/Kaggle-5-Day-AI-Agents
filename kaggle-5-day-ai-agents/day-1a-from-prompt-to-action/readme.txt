DAY 1A - FROM PROMPT TO ACTION
==============================

Purpose:
This example introduces the basic workflow for creating and running a simple AI agent 
locally using the Google Agent Development Kit (ADK). It demonstrates:
 - loading environment variables from .env
 - defining a root agent
 - using a runner to process prompts
 - generating direct model responses

----------------------------------------------------------------------
HOW TO RUN
----------------------------------------------------------------------

1. Open your terminal and navigate to this project:
   cd /path/to/KAGGLE-5-DAY-AI-AGENTS

2. Activate the virtual environment:
   - macOS/Linux: source .venv/bin/activate
   - Windows: .venv\Scripts\activate

3. Run the example:
   cd day-1a-from-prompt-to-action
   python main.py

----------------------------------------------------------------------
WHAT IT DOES
----------------------------------------------------------------------

- Loads your Google API key from .env
- Creates a Gemini-based AI agent using ADK
- Uses InMemoryRunner to simulate a session locally
- Runs one or more sample queries (defined in main.py)
- Prints the model responses in your console

----------------------------------------------------------------------
FILES
----------------------------------------------------------------------

main.py      - the full runnable example script
readme.txt   - this file (instructions)

----------------------------------------------------------------------
TROUBLESHOOTING
----------------------------------------------------------------------

- "GOOGLE_API_KEY not found":
    -> Make sure .env is in the root folder with your API key.
- "API key not valid":
    -> Regenerate your key from https://aistudio.google.com/app/apikey
- "ModuleNotFoundError: google.adk":
    -> Activate your environment and install dependencies using:
       pip install -r requirements.txt

----------------------------------------------------------------------
NEXT STEP
----------------------------------------------------------------------

Proceed to Day 1B to explore multi-agent architectures and workflows.