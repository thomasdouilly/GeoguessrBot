import docker
import subprocess
import re
import os
import glob
from geopy.geocoders import Nominatim
import sys
import ast
import numpy as np
from scipy.stats import median_abs_deviation

def get_all_files(dir_path):
    files = []
    for root, dirs, filenames in os.walk(dir_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def main():
    
	# Create a Docker client
	client = docker.from_env()

	# List all running containers
	# containers = client.containers.list(all=False)
	# print(containers)

	# Execute a command inside the container
	# exit_code, output = containers[0].exec_run("python src/inference.py", stdout=True)

	# Start a container
	output = client.containers.run("geoestimation_container", command='python src/inference.py',
		volumes={os.path.join(os.path.split(sys.path[0])[0], 'GeoEstimation'): {'bind': '/src', 'mode': 'rw'},
		os.path.join(os.path.split(sys.path[0])[0], 'data', 'picture'): {'bind': '/img', 'mode': 'rw'}}, auto_remove=True)

	# Log the output to a text file
	output_str = output.decode("utf-8")
	print(output_str)
	# Create a new instance of the geolocator
	geolocator = Nominatim(user_agent="geoapiExerciser")
	nb_images = len(get_all_files(os.path.join(os.path.split(sys.path[0])[0], 'data', 'picture')))
	print(f'{nb_images} files in the image folder for coordinates.')
	coordinates = re.findall(r'<hierarchy>:\s\((.*)\)', output_str)
	filename = re.findall(r'Processing:\s(.*\.png)', output_str)
 
	print(coordinates)
	print(filename)

	with open(os.path.join(os.path.split(sys.path[0])[0], 'data', 'output_agg.csv'), "w") as f:
		for i in range(nb_images):
			print(f'{filename[i]}: ({coordinates[i]}) - ', end='')
			location = geolocator.reverse(coordinates[i], exactly_one=True, language='en')
			country = ''
			try:
				country = location.raw['address']['country']
			except:
				print('Country not found.')
			print(country)

			f.write(f'{filename[i]};({coordinates[i]});{country}\n')
   
	panorama_detection=True
   
	if panorama_detection:
		# Read in the text file and extract the coordinates
		dir_geo = os.path.join(os.path.split(sys.path[0])[0], 'data')
  
		with open(dir_geo + '\\output_agg.csv', 'r') as f:
			lines = f.readlines()
			coordinates = [ast.literal_eval(line.split(';')[1]) for line in lines]
   
		coordinates = np.asarray(coordinates)
		print(coordinates)
	
		# Remove any potential outliers using the Z-score:
		median = np.median(coordinates, axis=0)
		mad = median_abs_deviation(coordinates, axis=0) + 1e-10
		modif_z_scores = 0.6745*np.abs(coordinates - median) / mad
		print(modif_z_scores)
		threshold = 3.5
		coordinates = coordinates[(modif_z_scores < threshold).all(axis=1)]
	
		# Calculate the average of the remaining coordinates
		avg_coordinate = np.mean(coordinates, axis=0)
		print(f"Average coordinate: {avg_coordinate}")
		with open(dir_geo + '\\output.csv', "w") as f:
			f.write(f'{avg_coordinate[0]},{avg_coordinate[1]}')