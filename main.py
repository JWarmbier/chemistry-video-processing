from pathlib import Path, PosixPath

from matplotlib.pyplot import stem
from video_processing import VideoProcessing
from image_processing import ImageProcessing
from operator import itemgetter
import os
import matplotlib.pyplot as plt
import pandas as pd


VIDEO_DIR           = './videos'
VIDEO_FRAMES_DIR    = './images'


def list_files(directory, extension="MP4"):
    directory = Path(directory)
    files = []

    if not directory.exists():
        raise Exception(f'Path {directory} does not exits.')

    files = list(directory.glob(f'**/*.{extension}'))

    return files


def extract_images(video_list, output_dir):
    video_processing = VideoProcessing()
    output_dir = Path(output_dir)

    if not output_dir.exists():
        os.mkdir(output_dir)

    for video_path in video_list:
        video_processing.set_video_path(video_path)
        video_processing.save_snapshots(output_dir, 0.5)


if __name__ == "__main__":
    video_path = Path(VIDEO_DIR)
    video_frame_output_path = Path(VIDEO_FRAMES_DIR)

    video_list = list_files(VIDEO_DIR, 'mp4')
    extract_images(video_list, video_frame_output_path)

    video_frame_paths = [video_frame_output_path.joinpath(video.stem) for video in video_list]

    for video_frame_path in video_frame_paths:
        frame_paths = list_files(video_frame_path, "jpg")
        frame_values = []

        for frame_path in frame_paths:
            img_processing = ImageProcessing(frame_path)
            frame_values.append([frame_path.stem, img_processing.find_min_height()])

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
        plt.savefig(video_frame_path.joinpath('results_graph.png'), format='png', dpi=300)
        # plt.show()
        df_results = pd.DataFrame(data={"Time" : time, "Value" : value})
        df_results.to_csv(video_frame_path.joinpath('results.csv'))
