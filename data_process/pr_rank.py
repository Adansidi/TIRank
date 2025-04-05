import pandas as pd
import json
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime
import pytz


domain_file = '../domain_list/all_PR_domains.txt'
matrix_results_path = '../matrix_results/0107-0331_new'

pr_rank_sub_path = 'pr_rank'

date_map_file = f'{matrix_results_path}/date_map.json'

suffix = 'rank_result'


with open(domain_file, 'r') as f:
    domains = f.read().splitlines()


date_map = {}
with open(date_map_file, 'r') as f:
    for line in f:
        date_map.update(json.loads(line))


start_date = min(date_map.keys())
end_date = max(date_map.keys())


domain_rank_parent_path = f'{matrix_results_path}/{pr_rank_sub_path}'
output_csv_file_path = f'{domain_rank_parent_path}/{suffix}_{start_date}_{end_date}.csv'


all_ranks = {domain: {} for domain in domains}


for date, timestamp in date_map.items():
    
    utc_now = datetime.now(pytz.timezone('UTC'))

    
    beijing_now = utc_now.astimezone(pytz.timezone('Asia/Shanghai'))

    file_path = f'{matrix_results_path}/{timestamp}_{suffix}.csv'
    

    
    if os.path.exists(file_path):
        
        df = pd.read_csv(file_path)

        
        for domain in domains:
            
            if domain in df['domain'].values:
                rank = df[df['domain'] == domain].index[0] + 1
            else:
                rank = np.nan

            
            all_ranks[domain][date] = rank
    else:
        
        for domain in domains:
            all_ranks[domain][date] = np.nan


for domain, ranks in all_ranks.items():
    

    
    output_img_file_path = f'{domain_rank_parent_path}/{domain}_{suffix}_{start_date}_{end_date}.png'

    

    
    plt.figure(figsize=(10, 6))
    plt.plot(list(ranks.keys()), list(ranks.values()))
    plt.xlabel('Date')
    plt.ylabel('Rank')
    plt.title(f'Rank of {domain} over time')
    plt.savefig(output_img_file_path)

    
    df_ranks = pd.DataFrame(ranks, index=[domain])
    if os.path.exists(output_csv_file_path):
        df_ranks.to_csv(output_csv_file_path, mode='a', header=False)
    else:
        df_ranks.to_csv(output_csv_file_path)