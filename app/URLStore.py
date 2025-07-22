from datetime import datetime

class URLStore:
    def __init__(self):
        self.db = {}

    def save(self, code, url):
        self.db[code] = {
            "url": url,
            "clicks": 0,
            "created_at": datetime.utcnow()
        }

    def get(self, code):
        return self.db.get(code)

    def exists(self, code):
        return code in self.db

    def increment_clicks(self, code):
        if code in self.db:
            self.db[code]["clicks"] += 1

    def get_all(self):
        return self.db.items()
