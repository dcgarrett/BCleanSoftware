import socket
import threading
import sql_functions as sq
#reload(sq)

#bind_ip = '172.24.1.1'
bind_ip = '10.254.58.49' # Dave testing
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

# Databse stuff:

#db = sq.openSQLdb("testdb")
#sq.createTable(db)

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

def handle_client_connection(client_socket,IP):
    request = client_socket.recv(1024)
#    print( 'Received %s ' % request)
    room, deviceType, batteryStatus, commandStatus = parseInput(request)
    print('Received %s %s %s %s ' % parseInput(request) )
    print('from IP address %s: ' % IP)
    client_socket.send('Message received by server \r')

    db = sq.openSQLdb("testdb")
    sq.insertEntry(db,IP,room,deviceType,batteryStatus,commandStatus)
    db.close()

    if request ==str(5).encode():
        writeToFile(request)
        client_socket.close()
    else:
        writeToFile(request)
        client_socket.close()

while True:
    client_sock, address = server.accept()
    print( 'Accepted connection from %s %s' % (address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,address[0],)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()

# def logReceipt(IP, message):
	# Add received messaege and associated IP address to a database

# def getIPfromDB(message):
	# Search for the IP address associated with a given device based on a message received from it


