import argparse
import json
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.linear_model import LinearRegression
import os
import glob
import csv


activation_parent_path = '../origin_data/activation'
client_cnt_parent_path = '../origin_data/client_cnt'
request_cnt_sum_parent_path = '../origin_data/request_cnt_sum'

activation_pattern = f'activation_*.csv'
request_cnt_sum_pattern = f'request_cnt_sum_*.csv'
client_cnt_pattern = f'client_cnt_*.csv'

key = 'fqdn'

client_cnt_value = 'client_cnt'
request_cnt_sum_value = 'request_cnt_sum'
activation_value = 'activation'

client_cnt_label = 'client_cnt_abnormal_index'
request_cnt_sum_label = 'request_cnt_sum_abnormal_index'
activation_label = 'activation_abnormal_index'

client_cnt_abnormal_index_parent_path = '../activity/client_cnt_abnormal_index'
request_cnt_sum_abnormal_index_parent_path = '../activity/request_cnt_sum_abnormal_index'
activation_abnormal_index_parent_path = '../activity/activation_abnormal_index'

def read_domain_list(domain_list):
    domains = set()
    for file in domain_list:
        file_path = os.path.join('../domain_list', file)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")
        with open(file_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                if 'fqdn' in data:
                    domains.add(data['fqdn'])
                elif 'domain' in data:
                    domains.add(data['domain'])
    return domains


def read_csv_files(parent_path, sub_pattern, domains, csv_key, csv_value_name, start_date, end_date):
    full_pattern = f'{parent_path}/{sub_pattern}'
    print(full_pattern)
    files = glob.glob(full_pattern)
    data = {}
    for file in files:
        date = int(file.split('_')[-1].split('.')[0])
        if start_date <= date <= end_date:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                domain = row[csv_key]
                csv_value = row[csv_value_name]
                if domain not in domains:
                    continue
                if domain not in data:
                    data[domain] = [0]*(end_date-start_date+1)
                data[domain][date-start_date] = csv_value
    return data


def periodical_quantification(data_dict, threshold):
    periodicity_dict = {}
    for domain, y_data in data_dict.items():
        fft_result = np.fft.fft(y_data)
        power_spectrum = np.abs(fft_result) ** 2
        frequencies = np.fft.fftfreq(len(y_data))

        max_power = np.max(power_spectrum)

        significant_frequencies = frequencies[power_spectrum > threshold * max_power]
        significant_frequencies = significant_frequencies[significant_frequencies != 0]
        if len(significant_frequencies) <= 1:
            periodicity_dict[domain] = 0
        else:
            periodicity_index = np.mean(np.diff(np.sort(1 / np.abs(significant_frequencies))))
            periodicity_dict[domain] = periodicity_index
    return periodicity_dict


def abnormal_quantification(data_dict, min_samples):
    abnormal_dict = {}
    for domain, y_data in data_dict.items():
        avg = np.mean(y_data)
        if avg < 10:
            epsilon = 5
        elif avg < 100:
            epsilon = 50
        else:
            epsilon = avg / 4
        if len(y_data) < min_samples:
            abnormal_dict[domain] = 0
            continue
        y_data_reshape = np.array(y_data).reshape(-1, 1)

        dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
        dbscan.fit(y_data_reshape)
        labels = dbscan.labels_
        num_outliers = np.sum(labels == -1)
        if num_outliers == len(y_data):
            abnormal_dict[domain] = 0
            continue
        abnormal_dict[domain] = num_outliers / len(y_data)
    return abnormal_dict



def write_csv_files(data, parent_path, output_value_label, timestamp, prefix):
    with open(f'{parent_path}/{timestamp}_{prefix}{output_value_label}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['fqdn', output_value_label])
        for domain, cv in data.items():
            writer.writerow([domain] + [cv])

def main():
    global activation_parent_path, client_cnt_parent_path, request_cnt_sum_parent_path
    global activation_pattern, request_cnt_sum_pattern, client_cnt_pattern
    global key, client_cnt_value, request_cnt_sum_value, activation_value
    global client_cnt_label, request_cnt_sum_label, activation_label
    global client_cnt_abnormal_index_parent_path, request_cnt_sum_abnormal_index_parent_path, activation_abnormal_index_parent_path
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain_list', nargs='+', required=True, help='List of domain list files')
    parser.add_argument('--start_date', required=True)
    parser.add_argument('--end_date', required=True)
    parser.add_argument('--timestamp', required=True)
    parser.add_argument('--min_samples', required=True, help='Threshold for significant frequencies')
    parser.add_argument('--prefix', required=False, help='Prefix of the input and output file')
    args = parser.parse_args()

    prefix = args.prefix
    if prefix == "null":
        prefix = ""

    activation_parent_path = '../origin_data/activation'
    client_cnt_parent_path = '../origin_data/client_cnt'
    request_cnt_sum_parent_path = '../origin_data/request_cnt_sum'
    activation_pattern = f'{prefix}activation_*.csv'
    request_cnt_sum_pattern = f'{prefix}request_cnt_sum_*.csv'
    client_cnt_pattern = f'{prefix}client_cnt_*.csv'


    key = 'fqdn'
    client_cnt_value = 'client_cnt'
    request_cnt_sum_value = 'request_cnt_sum'
    activation_value = 'activation'
    client_cnt_label = 'client_cnt_abnormal_index'
    request_cnt_sum_label = 'request_cnt_sum_abnormal_index'
    activation_label = 'activation_abnormal_index'

    client_cnt_abnormal_index_parent_path = '../activity/client_cnt_abnormal_index'
    request_cnt_sum_abnormal_index_parent_path = '../activity/request_cnt_sum_abnormal_index'
    activation_abnormal_index_parent_path = '../activity/activation_abnormal_index'

    start_date = int(args.start_date)
    end_date = int(args.end_date)
    timestamp = args.timestamp
    domain_list = args.domain_list
    min_samples = int(args.min_samples)

    domains = read_domain_list(domain_list)
    client_cnt_data = read_csv_files(client_cnt_parent_path, client_cnt_pattern, domains, key, client_cnt_value, start_date, end_date)
    request_cnt_sum_data = read_csv_files(request_cnt_sum_parent_path, request_cnt_sum_pattern, domains, key, request_cnt_sum_value, start_date, end_date)
    activation_data = read_csv_files(activation_parent_path, activation_pattern, domains, key, activation_value, start_date, end_date)

    client_cnt_abnormal = abnormal_quantification(client_cnt_data, min_samples)
    request_cnt_sum_abnormal = abnormal_quantification(request_cnt_sum_data, min_samples)
    activation_abnormal = abnormal_quantification(activation_data, min_samples)

    write_csv_files(client_cnt_abnormal, client_cnt_abnormal_index_parent_path, client_cnt_label, timestamp, prefix)
    write_csv_files(request_cnt_sum_abnormal, request_cnt_sum_abnormal_index_parent_path, request_cnt_sum_label, timestamp, prefix)
    write_csv_files(activation_abnormal, activation_abnormal_index_parent_path, activation_label, timestamp, prefix)

if __name__ == "__main__":
    main()
