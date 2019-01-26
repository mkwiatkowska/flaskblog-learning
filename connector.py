import sqlite3
from sqlite3 import Error
import csv



def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None


def select_all_from_table(conn, table):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM %s" %table)

    rows = cursor.fetchall()

    for row in rows:
        print(row)


def insert_data_into_db(conn, file):
    cursor = conn.cursor()
    query = "INSERT INTO Scents(scentId, scentName)" \
            "VALUES({0},{1})".format(1, 2)
    values = (scentId, scentName)
    cursor.execute(query, values)
    with open(file) as my_file:
        my_reader = csv.reader(my_file, delimiter=',')
        line_count += 0
        for row in my_reader:
            if line_count == 0:
                   

def main():
    database = "C:/Users/maria/Desktop/sqlite3 bd/testowa.db"

    connection = create_connection(database)
    with connection:
        print('select all')
        select_all_from_table(connection, 'PerfumeInfo')
        print('after')

if __name__ == '__main__':
    main()