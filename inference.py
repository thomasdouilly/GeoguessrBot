import argparse
import csv
import glob
import os
import pandas as pd
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses unnecessarily excessive console output
import tensorflow as tf
from imageio import imread as imread

# own imports
import utils
import geo_estimation
import draw_class_activation_maps as draw_cam

# VARIABLES
cur_path = os.path.abspath(os.path.dirname(__file__))

def get_all_files(dir_path):
    files = []
    for root, dirs, filenames in os.walk(dir_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--inputs', nargs='+', type=str, required=False, help='path to image file(s)')
    parser.add_argument('-l', '--labels', type=str, required=False, help='path to ground truth labels')
    parser.add_argument('-m',
                        '--model',
                        type=str,
                        default='ISN',
                        choices=['ISN', 'base_L', 'base_M'],
                        help='Choose from [ISN, base_L, base_M]')
    parser.add_argument('-s',
                        '--show_cam',
                        action='store_true',
                        help='set flag to enable visualization of class activation maps')
    parser.add_argument('-c', '--cpu', action='store_true', help='use cpu')
    args = parser.parse_args()
    return args


def main():
    # load arguments
    args = parse_args()
    print('Parsing arguments...')

    # check if gpu is available
    if not tf.test.is_gpu_available():
        print('No GPU available. Using CPU instead ... ')
        args.cpu = True

    # init models
    if args.model == 'ISN':
        print('Scene classification')
        # init model for scene_classification
        # NOTE: Caffe in Docker container is built without cpu support (unfortunately this is very slow)
        import scene_classification
        sc = scene_classification.SceneClassifier(use_cpu=True)

        # init ISN for concept 'indoor'
        ge_indoor = geo_estimation.GeoEstimator(os.path.join(cur_path, 'models', 'ISN_M_indoor', 'model.ckpt'),
                                                scope='indoor',
                                                use_cpu=args.cpu)
        # init ISN for concept 'natural'
        ge_natural = geo_estimation.GeoEstimator(os.path.join(cur_path, 'models', 'ISN_M_natural', 'model.ckpt'),
                                                 scope='natural',
                                                 use_cpu=args.cpu)
        # init ISN for concept 'urban'
        ge_urban = geo_estimation.GeoEstimator(os.path.join(cur_path, 'models', 'ISN_M_urban', 'model.ckpt'),
                                               scope='urban',
                                               use_cpu=args.cpu)

        ge_isns = {'indoor': ge_indoor, 'natural': ge_natural, 'urban': ge_urban}

    elif args.model == 'base_L':
        ge_base = geo_estimation.GeoEstimator(os.path.join(cur_path, 'models', 'base_L_m', 'model.ckpt'),
                                              scope='base_L_m',
                                              use_cpu=args.cpu)

    elif args.model == 'base_M':
        ge_base = geo_estimation.GeoEstimator(os.path.join(cur_path, 'models', 'base_M', 'model.ckpt'),
                                              scope='base_M',
                                              use_cpu=args.cpu)

    if args.labels:  # read labels (if specified)
        meta_info = pd.read_csv(args.labels)
    else:  # create empty dataframe
        meta_info = pd.DataFrame(columns=['IMG_ID', 'LAT', 'LON'])

    # get predictions
    gc_dists = {}
    i = 0

    inputs = get_all_files("/img")
    # inputs = glob.glob("img/*.jpg")
    print(inputs[:10])

    for img_file in inputs:
        i += 1
        print('{} / {} Processing: {}'.format(i, len(inputs), img_file))

        # get meta information if available
        fname = os.path.basename(img_file)
        img_meta = meta_info.loc[meta_info['IMG_ID'] == fname]
        if len(img_meta) > 0:
            img_meta = img_meta.iloc[0]
        else:
            img_meta = {}

        # predict scene label
        if args.model == 'ISN':
            # get scene label
            if 'Prob_indoor' in img_meta and 'Prob_natural' in img_meta and 'Prob_urban' in img_meta:
                scene_probabilities = [img_meta['Prob_indoor'], img_meta['Prob_natural'], img_meta['Prob_urban']]
            else:
                scene_probabilities = sc.get_scene_probabilities(img_path=img_file)

            print('\t### SCENECLASSIFICATION RESULTS ###')
            print('\tindoor : {}'.format(scene_probabilities[0]))
            print('\tnatural: {}'.format(scene_probabilities[1]))
            print('\turban  : {}'.format(scene_probabilities[2]))

            scene_label = sc.get_scene_label(scene_probabilities)
        else:
            scene_label = None

        # predict geolocation depending on model and scenery
        if scene_label:
            ge = ge_isns[scene_label]
        else:
            ge = ge_base

        print('\t--> Using {} network for geolocation'.format(ge.network_dict['scope']))

        ge.calc_output_dict(img_file)

        print('\t### GEOESTIMATION RESULTS ###')
        for p in range(len(ge.network_dict['partitionings'])):
            p_name = ge.network_dict['partitionings'][p]
            pred_loc = ge.output_dict['predicted_GPS_coords'][p]

            # only calculate result if ground truth location is specified in args.labels
            dist_str = ''
            if 'LAT' in img_meta and 'LON' in img_meta:
                if p_name not in gc_dists:
                    gc_dists[p_name] = {}
                gc_dists[p_name][fname] = utils.gc_distance(pred_loc, [img_meta['LAT'], img_meta['LON']])
                dist_str = f' --> GCD to true location: {gc_dists[p_name][fname]:.2f} km'

            print(f"\tPredicted GPS coordinate (lat, lng) for <{p_name}>: ({pred_loc[0]:.2f}, {pred_loc[1]:.2f})" +
                  dist_str)

        # draw class activation map for the class with the highest probability in the finest available partition
        # NOTE: hierarchical classification is used if more than one partition available
        if args.show_cam:
            predicted_class = ge.output_dict['predicted_cell_ids'][-1]
            cam = draw_cam.calc_class_activation_map(ge.network_dict,
                                                     ge.output_dict,
                                                     class_idx=predicted_class,
                                                     partition_idx=-1)

            img = imread(img_file)
            draw_cam.draw_class_activation_map(img, cam)

    # print results for all files with specified gt location
    if args.labels:
        print('### TESTSET RESULTS ###')
        utils.print_results(gc_dists)


if __name__ == '__main__':
    sys.exit(main())
