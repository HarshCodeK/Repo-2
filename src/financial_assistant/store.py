import sqlite3
from pathlib import Path

class InteractionStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS interactions (id INTEGER PRIMARY KEY, question TEXT NOT NULL, supported INTEGER NOT NULL, answer TEXT NOT NULL)")
    def record(self, question: str, supported: bool, answer: str) -> None:
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO interactions(question, supported, answer) VALUES (?, ?, ?)", (question, int(supported), answer))
