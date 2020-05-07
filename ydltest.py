import youtube_dl

youtube_dl_opts = {}

url = input("Enter url: ")
with youtube_dl.YoutubeDL(youtube_dl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        name = info_dict.get('title', None)
        duration = info_dict.get('duration', None)
print(f"Name: {name}\nDuration: {duration * 10}")