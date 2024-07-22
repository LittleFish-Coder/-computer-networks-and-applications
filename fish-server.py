import sys
import socket


def load_master_file():
    """Load resource records from master.txt file"""
    print("Loading master file...")
    records = {}
    with open("master.txt", "r") as f:
        for line in f:
            domain, rtype, data = line.strip().split()
            # print(domain, rtype, data)
            if domain not in records:
                records[domain] = []
            records[domain].append((rtype, data))
    return records

def handle_query(query_message, records):
    """Handle the query message and return the response"""
    qid, qtype, qname = query_message.decode().split()
    print(f"Query: {qid} {qtype} {qname}")

    response = ""
    if qname in records:
        for rtype, data in records[qname]:
            response += f"{qname} {rtype} {data}\n"
    else:
        response = f"{qname} {qtype} - Error: HOST NOT FOUND\n"
    
    return response.encode()
    pass

def start_server(server_port):
    """Start the server"""
    print("Starting server...")
    records = load_master_file()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', server_port))
    print(f"Server listening on port {server_port}")
    print(f"Current IP: {socket.gethostbyname(socket.gethostname())}")

    
    # keep listening for incoming requests
    while True:
        message, client_address = server_socket.recvfrom(2048)
        print(f"Received message from {client_address}, Message: {message}")
        handle_query(message, records)
        server_socket.sendto(message, client_address)

    server_socket.close()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:  python3 server.py server_port")
        raise 'Invalid arguments'
    
    server_port = int(sys.argv[1])
    start_server(server_port)