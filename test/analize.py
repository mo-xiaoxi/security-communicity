#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi '
__Filename__ = 'analize.py'

import math
import matplotlib.pyplot as plt

class Analize_:
    def __init__(self, key, val):
        self.key = (int(key[0]), int(key[1]))
        self.val = val

    def __str__(self):
        return "{:4}  {:4}  {:12}".format(self.key[0], self.key[1], round(self.val,3))


if '__main__' == __name__:

    f = open("result.txt")

    collect = {}
    data = []

    for line in f:
        d = line.split(",")
        d = [  i.strip() for i in d ]
        d_ = [ i.split(":")[1] for i in d ]
        d_ = [ i.strip() for i in d_ ]
        n = [ float(i) for i in d_ ]
        collect.setdefault((n[0], n[1]), []).append((n[2], n[3]))

    for d in collect:
        # print(d)
        s = collect[d]
        # k = "\n".join(str(i[1]) for i in s)
        k = sum(map(lambda x: x[1], s))/len(s)
        data.append(Analize_(d, k))

    data.sort(key=lambda x: x.key[0]*1000+x.key[1])

    g = []
    index = 0
    while index < len(data):

        d = data[index: index+8]
        index += 8
        t = []
        for i in d:
            t.append(i)
            print(i)
        print()

        plt.plot([i.val for i in t], label="window size: " + str(t[0].key[0]))
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                          ncol=2, mode="expand", borderaxespad=0.)

        g.append(t)


    plt.ylabel("Speed: bytes/sec")
    plt.xlabel("Error rate out of 10")
    plt.grid(b=True, which='major', color='b', linestyle='-')
    # plt.grid(b=True, which='minor', color='r', linestyle='--')
    plt.show()



