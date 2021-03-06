from io import StringIO
import configparser
from time import sleep

import psycopg2
from requests import *
import pandas as pd

dbconfig = configparser.ConfigParser()
dbconfig.read("settings.conf")

url = "http://comtrade.un.org/api/get"
periods = []
mon = [("0" + str(i))[-2:] for i in range(1, 13)]
choose = ""
years = []
print("Select years to download: ")
while 1:
    choose = input()
    if choose == "q":
        break
    try:
        year = int(choose)
        if year not in range(1962, 2016):
            print("Year must be in range 1962 - 2015")
        else:
            years += [year] if not year in years else []
    except ValueError:
        print("Invalid year format")
    print(years)
for i in years:
    for j in mon:
        periods += [str(i)+j]
server =   dbconfig.get("DB section", "server")
user =     dbconfig.get("DB section", "user")
password = dbconfig.get("DB section", "password")
dbname =   dbconfig.get("DB section", "dbname")

try:
    if dbconfig.get("DB section", "ODBC") == "PostgreSQL":
        from psycopg2 import connect, IntegrityError, OperationalError
        db = connect("postgresql://" + user + ":" + password + "@" + server + "/" + dbname)
    elif dbconfig.get("DB section", "ODBC") == "MSSQL":
        from pymssql import connect, IntegrityError, OperationalError
        db = connect(server, user, password, dbname)
    else:
        print("This ODBC not supported")
        exit()
except OperationalError:
    print("Cannot connect to database")
    exit()

cur = db.cursor()

for period in periods:
    prm = {"max":   dbconfig.get("Data section", "max"),
           "type":  dbconfig.get("Data section", "type"),
           "freq":  "M",
           "px":    dbconfig.get("Data section", "px"),
           "ps":    period,
           "r":     dbconfig.get("Data section", "r"),
           "p":     dbconfig.get("Data section", "p"),
           "rg":    dbconfig.get("Data section", "rg"),
           "cc":    dbconfig.get("Data section", "cc"),
           "fmt":   "csv",
           "token": dbconfig.get("Data section", "token")}
    sleep(1)
    try:
        r = get(url, params=prm)
    except ConnectionError as e:
        print("Connection error: cannot make request.")
        exit()
    csvData = str(r.content)[2:-1]
    csvData = csvData.replace("\\r\\n", " \n")
    if "No data matches your query or your query" in csvData:
        print("No data for " + period)
        continue
    data = pd.read_csv(StringIO(csvData))
    headers = ",".join(['"' + i + '"' for i in data])
    for row in data.as_matrix():
        qarr = []
        for i in row:
            if not pd.isnull(i):
                if type(i) == str:
                    i = i.replace("'", "")
                    qarr += ["'" + i + "'"]
                else:
                    qarr += [str(i)]
            else:
                qarr += ["NULL"]
        query = "INSERT INTO %s (%s) VALUES (%s);" % (dbconfig.get("DB section", "tableName"), headers, ",".join(qarr))
        try:
            cur.execute(query)
            db.commit()
        except IntegrityError:
            db.rollback()
    print("Downloading successful for " + period)

db.close()
