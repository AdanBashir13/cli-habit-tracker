from models.__init__ import CURSOR, CONN

class User:
    all = {}

    def __init__(self, username, password, id=None):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if isinstance(username, str) and len(username):
            self._username = username
        else:
            raise ValueError("Username must be a non-empty string")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        if isinstance(password, str) and len(password):
            self._password = password
        else:
            raise ValueError("Password must be a non-empty string")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS users;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = "INSERT INTO users (username, password) VALUES (?, ?)"
        CURSOR.execute(sql, (self.username, self.password))
        CONN.commit()
        self.id = CURSOR.lastrowid
        User.all[self.id] = self

    @classmethod
    def create(cls, username, password):
        user = cls(username, password)
        user.save()
        return user

    def update(self):
        sql = "UPDATE users SET username = ?, password = ? WHERE id = ?"
        CURSOR.execute(sql, (self.username, self.password, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM users WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del User.all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        user = cls.all.get(row[0])
        if user:
            user.username = row[1]
            user.password = row[2]
        else:
            user = cls(row[1], row[2])
            user.id = row[0]
            cls.all[user.id] = user
        return user

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM users"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM users WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_username(cls, username):
        sql = "SELECT * FROM users WHERE username = ?"
        row = CURSOR.execute(sql, (username,)).fetchone()
        return cls.instance_from_db(row) if row else None
