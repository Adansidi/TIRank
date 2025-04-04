import argparse
import json
import csv
import os
import numpy as np
from sklearn.linear_model import LinearRegression
import glob
import pandas as pd



activation_parent_path = '../origin_data/activation'
output_parent_path = '../activity/trend'

activation_pattern = f'activation_*.csv'

increase_black_pr_activation_pattern = f'increase_black_pr_activation_*.csv'



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

def read_activation_files(domains, sub_pattern, start_date, end_date):
    
    activation_files = glob.glob(f'{activation_parent_path}/{sub_pattern}')
    activation_data = {}
    for file in activation_files:
        date = int(file.split('_')[-1].split('.')[0])
        if start_date <= date <= end_date:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                domain = row['fqdn']
                activation = row['activation']
                
                if domain not in domains:
                    continue
                if domain not in activation_data:
                    activation_data[domain] = [0]*(end_date-start_date+1)
                activation_data[domain][date-start_date] = activation
    return activation_data

def main():
    global activation_parent_path
    global output_parent_path
    global activation_parent_path
    global increase_black_pr_activation_pattern
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain_list', nargs='+', required=True, help='List of domain list files')
    parser.add_argument('--timestamp', required=True, help='Timestamp string')
    parser.add_argument('--start_date', required=True, help='Start date')
    parser.add_argument('--end_date', required=True, help='End date')
    parser.add_argument('--prefix', required=False, help='Prefix of the input and output file')
    args = parser.parse_args()

    start_date = int(args.start_date)
    end_date = int(args.end_date)

    prefix = args.prefix
    if prefix == "null":
        prefix = ""

    activation_parent_path = '../origin_data/activation'
    output_parent_path = '../activity/trend'
    
    activation_pattern = f'{prefix}activation_*.csv'
    
    increase_black_pr_activation_pattern = f'increase_black_pr_activation_*.csv'

    
    domains = read_domain_list(args.domain_list)
    
    activation_data = read_activation_files(domains, activation_pattern, start_date, end_date)
    
    increase_black_pr_activation_data = read_activation_files(domains, increase_black_pr_activation_pattern, start_date, end_date)
    activation_data.update(increase_black_pr_activation_data)
    
    results = []
    for domain in domains:
        if domain in activation_data:
            k = linear_regression_fit(list(range(start_date, end_date+1)), activation_data[domain])
            results.append((domain, k))
        else :
            results.append((domain, 0))
    with open(f'{output_parent_path}/{args.timestamp}_{prefix}trend.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'k'])
        writer.writerows(results)

if __name__ == '__main__':
    main()
