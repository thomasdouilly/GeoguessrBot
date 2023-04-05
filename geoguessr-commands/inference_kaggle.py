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
from collections import Counter

def get_all_files(dir_path):
    files = []
    for root, dirs, filenames in os.walk(dir_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def haversine_mean(list_coords, weights, R=6378.137):
    '''
    The haversine formula determines the great-circle distance between two points on a sphere given their longitudes and latitudes.
    '''
    x = R * np.cos(list_coords[:, 0]) * np.cos(list_coords[:, 1])
    y = R * np.cos(list_coords[:, 0]) * np.sin(list_coords[:, 1])
    z = R * np.sin(list_coords[:, 0])

    x_mean = np.average(x, weights=weights, axis=0)
    y_mean = np.average(y, weights=weights, axis=0)
    z_mean = np.average(z, weights=weights, axis=0)

    # Convert the mean x, y, and z coordinates back to latitude and longitude values
    mean_lat = np.arcsin(z_mean / R)
    mean_lon = np.arctan2(y_mean, x_mean)

    return (np.degrees(mean_lat), np.degrees(mean_lon))

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
   			countries = [line.split(';')[2].replace("\n", "") for line in lines]
		coordinates = np.asarray(coordinates)
		print(f'Coordinates:\n{coordinates}\n')
		
		# Weight the predictions depending on the country
		most_common_country = Counter(countries).most_common(1)[0][0]
	        weights_countries = [1.5 if c == most_common_country else 1 for c in countries]
	        print(f'Countries weights: {weights_countries}\n')
	
		# Remove any potential outliers using the Z-score:
		median = np.median(coordinates, axis=0)
		mad = median_abs_deviation(coordinates, axis=0) + 1e-10
		modif_z_scores = 0.6745*np.abs(coordinates - median) / mad
		print(f'Z-scores for each coordinates:\n{modif_z_scores}\n')
		threshold = 3.5
		index_no_outliers = (modif_z_scores < threshold).all(axis=1)
		coordinates = coordinates[index_no_outliers]
		weights_countries = [weights_countries[i] for i in range(len(weights_countries)) if index_no_outliers[i]]

		# Calculate the average of the remaining coordinates
		avg_coordinate = haversine_mean(np.radians(coordinates), np.array(weights_countries))
		print(f"Average coordinate using the haversine distance: {avg_coordinate}")
		with open(dir_geo + '\\output.csv', "w") as f:
			f.write(f'{avg_coordinate[0]},{avg_coordinate[1]}')
