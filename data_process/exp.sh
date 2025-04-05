#!/bin/bash


domain_list=("blacklist.json")


start_date="20240309"
end_date="20240315"


register_status=1 
analyze_status=1
parking=1 
sinkhole=1 
freq=1 
register_lifespan=1 
trend=1 
predicted=1 
cv=1 
periodicity=1 
abnormal=1 
influence_score=1 
company_client_ip=0 
company_rdata=1


alpha=0.2

threshold=0.1
min_samples=5
G=1.8



declare -A params
declare -A time_costs
params=(
    ["timestamp"]=$timestamp
    ["domain_list"]=$domain_list
    ["start_date"]=$start_date
    ["end_date"]=$end_date
    ["register_status"]=$register_status
    ["analyze_status"]=$analyze_status
    ["parking"]=$parking
    ["sinkhole"]=$sinkhole
    ["freq"]=$freq
    ["register_lifespan"]=$register_lifespan
    ["trend"]=$trend
    ["predicted"]=$predicted
    ["cv"]=$cv
    ["periodicity"]=$periodicity
    ["abnormal"]=$abnormal
    ["influence_score"]=$influence_score
    ["company_client_ip"]=$company_client_ip
    ["company_rdata"]=$company_rdata
)


if [ $register_status -eq 1 ]; then
    echo "3.1 Calculating register status..."
    start_time=$(date +%s)
    python3 register_status.py --domain_list ${domain_list[@]} --timestamp $timestamp
    end_time=$(date +%s)
    time_costs["register_status"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi
if [ $analyze_status -eq 1 ]; then
    echo "3.2 Calculating analyze status..."
    start_time=$(date +%s)
    python3 analyze_status.py --domain_list ${domain_list[@]} --timestamp $timestamp
    end_time=$(date +%s)
    time_costs["analyze_status"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi
if [ $parking -eq 1 ]; then
    echo "3.3 Calculating parking..."
    start_time=$(date +%s)
    python3 parking.py --domain_list ${domain_list[@]} --timestamp $timestamp
    end_time=$(date +%s)
    time_costs["parking"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi
if [ $sinkhole -eq 1 ]; then
    echo "3.4 Calculating sinkhole..."
    start_time=$(date +%s)
    python3 sinkhole.py --domain_list ${domain_list[@]} --timestamp $timestamp
    end_time=$(date +%s)
    time_costs["sinkhole"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi
if [ $freq -eq 1 ]; then
    echo "3.5 Calculating freq..."
    start_time=$(date +%s)
    python3 freq.py --domain_list ${domain_list[@]} --timestamp $timestamp
    end_time=$(date +%s)
    time_costs["freq"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi
if [ $register_lifespan -eq 1 ]; then
    echo "3.6 Calculating register lifespan..."
    start_time=$(date +%s)
    python3 register_lifespan.py --domain_list ${domain_list[@]} --timestamp $timestamp
    end_time=$(date +%s)
    time_costs["register_lifespan"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi


if [ $trend -eq 1 ]; then
    echo "4.1 Calculating trend..."
    start_time=$(date +%s)
    python3 trend.py --domain_list ${domain_list[@]} --timestamp $timestamp --start_date $start_date --end_date $end_date
    end_time=$(date +%s)
    time_costs["trend"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi

if [ $predicted -eq 1 ]; then
    echo "4.2 Calculating predicted..."
    start_time=$(date +%s)
    python3 predicted.py --domain_list ${domain_list[@]} --timestamp $timestamp --start_date $start_date --end_date $end_date --alpha $alpha
    end_time=$(date +%s)
    time_costs["predicted"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi

if [ $cv -eq 1 ]; then
    echo "4.3 Calculating cv..."
    start_time=$(date +%s)
    python3 cv.py --domain_list ${domain_list[@]} --timestamp $timestamp --start_date $start_date --end_date $end_date
    end_time=$(date +%s)
    time_costs["cv"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi
if [ $periodicity -eq 1 ]; then
    echo "4.4 Calculating periodicity..."
    start_time=$(date +%s)
    python3 periodicity.py --domain_list ${domain_list[@]} --timestamp $timestamp --start_date $start_date --end_date $end_date --threshold $threshold
    end_time=$(date +%s)
    time_costs["periodicity"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi

if [ $abnormal -eq 1 ]; then
    echo "4.5 Calculating abnormal..."
    start_time=$(date +%s)
    python3 abnormal.py --domain_list ${domain_list[@]} --timestamp $timestamp --start_date $start_date --end_date $end_date --min_samples $min_samples
    end_time=$(date +%s)
    time_costs["abnormal"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi

if [ $influence_score -eq 1 ]; then
    echo "4.6 Calculating influence score..."
    start_time=$(date +%s)
    python3 influence_score.py --domain_list ${domain_list[@]} --timestamp $timestamp --start_date $start_date --end_date $end_date --G $G
    end_time=$(date +%s)
    time_costs["influence_score"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi

if [ $company_rdata -eq 1 ]; then
    echo "4.8 Calculating company rdata..."
    start_time=$(date +%s)
    python3 company_rdata.py --domain_list ${domain_list[@]} --timestamp $timestamp --start_date $start_date --end_date $end_date --alpha $alpha
    end_time=$(date +%s)
    time_costs["company_rdata"]=$(echo "scale=2; ($end_time-$start_time)/60" | bc)
fi



for key in "${!time_costs[@]}"; do
    params["time_costs_$key"]=${time_costs[$key]}
done

json_string=""
for key in "${!params[@]}"; do
    value=${params[$key]}
    if [[ $value =~ ^[0-9]+$ ]]; then
        json_string+=",\"$key\":$value"
    else
        json_string+=",\"$key\":\"$value\""
    fi
done
json_string=${json_string:1}
json_string="{$json_string}"
echo $json_string >> ../matrix_results/matrix_abs.json

python3 matrix.py --timestamp $timestamp
