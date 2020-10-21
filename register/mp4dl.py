import youtube_dl


def mp4dll(videourl):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(title)s.%(ext)s','format':'best'})
    print("URL ?")
    url = videourl

    with ydl:
        result = ydl.extract_info(
            url,
            download=True # We just want to extract the info
        )
