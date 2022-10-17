import cv2 as cv
from pathlib import Path
from progress_bar import printProgressBar
import os

MS_IN_SEC = 1000        # 1000 ms/sec


class VideoProcessing:
    def set_video_path(self, path):
        if not Path(path).exists():
            raise Exception(f'Path {path} does not exist.')

        self.path = path
        self.video_name = path.stem

    def get_video_duration(self, video):
        fps = fps = video.get(cv.CAP_PROP_FPS)
        frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        duration = frame_count/fps

        return duration

    def save_snapshots(self, output_dir, interval_sec=1):
        video = cv.VideoCapture(os.fspath(self.path))
        output_path = Path(output_dir).joinpath(self.video_name)
        interval_ms = int(interval_sec*MS_IN_SEC)
        frame_counter = 0
        success = True

        if not output_path.exists():
            os.mkdir(output_path)

        while success:
            success, frame = video.read()

            progress_status = min(frame_counter*interval_ms/1000, self.get_video_duration(video))
            printProgressBar(progress_status, self.get_video_duration(video))

            if success:
                img_path = str(output_path.joinpath(f'{int(interval_ms*frame_counter)}_ms.jpg'))
                cv.imwrite(img_path, frame)

            frame_counter = frame_counter + 1
            video.set(cv.CAP_PROP_POS_MSEC,(frame_counter*interval_ms))

        video.release()

