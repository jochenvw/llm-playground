import csv
import json

def csv_to_json(csv_filepath):
    max = 100
    i = 0
    
    with open(csv_filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for idx, row in enumerate(reader):
            json_data = {key: (int(value) if value.isdigit() else float(value) if value.replace('.', '', 1).isdigit() else value) for key, value in row.items()}
            with open(f"data_out/candidate-{idx}.txt", 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
                
            i += 1
            if i >= max:
                break

csv_filepath = 'data/stackoverflow_full.csv'
csv_to_json(csv_filepath)


