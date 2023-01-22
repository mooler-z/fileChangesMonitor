import sys
import random
import os
import json
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class CreateFilesData:
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("fileUpdate.db")

    if not database.open():
        print("unable to open data source file.")
        sys.exit(1)

    query = QSqlQuery()
    query.exec_("DROP TABLE files")

    query.exec_("""CREATE TABLE files
                (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                file_name VARCHAR(150) NOT NULL,
                mod_time FLOAT NOT NULL)
                """)

    query.exec_("""INSERT INTO files (
        file_name, mod_time)
        VALUES (?, ?)""")

    json_files_path = "/home/ultron/Documents/update_files.json"

    try:
        with open(json_files_path, 'r') as json_file:
            content = json.load(json_file)
        print("Done loading file")
    except Exception:
        print(Exception)

    for key, vals in content.items():
        query.addBindValue(key)
        query.addBindValue(vals)
        query.exec_()
    print("[INFO] Database successfully created.")
    sys.exit(0)


if __name__ == "__main__":
    CreateFilesData()
