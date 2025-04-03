import pandas as pd
import argparse
import tldextract

parser = argparse.ArgumentParser(description="Process an input CSV file.")
parser.add_argument('input_file', type=str, help='Path to the input CSV file (feature matrix)')
args = parser.parse_args()

input_file = args.input_file

horrible_domains = set()
with open('train_set.txt', 'r') as file:
    for line in file:
        horrible_domains.add(line.strip())

df = pd.read_csv(input_file)

df = df[df['domain'].str.contains('.', regex=False)]


with open('./filter_data/white_domains.txt', 'r') as file:
    white_domains = set(line.strip() for line in file)

df = df[~df['domain'].isin(white_domains)]

public_serve_domains = set()
with open('./filter_data/public_serve_domains.txt', 'r') as file:
    for line in file:
        if 'blogspot.' not in line:
            public_serve_domains.add(line.strip())


public_serve_fqdn = set()

def is_public_service_domain(fqdn):
    ext = tldextract.extract(fqdn)
    domain = f"{ext.domain}.{ext.suffix}"
    if domain not in horrible_domains and domain in public_serve_domains:
        public_serve_fqdn.add(fqdn)
        return True
    return False

df = df[~df['domain'].apply(is_public_service_domain)]

with open("public_serve_fqdns.txt", 'w') as out_file:
    public_serve_fqdn_list = list(public_serve_fqdn)
    public_serve_fqdn_list.sort()
    for item in public_serve_fqdn_list:
        out_file.write(item + "\n")
    print("public serve fqdn write out!")

df[['freq', 'predicted_company_score_rdata']] = df[['freq', 'predicted_company_score_rdata']].fillna(1)

df.fillna(0, inplace=True)

df['IsHorrible'] = 0

horrible_mask = df['domain'].isin(horrible_domains)

status_mask = (df[['hold', 'sinkholed']] == 0).all(axis=1)

df.loc[horrible_mask & status_mask, 'IsHorrible'] = 1

df.to_csv(input_file.split('/')[-1].split('.')[0] + '_MATRIX.csv', index=False)
