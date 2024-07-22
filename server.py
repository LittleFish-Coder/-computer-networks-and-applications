import sys
import socket
import threading
import random
import time

def load_master_file():
    """從 master.txt 文件中加載資源記錄"""
    records = {}
    with open("master.txt", "r") as f:
        for line in f:
            domain, rtype, data = line.strip().split()
            if domain not in records:
                records[domain] = []
            records[domain].append((rtype, data))
    return records

def resolve_query(qname, qtype, records):
    """解析查詢，返回相應的資源記錄"""
    answer = []
    authority = []
    additional = []
    
    # 查找回答記錄
    while qname in records:
        for rtype, data in records[qname]:
            if rtype == 'CNAME':
                answer.append((qname, rtype, data))
                qname = data
                break
            elif rtype == qtype or qtype == "ANY":
                answer.append((qname, rtype, data))
        else:
            break
    
    # 如果找不到回答記錄，查找權威記錄
    if not answer:
        domain_parts = qname.split('.')
        for i in range(len(domain_parts)):
            subdomain = '.'.join(domain_parts[i:])
            if subdomain in records:
                for rtype, data in records[subdomain]:
                    if rtype == 'NS':
                        authority.append((subdomain, rtype, data))
                        if data in records:
                            for artype, adata in records[data]:
                                if artype == 'A':
                                    additional.append((data, artype, adata))
                if authority:
                    break
    
    return answer, authority, additional

def construct_response_message(qid, qname, qtype, records):
    """構建響應消息"""
    response = f"{qid}\n{qname} {qtype}\n"
    answer_records, authority_records, additional_records = resolve_query(qname, qtype, records)
    
    for qname, rtype, data in answer_records:
        response += f"{qname} {rtype} {data}\n"
    
    if authority_records:
        response += "AUTHORITY SECTION:\n"
    for qname, rtype, data in authority_records:
        response += f"{qname} {rtype} {data}\n"
    
    if additional_records:
        response += "ADDITIONAL SECTION:\n"
    for qname, rtype, data in additional_records:
        response += f"{qname} {rtype} {data}\n"
    
    return response.encode()

def handle_client_message(message, client_address, server_socket, records):
    """處理客戶端消息"""
    qid, qtype, qname = message.decode().strip().split()
    qid = int(qid)
    
    # 隨機延遲處理查詢
    delay = random.randint(0, 4)
    time.sleep(delay)
    
    response_message = construct_response_message(qid, qname, qtype, records)
    server_socket.sendto(response_message, client_address)
    
    # 記錄響應日志
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime())
    print(f"{timestamp} snd {client_address[1]}: {qid} {qname} {qtype} (delay: {delay}s)")

def start_server(port):
    """服務器主函數"""
    records = load_master_file()
    
    # 創建UDP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', port))
    
    print(f"Server listening on port {port}")
    
    while True:
        message, client_address = server_socket.recvfrom(2048)
        
        # 記錄接收日志
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime())
        qid, qtype, qname = message.decode().strip().split()
        print(f"{timestamp} rcv {client_address[1]}: {qid} {qname} {qtype} (delay: 0s)")
        
        threading.Thread(target=handle_client_message, args=(message, client_address, server_socket, records)).start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server.py port")
        sys.exit(1)
    
    port = int(sys.argv[1])
    start_server(port)