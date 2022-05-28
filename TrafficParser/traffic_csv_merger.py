#!/usr/bin/env python
"""
traffic_csv_merger.py merge all filtered traffic_csvs from the same original_pacps_dataest, class and vpn type into one merged csv file.
"""

import os
import argparse
import csv
from sessions_plotter import *

FLAGS = None

# INPUT = "../raw_csvs/CICNTTor2017/tor"
# INPUT = "../raw_csvs/iscxNTVPN2016" # ""
# INPUT = "D:/TS/Internet Traffic Classification/TrafficParser/test_pcaps/my_chat"
INPUT = "./test_pcaps/my_chat"
# OUTPUT1 = "CICNTTor_browsing_tor.raw.csv"
# OUTPUT2 = "CICNTTor_browsing_others_tor.raw.csv"
# OUTPUT1 = "iscx_email.raw.csv"
# OUTPUT2 = "iscx_email_others.raw.csv"
# OUTPUT3 = "iscx_video_voip.raw.csv"
OUTPUT1 = "my_chat.raw.csv"
OUTPUT2 = "my_chat_others.raw.csv"

# FILTER_LIST = [(["audio", "voip"], True), (["tor", "vpn"], False)] #-> voip, , "tor"
# FILTER_LIST = [(["video", "youtube", "vimeo", "netflix"], True), (["tor", "vpn"], False)] #-> video
# FILTER_LIST = [(["audio", "voip"], True), (["spotify"], False)] #-> voip, , "tor"
# FILTER_LIST = [(["ftps", "scp", "sftp", "file"], True), (["mail", "pop", "tor"], False), (["vpn"], True)]
FILTER_LIST = [(["chat"], True), (["vpn"], False)]


def get_csvs_list(dir_path, filter_list=None):
    def filter_list_func(fn):
        if filter_list is not None:
            for filter_str_list, type in filter_list:
                result = any([filter_str in fn.lower() for filter_str in filter_str_list])
                if result is not type:
                    return False
        return True

    return [(os.path.join(dir_path, fn), fn) for fn in next(os.walk(dir_path))[2] if (".csv" in os.path.splitext(fn)[-1] and filter_list_func(fn))]


