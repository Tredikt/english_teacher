from sqlite3 import connect


class DataBase:
    def __init__(self, db_name):
        self.conn = connect(db_name)
        self.cur = self.conn.cursor()

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                tg_id INTEGER PRIMARY KEY,
                fullname TEXT,
                rating INTEGER
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS words_rating(
                tg_id INTEGER,
                word TEXT,
                word_rating INTEGER
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS polls(
                poll_id INTEGER,
                correct_id INTEGER,
                time TEXT
            )
            """
        )

    def create_words(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS words(
                level TEXT,
                word TEXT,
                picture TEXT,
                translation TEXT,
                type TEXT,
                transcription TEXT,
                example TEXT
            )
            """
        )
        self.conn.commit()

    def create_times(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS times(
                theme TEXT,
                question TEXT,
                option1 TEXT,
                option2 TEXT,
                option3 TEXT,
                option4 TEXT,
                option5 TEXT,
                option6 TEXT,
                option7 TEXT,
                option8 TEXT,
                option9 TEXT,
                option10 TEXT
            )
            """
        )
        self.conn.commit()

    def delete_words(self):
        self.cur.execute(
            """
            DROP TABLE words
            """
        )
        self.conn.commit()

    def delete_times(self):
        self.cur.execute(
            """
            DROP TABLE times
            """
        )
        self.conn.commit()

    def add_poll(self, poll_id: int, correct_id: int, time: str):
        self.cur.execute(
            """
            INSERT INTO polls
            (poll_id, correct_id, time)
            VALUES
            (?, ?, ?)
            """,
            (poll_id, correct_id, time)
        )

        self.conn.commit()

    def get_answer(self, poll_id: int):
        correct_id = self.cur.execute(
            f"""
            SELECT correct_id FROM polls
            WHERE poll_id = {poll_id}
            """
        ).fetchone()

        return correct_id[0]

    def get_poll_time(self, poll_id: int):
        time = self.cur.execute(
            f"""
            SELECT time FROM polls
            WHERE poll_id = {poll_id}
            """
        ).fetchone()

        return time[0]

    def delete_poll(self, poll_id: int):
        self.cur.execute(
            f"""
            DELETE FROM polls
            WHERE poll_id = {poll_id}
            """
        )
        self.conn.commit()

    def add_user(self, tg_id: int, fullname: str):
        self.cur.execute(
            """
            INSERT INTO users
            (tg_id, fullname, rating)
            VALUES
            (?, ?, ?)
            """,
            (tg_id, fullname, 0)
        )

        self.conn.commit()

    def add_word(self, level, word, picture, translation, word_type, transcription, example):
        self.cur.execute(
            """
            INSERT INTO words
            (level, word, picture, translation, type, transcription, example)
            VALUES
            (?, ?, ?, ?, ?, ?, ?)
            """,
            (level, word, picture, translation, word_type, transcription, example)
        )

        self.conn.commit()

    def add_time(self, theme, question, option1, option2, option3, option4, option5, option6, option7, option8, option9, option10):
        self.cur.execute(
            """
            INSERT INTO times
            (theme, question, option1, option2, option3, option4, option5, option6, option7, option8, option9, option10)
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (theme, question, option1, option2, option3, option4, option5, option6, option7, option8, option9, option10)
        )

        self.conn.commit()


    def get_users_ids(self):
        users_ids = self.cur.execute(
            """
            SELECT tg_id FROM users
            """
        ).fetchall()

        return [] if users_ids is None else [elem[0] for elem in users_ids]

    def get_users_rating(self):
        users = self.cur.execute(
            """
            SELECT tg_id, fullname, rating FROM users
            """
        ).fetchall()

        return users

    def rating_to_null(self, tg_id):
        self.cur.execute(
            f"""
            UPDATE users
            SET rating = 0
            WHERE tg_id = {tg_id}
            """
        )

    def add_word_rating(self, tg_id: int, word: str):
        self.cur.execute(
            """
            INSERT INTO words_rating
            (tg_id, word, word_rating)
            VALUES
            (?, ?, ?)
            """,
            (tg_id, word, 1)
        )

        self.conn.commit()

    def get_rating_words(self, tg_id):
        rate_words = self.cur.execute(
            f"""
            SELECT word FROM words_rating
            WHERE tg_id = {tg_id}
            """
        ).fetchall()

        return [] if rate_words is None else [elem[0] for elem in rate_words]

    def plus_user_rating(self, tg_id):
        self.cur.execute(
            f"""
            UPDATE users
            SET rating = rating + 1
            WHERE tg_id = {tg_id}
            """
        )

        self.conn.commit()

    def minus_user_rating(self, tg_id):
        self.cur.execute(
            f"""
            UPDATE users
            SET rating = rating - 1
            WHERE tg_id = {tg_id} AND rating != 0
            """
        )

        self.conn.commit()

    def get_words_by_lvl(self, level: str, tg_id: int):
        words = self.cur.execute(
            f"""
            SELECT word, picture, translation, type, transcription, example FROM words
            WHERE level = '{level}'
            """
        ).fetchall()

        tuples_list = []
        for elem in words:
            word = elem[0]
            if self.get_word_rating(tg_id=tg_id, word=word) < 7:
                tuples_list.append(elem)

        return tuples_list

    def get_times_data(self, time: str):
        times = self.cur.execute(
            f"""
            SELECT question, option1, option2, option3, option4, option5, option6, option7, option8, option9, option10 FROM times
            WHERE theme = '{time}'
            """
        ).fetchall()

        return times

    def get_time_buy_question(self, question: str):
        theme = self.cur.execute(
            f"""
            SELECT theme FROM times
            WHERE question = '{question}'
            """
        ).fetchone()

        return theme[0]

    def get_times_list(self):
        times = self.cur.execute(
            """
            SELECT theme FROM times
            """
        ).fetchall()

        return [] if times is None else list(map(lambda x: x.replace(" ", "_", 1), list(set([elem[0] for elem in times]))))

    def plus_word_rating(self, tg_id, word):
        self.cur.execute(
            f"""
            UPDATE words_rating
            SET word_rating = word_rating + 1
            WHERE tg_id = {tg_id}
            AND word = '{word}'
            """
        )

        self.conn.commit()

    def minus_word_rating(self, tg_id, word):
        self.cur.execute(
            f"""
            UPDATE words_rating
            SET word_rating = word_rating - 1
            WHERE tg_id = {tg_id} AND word_rating != 0
            AND word = '{word}'
            """
        )

        self.conn.commit()

    def get_word_rating(self, tg_id, word):
        rating = self.cur.execute(
            f"""
            SELECT word_rating FROM words_rating
            WHERE tg_id = {tg_id} AND word = '{word}'
            """
        ).fetchone()

        return 0 if rating is None else rating

    def get_words(self):
        words = self.cur.execute(
            """
            SELECT word FROM words
            """
        ).fetchall()

        return [] if words is None else [elem[0] for elem in words]

    def get_questions(self):
        questions = self.cur.execute(
            """
            SELECT question FROM times
            """
        ).fetchall()

        return [] if questions is None else [elem[0] for elem in questions]