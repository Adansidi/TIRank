import argparse
import json
import csv
import os

register_lifespan_path = ''
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


def read_register_lifespan(domains):
    domain_register_lifespan = {}
    with open(register_lifespan_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['domain'] in domains:
                domain_register_lifespan[row['domain']] = row['register_lifespan']
    return domain_register_lifespan


def write_register_lifespan(domain_register_lifespan, timestamp, prefix):
    with open(f'{output_parent_path}/{timestamp}_{prefix}register_lifespan.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'register_lifespan'])
        for domain, lifespan in domain_register_lifespan.items():
            writer.writerow([domain] + [lifespan])

def main():
    global register_lifespan_path
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

    register_lifespan_path = f'../activity/register_lifespan/{prefix}whois_sld_register_lifespan.csv'
    output_parent_path = f'../activity/register_lifespan'

    
    domain_register_lifespan = read_register_lifespan(domains)
    
    write_register_lifespan(domain_register_lifespan, args.timestamp, prefix)

if __name__ == '__main__':
    main()
