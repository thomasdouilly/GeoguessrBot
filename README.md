Welcome to the TIBHannover GeoEstimation model configuration !
Here are all the commands you will need to make the model work and the tips to avoid a maximum of debugging.

++++++++++++++++++++++++++++++++++++++++++
The code will always be situated between these markers.
++++++++++++++++++++++++++++++++++++++++++


______________________________________________________________________________________________________________



----- Requirements -----

Appropriate conda environment configured with python 3.8 (PATH vairables etc.)
Github account

----- Clone TIBHannover GeoEstimation git repository -----

++++++++++++++++++++++++++++++++++++++++++
git clone https://github.com/TIBHannover/GeoEstimation.git && cd GeoEstimation
conda env create -f environment.yml 
conda activate geoestimation-github-pytorch
++++++++++++++++++++++++++++++++++++++++++

----- Optionnal resources downloading -----

For some resources and depending on your connection speed, it may be faster to download them directly from the url and to place them in the appropriate directory.
/!\ Do not forget to rename them if you do so e.g epoch.014-val_loss.18.4833.ckpt -> epoch=014-val_loss=18.4833.ckpt

++++++++++++++++++++++++++++++++++++++++++
mkdir -p models/base_M
wget https://github.com/TIBHannover/GeoEstimation/releases/download/pytorch/epoch.014-val_loss.18.4833.ckpt -O models/base_M/epoch=014-val_loss=18.4833.ckpt
wget https://github.com/TIBHannover/GeoEstimation/releases/download/pytorch/hparams.yaml -O models/base_M/hparams.yaml
++++++++++++++++++++++++++++++++++++++++++

# Download pre-calculated partitonings
++++++++++++++++++++++++++++++++++++++++++
mkdir -p resources/s2_cells
wget https://raw.githubusercontent.com/TIBHannover/GeoEstimation/original_tf/geo-cells/cells_50_5000.csv -O resources/s2_cells/cells_50_5000.csv
wget https://raw.githubusercontent.com/TIBHannover/GeoEstimation/original_tf/geo-cells/cells_50_2000.csv -O resources/s2_cells/cells_50_2000.csv
wget https://raw.githubusercontent.com/TIBHannover/GeoEstimation/original_tf/geo-cells/cells_50_1000.csv -O resources/s2_cells/cells_50_1000.csv
++++++++++++++++++++++++++++++++++++++++++

# Download im2gps testset
++++++++++++++++++++++++++++++++++++++++++
cd resources
mkdir images/im2gps
wget http://graphics.cs.cmu.edu/projects/im2gps/gps_query_imgs.zip -O resources/images/im2gps.zip
unzip resources/images/im2gps.zip -d resources/images/im2gps/
wget https://raw.githubusercontent.com/TIBHannover/GeoEstimation/original_tf/meta/im2gps_places365.csv -O resources/images/im2gps_places365.csv
wget https://raw.githubusercontent.com/TIBHannover/GeoEstimation/original_tf/meta/im2gps3k_places365.csv -O resources/images/im2gps3k_places365.csv
++++++++++++++++++++++++++++++++++++++++++

----- original_tf branch: files and models -----

Go back to the project "base" folder

++++++++++++++++++++++++++++++++++++++++++
git checkout original_tf
python downloader.py
++++++++++++++++++++++++++++++++++++++++++

make sure all zip files unzip correctly. If an error like this "urllib.error.HTTPError: HTTP Error 403: Server failed to authenticate the request. Make sure the value of Authorization header is formed correctly including the signature." occurs, you can still download manually the zip file from the url and unzip it at the right place.

----- Docker container: build and run -----

Check first that Docker Desktop is running.
Add RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC in the dockerfile

++++++++++++++++++++++++++++++++++++++++++
docker build C:\Users\douil\OneDrive\Bureau\Codes\GeoEstimation -t geoestimation_container
docker run --volume C:\Users\douil\OneDrive\Bureau\Codes\GeoEstimation:/src --volume C:\Users\douil\OneDrive\Bureau\Codes\test_images:/img -it geoestimation_container bash
++++++++++++++++++++++++++++++++++++++++++

Normally, you are supposed to add the args "-u $(id -u):$(id -g)" to the previous command but sometimes it does not work I don't know why.

----- Commands to get image geoestimation -----

++++++++++++++++++++++++++++++++++++++++++
cd /src
python inference.py -i /img/*.jpg
++++++++++++++++++++++++++++++++++++++++++

generated images

++++++++++++++++++++++++++++++++++++++++++
cd ../geoguessr-commands/
python inference_kaggle.py
++++++++++++++++++++++++++++++++++++++++++