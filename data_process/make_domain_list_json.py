import json

with open('../domain_list/use_this_blacklist.txt', 'r') as f:
    domains = [line.strip() for line in f]

domain_dicts = [{'fqdn': domain, 'value': 1} for domain in domains]

with open('../domain_list/use_this_blacklist.json', 'w') as f:
    for domain_dict in domain_dicts:
        f.write(json.dumps(domain_dict) + '\n')
