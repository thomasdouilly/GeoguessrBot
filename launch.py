import os
import subprocess
import requests

subprocess.run('bash -c "conda activate geoestimation-github-pytorch; python -V"', shell=True)
os.system('pip install django')
os.system('pip install geopy')

os.system('pip install keyboard')
os.system('pip install mouse')
os.system('pip install pyautogui')
os.system('pip install chardet')

open('leaflet.js', 'wb').write(requests.get('https://unpkg.com/leaflet@1.9.3/dist/leaflet.js', allow_redirects=True).content)

os.system('python ./backend_geoguessr/manage.py runserver 8000')