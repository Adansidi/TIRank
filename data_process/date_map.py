import json
from datetime import datetime, timedelta

date_range_st = "20240107"
date_range_ed = "20240331"

matrix_abs_path = "../matrix_results/matrix_abs.json"
date_map_path = "../matrix_results/date_map.json"

date_map = {}

with open(matrix_abs_path, "r") as file:
    for line in file:
        try:
            json_obj = json.loads(line)

            if "start_date" in json_obj and "end_date" in json_obj and "timestamp" in json_obj:
                start_date = datetime.strptime(str(json_obj["start_date"]), "%Y%m%d")  
                end_date = datetime.strptime(str(json_obj["end_date"]), "%Y%m%d")  

                if (end_date - start_date).days == 6:
                    if date_range_st <= end_date.strftime("%Y%m%d") <= date_range_ed:
                        date_map[end_date.strftime("%Y%m%d")] = json_obj["timestamp"]
        except json.JSONDecodeError:
            continue

with open(date_map_path, "w") as file:
    for key in sorted(date_map.keys()):
        json.dump({key: date_map[key]}, file)
        file.write('\n')
