import cv2
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pathlib import Path
from moviepy.editor import *
import glob

def vid_to_frames():
    cap = cv2.VideoCapture('/home/ddd/Videos/matan0014.mp4')
    i = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i%10==0:
            cv2.imwrite('/home/ddd/Videos/matan0014_frames/matan14' + str(i) + '.jpg', frame)
        i += 1
        print(i)
    cap.release()
    cv2.destroyAllWindows()


def generate_small_vid(vid_path,vid_name,start_time,end_time):
    ffmpeg_extract_subclip(vid_path+vid_name, start_time, end_time, targetname= vid_path+"12.mp4")

def generate_movies_from_jpgs(root_directory):
    paths = []
    for dir_name in Path(root_directory).rglob('JPEGImages'):
        paths.append(dir_name)
        print(dir_name)
        #images = glob.glob(str(dir_name)+'/*.jpg')
        #clips = [ImageClip(m).set_duration(2) for m in images]
        #concat_clip = concatenate_videoclips(clips, method="compose")
        #concat_clip.write_videofile(str(dir_name) + "/30.mp4", fps=5)
        #print(len(paths))
    #return pairs
generate_movies_from_jpgs('/home/ddd/Videos/NogaMovies/')
#generate_movies_from_jpgs('/home/ddd/Videos/')

