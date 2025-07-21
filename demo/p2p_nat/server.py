import socket
import json

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 12500))

logging.info("Server listening on port 12500...")

while True:
    try:
        data, addr = server.recvfrom(1024)
        message = data.decode()

        logging.info(f"Received '{message}' from {addr}")

        if message.startswith("REGISTER:"):
            name = message.split(":")[1]
            clients[name] = addr
            logging.info(f"Registered {name} with address {addr}")

        elif message.startswith("GETPEER:"):
            peer_name = message.split(":")[1]
            if peer_name in clients:
                peer_addr = clients[peer_name]
                # 确保返回的是PEER地址
                response = f"PEER:{peer_addr[0]}:{peer_addr[1]}"
                server.sendto(response.encode(), addr)
            else:
                server.sendto(b"ERROR: Peer not found", addr)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
