import os
import asyncio
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.adk.tools.function_tool import FunctionTool

# ----------------------------------------------------------------------
# Load environment and validate API key
# ----------------------------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in your .env file.")
else:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
    print("✅ API key loaded successfully!")

# ----------------------------------------------------------------------
# Define some example function tools the agent can use
# ----------------------------------------------------------------------

def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b

def get_weather(location: str) -> str:
    """Return a fake weather report for the given location."""
    return f"The weather in {location} is sunny with 28°C (demo data)."

# Wrap functions as tools
math_tool = FunctionTool(add_numbers)
weather_tool = FunctionTool(get_weather)

# ----------------------------------------------------------------------
# Define the agent
# ----------------------------------------------------------------------

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "An intelligent assistant that can use function tools "
        "and external search to solve user requests efficiently."
    ),
    instruction=(
        "You are a tool-enabled AI agent. Use the available tools (math, weather, Google Search) "
        "to answer questions accurately. Explain your reasoning where possible."
    ),
    tools=[math_tool, weather_tool, google_search],
)

runner = InMemoryRunner(agent=root_agent)
print("✅ Agent and runner initialized successfully!\n")

# ----------------------------------------------------------------------
# Run example queries
# ----------------------------------------------------------------------

async def main():
    print("🧠 Query 1: Basic math tool usage")
    await runner.run("Add 35.5 and 62.3")

    print("\n🌤️ Query 2: Weather tool usage")
    await runner.run("What is the weather in Bangalore?")

    print("\n🔎 Query 3: Search tool usage")
    await runner.run("Who won the Nobel Prize in Physics in 2024?")

asyncio.run(main())