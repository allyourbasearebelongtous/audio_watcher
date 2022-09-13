from moviepy.editor import *
from watcher import *
from watcher.processor import *
import pathlib
import subprocess
import ffmpeg
import sys
from pprint import pprint # for printing Python dictionaries in a human-readable way
from converter import Converter
from tinytag import TinyTag
from pymediainfo import MediaInfo



conv = Converter()

movieclips = []
introformat = 0
introbrate = 0
intofrate = "string"
#print("mv.py = %", movieclips)

def getClipInfo(clips):
    for MediaClip in clips:
        # for MediaClip in clipList:
        # print("file type: %", type(MediaClip))
        print("path: %", clips)
        mediameta = MediaInfo.parse(str(MediaClip))
        for track in mediameta.tracks:
            if track.track_type == "Video":
                print("Bit rate: {t.bit_rate}, Frame rate: {t.frame_rate}, "
                "Format: {t.format}".format(t=track)
            )
            introbrate = track.bit_rate
            introfrate = track.frame_rate
            introformat = track.format
            print(introbrate, introformat, introfrate)
            # conversion(MediaClip)
            # print("Duration (raw value):", track.duration)
            # print("Duration (other values:")
            # pprint(track.other_duration)
            
            
def conversion(mclip):
    filetoconvert = subprocess.run("ffmpeg", " -i ", mclip, " -r ", 59.94, " output.mp4")
    # filetoconvert = ffmpeg.input(mclip)
    #  audio = filetoconvert.audio
    #  video = filetoconvert.video
    #  output = ffmpeg.output(audio, video, format=mp4, 'output.mp4')
    

def edit_clips(video_file):
    #print("this is from mv %", video_file)
   
    #probe_file(str(video_file))
    getClipInfo(video_file)
    
    clips = []
    for i in video_file:
        #clips = []
        
        #clips.append(i)
        
        #print(video_file)            
        #print("i = %", clips)
        
        ## Set FPS ##
        #video_file.set_fps(30)
        
        #ffmpeg_probe(i)
        
        print("this is video_file %", video_file)
        
        clipList = [VideoFileClip(c) for c in video_file]
        print(clipList)
        
        videoExt = pathlib.Path(i).suffix
        print(videoExt)
        
        ## add clip fps ##
        for vid in clipList:
            vid.set_fps(29.97)
            print(vid)
            #metad = TinyTag.get(vid)
            #print("Bitrate: " + str(metad.bitrate))
        
    
    
    
    if len(clipList) <= len(video_file):
        write_final_clips(clipList)    
        
        
        
    #final_video = concatenate_videoclips(clipList)
    #final_video.write_videofile("/Users/leahlerner/Movies/output.mp4")
    
    
def write_final_clips(final_video):
    final_video = concatenate_videoclips(final_video)
    ## UNCOMMENT WHEN READY TO DEPLOY ##
    final_video.write_videofile("/Users/leahlerner/Movies/output.mp4", fps = 29.97)
    
def video_options(video_info):
    videoInfo = subprocess.run("ffmpeg -i %", video_info)
    print(videoInfo)


## First attempt? ##
def ffmpeg_probe(clip):
    # read the audio/video file from the command line arguments
    clipFile = sys.argv[1]
    # uses ffprobe command to extract all possible metadata from the media file
    pprint(ffmpeg.probe(clipFile)["streams"])


## FFPROBE for file ##
def probe_file(filename):
    cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(filename)
    out, err =  p.communicate()
    print("==========output==========")
    print(out)
    if err:
        print("========= error ========")
        print(err)
        
        
## Prepare Video for Conversion ##
def pvc(videoFile):
    info = conv.probe(videoFile)

    convert = conv.convert('test/test1.avi', 'test/test1.mp4', {
        'format': 'mp4',
        'audio': {
            'codec': 'aac',
            'samplerate': 11025,
            'channels': 2
        },
        'video': {
            'codec': 'hevc',
            'width': 1280,
            'height': 720,
            'fps': 29.97
        }})

    for timecode in convert:
        print(f'\rConverting ({timecode:.2f}) ...')

## message pop up TO DO ##
""" def success():
    title = "Success"
    message = "File downloaded"
    command = f'''
    osascript -e 'display notification "{message}" with title "{title}"'
    '''
    os.system(command)
 """