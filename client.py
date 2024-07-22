import sys
import socket
import random
import time

def construct_query_message(qid, qtype, qname):
    """構建查詢消息"""
    message = f"{qid} {qtype} {qname}"
    return message.encode()

def parse_response_message(response):
    """解析響應消息"""
    response = response.decode()
    parts = response.split("\n")
    return parts

def client(server_port, qname, qtype, timeout):
    """客戶端主函數"""
    qid = random.randint(0, 65535)  # 生成隨機查詢ID
    query_message = construct_query_message(qid, qtype, qname)

    # 創建UDP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)
    server_address = ('localhost', server_port)

    try:
        # 發送查詢消息到服務器
        print(f"Sending query: {query_message}")
        client_socket.sendto(query_message, server_address)

        # 等待響應
        response_message, _ = client_socket.recvfrom(2048)
        response_parts = parse_response_message(response_message)
        
        # 打印響應
        print(f"ID: {response_parts[0]}")
        print("QUESTION SECTION:")
        print(f"{response_parts[1]}\n")
        print("ANSWER SECTION:")
        in_authority = False
        in_additional = False
        for part in response_parts[2:]:
            if part == "AUTHORITY SECTION:":
                in_authority = True
                in_additional = False
                print("\nAUTHORITY SECTION:")
            elif part == "ADDITIONAL SECTION:":
                in_additional = True
                in_authority = False
                print("\nADDITIONAL SECTION:")
            else:
                if part:
                    print(part)

    except socket.timeout:
        print("timed out")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 client.py server_port qname qtype timeout")
        sys.exit(1)

    server_port = int(sys.argv[1])
    qname = sys.argv[2]
    qtype = sys.argv[3]
    timeout = int(sys.argv[4])

    client(server_port, qname, qtype, timeout)