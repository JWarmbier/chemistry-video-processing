import cv2 as cv
from pathlib import Path
import os

class VideoProcessing:
    def set_video_path(self, path):
        if not Path(path).exists():
            raise Exception(f'Path {path} does not exist.')

        self.path = path
        self.video_name = path.stem

    def save_snapshots(self, output_dir, interval=1):
        video = cv.VideoCapture(os.fspath(self.path))
        output_path = Path(output_dir).joinpath(self.video_name)
        interval_ms = int(interval*1000)
        frame_counter = 0
        success = True

        if not output_path.exists():
            os.mkdir(output_path)

        while success:
            success, frame = video.read()
            if success:
                img_path = str(output_path.joinpath(f'{self.video_name}_{int(interval_ms*frame_counter)}_ms.jpg'))
                cv.imwrite(img_path, frame)

            frame_counter = frame_counter + 1
            video.set(cv.CAP_PROP_POS_MSEC,(frame_counter*interval_ms))

        video.release()

