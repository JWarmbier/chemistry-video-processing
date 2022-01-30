from pathlib import Path


def list_video_files(path, extension="*.MP4"):
    path = Path(path)
    video_paths = []

    if not path.exists():
        raise Exception(f'Path {path} does not exits.')

    video_paths = list(path.glob('**/*' + '.MP4'))

    return video_paths



if __name__ == "__main__":
    print(list_video_files('./videos'))

