import os
import json

directory_path = "/GPUFS/yt_ust_junxianh_1/jhzhang/NPHardEval/Results/edp_prompts13_3s/"

# use the os module to get a list of all JSON files in the specified directory
json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

# loop through each JSON file and print its contents
for json_file in json_files:
    with open(os.path.join(directory_path, json_file), 'r') as f:
        data = json.load(f)
        acc=0
        for dt in data:
            if dt['correctness'][0]:
                acc+=1
        print(json_file, acc, acc/100)