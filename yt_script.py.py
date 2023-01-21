from pytube import YouTube
import argparse

def record_livestream(url, duration, chunks):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Record a YouTube livestream to a local mp4 file')
    parser.add_argument('url', type=str, help='URL of the YouTube livestream')
    args = parser.parse_args()

    record_livestream(args.url, args.duration, args.chunks)
