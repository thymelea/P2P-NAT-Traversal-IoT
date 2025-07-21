# P2P NAT Traversal Demo

## 环境要求
- Python 3.7+
- 本地和公网服务器网络正常可达

## 文件说明
- `server.py`: UDP 中转服务器（部署在有公网 IP 的主机）
- `client_a.py`: 客户端 A （部署在有内网的主机）
- `client_b.py`: 客户端 B （部署在有内网的主机）

## 启动步骤

1. 启动服务器：
   ```bash
   python server.py
