from socket import*
from select import*

def main():
    server_socket = socket(AF_INET, SOCK_STREAM) # 欢迎套接字
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 允许地址重用
    server_port = 12345
    server_socket.bind(('', server_port))
    server_socket.listen(10) # 限定最大并行连接数量：10
    print("TCP服务器已启动！")

    inputs = [server_socket]

    while True:
        readable, _, _ = select(inputs, [], [])  # 使用 select 监听可读事件

        for sock in readable:
            if sock == server_socket: # 有新的连接请求
                connection_socket, addr = server_socket.accept()    # 连接套接字，完成握手
                print(f"收到来自 {addr} 的连接")
                connection_socket.setblocking(False)  # 设置连接套接字为非阻塞模式
                inputs.append(connection_socket)  # 将新的连接套接字添加到 inputs 列表中
            else: # sock = connection_socket
                try:
                    message = sock.recv(1024) # initialization
                    if message:
                        type_no = int.from_bytes(message[:2])
                        length = int.from_bytes(message[2:6])
                        data = message[6:6 + length].decode()
                        print(f"收到来自 {sock.getpeername()} 的数据：", type_no, length, data)

                        if type_no == 1:
                            type_no = 2
                            packet = type_no.to_bytes(2,'big')
                            sock.send(packet)
                        else:
                            type_no = 4
                            length = length.to_bytes(4,'big')
                            reverse_data = data[::-1].encode()
                            packet = type_no.to_bytes(2,'big')+length+reverse_data
                            sock.send(packet)
                    else:
                        print(f"客户端 {sock.getpeername()} 已断开连接")
                        inputs.remove(sock)
                        sock.close()

                except ConnectionResetError:
                    # 客户端强制断开连接
                    print(f"客户端 {sock.getpeername()} 强制断开连接")
                    inputs.remove(sock)
                    sock.close()

    server_socket.close()


if __name__ == '__main__':
    main()