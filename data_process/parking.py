import argparse
import json
import csv
import os

parking_path = ''
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


def read_parking(domains):
    domain_parking = {}
    with open(parking_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['FQDN'] in domains:
                domain_parking[row['FQDN']] = row['Parked']
    return domain_parking


def write_parking(domain_parking, timestamp, prefix):
    with open(f'{output_parent_path}/{timestamp}_{prefix}parking.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'parked'])
        for domain, status in domain_parking.items():
            writer.writerow([domain] + [status])

def main():
    global parking_path
    global output_parent_path
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain_list', nargs='+', required=True, help='List of domain list files')
    parser.add_argument('--timestamp', required=True, help='Timestamp string')
    parser.add_argument('--prefix', required=False, help='Prefix of the input and output file')
    args = parser.parse_args()

    prefix = args.prefix
    if prefix == "null":
        prefix = ""

    
    domains = read_domain_list(args.domain_list)

    parking_path = f'../validity/parking/{prefix}validity_parking_analyze.csv'
    output_parent_path = '../validity/parking'

    
    domain_parking = read_parking(domains)
    
    write_parking(domain_parking, args.timestamp, prefix)

if __name__ == '__main__':
    main()
