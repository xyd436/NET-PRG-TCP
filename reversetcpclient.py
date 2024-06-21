from socket import *
from random import *


def main():
    # 初始化：
    server_ip = input("请输入server IP：")
    server_port = int(input("请输入server port："))

    # 建立连接：
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # 确定报文：
    Lmin = int(input("请输入Lmin(>0)："))
    Lmax = int(input("请输入Lmax(<100)："))
    # txt = "Once upon a time, in a small village nestled between rolling hills, lived a young girl named Emily. She loved exploring the woods near her home, searching for hidden treasures and secret pathways. One sunny afternoon, she stumbled upon an old, abandoned cabin hidden behind a curtain of ivy. Curiosity tingling, she pushed open the creaky door and discovered a dusty book filled with magical drawings. As she flipped through its pages, a gentle breeze whisked through the cabin, carrying with it whispers of stories long forgotten. From that day on, Emily's adventures took her beyond the woods, into realms of enchantment and wonder."
    txt = "i miss you"
    total = len(txt)
    pos = 0
    N = 0
    n = 0
    length_list = []
    data_list = []

    while pos < total:
        length = randint(Lmin, Lmax)
        if length + pos > total:
            length = total - pos

        data = txt[pos:pos + length]
        print(length, data)
        length_list.append(length)
        data_list.append(data)
        pos += length
        N += 1

    # Initialization & Agreement:
    type_no = 1
    packet = type_no.to_bytes(2, 'big') + N.to_bytes(4, 'big')
    client_socket.send(packet)
    message = client_socket.recv(1024)
    type_no = int.from_bytes(message)

    # reverseRequest & reverseAnswer:
    if type_no == 2:
        print("成功与server建立连接，即将开始传输数据！")

        while n < N:
            type_no = 3
            length = length_list[n]
            data = data_list[n]
            packet = type_no.to_bytes(2, 'big') + length.to_bytes(4, 'big') + data.encode()
            client_socket.send(packet)

            message = client_socket.recv(1024)
            type_no = int.from_bytes(message[:2])
            length = int.from_bytes(message[2:6])
            reverse_data = message[6:6 + length].decode()
            print('From Server:', type_no, length, reverse_data)

            n += 1
        client_socket.close()
        print("成功与server端断开连接！")
    else:
        print("建立连接失败：server端没有返回agreement报文")


if __name__ == '__main__':
    main()