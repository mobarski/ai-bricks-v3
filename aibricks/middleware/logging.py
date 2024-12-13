import time
import json

from aibricks.middleware import MiddlewareBase
from ..utils import DatabaseFactory


class LoggingMiddleware(MiddlewareBase):

    def __init__(self, db):
        super().__init__()
        # Handle db parameter - can be either a connection or a path
        self.db = db if hasattr(db, 'execute') else DatabaseFactory.get_connection(db)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider,
                model,
                request_json,
                request_ts,
                response_json,
                response_ts
            )""")

    def request(self, data, ctx):
        ctx['request'] = data.copy()  # allow obfuscation
        ctx['request']['headers'] = 'OBFUSCATED'
        ctx['request_ts'] = time.time()
        return data

    def response(self, data, ctx):
        ctx['response'] = data
        ctx['response_ts'] = time.time()
        #
        sql = """
            INSERT INTO logs (provider, model, request_json, request_ts, response_json, response_ts)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute(sql, (
            self.parent.provider,
            self.parent.model,
            json.dumps(ctx['request']),
            ctx['request_ts'],
            json.dumps(ctx['response'].to_dict()),
            ctx['response_ts']
        ))
        self.db.commit()
        return data
