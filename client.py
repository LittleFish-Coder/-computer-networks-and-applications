import sys
import socket
import random


def construct_query_message(qid, qname, qtype):
    message = f"{qid} {qname} {qtype}"
    return message.encode()


def client(server_port, qname, qtype, timeout):
    # client message and info
    qid = random.randint(0, 65535)  # Assign a randomly generated, 16-bit unsigned integer as the qid
    query_message = construct_query_message(qid, qname, qtype)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)

    server_address = ("localhost", server_port)

    # connect to server
    try:
        # print(f"Sending query: {query_message}\n")
        client_socket.sendto(query_message, server_address)

        # wait for response
        response_message, _ = client_socket.recvfrom(2048)
        response_parts = response_message.decode()

        print(f"ID: {qid}\n")
        print("QUESTION SECTION: ")
        print(f"{qname} {qtype}")
        # print("ANSWER SECTION: ")
        print(f"{response_parts}\n")

    except socket.timeout:
        print("timed out")
    finally:
        client_socket.close()


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: python3 client.py server_port qname qtype timeout")
        raise "Invalid arguments"

    """ Example
    $ python3 client.py 54321 example.com. A 5
    ID: 17564

    Question Section:
    example.com. A

    Answer Section:
    example.com. A 93.184.215.14

    > Server log:
    2024-05-21 19:20:31.750 rcv 62370: 17564 example.com. A (delay: 3s)
    2024-05-21 19:20:34.756 snd 62370: 17564 example.com. A
    
    """

    server_port = int(sys.argv[1])
    qname = sys.argv[2]
    qtype = sys.argv[3]
    timeout = int(sys.argv[4])

    client(server_port, qname, qtype, timeout)
