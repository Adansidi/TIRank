import argparse
import json
import csv
import os

register_status_path = ''
output_parent_path = ''




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


def read_register_status(domains):
    domain_register_status = {}
    with open(register_status_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['fqdn'] in domains:
                domain_register_status[row['fqdn']] = (row['hold'], row['pending'], row['deleted'])
    return domain_register_status


def write_register_status(domain_register_status, timestamp, prefix):
    with open(f'{output_parent_path}/{timestamp}_{prefix}register_status.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'hold', 'pending', 'deleted'])
        for domain, status in domain_register_status.items():
            writer.writerow([domain] + list(status))

def main():
    global register_status_path
    global output_parent_path
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain_list', nargs='+', required=True, help='List of domain list files')
    parser.add_argument('--timestamp', required=True, help='Timestamp string')
    parser.add_argument('--prefix', required=False, default='')

    args = parser.parse_args()
    
    prefix = args.prefix
    if prefix == "null":
        prefix = ""
    
    domains = read_domain_list(args.domain_list)

    register_status_path = f'../validity/register_status/{prefix}whois_sld_based_fqdn_register_status.csv'
    output_parent_path = f'../validity/register_status'

    
    domain_register_status = read_register_status(domains)
    
    write_register_status(domain_register_status, args.timestamp, prefix)

if __name__ == '__main__':
    main()
