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









