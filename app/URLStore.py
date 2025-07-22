from datetime import datetime

class URLStore:
    def __init__(self):
        self.db = {}  # ✅ This initializes the in-memory "database"

    def save(self, code, url):
        self.db[code] = {
            "url": url,
            "clicks": 0,
            "created_at": datetime.utcnow()  # ✅ add this line
        }


    def get(self, code):
        return self.db.get(code)

    def exists(self, code):
        return code in self.db

    def increment_clicks(self, code):
        if code in self.db:
            self.db[code]["clicks"] += 1

    def stats(self, code):
        return self.db.get(code)

    def get_all(self):
        return self.db.items()

    def reset(self):  # for tests
        self.db.clear()
