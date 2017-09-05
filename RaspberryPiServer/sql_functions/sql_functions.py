import sqlite3


def openSQLdb(fileName):
	db = sqlite3.connect('./'+fileName)
	return db

def createTable(db):
	# Get a cursor object
	cursor = db.cursor()
	cursor.execute('''
    	CREATE TABLE entries(id INTEGER PRIMARY KEY, IP TEXT, room TEXT,
                       	deviceType TEXT, batteryStatus TEXT, commandStatus TEXT)
	''')
	db.commit()


def insertEntry(db, IPin, roomIn, deviceTypeIn, batteryStatusIn, status): 
	cursor = db.cursor()
	# Insert user 1
	cursor.execute('''INSERT INTO entries(IP, room, deviceType, batteryStatus, commandStatus)
       	           VALUES(?,?,?,?,?)''', (IPin, roomIn, deviceTypeIn, batteryStatusIn, status))
	print('Inserted entry successfully')
 
	db.commit()


