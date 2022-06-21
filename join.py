from moviepy.editor import *
import math

try:
	video_1 = VideoFileClip(sys.argv[1])
	video_2 = VideoFileClip(sys.argv[2])
	video_3 = video_1.subclip(0,math.floor(video_1.duration)*0.8)
	video_4 = video_2
	final1 = video_3.resize((1080,1920))
	final2 = video_4.resize((1080,1920))

	finalVideo = concatenate_videoclips([final1,final2])
	finalVideo.write_videofile('final2.mp4',threads=20,fps=60,bitrate="2500k")
except:
	print("Usage : python join.py 1.mp4 2.mp4")