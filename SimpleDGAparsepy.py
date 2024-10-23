def dga():
    a = ['s', 'l', 'm', 'r', 't', 'o', 'k', '.', 'd', 'w']
    buf = [''] * 11

    for i in range(15):
        buf[0] = '\0'
        buf[1:] = "{}{}{}{}{}{}{}{}{}{}".format(
            a[0], a[1], a[2], a[3],
            a[4], a[5], a[6], a[7], a[8], a[9]
        )

        for j in range(len(a)):
            a[j] = chr(ord(a[j]) + 10)
            if ord(a[j]) > 122:
                a[j] = chr(97 + (ord(a[j]) % 122))

        a[7] = '.'
        print("".join(buf))

dga()
