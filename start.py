from pathlib import Path, PosixPath

from matplotlib.pyplot import stem
from video_processing import VideoProcessing
from image_processing import ImageProcessing
from operator import itemgetter
from progress_bar import printProgressBar
from log_colours import log_colors as color
import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import re

MP4_REGEX = '\.mp4$'
JPG_REGEX = '\.jpg$'

def parse_input_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='./videos/',
                        help='indicate the input directory where the program should find all videos for processing.')
    parser.add_argument('--result_dir', type=str, default='./results/', help='indicate the output directory for results.')

    return parser.parse_args()

def select_paths(paths, regex):
    matched_paths = []
    for file in paths:
        if re.search(regex, file.name.lower()) is not None:
            matched_paths.append(file)

    return matched_paths


def list_files(directory, MP4_REGEX, verbose=False):
    directory = Path(directory)

    if verbose:
        print(color.HEADER + color.BOLD + f'Searching all files with {MP4_REGEX} extension in {directory}' + color.END)

    if not directory.exists():
        raise Exception(f'Path {directory} does not exits.')

    found_files = list(directory.glob(f'**/*'))

    files = select_paths(found_files, MP4_REGEX)

    if verbose:
        if files is not None and len(files) > 0:
            print(color.GREEN + 'Some files are found!' + color.END)
            for file in files:
                print(f' - {file.name}')
        else:
            print('No files are found.\n')

    return files


def extract_images(video_list, output_dir):
    if len(video_list) > 0:
        video_processing = VideoProcessing()
        print(color.HEADER + color.BOLD + "\nExtracting frames from videos." + color.END)
        output_dir = Path(output_dir)

        if not output_dir.exists():
            os.mkdir(output_dir)

        for video_path in video_list:
            print(f'  Processing file: {video_path.name}')
            video_processing.set_video_path(video_path)
            video_processing.save_snapshots(output_dir, 0.5)


if __name__ == "__main__":
    args  = parse_input_arguments()

    video_path = Path(args.input_dir)
    video_frame_output_path = Path(args.result_dir)

    video_list = list_files(args.input_dir, MP4_REGEX, verbose=True)
    extract_images(video_list, video_frame_output_path)

    video_frame_paths = [video_frame_output_path.joinpath(video.stem) for video in video_list]

    if len(video_frame_paths) > 0:
        print(color.HEADER + color.BOLD + "\nProcessing extracted frames." + color.END)

        for video_frame_path in video_frame_paths:
            print(f'\n Processing frames from directory: ./{video_frame_path}/')
            frame_paths = list_files(video_frame_path, JPG_REGEX)
            frame_values = []

            for frame_path in frame_paths:
                printProgressBar(frame_paths.index(frame_path), len(frame_paths) - 1)
                img_processing = ImageProcessing(frame_path)
                frame_values.append([frame_path.stem, img_processing.find_min_height()])

            figure_path = video_frame_path.joinpath('results_graph.png')
            print(f'   Saving figure: {figure_path}')
            for i in range(len(frame_values)):
                timestamp = frame_values[i][0]
                timestamp = timestamp.split('_')[0]
                timestamp = int(timestamp)/1000
                frame_values[i][0] = timestamp

            frame_values = sorted(frame_values,key=itemgetter(0))
            time, value = zip(*frame_values)
            plt.plot(time, value)
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.savefig(figure_path, format='png', dpi=300)
            # plt.show()

            csv_result_path = video_frame_path.joinpath('results.csv')
            print(f'   Saving results: {csv_result_path}')
            df_results = pd.DataFrame(data={"Time" : time, "Value" : value})
            df_results.to_csv(csv_result_path)

