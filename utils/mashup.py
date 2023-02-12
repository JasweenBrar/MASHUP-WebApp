import os                   # To deal with paths (get current working directory, make directories)
import shutil               # To empty the entire directory Videos, Audios, ShortAudios

import streamlit as st      # For handling errors

from pytube import Search   # To get list of search results
from pytube import YouTube  # To download YouTube videos

import moviepy              # For converting videos to audio
from moviepy.editor import *
from pathlib import Path    # To append file names

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip # To clip audios

from pydub import AudioSegment  # To merge audio
import wave                     # To combine audios

def MASHUP(singerName,Num,Ysec):

    ############################################################
    #       TASK 1) Create 3 directories for future use
    #       -Videos        -Audios         -ShortAudios   
    ############################################################

    # Parent Directory path
    parent_dir = os.path.abspath(os.getcwd())

    # Directory to keep all videos
    dir_vid = "Videos"
    
    # Absolute path of directory
    VIDEO_PATH = os.path.join(parent_dir, dir_vid)

    # Empty the entire contents of directory if it already exists
    if Path(VIDEO_PATH).is_dir():
        shutil.rmtree(VIDEO_PATH)
    
    # Create the directory
    os.mkdir(VIDEO_PATH)
    # ------------------------------------------------------------

    # Directory to keep all audios
    dir_aud = "Audios"
    # Absolute path of directory
    AUDIO_PATH = os.path.join(parent_dir, dir_aud)
    
    # Empty the entire contents of directory if it already exists
    if Path(AUDIO_PATH).is_dir():
        shutil.rmtree(AUDIO_PATH)

    # Create the directory
    os.mkdir(AUDIO_PATH)
    # ------------------------------------------------------------

    # Directory to keep all clipped audios
    dir_aud_short = "ShortAudios"

    # Absolute path of directory
    SHORT_AUD_PATH = os.path.join(parent_dir, dir_aud_short)
    
    # Empty the entire contents of directory if it already exists
    if Path(SHORT_AUD_PATH).is_dir():
        shutil.rmtree(SHORT_AUD_PATH)

    # Create the directory
    os.mkdir(SHORT_AUD_PATH)

    # ------------------------------------------------------------


    ############################################################
    #     TASK 2) Assigning arguments and handling errors  
    ############################################################

    s = Search(singerName) # Name of the singer you want to search songs of
    # Search returns list of all results on the page
    x = int(Num)           # Number of videos needed
    y = int(Ysec)          # Duration of each video
    c = 1                  # Counter

    if x < 10:
        st.error("No of videos should be >= 10")

    if y < 20:
        st.error("Duration of each video should be >= 20")


    ############################################################
    #   TASK 3) Downloading videos & saving in Videos folder
    ############################################################
    
    link = [] # list of links of the videos to be downloaded
    for v in s.results:
        if c <= x:
            link.append(v.watch_url)
            c = c+1
    
    for i in link:
        try:
            
            # object creation using YouTube
            # which was imported in the beginning
            yt = YouTube(i)
        except:
            
            #to handle exception
            print("Connection Error")

        # download videos with lowest resolution
        d_video = yt.streams.get_lowest_resolution()
        try:
            # downloading the video
            d_video.download(VIDEO_PATH)
        except:
            print("Some Error in downloading!")

    ##################################################################
    # TASK 4) Converting videos to audio and saving in Audios folder  
    ##################################################################

    for v in os.listdir(VIDEO_PATH):
        vid = os.path.join(VIDEO_PATH,v)
        video = moviepy.editor.VideoFileClip(vid)
        audio = video.audio
        v1 = Path(v)
        v_name =  v1.with_suffix('')
        audio.write_audiofile(AUDIO_PATH +  "\\" + str(v_name) + ".wav")

    ##################################################################
    #    TASK 5) Clipping audios & saving in ShortAudios folder  
    ##################################################################

    Startsec = 30 
    Endsec = Startsec + y
    for s in os.listdir(AUDIO_PATH):
        so = os.path.join(AUDIO_PATH,s)
        s1 = Path(s)
        s_name =  s1.with_suffix('')
        p = SHORT_AUD_PATH + "\\" + str(s_name) + ".wav"

        ffmpeg_extract_subclip(so, Startsec, Endsec, targetname=p)

    ##################################################################
    #      TASK 6) Merging audios ; final file -> mashup.wav  
    ##################################################################
    wavs=[]
    for i in os.listdir(SHORT_AUD_PATH):
        i1 = Path(i)
        i_name =  i1.with_suffix('')
        p = SHORT_AUD_PATH + "\\" + str(i_name) + ".wav"
        wavs.append(AudioSegment.from_wav(p))

    
    combined = wavs[0]
    for wav in wavs[1:]:
        combined = combined + wav
            
    combined.export("mashup.wav",format="wav")

    f = parent_dir + "\\" + "mashup.wav"
    return f







