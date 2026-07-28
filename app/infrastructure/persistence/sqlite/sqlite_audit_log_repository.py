import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository


class SQLiteAuditLogRepository(AuditLogRepository):

    def __init__(
        self,
        database_path: Path,
    ):
        database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            str(database_path),
            check_same_thread=False,
        )

        self._create_table()

    def _create_table(self):
        self.connection.execute(
            """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    sources TEXT NOT NULL,
                    retrieved_chunks INTEGER NOT NULL,
                    latency_ms INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                )
            """
        )

        self.connection.commit()

    def save(
        self,
        log: AuditLog,
    ):

        self.connection.execute(
            """
            INSERT INTO audit_logs(
                question,
                answer,
                sources,
                retrieved_chunks,
                latency_ms,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                log.question,
                log.answer,
                json.dumps(log.sources),
                log.retrieved_chunks,
                log.latency_ms,
                log.created_at.isoformat(),
            ),
        )

        self.connection.commit()


    def find_all(self):

        cursor = self.connection.execute("""
            SELECT
                question,
                answer,
                sources,
                retrieved_chunks,
                latency_ms,
                created_at
            FROM audit_logs
            ORDER BY created_at DESC
        """)

        logs = []

        for row in cursor.fetchall():
            logs.append(
                AuditLog(
                    question=row[0],
                    answer=row[1],
                    sources=json.loads(row[2]),
                    retrieved_chunks=row[3],
                    latency_ms=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                )
            )

        return logs

    def clear(self):

        self.connection.execute("DELETE FROM audit_logs")

        self.connection.commit()


