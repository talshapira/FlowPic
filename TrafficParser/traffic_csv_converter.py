#!/usr/bin/env python
"""
Read traffic_csv
"""

import os
import argparse
import csv
from sessions_plotter import *
import glob
import re

FLAGS = None
INPUT = "../raw_csvs/classes/browsing/reg/CICNTTor_browsing.raw.csv"#"../dataset/iscxNTVPN2016/CompletePCAPs" # ""
INPUT_DIR = "../raw_csvs/classes/chat/vpn/"
CLASSES_DIR = "../raw_csvs/classes/**/**/"

# LABEL_IND = 1
TPS = 60 # TimePerSession in secs
DELTA_T = 60 # Delta T between splitted sessions
MIN_TPS = 50

# def insert_dataset(dataset, labels, session, label_ind=LABEL_IND):
#     dataset.append(session)
#     labels.append(label_ind)

# def export_dataset(dataset, labels):
#     print "Start export dataset"
#     np.savez(INPUT.split(".")[0] + ".npz", X=dataset, Y=labels)
#     print dataset.shape, labels.shape

#
# def import_dataset():
#     print "Import dataset"
#     dataset = np.load(INPUT.split(".")[0] + ".npz")
#     print dataset["X"].shape, dataset["Y"].shape


def export_dataset(dataset):
    print("Start export dataset")
    np.save(os.path.splitext(INPUT)[0], dataset)
    print(dataset.shape)


def export_class_dataset(dataset, class_dir):
    print("Start export dataset")
    np.save(class_dir + "/" + "_".join(re.findall(r"[\w']+", class_dir)[-2:]), dataset)
    print(dataset.shape)


def import_dataset():
    print("Import dataset")
    dataset = np.load(os.path.splitext(INPUT)[0] + ".npy")
    print(dataset.shape)
    return dataset


def traffic_csv_converter(file_path):
    print("Running on " + file_path)
    dataset = []
    # labels = []
    counter = 0
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            # print row[0], row[7]
            session_tuple_key = tuple(row[:8])
            length = int(row[7])
            ts = np.array(row[8:8+length], dtype=float)
            sizes = np.array(row[9+length:], dtype=int)

            # if (sizes > MTU).any():
            #     a = [(sizes[i], i) for i in range(len(sizes)) if (np.array(sizes) > MTU)[i]]
            #     print len(a), session_tuple_key

            if length > 10:
                # print ts[0], ts[-1]
                # h = session_2d_histogram(ts, sizes)
                # session_spectogram(ts, sizes, session_tuple_key[0])
                # dataset.append([h])
                # counter += 1
                # if counter % 100 == 0:
                #     print counter

                for t in range(int(ts[-1]/DELTA_T - TPS/DELTA_T) + 1):
                    mask = ((ts >= t * DELTA_T) & (ts <= (t * DELTA_T + TPS)))
                    # print t * DELTA_T, t * DELTA_T + TPS, ts[-1]
                    ts_mask = ts[mask]
                    sizes_mask = sizes[mask]
                    if len(ts_mask) > 10 and ts_mask[-1] - ts_mask[0] > MIN_TPS:
                        # if "facebook" in session_tuple_key[0]:
                        #     session_spectogram(ts[mask], sizes[mask], session_tuple_key[0])
                        #     # session_2d_histogram(ts[mask], sizes[mask], True)
                        #     session_histogram(sizes[mask], True)
                        #     exit()
                        # else:
                        #     continue

                        h = session_2d_histogram(ts_mask, sizes_mask)
                        # session_spectogram(ts_mask, sizes_mask, session_tuple_key[0])
                        dataset.append([h])
                        counter += 1
                        if counter % 100 == 0:
                            print(counter)

    return np.asarray(dataset) #, np.asarray(labels)


def traffic_csv_converter_splitted(file_path):
    def split_converter(ts, sizes, dataset, counter):
        if ts[-1] - ts[0] > MIN_TPS and len(ts) > 20:
            # print ts[0], ts[-1]
            h = session_2d_histogram(ts-ts[0], sizes)
            # session_spectogram(ts, sizes, session_tuple_key[0])
            dataset.append([h])
            counter += 1
            # if counter % 100 == 0:
            #     print counter

            total_time = ts[-1] - ts[0]
            if total_time > TPS:
                for ts_split, sizes_split in zip(np.split(ts, [len(ts)/2]), np.split(sizes, [len(sizes)/2])):
                    split_converter(ts_split, sizes_split, dataset, counter)

    print("Running on " + file_path)
    dataset = []
    # labels = []
    counter = 0
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            # print row[0], row[7]
            session_tuple_key = tuple(row[:8])
            length = int(row[7])
            ts = np.array(row[8:8+length], dtype=float)
            sizes = np.array(row[9+length:], dtype=int)

            # if (sizes > MTU).any():
            #     a = [(sizes[i], i) for i in range(len(sizes)) if (np.array(sizes) > MTU)[i]]
            #     print len(a), session_tuple_key

            if length > 10:
                split_converter(ts, sizes, dataset, counter)

    return np.asarray(dataset)


def traffic_class_converter(dir_path):
    dataset_tuple = ()
    for file_path in [os.path.join(dir_path, fn) for fn in next(os.walk(dir_path))[2] if (".csv" in os.path.splitext(fn)[-1])]:
        dataset_tuple += (traffic_csv_converter(file_path),)  ################

    return np.concatenate(dataset_tuple, axis=0)


def iterate_all_classes():
    for class_dir in glob.glob(CLASSES_DIR):
        if "other" not in class_dir: #"browsing" not in class_dir and
            print("working on " + class_dir)
            dataset = traffic_class_converter(class_dir)
            print(dataset.shape)
            export_class_dataset(dataset, class_dir)


def random_sampling_dataset(input_array, size=2000):
    print("Import dataset " + input_array)
    dataset = np.load(input_array)
    print(dataset.shape)
    p = size*1.0/len(dataset)
    print(p)
    if p >= 1:
        raise Exception

    mask = np.random.choice([True, False], len(dataset), p=[p, 1-p])
    dataset = dataset[mask]
    print("Start export dataset")

    np.save(os.path.splitext(input_array)[0] + "_samp", dataset)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=INPUT, help='Path to csv file')

    FLAGS = parser.parse_args()
    ##
    # iterate_all_classes()

    # dataset = traffic_class_converter(INPUT_DIR)
    # dataset = traffic_csv_converter(INPUT)

    input_array = "../raw_csvs/classes/browsing/reg/browsing_reg.npy"
    random_sampling_dataset(input_array)


    # export_class_dataset(dataset)
    # import_dataset()
