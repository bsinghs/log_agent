from crewai import Crew, Task
from agents.log_agent import LogAgent
from agents.db_agent import DBAgent

log_task = Task(
    description="Read and analyze error.log and code snippets to find what's going wrong.",
    expected_output="Root cause of the error and a suggestion to fix the code or SQL.",
    agent=LogAgent
)

db_task = Task(
    description="Analyze the sample.db schema and suggest changes if necessary.",
    expected_output="Insights on database table structure and any issues with column names or types.",
    agent=DBAgent
)

crew = Crew(
    agents=[LogAgent, DBAgent],
    tasks=[log_task, db_task],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n=== Crew Output ===\n")
    print(result)
