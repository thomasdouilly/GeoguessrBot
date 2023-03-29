from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pyautogui
import keyboard
import mouse
import time
import os
import csv
import sys
import logging
import random as rd

@csrf_exempt

def index(request):
    return HttpResponse("Hello, world.")


def reload(_):
    
    keyboard.press_and_release('f5')
    
    return JsonResponse({})


def screen_capture(_):

    geo_picture = pyautogui.screenshot()
    geo_picture.save('../data/picture/geo_picture-' + str(rd.randint(0, 1e+12)) +'.png')

    keyboard.press_and_release('f11')
    
    return JsonResponse({})

def reset_pictures(_):
    
    files = os.listdir('../data/picture')
    
    for file in files:

        os.remove('../data/picture/' + file)
    
    return JsonResponse({})


def process(_):
    
    sys.path.append(os.path.join(os.path.split(sys.path[0])[0], 'geoguessr-commands'))
    import inference_kaggle
    
    inference_kaggle.main()
    
    data = {}
    
    reader = csv.reader(open('../data/output.csv', 'r'), delimiter=';')
    
    for row in reader:

        if row != '':    
                
            [coords] = row

            lat, long = coords.split(',')
            lat = float(lat)
            long = float(long)

            data["longitude"] = long
            data["latitude"] = lat
        
    reader = csv.reader(open('../data/output_agg.csv', 'r'), delimiter=';')

    intermediate_coords = []
    
    for row in reader:

        if row != '':    
                
            [_, coords, _] = row

            lat, long = coords.split(',')
            lat = float(lat.split('(')[1])
            long = float(long.split(')')[0])

            intermediate_coords.append([lat, long])

    data['intermediate'] = intermediate_coords
    
    return JsonResponse(data)