import socket
import threading
import time
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

NAME = "CLIENT_B"
PEER = "CLIENT_A"

SERVER_IP = "192.168.1.29"
SERVER_PORT = 12500

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('', 0))  # 随机端口

# 监听线程
def listen():
    while True:
        try:
            data, addr = client.recvfrom(1024)
            logging.info(f"[{NAME}] Received from {addr}: {data.decode()}")
        except socket.timeout:
            logging.warning(f"[{NAME}] Timeout while listening for data.")
        except Exception as e:
            logging.error(f"[{NAME}] Error while receiving data: {e}")
            break

# 发送数据的函数
def send_message(message, addr):
    try:
        client.sendto(message.encode(), addr)
        logging.info(f"[{NAME}] Sent message: {message}")
    except Exception as e:
        logging.error(f"[{NAME}] Error while sending message: {e}")

# 获取对方地址的函数
def get_peer_address():
    send_message(f"GETPEER:{PEER}", (SERVER_IP, SERVER_PORT))
    try:
        data, _ = client.recvfrom(1024)
        response = data.decode()
        logging.info(f"[{NAME}] Response from server: {response}")

        if response.startswith("PEER:"):
            ip, port = response.split(":")[1:]
            peer_addr = (ip, int(port))
            logging.info(f"[{NAME}] Got peer address: {peer_addr}")
            return peer_addr
        else:
            logging.error(f"[{NAME}] Failed to get peer address: {response}")
            return None
    except socket.timeout:
        logging.error(f"[{NAME}] Timeout while getting peer address.")
        return None
    except Exception as e:
        logging.error(f"[{NAME}] Error while getting peer address: {e}")
        return None

# 注册到服务器的函数
def register_to_server():
    send_message(f"REGISTER:{NAME}", (SERVER_IP, SERVER_PORT))
    logging.info(f"[{NAME}] Registered to server")

# 打洞函数
def hole_punch(peer_addr):
    for i in range(5):
        try:
            send_message(f"Punch from {NAME}", peer_addr)
            time.sleep(1)
        except socket.timeout:
            logging.warning(f"[{NAME}] Timeout while punching. Retrying...")
        except Exception as e:
            logging.error(f"[{NAME}] Error while sending punch: {e}")
            break

def main():
    # 注册到服务器
    register_to_server()

    # 获取对方地址
    peer_addr = get_peer_address()
    if not peer_addr:
        exit(1)

    # 启动监听线程
    threading.Thread(target=listen, daemon=True).start()

    # 打洞
    hole_punch(peer_addr)

    # 聊天循环
    while True:
        msg = input(f"[{NAME}] Enter message (type 'exit' to quit): ")
        if msg.lower() == 'exit':
            logging.info(f"[{NAME}] Exiting chat...")
            break
        try:
            send_message(f"{NAME} says: {msg}", peer_addr)
        except socket.timeout:
            logging.warning(f"[{NAME}] Timeout while sending message.")
        except Exception as e:
            logging.error(f"[{NAME}] Error while sending message: {e}")

if __name__ == '__main__':
    main()

