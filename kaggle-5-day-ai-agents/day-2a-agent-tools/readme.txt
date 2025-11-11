DAY 2A - AGENT TOOLS
====================

This example shows how to extend your AI agent using tools such as:
1. Function Tools (custom Python functions)
2. Google Search (prebuilt tool)
3. Composite workflows using the Agent Development Kit (ADK)

----------------------------------------------------------------------
HOW TO RUN
----------------------------------------------------------------------

1. Make sure you are in the main project folder:
   cd /path/to/KAGGLE-5-DAY-AI-AGENTS

2. Activate your virtual environment:
   - macOS/Linux: source .venv/bin/activate
   - Windows: .venv\Scripts\activate

3. Run the agent:
   cd day-2a-agent-tools
   python main.py

----------------------------------------------------------------------
HOW IT WORKS
----------------------------------------------------------------------

- The agent uses a Gemini model (gemini-2.5-flash-lite) for reasoning.
- Custom function tools are registered:
    add_numbers(a, b) → adds two numbers.
    get_weather(location) → returns demo weather data.
- It also uses Google Search for real information.
- The InMemoryRunner allows direct async execution locally.

----------------------------------------------------------------------
EXPECTED OUTPUT
----------------------------------------------------------------------

🧠 Query 1: Basic math tool usage
→ The agent calls add_numbers and prints the result.

🌤️ Query 2: Weather tool usage
→ The agent uses get_weather() and gives a short report.

🔎 Query 3: Search tool usage
→ The agent uses google_search and summarizes recent info.

----------------------------------------------------------------------
NOTES
----------------------------------------------------------------------

- Make sure your GOOGLE_API_KEY is set in the .env file.
- Avoid running too many queries in one go (to prevent rate limits).
- You can modify or add new FunctionTool() entries to expand abilities.

----------------------------------------------------------------------
NEXT STEP
----------------------------------------------------------------------

Move on to Day 2B (Agent Tools – Best Practices), where we improve 
tool chaining, validation, and error handling.