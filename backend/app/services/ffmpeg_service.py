# Simple wrapper example for ffmpeg
import subprocess

def run_ffmpeg(args):
    cmd = ['ffmpeg'] + args
    subprocess.run(cmd)
    return True
