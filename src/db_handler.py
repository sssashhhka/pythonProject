import sqlite3
import os
from src import logger

version: str = "DB_handler v.1.2 stable"


class Database:
    def __init__(self, db_name: str):
        self.database = None
        self.db_cursor = None
        self.db_path: str = f"database/{db_name}.sqlite"
        self.log = logger.log

    @staticmethod
    def db(func):
        def inner(*args, **kwargs):
            logger.log(f"Connecting to database for [{func.__name__}]", "Info")
            db.db_open()
            f = func(*args, **kwargs)
            db.db_close()
            return f
        return inner

    def db_open(self):
        try:
            self.database = sqlite3.connect(self.db_path)
        except sqlite3.OperationalError:
            try:
                os.mkdir("database")
            except FileExistsError:
                pass
        else:
            pass
        finally:
            self.log("Connected to database", "Info")
            self.db_cursor = self.database.cursor()

    def db_close(self):
        self.database.commit()
        self.db_cursor.close()
        self.log("Connection closed", "Info")

    @db
    def insert(self, *, table_name: str, **values):
        list_of_columns: list = []
        list_of_values: list = []
        n = 0
        while n < len(values):
            for parameter, value in values.items():
                n += 1
                list_of_columns.append(parameter)
                list_of_values.append('"')
                list_of_values.append(value)
                list_of_values.append('"')
                if n < len(values):
                    list_of_columns.append(", ")
                    list_of_values.append(", ")
                else:
                    pass

        columns_out = "".join(list_of_columns)
        values_out = "".join(list_of_values)
        try:
            self.db_cursor.execute(f"INSERT INTO '{table_name}' ({columns_out}) VALUES ({values_out})")
        except sqlite3.OperationalError:
            self.log("Invalid arguments!", "Error")
        else:
            self.log("Values successfully inserted", "Info")

    @db
    def update(self, *, table_name: str, where: tuple[str, str], **values):
        data = self.db_cursor.execute(f"SELECT rowid FROM {table_name} WHERE {where[0]} = '{where[1]}'")
        try:
            rowid = data.fetchone()[0]
        except TypeError:
            self.log("Invalid filter", "Error")
        else:
            for column, value in values.items():
                self.db_cursor.execute(f"UPDATE '{table_name}' SET {column} = '{value}' WHERE rowid = '{rowid}'")

    @db
    def delete(self, *, table_name: str, where: tuple[str, str]):
        # USE WITH CARE because record deletes permanently
        self.db_cursor.execute(f"DELETE FROM {table_name} WHERE {where[0]} = '{where[1]}'")

    @db
    def get(self, *, table_name: str, column: str, where: tuple[str, str] = ("None", "None")) -> list:
        try:
            if where[0] == "None" or where[1] == "None":
                result = self.db_cursor.execute(f"SELECT {column} FROM {table_name}")
                result = result.fetchall()

                return result
            else:
                result = self.db_cursor.execute(f"SELECT {column} FROM {table_name} WHERE {where[0]} = '{where[1]}'")
                result = result.fetchall()
                return result
        except sqlite3.OperationalError:
            self.log("Invalid arguments!", "Error")


db = Database("users")
