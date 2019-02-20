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

    def customQueryToSQL(self,query):
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

        df = pd.DataFrame(cursor.fetchall())
        cursor.execute("SHOW columns FROM " + table)
        columns = [column[0] for column in cursor.fetchall()]
        df.columns = columns
        df.set_index('id', inplace=True, drop=True)
        try:
            return df
        except:
            raise TypeError("Custom query given doesn't return a proper table to convert to a dataFrame")

    def setDayToPickup(self,day='na'):
        self._day = day
        cursor = self._mySQLconnection.cursor()
        cursor.execute("update day set day="+day+" where id=1")

    def close(self):
        # closing database connection.
        if (self._mySQLconnection.is_connected()):
            self._mySQLconnection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    sql = SQLServer('dumpstersite')
    #print(sql.customQueryToSQL('select accessibility from markers'))
    #print(sql.customQueryToSQL('alter table markers add distance decimal'))
    print(sql.getPandasTable("markers"))
    sql.close()