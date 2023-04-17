import os
import subprocess
import requests
import time

subprocess.run("conda env create -f environment.yml")
subprocess.run("conda activate geoestimation-github-pytorch")
subprocess.run('bash -c "conda activate geoestimation-github-pytorch; python -V"', shell=True)

os.system('pip install django')
os.system('pip install geopy')
os.system('pip install keyboard')
os.system('pip install mouse')
os.system('pip install pyautogui')
os.system('pip install chardet')
os.system('pip install docker')
os.system('pip install scipy')

open('leaflet.js', 'wb').write(requests.get('https://unpkg.com/leaflet@1.9.3/dist/leaflet.js', allow_redirects=True).content)

os.system('python ./backend_geoguessr/manage.py runserver 8000')