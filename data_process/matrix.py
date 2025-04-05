import json
import argparse
import pandas as pd

def register_status_func(df, timestamp, prefix):
    
    register_status_df = pd.read_csv(f'../validity/register_status/{timestamp}_{prefix}register_status.csv')
    
    
    return register_status_df

def analyze_status_func(df, timestamp, prefix):
    
    analyze_status_df = pd.read_csv(f'../validity/analyze_status/{timestamp}_{prefix}analyze_status.csv')
    
    df = pd.merge(df, analyze_status_df, on='domain', how='outer')
    return df

def parking_func(df, timestamp, prefix):
    
    parking_df = pd.read_csv(f'../validity/parking/{timestamp}_{prefix}parking.csv')
    
    df = pd.merge(df, parking_df, on='domain', how='outer')
    return df

def sinkhole_func(df, timestamp, prefix):
    
    sinkhole_df = pd.read_csv(f'../validity/sinkhole/{timestamp}_{prefix}sinkhole.csv')
    
    df = pd.merge(df, sinkhole_df, on='domain', how='outer')
    return df

def freq_func(df, timestamp, prefix):
    
    freq_df = pd.read_csv(f'../validity/freq/{timestamp}_freq.csv')
    
    df = pd.merge(df, freq_df, on='domain', how='outer')
    return df

def register_lifespan_func(df, timestamp, prefix):
    
    register_lifespan_df = pd.read_csv(f'../activity/register_lifespan/{timestamp}_{prefix}register_lifespan.csv')
    
    df = pd.merge(df, register_lifespan_df, on='domain', how='outer')
    return df

def trend_func(df, timestamp, prefix):
    
    trend_df = pd.read_csv(f'../activity/trend/{timestamp}_{[prefix]}trend.csv')
    
    df = pd.merge(df, trend_df, on='domain', how='outer')
    return df

def predicted_func(df, timestamp, prefix):
    df = predicted_client_cnt_func(df, timestamp, prefix)
    df = predicted_request_cnt_sum_func(df, timestamp, prefix)
    df = predicted_activation_func(df, timestamp, prefix)
    return df

def predicted_client_cnt_func(df, timestamp, prefix):
    
    predicted_client_cnt_df = pd.read_csv(f'../activity/predicted_client_cnt/{timestamp}_{prefix}predicted_client_cnt.csv')
    predicted_client_cnt_df = predicted_client_cnt_df.iloc[:, [0, -1]]
    
    last_column_name = predicted_client_cnt_df.columns[-1]
    
    predicted_client_cnt_df = predicted_client_cnt_df.rename(columns={'fqdn': 'domain', last_column_name: 'predicted_client_cnt'})
    
    df = pd.merge(df, predicted_client_cnt_df, on='domain', how='outer')
    return df

def predicted_request_cnt_sum_func(df, timestamp, prefix):
    
    predicted_request_cnt_sum_df = pd.read_csv(f'../activity/predicted_request_cnt_sum/{timestamp}_{prefix}predicted_request_cnt_sum.csv')
    predicted_request_cnt_sum_df = predicted_request_cnt_sum_df.iloc[:, [0, -1]]
    
    last_column_name = predicted_request_cnt_sum_df.columns[-1]
    
    predicted_request_cnt_sum_df = predicted_request_cnt_sum_df.rename(columns={'fqdn': 'domain', last_column_name: 'predicted_request_cnt_sum'})
    
    df = pd.merge(df, predicted_request_cnt_sum_df, on='domain', how='outer')
    return df

def predicted_activation_func(df, timestamp, prefix):
    
    predicted_activation_df = pd.read_csv(f'../activity/predicted_activation/{timestamp}_{prefix}predicted_activation.csv')
    predicted_activation_df = predicted_activation_df.iloc[:, [0, -1]]
    
    last_column_name = predicted_activation_df.columns[-1]
    
    predicted_activation_df = predicted_activation_df.rename(columns={'fqdn': 'domain', last_column_name: 'predicted_activation'})
    
    df = pd.merge(df, predicted_activation_df, on='domain', how='outer')
    return df

def cv_func(df, timestamp, prefix):
    df = cv_client_cnt_func(df, timestamp, prefix)
    df = cv_request_cnt_sum_func(df, timestamp, prefix)
    df = cv_activation_func(df, timestamp, prefix)
    return df

def cv_client_cnt_func(df, timestamp, prefix):
    
    cv_client_cnt_df = pd.read_csv(f'../activity/client_cnt_coefficient_of_variation/{timestamp}_{prefix}client_cnt_coefficient_of_variation.csv')
    
    cv_client_cnt_df = cv_client_cnt_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, cv_client_cnt_df, on='domain', how='outer')
    return df

def cv_request_cnt_sum_func(df, timestamp, prefix):
    
    cv_request_cnt_sum_df = pd.read_csv(f'../activity/request_cnt_sum_coefficient_of_variation/{timestamp}_{prefix}request_cnt_sum_coefficient_of_variation.csv')
    
    cv_request_cnt_sum_df = cv_request_cnt_sum_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, cv_request_cnt_sum_df, on='domain', how='outer')
    return df

