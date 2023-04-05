import os
import subprocess

subprocess.run('bash -c "conda activate geoestimation-github-pytorch; python -V"', shell=True)
os.system('pip install django')
os.system('pip install geopy')

os.system('pip install keyboard')
os.system('pip install mouse')
os.system('pip install pyautogui')
os.system('pip install chardet')

os.system('python ./backend_geoguessr/manage.py runserver 8000')