# Welcome to GeoguessrBot 🌍

Here are all the commands you will need to make the program work and the tips to avoid a maximum of debugging.

The bot is composed of 2 main parts:
- the TIBHannover GeoEstimation model which predicts the coordinates given a picture.
- the Google Chrome extension to interact with the model and obtain the best scores possible.

## Configure TIBHannover GeoEstimation model

### Clone GeoEstimation repository and install requirements

To do so, please make sure you have an appropriate conda environment configured with python 3.8 (PATH variables etc.) and a Github account.

```
git clone https://github.com/thomasdouilly/GeoguessrBot.git
git clone https://github.com/TIBHannover/GeoEstimation.git
move C:\your_path_to_GeoEstimation_folder C:\your_path_to_GeoguessrBot_folder
cd GeoguessrBot\GeoEstimation
conda env create -f environment.yml 
conda activate geoestimation-github-pytorch
git checkout original_tf
python downloader.py
move ..\inference.py .
```

Make sure all zip files unzip correctly. If an error like this `urllib.error.HTTPError: HTTP Error 403: Server failed to authenticate the request. Make sure the value of Authorization header is formed correctly including the signature.` occurs, you can still download manually the zip file from the url, unzip it at the right place, and re-execute the command.

### Build the Docker container

To continue the installation of GeoguessrBot, we will need to set up a Docker container. 

- Check first that Docker Desktop is running.

Then, it is needed to follow one of the two following methods (The second one shall be prefered) :

#### Use a manually built Docker container (To be done at each use of GeoguessrBot)

- In file geoguessr-commands/inference_kaggle.py, make sure that lines 46-47 and 50 are uncommented and that lines 53 to 55 are commented
- Manually add `RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC` in the Dockerfile within the GeoEstimation folder just before `RUN apt-get update`.

```
docker build C:\your_path_to_GeoEstimation_folder -t geoestimation_container
docker run --volume C:\your_path_to_GeoguessrBot_folder\GeoEstimation:/src --volume C:\your_path_to_GeoguessrBot_folder\data\picture:/img -it geoestimation_container bash
```

#### Use an automatically built Docker container (To be done once at installing)

- In file geoguessr-commands/inference_kaggle.py, make sure that lines 46-47 and 50 are commented and that lines 53 to 55 are uncommented

## Chrome extension

### Add the extension and launch the server

- Open Chrome.
- Go to the extension settings.
- Enable Developer mode.
- Click on *Load unpacked* and select the GeoguessrBot folder.
- Pin the GeoguessrBot extension in the jigsaw icon in the top right corner of your window.
- Open a new shell page.

```
cd C:\your_path_to_GeoguessrBot_folder
python launch.py
```

You can now go to https://www.geoguessr.com and play while interacting with the extension.

⚠️ Please not that the computation time of the coordinates can take some time depending on the number of screenshots you took.

## Stop and replay

Once you finished playing, you can stop the server and the container.

If you want to replay, don't forget to execute in 2 separate shell windows the following commands.

```
docker run --volume C:\your_path_to_GeoguessrBot_folder\GeoEstimation:/src --volume C:\your_path_to_GeoguessrBot_folder\data\picture:/img -it geoestimation_container bash
```

```
cd C:\your_path_to_GeoguessrBot_folder
python launch.py
```

Enjoy! 🕹️
