import mysql.connector
from mysql.connector import FieldType

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(option_files='dbFile/config.cnf', autocommit=True)
    # connection = mysql.connector.connect(option_files='/home/COMP639S1GroupAZ/COMP639S1_Group_AZ/dbFile/config.cnf', autocommit=True)
    dbconn = connection.cursor()
    return dbconn

# def updateSQL(sql command, values in list):
def updateSQL(sql, val):
    connection = getCursor()
    connection.execute(sql, val)
    return connection.rowcount

# def insertSQL(sql command, values in list):
def insertSQL(sql, val):
    connection = getCursor()
    connection.execute(sql, val)
    return connection.lastrowid

# def deleteSQL(sql command, values in list):
def deleteSQL(sql, val):
    connection = getCursor()
    connection.execute(sql, val)
    return connection.rowcount

# def fetchAll(sql command, values in list):
def fetchAll(sql, val=None):
    connection = getCursor()
    connection.execute(sql,val)
    return connection.fetchall()

# def fetchOne(sql command, values in list, return with description):
def fetchOne(sql, val, withDescription=False):
    connection = getCursor()
    connection.execute(sql, val)
    result = connection.fetchone()
    try:
        if withDescription:
            # Extract field names from the description of the connection object and store them in the 'keys' list
            keys = [i[0] for i in connection.description]
            # Use the zip function to pair each field name with its corresponding result and create a dictionary
            result_dict = dict(zip(keys, result))
            return result_dict
    except:
        return False
    return result

