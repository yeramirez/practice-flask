from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
 
 
def select_user(name):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        #query = ("SELECT username, password FROM users")
        query = ("SELECT * FROM users WHERE username = %s")

        #cursor.execute(query)
        cursor.execute(query, (name, ))
        rows = cursor.fetchall()

        if rows is not None:
            for row in rows:
                x = ("{}, {}".format(row[1],row[2]))
        else:
            print Error
            
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return rows[0]