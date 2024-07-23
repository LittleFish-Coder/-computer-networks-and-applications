import sys
import socket
import random
import time
import threading

# Step 1: Initialize thread-local storage
thread_local_data = threading.local()

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


def generate_subdomains(domain):
    # metalhead.com. -> generate com. and .
    parts = domain.split(".")
    subdomains = []
    for i in range(1, len(parts) - 1):
        subdomains.append(".".join(parts[i:]))
    subdomains.append(".")
    return subdomains


def handle_query(qid, qname, qtype, records):
    """Handle the query message and return the response"""
    # print(f"Query: {qid} {qname} {qtype}")

    result = []
    if qname in records.keys():
        result.append(f"\nANSWER SECTION: ") if thread_local_data.ANSWER_SECTION_FLAG == False else None
        thread_local_data.ANSWER_SECTION_FLAG = True
        for rtype, data in records[qname]:
            if rtype == "CNAME" and qtype != "CNAME":  # G.5, G.6 example
                result.append(f"{qname} {rtype} {data}")
                new_qname = data
                result += handle_query(qid, new_qname, qtype, records)
            elif rtype == qtype:  # G.1, G.2, G.3, G.4 example
                result.append(f"{qname} {rtype} {data}")
    else:
        """
        Find the closest ancestor zone to qname for which there are known name servers.  Copy 
        all NS RRs for the zone into the authority section.  For each name server, copy any 
        known A records into the additional section.
        """
        # example.org. -> find -> org. and .
        subdomains = generate_subdomains(qname)
        for sub_qname in subdomains:
            if sub_qname in records.keys():
                result.append(f"\nAUTHORITY SECTION: ")
                authority_resource = []
                for rtype, data in records[sub_qname]:
                    result.append(f"{sub_qname} {rtype} {data}")
                    authority_resource.append(data)

                result.append(f"\nADDITIONAL SECTION: ")
                for referrer in authority_resource:
                    if referrer in records.keys():
                        for rtype, data in records[referrer]:
                            if rtype == "A":
                                result.append(f"{referrer} {rtype} {data}")
                break

    return result

def handle_client(message, client_address, server_socket, records):
    qid, qname, qtype = message.decode().split()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime())
    delay = random.randint(0, 4)  # simulate delay
    print(f"{timestamp} rcv {client_address[1]}: {qid} {qname} {qtype} (delay: {delay}s)")

    thread_local_data.ANSWER_SECTION_FLAG = False

    # handle query
    result = handle_query(qid, qname, qtype, records)
    # simulate delay
    time.sleep(delay)
    server_response = "\n".join(result).encode()
    server_socket.sendto(server_response, client_address)

    # end time
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime())
    print(f"{timestamp} snd {client_address[1]}: {qid} {qname} {qtype} \n")

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

        # Create a new thread for each client request
        client_thread = threading.Thread(target=handle_client, args=(message, client_address, server_socket, records))
        client_thread.start()

    server_socket.close()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:  python3 server.py server_port")
        raise "Invalid arguments"

    server_port = int(sys.argv[1])
    start_server(server_port)
