import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


class SQLServer:
    def __init__(self, database, user='root', password='', host='localhost'):
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

    def customQueryToSQL(self, query):
        cursor = self._mySQLconnection.cursor()
        cursor.execute(query)
        try:
            return cursor.fetchall()
        except:
            return 'Nothing returned'

    def getPandasTable(self, table, query=None, columns=None):
        cursor = self._mySQLconnection.cursor(buffered=True)
        if query == None:
            cursor.execute("SELECT * FROM " + table)
        else:
            cursor.execute(query)

        try:
            df = pd.DataFrame(cursor.fetchall())
        except:
            raise TypeError("Custom query given doesn't return a proper table to convert to a dataFrame")

        # Get column names
        cursor.execute("SHOW columns FROM " + table)
        if columns == None:
            columns = [column[0] for column in cursor.fetchall()]
        df.columns = columns
        # Remove automatic index
        df.set_index('id', inplace=True, drop=True)
        df = df.where((pd.notnull(df)), None)
        try:
            return df
        except:
            raise TypeError("Custom query given doesn't return a proper table to convert to a dataFrame")

    def createMetaTable(self):
        self.customQueryToSQL('DROP TABLE IF EXISTS meta')
        self.customQueryToSQL("""CREATE TABLE IF NOT EXISTS meta (
          `id` int(1) NOT NULL AUTO_INCREMENT,
          `lat` double NOT NULL,
          `lng` double NOT NULL,
          `accuracy` float,
          `scheduled` varchar(5),
          `threshold` float,
          `day` varchar(2) NOT NULL ,
          PRIMARY KEY (`id`)
        )""")
        self.customQueryToSQL(
            "INSERT INTO meta (lng,lat,day) VALUES ('"
            + str(-79.403610) + "','" + str(43.652042) + "','" + 'na' + "')")

    def setDayToPickupWithAcc(self, accuracy, day='na'):
        self._day = day
        cursor = self._mySQLconnection.cursor(buffered=True)
        cursor.execute("UPDATE meta SET day='" + day + "',accuracy= '" + accuracy + "' WHERE id=1")

    def setDayToPickup(self, day='na'):
        self._day = day
        cursor = self._mySQLconnection.cursor(buffered=True)
        cursor.execute("UPDATE meta SET day='" + day + "' WHERE id=1")

    def getIntialLocation(self):
        cursor = self._mySQLconnection.cursor(buffered=True)
        cursor.execute("SELECT lat,lng FROM meta WHERE id = 1")
        try:
            self._coordinate = cursor.fetchall()
            self._coordinate = self._coordinate[0]
        except:
            self._coordinate = cursor.fetchall()
        return self._coordinate

    def getDayToPickup(self):
        cursor = self._mySQLconnection.cursor(buffered=True)
        cursor.execute("SELECT day FROM meta WHERE id = 1")
        try:
            self._day = cursor.fetchall()
            self._day = self._day[0][0]
        except:
            self._day = cursor.fetchall()
        return self._day

    def close(self):
        # closing database connection.
        if (self._mySQLconnection.is_connected()):
            self._mySQLconnection.close()
            print("MySQL connection is closed")

    def getSQL(self):
        return self._mySQLconnection

    def insertPandas(self, table, df, drop=False, create=None, withSchedule=False):

        if drop:
            self.customQueryToSQL('DROP TABLE ' + table)
        if not create == None:
            self.customQueryToSQL(create)

        if table == 'trainingData':
            if withSchedule:
                for index, row in df.iterrows():
                    self.customQueryToSQL(
                        "INSERT INTO " + table + " (distance,time,day,month,availability,schedule,date,lat,lng) VALUES ('"
                        + str(row['distance']) + "','" + str(row['time']) + "','" + str(row['day']) + "','" + str(
                            row['month']) + "','" + str(row[
                                                            'availability']) + "','" + str(
                            row['schedule']) + "','" + str(row['date']) + "','" +
                        str(row['lat']) + "','" + str(row['lng']) + "')")
            else:
                for index, row in df.iterrows():
                    self.customQueryToSQL(
                        "INSERT INTO " + table + " (distance,time,day,month,availability,date,lat,lng) VALUES ('"
                        + str(row['distance']) + "','" + str(row['time']) + "','" + str(row['day']) + "','" + str(
                            row['month']) + "','" + str(row[
                                                            'availability']) + "','" + str(row['date']) + "','" +
                        str(row['lat']) + "','" + str(row['lng']) + "')")
        elif table == 'markers':
            self.customQueryToSQL('DELETE FROM ' + table)
            self.customQueryToSQL('ALTER TABLE ' + table + ' AUTO_INCREMENT = 1')
            for index, row in df.iterrows():
                self.customQueryToSQL(
                    "INSERT INTO " + table + " (priority,lat,lng,availability,date,time,DayOfTheWeek,address) VALUES ('" +
                    str(row['priority']) + "','"
                    + str(row['lat']) + "','" + str(row['lng']) + "','" + str(row['availability']) + "','" + str(row[
                                                                                                                     'date']) + "','" + str(
                        row['time']) + "','" + str(row['DayOfTheWeek']) + "','" + str(row['address']) + "')")
        else:
            raise TypeError("Table given not correct")

    def getMarkersFromTraining(self, table='trainingData'):
        return self.getPandasTable(table,
                                   query="SELECT t1.id,t1.lat,t1.lng,t1.availability,t1.date,t1.time FROM " + table + " t1 WHERE t1.id = (SELECT MAX(t2.id) FROM " + table + " t2 WHERE t2.lat = t1.lat AND t2.lng = t1.lng)",
                                   columns=['id', 'lat', 'lng', 'availability', 'date', 'time'])


if __name__ == '__main__':
    sql = SQLServer('dumpstersite')
    # print(sql.customQueryToSQL('select accessibility from markers'))
    # print(sql.customQueryToSQL('alter table markers add distance decimal'))
    print(sql.getPandasTable("markers"))
    sql.writePandas("raw", pd.read_csv("training.csv", na_values=['NA', '?']))
    sql.close()
