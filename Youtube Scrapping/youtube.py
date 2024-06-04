#Copyright of the code belongs to Arnob Rahee and Richard Lee Rogers

import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from openpyxl import Workbook
import requests
import warnings
channelname='@Moms4Liberty'
channelid='UC2H19eKURyI364Q3Rv-o_5g'
date='20240604'
import scrapetube
list=[]
url="https://www.youtube.com/watch?v="
dataframe=pd.DataFrame(columns=["videoid"])
videos=scrapetube.get_channel(channelid)
for video in videos:
    videoid=str(video['videoId'])
    print(videoid)
    list.append(videoid)
dataframe['videoid']=list
outputfile="archive.xlsx"
dataframe.to_excel(outputfile)
print(" ")
print("done with videos-- switch to transcripts pulls")

warnings.filterwarnings("ignore")
exc_workbook = Workbook()
exc_sheet = exc_workbook.active
exc_sheet.title = 'Exceptions'
exc_sheet.append(['Video ID', 'Exception Message'])  
inputfile = pd.read_excel('archive.xlsx', engine='openpyxl')
inputfile = inputfile.videoid.unique()
for i in inputfile:
    print(i)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(i)
        fileframe = pd.DataFrame(transcript)
        #outputfile = i + ".dta"
       # fileframe.to_stata(outputfile, version=118)
    except Exception as e:
        exception_message = str(e)
        print(f"exception: {i}, {exception_message}")
        # Write the exception to the Excel file
        exc_sheet.append([i, exception_message])
exc_workbook.save('exceptions.xlsx')