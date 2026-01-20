for num_sx in range(100, 1000):
    gw = num_sx % 10
    sw = (num_sx // 10) % 10
    bw = num_sx // 100
    if gw**3 + sw**3 + bw**3 == num_sx:
        print("当前的三位数为水仙花数，它的值是:", num_sx)
