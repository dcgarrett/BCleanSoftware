import socket
import threading
import sql_functions as sq
#reload(sq)
from PIL import Image
import webbrowser

#bind_ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1] # For network-connected computers
bind_ip = '172.24.1.1'
#bind_ip = '10.254.58.49' # Dave testing
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

# Databse stuff:
db_name = 'currentDB'
# Only need these lines if you're initializing a db:
db = sq.openSQLdb(db_name)
#sq.createTable(db)
db.close()

print( "Listening on %s %d" % (bind_ip, bind_port))

def parseInput(inputString):
    parsedList = inputString.split(",") # split on every comma
    room = parsedList[0].split(": ")[1]
    deviceType = parsedList[1].split(": ")[1]
    batteryStatus = parsedList[2].split(": ")[1]
    status = parsedList[3].split(": ")[1]
    return room, deviceType, batteryStatus, status

def writeToFile(request):
	with open('./log_test.txt','w') as f:
		f.write(request)

def tupleToString(tup):
    str1 = str(tuple(map(str,tup)))
    #str1.lstrip(['(\''])
    #str1.rstrip([\',)'])
    return str1
 
def handle_client_connection(client_socket,IP):
    print('\n')
    request = client_socket.recv(1024)
#    print( 'Received %s ' % request)
    room, deviceType, batteryStatus, commandStatus = parseInput(request)
    print('Received %s %s %s %s ' % parseInput(request) )
#    print('from IP address %s: ' % IP)

    # Need to convert tuples to strings:
    #room_str = tuple(map(str,room))
    #deviceType_str = tuple(map(str,deviceType))
    #batteryStatus_str = tuple(map(str,batteryStatus))
    #status_str = tuple(map(str,status)) 

    # Log all entries
    db = sq.openSQLdb(db_name)
    if sq.checkIfEntryExists(db,room,deviceType):
        sq.updateEntry(db,room,commandStatus,deviceType)
        #sq.updateEntry(db,str(room).encode(),str(commandStatus).encode(),str(deviceType).encode())
    else:
        sq.insertEntry(db,IP,room,deviceType,batteryStatus,commandStatus)

    if deviceType == "DISPENSER":
        # Check if the toilet was flushed
        print("Dispenser detected - checking associated toilet: ") 
        
        dispToiletStatus = sq.searchForEntry(db,room,"TOILET")[0].encode('ascii')

        if dispToiletStatus.strip() == "FLUSH":
            print("Flush detected. Current message: %s Sending message to dispenser." % dispToiletStatus.strip()) 
            client_socket.send('FLUSH\r')
            print("Updating database to NOFLUSH")
            #sq.updateEntry(db,room, "NOFLUSH","TOILET")
        else:
            print("No flush detected. Current associated toilet message:\'%s\'" % dispToiletStatus )
            client_socket.send('Message received by server \r')

        if commandStatus == "DISPENSED":
            webbrowser.open('Compliance.png')
            sq.updateEntry(db,room,"NOFLUSH","TOILET")

        if commandStatus == "ALARM":
            print("Alarm detected. Opening warning.")
            #img = Image.open('Noncompliance.png')
            #img.show()
            webbrowser.open('Noncompliance.png')
            sq.updateEntry(db,room,"NOFLUSH","TOILET")

        client_socket.close()
    else: # Toilet
        # Depending if it was flushed, update database
        print("Message received from toilet")
        if commandStatus == "FLUSH ":
            client_socket.send('Flush command received \r')
            client_socket.send('Message received by server \r')
        else:
            client_socket.send('Message received by server \r')
        client_socket.close()
    db.close()

while True:
    client_sock, address = server.accept()
    #    print( 'Accepted connection from %s %s' % (address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,address[0],)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()

# def logReceipt(IP, message):
	# Add received messaege and associated IP address to a database

# def getIPfromDB(message):
	# Search for the IP address associated with a given device based on a message received from it


