from crewai import Agent
from tools.log_tools import read_log_file
from tools.code_tools import read_code_files

LogAgent = Agent(
    role="Python Log Analyzer",
    goal="Analyze log errors and diagnose root causes",
    backstory="Expert Python developer good at reading logs and identifying bugs in code.",
    tools=[read_log_file, read_code_files],
    verbose=True
)
