import sys
import socket
import random
import time


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


def handle_query(qid, qname, qtype, records):
    """Handle the query message and return the response"""
    # print(f"Query: {qid} {qname} {qtype}")

    result = []
    if qname in records.keys():
        for rtype, data in records[qname]:
            if rtype == "CNAME" and qtype != "CNAME":  # G.5, G.6 example
                result.append(f"{qname} {rtype} {data}")
                new_qname = data
                result += handle_query(qid, new_qname, qtype, records)
            elif rtype == qtype:  # G.1, G.2, G.3, G.4 example
                result.append(f"{qname} {rtype} {data}")
    else:
        result.append(f"{qname} {qtype} -")

    return result


def start_server(server_port):
    """Start the server"""
    print("Starting server...")
    records = load_master_file()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", server_port))
    print(f"Server listening on port {server_port}")
    print(f"Current IP: {socket.gethostbyname(socket.gethostname())}")
    print(f"Server log: \n")

    # keep listening for incoming requests
    while True:
        message, client_address = server_socket.recvfrom(2048)
        qid, qname, qtype = message.decode().split()
        # print(f"Received message from {client_address}, Message: {message}")

        # start time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime())
        delay = random.randint(0, 4)  # simulate delay
        print(f"{timestamp} rcv {client_address[1]}: {qid} {qname} {qtype} (delay: {delay}s)")

        # handle query
        result = handle_query(qid, qname, qtype, records)
        # simulate delay
        time.sleep(delay)
        server_response = "\n".join(result).encode()
        server_socket.sendto(server_response, client_address)

        # end time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime())
        print(f"{timestamp} snd {client_address[1]}: {qid} {qname} {qtype} ")

    server_socket.close()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:  python3 server.py server_port")
        raise "Invalid arguments"

    server_port = int(sys.argv[1])
    start_server(server_port)
