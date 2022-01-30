from pathlib import Path, PosixPath
from video_processing import VideoProcessing
import os


def list_video_files(path, extension="*.MP4"):
    path = Path(path)
    video_paths = []

    if not path.exists():
        raise Exception(f'Path {path} does not exits.')

    video_paths = list(path.glob('**/*' + '.MP4'))

    return video_paths


def extract_images(video_list, output_dir):
    video_processing = VideoProcessing()
    output_dir = Path(output_dir)

    if not output_dir.exists():
        os.mkdir(output_dir)

    for video_path in video_list:
        video_processing.set_video_path(video_path)
        video_processing.save_snapshots(output_dir, 0.5)


if __name__ == "__main__":
    video_list = list_video_files('./videos')

    extract_images(video_list, './images')


