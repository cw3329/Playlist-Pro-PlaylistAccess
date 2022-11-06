import pymysql

def get_count_from_cursor_execution(cursor):
    values = list(cursor.fetchone().values())
    if len(values) > 1:
        return 0
    return values[0]

