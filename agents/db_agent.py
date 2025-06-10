from crewai import Agent
from tools.db_tools import get_db_schema_with_data

DBAgent = Agent(
    role="SQLite Inspector",
    goal="Analyze database schema and suggest necessary changes",
    backstory="You specialize in inspecting schemas and fixing structural issues in SQL databases.",
    tools=[get_db_schema_with_data],
    verbose=True
)
