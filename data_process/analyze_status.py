import argparse
import json
import csv
import os

analyze_status_path = ''
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


def read_analyze_status(domains):
    domain_analyze_status = {}
    with open(analyze_status_path, 'r') as f:
        for line in f:
            data = json.loads(line.strip())
            fqdn = data['name']
            if fqdn in domains:
                if fqdn not in domain_analyze_status:
                    domain_analyze_status[fqdn] = 0
                status = data['status']
                if status == 'NXDOMAIN':
                    domain_analyze_status[fqdn] = 1
    return domain_analyze_status

# 将 domain_analyze_status 输出到 ../validity/analyze_status/{$timestamp}_analyze_status.csv 中
def write_analyze_status(domain_analyze_status, timestamp, prefix):
    with open(f'{output_parent_path}/{timestamp}_{prefix}analyze_status.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'NXDOMAIN'])
        for domain, status in domain_analyze_status.items():
            writer.writerow([domain] + [status])

def main():
    global analyze_status_path
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


    analyze_status_path = f'../validity/analyze_status/allDomains.json'
    output_parent_path = f'../validity/analyze_status'

    domain_analyze_status = read_analyze_status(domains)

    write_analyze_status(domain_analyze_status, args.timestamp, prefix)

if __name__ == '__main__':
    main()
