import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.ticker as ticker

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


input_csv_file_path = '../matrix_results/0107-0331_new/pr_rank/rank_result_20240107_20240331.csv'

output_folder_path = '../matrix_results/0107-0331_new/pr_rank/sel/'


if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


df = pd.read_csv(input_csv_file_path)


domains = ['1-31.qq-weixin.org', '6j312.rchan0.com', 'data-dev.helpkaspersky.top']  


df.columns = pd.to_datetime(df.columns, format='%Y%m%d', errors='ignore')


for domain in domains:
    if domain in df['domain'].values:
        
        domain_data = df[df['domain'] == domain].iloc[0].drop('domain')

        
        domain_data.index = pd.to_datetime(domain_data.index, format='%Y%m%d', errors='coerce')

        
        missing_dates = domain_data[domain_data.isna()].index
        if not missing_dates.empty:
            

        
        plt.figure(figsize=(10, 6))
        plt.plot(domain_data.index, domain_data.values, marker='')

        
        xticks = np.linspace(domain_data.index.min().value, domain_data.index.max().value, 6)
        xticks = pd.to_datetime(xticks)  

        plt.xticks(xticks, xticks.strftime('%m-%d'), fontsize=20)

        
        for xtick in xticks:
            plt.axvline(x=xtick, color='gray', linestyle='--', linewidth=0.5, dashes=(5, 10))

        
        yticks = plt.yticks()[0]
        plt.yticks(yticks, fontsize=20)  
        for ytick in yticks:
            plt.axhline(y=ytick, color='gray', linestyle='--', linewidth=0.5, dashes=(5, 10))

        
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.gca().yaxis.get_offset_text().set_fontsize(20)  

        plt.ylim(bottom=0)  

        plt.xlabel('Date', fontsize=20)
        plt.ylabel('Rank', fontsize=20)
        

        
        plt.savefig(f'{output_folder_path}{domain}_20240107_20240331.pdf')
        plt.close()
