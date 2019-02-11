import mysql.connector
from mysql.connector import Error
import pandas as pd

class SQLServer:
    def __init__(self,database,user='root',password='',host='localhost'):
        try:
            self._mySQLconnection = mysql.connector.connect(host=host,
                                                      database=database,
                                                      user=user,
                                                      password=password)
        except Error as e:
            print("Error while connecting to MySQL", e)

    def queryToSQL(self,query):
        cursor = self._mySQLconnection.cursor()
        cursor.execute(query)
        try:
            return cursor.fetchall()
        except:
            return 'Nothing returned'

    def getPandasTable(self, table, query=None):
        cursor = self._mySQLconnection.cursor()
        if query == None:
            cursor.execute("select * from "+table)
        else:
            cursor.execute(query)
        try:
            return pd.DataFrame(cursor.fetchall())
        except:
            return None

    def close(self):
        # closing database connection.
        if (self._mySQLconnection.is_connected()):
            self._mySQLconnection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    sql = SQLServer('dumpstersite')
    print(sql.queryToSQL('select availability from markers'))
    print(sql.queryToSQL('alter table markers add distance decimal'))