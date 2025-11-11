KAGGLE 5-DAY AI AGENTS
======================

This project contains local, runnable versions of the Kaggle "5 Days of AI Agents" course examples using the Google Agent Development Kit (ADK).

Each day is in a separate folder. 
Example: 
- day-1a-from-prompt-to-action
- day-1b-agent-architectures

----------------------------------------------------------------------
SETUP INSTRUCTIONS (FOR MAC / LINUX)
----------------------------------------------------------------------

1. Open Terminal and navigate to the project folder:
   cd /path/to/KAGGLE-5-DAY-AI-AGENTS

2. Create a Python virtual environment:
   python3 -m venv .venv

3. Activate the environment:
   source .venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Create a new .env file based on the provided example:
   cp .env.example .env

6. Open the .env file and add your Google API key:
   GOOGLE_API_KEY=your_api_key_here
   GOOGLE_GENAI_USE_VERTEXAI=FALSE

----------------------------------------------------------------------
SETUP INSTRUCTIONS (FOR WINDOWS)
----------------------------------------------------------------------

1. Open PowerShell and navigate to the project folder:
   cd C:\path\to\KAGGLE-5-DAY-AI-AGENTS

2. Create and activate the environment:
   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create a new .env file:
   copy .env.example .env

5. Open .env in Notepad and paste your API key:
   GOOGLE_API_KEY=your_api_key_here
   GOOGLE_GENAI_USE_VERTEXAI=FALSE

----------------------------------------------------------------------
HOW TO GET YOUR GOOGLE API KEY
----------------------------------------------------------------------

1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key shown
4. Paste it into your .env file as:
   GOOGLE_API_KEY=AIzaSy...
5. Save the file and restart your terminal.

----------------------------------------------------------------------
RUNNING THE PROJECTS
----------------------------------------------------------------------

Example 1a:
   cd day-1a-from-prompt-to-action
   python main.py

Example 1b (Agent Architectures):
   cd day-1b-agent-architectures
   python sequential_agent.py
   python parallel_agent.py
   python hierarchical_agent.py
   python multi_agent_negotiation.py

----------------------------------------------------------------------
COMMON PROBLEMS
----------------------------------------------------------------------

- ERROR: "GOOGLE_API_KEY not found"
  -> Make sure .env exists in the main project folder and is correctly written.

- ERROR: "API key not valid"
  -> Regenerate the key from AI Studio (link above). Don’t include quotes or spaces.

- ERROR: "ModuleNotFoundError: google.adk"
  -> Run pip install -r requirements.txt after activating .venv.

----------------------------------------------------------------------
FILES INCLUDED
----------------------------------------------------------------------

requirements.txt     - Python dependencies
.env.example         - Template for environment variables
.gitignore           - Files to exclude from Git
day-1a-from-prompt-to-action/  - Your first agent example
day-1b-agent-architectures/    - Sequential, parallel, hierarchical & negotiation agents

----------------------------------------------------------------------
CREDITS
----------------------------------------------------------------------

Created as part of the Kaggle x Google "5 Days of AI Agents" challenge.
This repository allows you to run all exercises locally with your own API key.