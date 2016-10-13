__author__ = 'minh'


from datetime import datetime
import numpy as np
import os
import glob

aggregated_cols = ['sum', 'sum', 'avg', 'max', 'min']
NORM_TYPE = 'one_user'
PATIENT_DESCRIPTION_FILE = 'patient_description_date.csv'
PREPROCESS_ATOMHP = './Preprocess/ATOM-HP/'

# visit
visit_indices = [4, 5]

# Chemo
chemo_indices = [6, 7]


def validate(date_text, date_format):
    try:
        datetime.strptime(date_text, date_format)
        return True
    except ValueError:
        return False


def mapping_labels(labels, label_map):
    _labels = []
    for label in labels:
        _labels.append(label_map[label])

    return _labels



"""
read band data
"""
def parse_band_data(path_to_data, wanted_cols, discard_inactive_data):
    data = []
    files = []
    timestamps = []

    for file in glob.glob(path_to_data + "/*.csv"):
        matrix_data = np.loadtxt(file, delimiter=',', skiprows=1, usecols=wanted_cols)
        date_time = np.genfromtxt(file, dtype='str', delimiter=',', skip_header=1,
                                  usecols=(1))  # time feature has index 1

        if discard_inactive_data:
            # steps data and calories data must be non zeros
            non_zeros_matrix_data = np.loadtxt(file, delimiter=',', skiprows=1, usecols=(7, 8))

            # find row indices with all zeros
            zeros_rows = np.where(~non_zeros_matrix_data.any(axis=1))[0]

            # remove zeros rows
            matrix_data = np.delete(matrix_data, zeros_rows, 0)
            date_time = np.delete(date_time, zeros_rows, 0)

        data.append(matrix_data)

        timestamps.append(date_time)

        files.append(os.path.basename(file))

    return data, timestamps, files


"""
read band data for each user
input: data and timestamp for each user
"""
def parse_daily_band_data(data, timestamp, filename, aggregated_cols):
    daily_data, daily_timestamps = [], []

    # create folder of each patient
    if not os.path.exists(PREPROCESS_ATOMHP + os.path.splitext(filename)[0]):
        os.makedirs(PREPROCESS_ATOMHP + os.path.splitext(filename)[0])

    # use date of the last hour to check if we parse data for a new date
    # curr_date = datetime.strptime(timestamp[0].strip("\""), "%Y-%m-%d %H:%M:%S").date()
    if validate(timestamp[0].strip("\""), "%m/%d/%Y %H:%M"):
        curr_date = datetime.strptime(timestamp[0].strip("\""), "%m/%d/%Y %H:%M").date()
    else:
        curr_date = datetime.strptime(timestamp[0].strip("\""), "%Y-%m-%d %H:%M:%S").date()
    daily_timestamps.append(curr_date)
    last_hour_index = 0

    aggregated_values = []
    for j in range(0, len(timestamp)):  # matrices of one patient
        # day = datetime.strptime(timestamp[j].strip("\""), "%Y-%m-%d %H:%M:%S").date()
        if validate(timestamp[j].strip("\""), "%m/%d/%Y %H:%M"):
            day = datetime.strptime(timestamp[j].strip("\""), "%m/%d/%Y %H:%M").date()
        else:
            day = datetime.strptime(timestamp[j].strip("\""), "%Y-%m-%d %H:%M:%S").date()
        if day != curr_date or j == len(timestamp) - 1:
            if j != len(timestamp) - 1:  # to avoid dumplicate last date
                daily_timestamps.append(day)
            curr_matrix = np.matrix(data[last_hour_index:j, :])
            if j == len(timestamp) - 1:
                curr_matrix = np.matrix(data[last_hour_index:j + 1, :])

            # compute aggregated values
            daily_aggregated_values = []
            for i in range(len(aggregated_cols)):
                if aggregated_cols[i] == 'sum':
                    daily_aggregated_values.append(np.sum(curr_matrix[:, i]))
                elif aggregated_cols[i] == 'avg':
                    daily_aggregated_values.append(np.average(curr_matrix[:, i]))
                elif aggregated_cols[i] == 'max':
                    daily_aggregated_values.append(np.max(curr_matrix[:, i]))
                elif aggregated_cols[i] == 'min':
                    daily_aggregated_values.append(np.min(curr_matrix[:, i]))
            aggregated_values.append(daily_aggregated_values)

            # dump current matrix using curr_date as file name
            np.savetxt(PREPROCESS_ATOMHP + os.path.splitext(filename)[0] + '/' + "daily_" + str(curr_date), curr_matrix,
                       delimiter='\t')
            daily_data.append(curr_matrix)
            if j == len(timestamp) - 1:
                break

            last_hour_index = j
            curr_date = day

    if NORM_TYPE == 'one_user':
        (n, d) = data.shape;
        data -= - np.tile(np.mean(data, 0), (n, 1));
        _sd = np.tile(np.std(data, 0), (n, 1));
        data -= _sd

    daily_data, daily_timestamps = [], []

    # create folder of each patient
    if not os.path.exists(PREPROCESS_ATOMHP + os.path.splitext(filename)[0]):
        os.makedirs(PREPROCESS_ATOMHP + os.path.splitext(filename)[0])

    # use date of the last hour to check if we parse data for a new date
    # curr_date = datetime.strptime(timestamp[0].strip("\""), "%Y-%m-%d %H:%M:%S").date()
    if validate(timestamp[0].strip("\""), "%m/%d/%Y %H:%M"):
        curr_date = datetime.strptime(timestamp[0].strip("\""), "%m/%d/%Y %H:%M").date()
    else:
        curr_date = datetime.strptime(timestamp[0].strip("\""), "%Y-%m-%d %H:%M:%S").date()
    daily_timestamps.append(curr_date)
    last_hour_index = 0

    normed_aggregated_values = []
    for j in range(0, len(timestamp)):  # matrices of one patient
        # day = datetime.strptime(timestamp[j].strip("\""), "%Y-%m-%d %H:%M:%S").date()
        if validate(timestamp[j].strip("\""), "%m/%d/%Y %H:%M"):
            day = datetime.strptime(timestamp[j].strip("\""), "%m/%d/%Y %H:%M").date()
        else:
            day = datetime.strptime(timestamp[j].strip("\""), "%Y-%m-%d %H:%M:%S").date()
        if day != curr_date or j == len(timestamp) - 1:
            if j != len(timestamp) - 1:  # to avoid dumplicate last date
                daily_timestamps.append(day)
            curr_matrix = np.matrix(data[last_hour_index:j, :])
            if j == len(timestamp) - 1:
                curr_matrix = np.matrix(data[last_hour_index:j + 1, :])

            # compute aggregated values
            daily_aggregated_values = []
            for i in range(len(aggregated_cols)):
                if aggregated_cols[i] == 'sum':
                    daily_aggregated_values.append(np.sum(curr_matrix[:, i]))
                elif aggregated_cols[i] == 'avg':
                    daily_aggregated_values.append(np.average(curr_matrix[:, i]))
                elif aggregated_cols[i] == 'max':
                    daily_aggregated_values.append(np.max(curr_matrix[:, i]))
                elif aggregated_cols[i] == 'min':
                    daily_aggregated_values.append(np.min(curr_matrix[:, i]))
            normed_aggregated_values.append(daily_aggregated_values)

            # dump current matrix using curr_date as file name
            np.savetxt(PREPROCESS_ATOMHP + os.path.splitext(filename)[0] + '/' + "normed_daily_" + str(curr_date),
                       curr_matrix,
                       delimiter='\t')
            daily_data.append(curr_matrix)
            if j == len(timestamp) - 1:
                break

            last_hour_index = j
            curr_date = day

    return daily_data, aggregated_values, normed_aggregated_values, daily_timestamps