def traffic_csv_reader(file_list):

    output1 = open(OUTPUT1, 'w')
    writer1 = csv.writer(output1)
    counter1 = 0
    output2 = open(OUTPUT2, 'w')
    writer2 = csv.writer(output2)
    counter2 = 0
    # output3 = open(OUTPUT3, 'wb')
    # writer3 = csv.writer(output3)
    # counter3 = 0

    rate_list = []
    for i, (file_path, file_name) in enumerate(file_list):
        print("Running on " + str(i) + " file - " + file_path)
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                session_tuple_key = tuple(row[:8])
                length = int(row[7])
                ts = np.array(row[8:8+length], dtype=float)
                if length >= 20:
                    total_time = ts[-1] - ts[0]
                    sizes = np.array(row[9+length:], dtype=int)
                    # print row[0], length, total_time, length/total_time
                    rate = length/total_time
                    rate_list.append(rate)
                    # if (sizes > MTU).any():
                    #     a = [(sizes[i], i) for i in range(len(sizes)) if (np.array(sizes) > MTU)[i]]
                    #     print len(a), session_tuple_key, a

                    # if ("facebook" in row[0] and rate > 40) or ("facebook" not in row[0] and 20 <= rate and length >= 1000): # for iscx_voip
                    # if "facebook" not in row[0] and 40 <= rate and length >= 1000: # for iscx_voip_vpn
                    # if ("youtube" in row[0] and row[2] == '443' and total_time > 10 and rate > 15) or ("vimeo" in row[0] and rate > 30 and total_time > 15) or ("netflix" in row[0] and rate > 60) or ("facebook" in row[0] and rate > 60) or (40 <= rate and row[5] == "UDP" and "facebook" not in row[0]): # for iscx_video
                    # if length > 6000 and rate > 10 and total_time > 10 and (row[2] == '443' or row[2] == '80'): # for iscx_video_vpn
                    # if total_time > 30 and rate > 30 and (row[2] == '443' or row[2] == '80'): # for CICNTTor_video
                    # if total_time > 30 and (row[2] == '443' or row[2] == '80'): # for CICNTTor_video
                    # if total_time > 10 and rate > 10 and length > 1000 and (session_tuple_key[-1] != '3326' and session_tuple_key[-1] != '6367'): # for CICNTTor_voip
                    # if (total_time > 10 and ((rate > 100) or ("skype" in row[0] and rate > 10))) or ("rent" in row[0] and total_time > 20 and row[2] != '21943' and row[4] != '28904'): #for iscx_file
                    # if ("torrent"  in row[0] and total_time > 30 and rate > 10 and (row[2] == '443' or row[2] == '80')) or ("torrent" not in row[0] and total_time > 30 and rate > 10 and int(row[2]) not in [22, 1781, 59886, 35968]): #for iscx_file_vpn
                    # if (total_time > 20) and (("POP" in row[0] and rate > 150) or (("IMAP" in row[0] and rate > 10 and row[7][0] == '8') or row[0] == 'FTP_filetransfer' and total_time > 20 and rate > 100) or ( rate > 10 and "SFTP" in row[0])): #for CICNTTor_file
                    # if total_time > 20 and rate > 5: #for CICNTTor_file_tor
                    # if ("skype" in row[0] and total_time > 20 and rate > 3 and row[1][:2] == "10") or ("ftps" in row[0] and total_time > 20 and rate > 300 and row[2] != '1781') or ("sftp" in row[0] and total_time > 20 and rate > 5 and (('A' in row[0] and row[4]=='22') or ('B' in row[0] and row[2]=='22'))):#for iscx_file_vpn
                    if (total_time > 50 and rate<5) and (("whats" in row[0] and ("185.60." in row[1] or "185.60." in row[3])) or ("hang" in row[0] and ("216.58." in row[1] or "216.58." in row[3])) or ("book" in row[0] and ("192.114." in row[1] or "192.114." in row[3]))): #my_chat
                    # if (row[1] in ["131.202.240.242","131.202.240.45"] and row[3] in ["131.202.240.242","131.202.240.45"]) or ("gmail" in row[0] and "131.202.240.87" in [row[1], row[3]] and total_time > 40 and row[5] == 'TCP' and rate < 0.3): #for scx_chat
                    # if ("skype" in row[0] and (row[1] in ["86.4.212.228", '157.56.52.13', '64.4.23.162'] or row[3] in ["86.4.212.228", '157.56.52.13', '64.4.23.162'])) or (total_time > 20 and rate < 2 and (("205.188." not in (row[1]+row[3]) and "hang" not in row[0]) or ("hang" in row[0] and "216.58" in (row[1]+row[3])))): #for iscx_chat_vpn
                    # if total_time > 20 and rate < 2: #for CICNTTor_chat
                    # if total_time > 20 and (row[2] in ['80', '443'] or row[4] in ['80', '443']): #for CICNTTor_browsing_tor
                    # if total_time > 20:
                        writer1.writerow(row)
                        counter1 += 1
                        print(session_tuple_key, total_time, rate)
                        # session_spectogram(ts, sizes, session_tuple_key[0])
                    # elif "facebook" in row[0] and rate > 50:# --> voip
                    else:
                        writer2.writerow(row)
                        counter2 += 1
                    # # #
                    # if "skype" in row[0] and (row[1] in ["86.4.212.228", '157.56.52.13', '64.4.23.162'] or row[3] in ["86.4.212.228", '157.56.52.13', '64.4.23.162']):# and row[2] == '443'  and rate >10:
                    #     print session_tuple_key, total_time, rate
                    #     session_spectogram(ts, sizes, session_tuple_key[0])

    print("Total sessions in " + OUTPUT1 + " : " + str(counter1))
    print("Total sessions in " + OUTPUT2 + " : " + str(counter2))
    output1.close()
    output2.close()

    print(rate_list)
    plt.hist(rate_list)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=INPUT, help='Path to csvs folder')

    FLAGS = parser.parse_args()
    file_list = get_csvs_list(FLAGS.input, FILTER_LIST)
    print("Total number of files " + str(len(file_list)) + " in " + INPUT)
    traffic_csv_reader(file_list)
