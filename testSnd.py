# coding=utf-8
import svgwrite
from svgwrite.container import Hyperlink


def generate_slogan():
    width = 600
    height = 50

    dwg = svgwrite.Drawing('slogan.svg', profile='full', size=(u'540', u'50'))

    mask = dwg.mask((0, 0), (540, height), id='a')
    mask.add(dwg.rect((0, 0), (540, height), fill='#eee', rx=5))

    dwg.add(mask)

    g = dwg.add(dwg.g(id='g', fill='none', mask='url(#a)'))
    g.add(dwg.rect((0, 0), (width / 3, height), fill='#03a9f4'))
    g.add(dwg.rect((width / 3, 0), (width / 3, height), fill='#e91e63'))
    g.add(dwg.rect((width * 2 / 3, 0), (width * 2 / 3, height), fill='#ecf0f1'))

    slogan_link = Hyperlink('http://www.xuntayizhan.com/person/ji-ke-ai-qing-zhi-er-shi-dai-wo-dai-ma-bian-cheng-qu-ni-wei-qi-ke-hao-wan/', target='_blank')
    slogan_link.add(dwg.text('待我代码编成', insert=(10, 35), fill='#fff', font_size=30, font_family='STFangSong'))
    slogan_link.add(dwg.text('娶你为妻可好', insert=(210, 35), fill='#fff', font_size=30, font_family='STFangSong'))
    dwg.add(slogan_link)

    link = Hyperlink('http://www.hug8217.com/', target='_blank')
    link.add(dwg.text('@花仲马', insert=(410, 35), fill='#34495e', font_size=30, font_family='STFangSong'))

    dwg.add(link)

    dwg.save()


if __name__ == '__main__':
    generate_slogan()

    # __author__ = 'moxiaoxi'

# import socket
# import sys

# from netsocket import communication
# import time

# if __name__ == '__main__':

#     if len(sys.argv) < 3:
#         print("\nUsage: \n\tpython main.py <error rate> <window size> ")
#         print("\terror rate  -- the percentage error rate this is from 0% to 100%")
#         print("\twindow size -- the size of the sliding window (this must be same in both sender and receiver)")
#         exit()
#     else:
#         try:
#             WINDOW_SIZE = int(sys.argv[2])
#             ERR_RATE = int(sys.argv[1])
#         except ValueError:
#             print("Arguments must be ints ")
#             exit()

#     try:
#         f = open("myfile.txt")
#         result = open("result.txt", "a")
#     except IOError:
#         print("File Opening Error\nExiting...")
#         exit(-1)

#     sender = communication.Send('127.0.0.1',40000)
#     sender.checkState()
#     data_from_file = f.read()
#     print("Sending {} bytes of data ".format(len(data_from_file)))
#     time_1 = time.clock()
#     sender.SendSecurity(bytes(data_from_file, 'utf-8'))
#     time_2 = time.clock()
#     print("\n\n====================================================================")
#     print("TIME spent: ", time_2 - time_1)
#     print("====================================================================\n")
#     sender.close()

#     time_diff = (time_2 - time_1)
#     mesurements = "window_size: {}, error_rate: {}, time_spent: {}, speed: {}\n".format(WINDOW_SIZE, ERR_RATE, time_diff, len(data_from_file)/time_diff)
#     result.write(mesurements)
#     result.close()









