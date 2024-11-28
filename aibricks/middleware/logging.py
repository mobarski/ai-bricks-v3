from types import SimpleNamespace
import time
import json

from aibricks.middleware import MiddlewareBase


class LoggingMiddleware(MiddlewareBase):

    def __init__(self, ctx: SimpleNamespace | object, db):
        super().__init__(ctx)
        self.db = db
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

    def request(self, data):
        self.ctx.request = data.copy()  # allow obfuscation
        self.ctx.request['headers'] = 'OBFUSCATED'
        self.ctx.request_ts = time.time()
        return data

    def response(self, data):
        self.ctx.response = data
        self.ctx.response_ts = time.time()
        #
        sql = """
            INSERT INTO logs (provider, model, request_json, request_ts, response_json, response_ts)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute(sql, (
            self.parent.provider,
            self.parent.model,
            json.dumps(self.ctx.request),
            self.ctx.request_ts,
            json.dumps(self.ctx.response),
            self.ctx.response_ts
        ))
        self.db.commit()
        return data
