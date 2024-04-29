import socket

def getIPv4Addr():
    hostname = socket.gethostname()
    exHost = socket.gethostbyname_ex(hostname)

    listTypeReference = []

    for addrInfo in exHost:
        # Filter the list which has items inside
        if (type(addrInfo) == type(listTypeReference) and addrInfo.__len__() > 0):
            for ip in addrInfo:
                # Find the IP that starts in 10.0
                if (ip.rfind("10.0.") > -1):
                    return ip