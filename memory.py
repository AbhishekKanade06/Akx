from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

def get_memory(db_path: str = "agent_memory.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return SqliteSaver(conn)