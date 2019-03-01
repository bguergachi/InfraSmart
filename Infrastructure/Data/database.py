import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine

class SQLServer:
    def __init__(self,database,user='root',password='',host='localhost'):
        try:
            self._mySQLconnection = mysql.connector.connect(host=host,
                                                      database=database,
                                                      user=user,
                                                      password=password)
        except Error as e:
            print("Error while connecting to MySQL", e)

        self._database = database
        self._user = user
        self._password = password
        self._host = host

    def customQueryToSQL(self,query):
        cursor = self._mySQLconnection.cursor()
        cursor.execute(query)
        try:
            return cursor.fetchall()
        except:
            return 'Nothing returned'

    def getPandasTable(self, table=None, query=None):
        cursor = self._mySQLconnection.cursor()
        if query == None:
            cursor.execute("select * from "+table)
        elif table==None:
            cursor.execute(query)
        else:
            raise TypeError("Custom query given doesn't return a proper table to convert to a dataFrame")

        try:
            df = pd.DataFrame(cursor.fetchall())
        except:
            raise TypeError("Custom query given doesn't return a proper table to convert to a dataFrame")

        #Get column names
        cursor.execute("SHOW columns FROM " + table)
        columns = [column[0] for column in cursor.fetchall()]
        df.columns = columns
        #Remove automatic index
        df.set_index('id', inplace=True, drop=True)
        try:
            return df
        except:
            raise TypeError("Custom query given doesn't return a proper table to convert to a dataFrame")

    def setDayToPickup(self,day='na'):
        self._day = day
        cursor = self._mySQLconnection.cursor()
        cursor.execute("update day set day='"+day+"' where id=1")

    def getDayToPickup(self):
        cursor = self._mySQLconnection.cursor()
        cursor.execute("SELECT day from day WHERE id = 1")
        self._day = cursor.fetchall()
        return self._day

    def close(self):
        # closing database connection.
        if (self._mySQLconnection.is_connected()):
            self._mySQLconnection.close()
            print("MySQL connection is closed")

    def getSQL(self):
        return self._mySQLconnection

    def writePandas(self,table,df,exists='replace'):
        engine = create_engine("mysql+mysqlconnector://"+self._user+":"+self._password+"@"+self._host+"/"+self._database,echo=False)
        df.to_sql(name=table,con=engine,if_exists = exists)

    def getMarkersFromRaw(self):
        return self.getPandasTable(query="SELECT t1.* FROM raw t1 WHERE t1.index = (SELECT MAX(t2.index) FROM raw t2 WHERE t2.Day = t1.Day)")

if __name__ == '__main__':
    sql = SQLServer('dumpstersite')
    #print(sql.customQueryToSQL('select accessibility from markers'))
    #print(sql.customQueryToSQL('alter table markers add distance decimal'))
    print(sql.getPandasTable("markers"))
    sql.writePandas("raw",pd.read_csv("training.csv", na_values=['NA', '?']))
    sql.close()