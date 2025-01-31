import json
import csv
import os

def process_line_to_csv(json_line, csv_writer):
    try:
        article = json.loads(json_line)
        content = article.get('text', '')
        url = article.get('url', '')
        title = article.get('title', '')
        csv_writer.writerow([content, url, title])
    except json.JSONDecodeError:
        print('Warning: Line decode error')
        
def process_file(json_file_path, csv_writer):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            process_line_to_csv(line, csv_writer)

def process_directory(directory_path, output_file, num_file=100):
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['content', 'url', 'title'])
        
        file_count = 0
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_count += 1
                json_file_path = os.path.join(root, file)
                process_file(json_file_path, writer)
                print(f'Iter: {file_count} / {num_file}  Process File: {json_file_path}')
                if file_count > num_file:
                    return
                
if __name__ == '__main__':
    wiki_directory = './data/wiki_zh'
    output_csv = './data/wiki_zh.csv'
    num_file = 500
    process_directory(wiki_directory, output_csv, num_file)
