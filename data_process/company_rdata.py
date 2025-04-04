import argparse
import json
import csv
import os
import numpy as np
from sklearn.linear_model import LinearRegression
import glob
import pandas as pd
from datetime import datetime, timedelta


company_score_rdatas_parent_path = '../origin_data/company_score_rdatas'
output_parent_path = '../aggregation/predicted_company_score_rdata'
fqdn_score_pattern = 'fqdn_rdata_score_*.csv'
output_value_label = 'predicted_company_score_rdata'


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



def linear_regression_fit(x, y):
    x = np.array(x).reshape((-1, 1))
    model = LinearRegression().fit(x, y)
    return model.coef_[0]

def read_company_score_rdatas_files(domains, sub_pattern, start_date, end_date):
    company_score_rdatas_files = glob.glob(f'{company_score_rdatas_parent_path}/{sub_pattern}')
    company_score_rdata_data = {}
    for file in company_score_rdatas_files:
        date = int(file.split('_')[-1].split('.')[0])
        if start_date <= date <= end_date:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                domain = row['fqdn']
                company_score_rdata = row['score']
                if domain not in domains:
                    continue
                if domain not in company_score_rdata_data:
                    company_score_rdata_data[domain] = [0]*(end_date-start_date+1)
                company_score_rdata_data[domain][date-start_date] = company_score_rdata
    return company_score_rdata_data

def calculate_score(data_dict, G):
    influence_score_dict = {}
    for domain, y_data in data_dict.items():
        T = len(y_data)
        P = 0
        for activation in y_data:
            P += activation
        score = P / ((T + 2) ** G)
        influence_score_dict[domain] = score
    return influence_score_dict

def predict_next_data(origin_data, alpha):
    predicted_data = {}
    for domain, datas in origin_data.items():
        s = pd.Series(datas)
        ema = s.ewm(alpha=alpha, adjust=False).mean()
        ema_shifted = ema.shift(1)
        ema_shifted = ema_shifted.fillna(datas[0])
        predicted = (ema_shifted * (1 - alpha)) + (s * alpha)
        predicted_data[domain] = predicted.tolist()
    return predicted_data


def write_csv_files(data, parent_path, start_date, end_date, timestamp, prefix):
    with open(f'{parent_path}/{timestamp}_{prefix}{output_value_label}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['fqdn'] + list(range(start_date, end_date + 1)))
        for domain, datas in data.items():
            writer.writerow([domain] + datas)

def main():
    global company_score_rdatas_parent_path
    global output_parent_path
    global fqdn_score_pattern
    global increase_black_pr_fqdn_score_pattern
    global output_value_label

    parser = argparse.ArgumentParser()
    parser.add_argument('--domain_list', nargs='+', required=True, help='List of domain list files')
    parser.add_argument('--timestamp', required=True, help='Timestamp string')
    parser.add_argument('--start_date', required=True, help='Start date')
    parser.add_argument('--end_date', required=True, help='End date')
    parser.add_argument('--alpha', required=True)
    parser.add_argument('--prefix', required=False, help='Prefix of the input and output file')
    args = parser.parse_args()

    prefix = args.prefix
    if prefix == "null":
        prefix = ""

    company_score_rdatas_parent_path = '../origin_data/company_score_rdatas'
    output_parent_path = '../aggregation/predicted_company_score_rdata'
    fqdn_score_pattern = f'{prefix}fqdn_rdata_score_*.csv'
    output_value_label = 'predicted_company_score_rdata'

    start_date = int(args.start_date)
    end_date = int(args.end_date)
    domain_list = args.domain_list
    timestamp = args.timestamp
    alpha = float(args.alpha)


    domains = read_domain_list(domain_list)
    company_score_rdata_data = read_company_score_rdatas_files(domains, fqdn_score_pattern, start_date, end_date)
    increase_black_pr_company_score_rdata_data = read_company_score_rdatas_files(domains, increase_black_pr_fqdn_score_pattern, start_date, end_date)
    company_score_rdata_data.update(increase_black_pr_company_score_rdata_data)
    predicted_company_score_rdata = predict_next_data(company_score_rdata_data, alpha)
    write_csv_files(predicted_company_score_rdata, output_parent_path, start_date, end_date, timestamp, prefix)

if __name__ == '__main__':
    main()
