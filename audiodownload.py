import csv
import os
import subprocess

if not os.path.exists('audio'):
    os.makedirs('audio')

with open('media_urls.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        url = row[0]  
        
        try:
            filename = url.split("/")[-1]  
            command = [
                'yt-dlp',  
                '-x', 
                '--audio-format', 'mp3',  
                '--audio-quality', '0',  
                '--output', f'audio/{filename}.%(ext)s', 
                url  
            ]
            
            subprocess.run(command, check=True)
            print(f'Downloaded audio from URL: {url}')
        
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {url}: {e}")
        except Exception as e:
            print(f"Unexpected error for {url}: {str(e)}")