def cv_activation_func(df, timestamp, prefix):
    
    cv_activation_df = pd.read_csv(f'../activity/activation_coefficient_of_variation/{timestamp}_{prefix}activation_coefficient_of_variation.csv')
    
    cv_activation_df = cv_activation_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, cv_activation_df, on='domain', how='outer')
    return df

def periodicity_func(df, timestamp, prefix):
    df = periodicity_client_cnt_func(df, timestamp, prefix)
    df = periodicity_request_cnt_sum_func(df, timestamp, prefix)
    df = periodicity_activation_func(df, timestamp, prefix)
    return df

def periodicity_client_cnt_func(df, timestamp, prefix):
    
    periodicity_client_cnt_df = pd.read_csv(f'../activity/client_cnt_periodicity_index/{timestamp}_{prefix}client_cnt_periodicity_index.csv')
    
    periodicity_client_cnt_df = periodicity_client_cnt_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, periodicity_client_cnt_df, on='domain', how='outer')
    return df

def periodicity_request_cnt_sum_func(df, timestamp, prefix):
    
    periodicity_request_cnt_sum_df = pd.read_csv(f'../activity/request_cnt_sum_periodicity_index/{timestamp}_{prefix}request_cnt_sum_periodicity_index.csv')
    
    periodicity_request_cnt_sum_df = periodicity_request_cnt_sum_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, periodicity_request_cnt_sum_df, on='domain', how='outer')
    return df

def periodicity_activation_func(df, timestamp, prefix):
    
    periodicity_activation_df = pd.read_csv(f'../activity/activation_periodicity_index/{timestamp}_{prefix}activation_periodicity_index.csv')
    
    periodicity_activation_df = periodicity_activation_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, periodicity_activation_df, on='domain', how='outer')
    return df

def abnormal_func(df, timestamp, prefix):
    df = abnormal_client_cnt_func(df, timestamp, prefix)
    df = abnormal_request_cnt_sum_func(df, timestamp, prefix)
    df = abnormal_activation_func(df, timestamp, prefix)
    return df

def abnormal_client_cnt_func(df, timestamp, prefix):
    
    abnormal_client_cnt_df = pd.read_csv(f'../activity/client_cnt_abnormal_index/{timestamp}_{prefix}client_cnt_abnormal_index.csv')
    
    abnormal_client_cnt_df = abnormal_client_cnt_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, abnormal_client_cnt_df, on='domain', how='outer')
    return df

def abnormal_request_cnt_sum_func(df, timestamp, prefix):
    
    abnormal_request_cnt_sum_df = pd.read_csv(f'../activity/request_cnt_sum_abnormal_index/{timestamp}_{prefix}request_cnt_sum_abnormal_index.csv')
    
    abnormal_request_cnt_sum_df = abnormal_request_cnt_sum_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, abnormal_request_cnt_sum_df, on='domain', how='outer')
    return df

def influence_score_func(df, timestamp, prefix):
    influence_score_df = pd.read_csv(f'../activity/influence_score/{timestamp}_{prefix}influence_score.csv')
    influence_score_df = influence_score_df.rename(columns={'fqdn': 'domain'})
    df = pd.merge(df, influence_score_df, on='domain', how='outer')
    return df

def abnormal_activation_func(df, timestamp, prefix):
    
    abnormal_activation_df = pd.read_csv(f'../activity/activation_abnormal_index/{timestamp}_{prefix}activation_abnormal_index.csv')
    
    abnormal_activation_df = abnormal_activation_df.rename(columns={'fqdn': 'domain'})
    
    df = pd.merge(df, abnormal_activation_df, on='domain', how='outer')
    return df

def company_rdata_func(df, timestamp, prefix):
    
    company_rdata_df = pd.read_csv(f'../aggregation/predicted_company_score_rdata/{timestamp}_{prefix}predicted_company_score_rdata.csv')
    company_rdata_df = company_rdata_df.iloc[:, [0, -1]]
    
    last_column_name = company_rdata_df.columns[-1]
    
    company_rdata_df = company_rdata_df.rename(columns={'fqdn': 'domain', last_column_name: 'predicted_company_score_rdata'})
    
    df = pd.merge(df, company_rdata_df, on='domain', how='outer')
    return df


functions = {
    'register_status': register_status_func,
    'analyze_status': analyze_status_func,
    'parking': parking_func,
    'sinkhole': sinkhole_func,
    'freq': freq_func,
    'register_lifespan': register_lifespan_func,
    'predicted': predicted_func,
    'cv': cv_func,
    'periodicity': periodicity_func,
    'abnormal': abnormal_func,
    'influence_score': influence_score_func,
    'company_rdata': company_rdata_func
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--timestamp', required=True, help='Timestamp to match')
    parser.add_argument('--prefix', required=False, help='Prefix of the input and output file')
    args = parser.parse_args()

    prefix = args.prefix
    if prefix == "null":
        prefix = ""

    timestamp = str(args.timestamp)

    
    df = pd.DataFrame()

    with open('../matrix_results/matrix_abs.json', 'r') as f:
        for line in f:
            data = json.loads(line)
            if str(data['timestamp']) == timestamp:
                for key, function in functions.items():
                    if data.get(key) == 1:
                        df = function(df, timestamp, prefix)
    df.to_csv(f'../matrix_results/{timestamp}_{prefix}matrix.csv', index=False)

if __name__ == "__main__":
    main()
