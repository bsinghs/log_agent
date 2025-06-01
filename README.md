# Log and DB Analysis Agent

## Overview
This project demonstrates a Python agent that:
- Creates a local SQLite database (`setup_db.py`)
- Reads an error log file (`error.log`)
- Reads the SQLite database schema
- Sends both the log and schema to OpenAI GPT to get SQL query or data fix suggestions

## Prerequisites
- Python 3.8+
- An OpenAI API key ([Get your key here](https://platform.openai.com/account/api-keys))

## Setup Steps (Windows)
1. Create a virtual environment and activate it:
```
python -m venv log_agent_env
.\log_agent_env\Scripts\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create your local database:
```
python setup_db.py
```

4. Rename `.env.example` to `.env` and add your OpenAI API key.

5. Run the log analyzer:
```
python log_agent.py
```

## Notes
- The sample error log contains a SQL syntax error (`FROMM` instead of `FROM`).
- The agent sends the schema and log to GPT-4o for suggestions.
- Replace `model` in `log_agent.py` with `"gpt-3.5-turbo"` if you want a cheaper option.

## Troubleshooting
- Make sure your `.env` is set correctly with a valid OpenAI API key.
- Ensure virtual environment is activated before running scripts.
