
import csv
import json
import os

input_file = '../domain_list/rank_result.csv'
output_file = '../domain_list/domain_list_0111.json'

domains = []

with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        domains.append({"fqdn": row['domain'], "value": 1})

with open(output_file, 'w') as jsonfile:
    for domain in domains:
        json.dump(domain, jsonfile)
        jsonfile.write('\n')
