import ctypes as C
import multiprocessing as mp
import subprocess
from dataclasses import dataclass

@dataclass
class Connection:
    local_addr: str
    remote_addr: str
    state: str

    def __repr__(self):
        return f'Ip local: {self.local_addr}, ip remote: {self.remote_addr}, state: {self.state}'

# Only supports ipv4, later ipv6 and both
class IpStat:
    def __init__(self, ip = "ipv4"):
        self.connections = self.getIpStat()
        self.amount = len(self.connections)
        self.ptr = 0

    def parseIpStat(self, _stdout):
        connections = []

        for line in _stdout.split("\n")[1:]:
            try:
                line = line.split()
                connections.append(Connection(line[0], line[1], line[2]))
            except:
                continue

        return connections
        
    # Allows you to create an C++ ForeignConnections_IPv4 using createForeignConnections_IPv4()
    def getIpStat(self):
        return self.parseIpStat(subprocess.run(["./cffi/ipstat"], capture_output=True).stdout.decode())

    def __iter__(self):
        return self

    def __next__(self):
        if self.ptr < self.amount:
            nextConnection = self.connections[self.ptr]
            self.ptr += 1
            return nextConnection
        else:
            raise StopIteration()

def getForeignIPs():
    addresses = []
    for conn in IpStat():
        if conn.remote_addr != "0.0.0.0:0":
            addresses.append(conn.remote_addr.split(":")[0])
    return addresses

if __name__ == "__main__":
    print(getForeignIPs())
    #print("Right now let's make our netstat version iterable")
    #for conn in IpStat():
    #    print(conn)
    #print(type(conn))
    #print(f'Ip local: {conn.local_addr}, ip remote: {conn.remote_addr}, stat: {conn.state}')
