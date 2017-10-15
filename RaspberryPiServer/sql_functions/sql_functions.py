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
	cursor.execute('''INSERT INTO entries(IP, room, deviceType, batteryStatus, commandStatus)
       	           VALUES(?,?,?,?,?)''', (IPin, roomIn, deviceTypeIn, batteryStatusIn, status))
	print('Inserted entry successfully')
 
	db.commit()


def updateEntry(db, room, newStatus, deviceType):
	cursor = db.cursor()
	
	cursor.execute('''UPDATE entries SET commandStatus = ? WHERE room = ? and deviceType = ? ''', (newStatus, room, deviceType,) )
	#cursor.execute('''UPDATE entries SET commandStatus = ? WHERE room = ?''', (newStatus, room,) )
	print("Successfully updated database")
	db.commit()

def searchForEntry(db, room,deviceType):
	cursor = db.cursor()
	cursor.execute('''SELECT commandStatus from entries WHERE room = ? and deviceType = ?''', (room,deviceType,))
	roomStatus = cursor.fetchone()

	return roomStatus

def checkIfEntryExists(db,room,deviceType):
	cursor = db.cursor()
	cursor.execute('''SELECT commandStatus from entries WHERE room = ? and deviceType = ?''', (room,deviceType,))
	data=cursor.fetchone()
    	if data is None:
       		print('There is no component named this ')
		return False
    	else:
        	print('Component found')
		return True
