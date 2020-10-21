# coding:utf-8
import os
import csv

# htmlからのデータをcsvファイルに記録
def write_csv(data):
    print([data])
    import pandas as pd
    from apiclient.discovery import build
    from apiclient.errors import HttpError
    #API_KEY ='AIzaSyChMF4elfMUmUxVr08AK522g0dIZKf3Z4Y'
    API_KEY = 'AIzaSyAjT-Z7wCNHQ5iTWmWdu6-pL34HUp6DZ4s'
    #'AIzaSyAjT-Z7wCNHQ5iTWmWdu6-pL34HUp6DZ4s'
    #'AIzaSyAl5j0lpQR7X8_wOk5lwuMPaiSxccUQJ3Y'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    #CHANNEL_ID = 'UC69URn8iP4u8D_zUp-IJ1sg'
    CHANNEL_ID = data.split('channel/')[1]
    channels = [] #チャンネル情報を格納する配列
    searches = [] #videoidを格納する配列
    videos = [] #各動画情報を格納する配列
    nextPagetoken = None
    nextpagetoken = None

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION,
        developerKey=API_KEY
        )

    channel_response = youtube.channels().list(
        part = 'snippet,statistics',
        id = CHANNEL_ID,
        ).execute()
    
    while True:
        if nextPagetoken != None:
            nextpagetoken = nextPagetoken

        search_response = youtube.search().list(
        part = "snippet",
        channelId = CHANNEL_ID,
        maxResults = 50,
        order = "date", #日付順にソート
        pageToken = nextpagetoken #再帰的に指定
        ).execute()  

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                searches.append(search_result["id"]["videoId"])

        try:
            nextPagetoken =  search_response["nextPageToken"]
        except:
            break

    for result in searches:
        video_response = youtube.videos().list(
        part = 'snippet,statistics',
        id = result
        ).execute()
        #print(video_response.get("items", []))
        for video_result in video_response.get("items", []):
            if video_result["kind"] == "youtube#video":
                tagg=''
                videoo =''
                try :
                    tagg=video_result['snippet']['tags']
                except :
                    tagg=''
                try :
                    videoo=video_result["snippet"]['thumbnails']['maxres']['url']
                except :
                    videoo=''
                try :
                    commentt=video_result["statistics"]["commentCount"]
                except :
                    commentt=''
                videos.append([video_result['snippet']['channelTitle'],tagg,'https://www.youtube.com/watch?v=' + video_result['id'],videoo,video_result["snippet"]["description"].split('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')[0],video_result["snippet"]["title"],video_result["statistics"]["viewCount"],video_result["statistics"]["likeCount"],video_result["statistics"]["dislikeCount"],commentt,video_result["snippet"]["publishedAt"]])  

    videos_report = pd.DataFrame(videos, columns=['Channelname','tag','VideoID','Thumbnail','escr','title', 'viewCount', 'likeCount', 'dislikeCount', 'commentCount', 'publishedAt'])
    videos_report.to_csv("media/apifile/channel.csv", index=None)

