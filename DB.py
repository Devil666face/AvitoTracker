import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_user(self, id):
        with self.connection:
            try:
                insert_query = f"INSERT INTO users (id) VALUES ({id})"
                self.exec_and_save(insert_query)
                return "Пользователь успешно создан"
            except Exception as error:
                print(error)
                return "Пользователь не создан"

    def update_url(self, id, url):
        with self.connection:
            update_query = f"UPDATE users SET url = '{url}', active = 1 WHERE id={id}"
            self.exec_and_save(update_query)

    def update_key_word(self, id, query):
        with self.connection:
            update_query = f"UPDATE users SET query = '{query}' WHERE id={id}"
            self.exec_and_save(update_query)

    def deactivate_track(self, id):
        with self.connection:
            update_query = f"UPDATE users SET active = 0 WHERE id={id}"
            self.exec_and_save(update_query)

    def get_url(self, id):
        with self.connection:
            select_query = f"SELECT url FROM users WHERE id = {id}"
            self.exec_and_save(select_query)
            for url in self.cursor:
                return url[0]

    def get_query(self, id):
        with self.connection:
            select_query = f"SELECT query FROM users WHERE id = {id}"
            self.exec_and_save(select_query)
            for query in self.cursor:
                return query[0]

    def exec_and_save(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def get_state(self, id):
        with self.connection:
            select_query = f"SELECT active FROM users WHERE id = {id}"
            self.exec_and_save(select_query)
            for query in self.cursor:
                return True if query[0]==1 else False



