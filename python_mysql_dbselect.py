from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
 
 
def select_user(name):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = ("SELECT username, password FROM users WHERE username = %s")

        cursor.execute(query, (name, ))

        information = 

        for (username, password) in cursor:
            return ("{}, {}".format(username, password))
        
        # cursor.close()
        # cnx.close()

        # while row is not None:
        #     print(row)
        #     row = cursor.fetchone()
 
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()