"""
create labels for band data based on visit date or Chemo date
"""
def create_label_for_band(data, timestamp, file, aggregated_cols):
    visit_labels, chemo_labels = [], []
    patient_id = file.split('_')[0]

    visit_dates, chemo_dates = [], []

    # read patent description data
    with open(PATIENT_DESCRIPTION_FILE) as f:
        lines = f.readlines()
    for line in lines:
        temp_arr = line.split(',')
        if temp_arr[0] == patient_id:
            visit_dates = [datetime.strptime(temp_arr[v], "%m/%d/%Y").date() for v in visit_indices]
            chemo_dates = [datetime.strptime(temp_arr[c], "%m/%d/%Y").date() for c in chemo_indices]
            break

    # reuse this function to obtain date
    daily_data, aggregated_values, normed_aggregated_values, daily_timestamps = parse_daily_band_data(data, timestamp,
                                                                                                      file,
                                                                                                      aggregated_cols)
    # manually since not sure of data!
    # visit date labeling
    for day in daily_timestamps:
        if day > visit_dates[0] and day < visit_dates[1]:
            visit_labels.append(2)
        elif day == visit_dates[0]:
            visit_labels.append(1)
        elif day == visit_dates[1]:
            visit_labels.append(3)
        elif day < visit_dates[0]:
            visit_labels.append(0)
        elif day > visit_dates[1]:
            visit_labels.append(4)

    # chemo date labeling
    for day in daily_timestamps:
        if day > chemo_dates[0] and day < chemo_dates[1]:
            chemo_labels.append(2)
        elif day == chemo_dates[0]:
            chemo_labels.append(1)
        elif day == chemo_dates[1]:
            chemo_labels.append(3)
        elif day < chemo_dates[0]:
            chemo_labels.append(0)
        elif day > chemo_dates[1]:
            chemo_labels.append(4)

    return visit_labels, chemo_labels