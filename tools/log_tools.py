from crewai.tools import tool

@tool("Reads log file contents")
def read_log_file(path="sample_data/error.log"):
    """Reads the contents of a log file given its path."""
    with open(path, "r") as file:
        logs = file.read()
    return logs
