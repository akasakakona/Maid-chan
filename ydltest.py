import os

youtube_dl_opts = {}

url = input("Enter filename: ")
for file in os.listdir("./"):
        if(file.startswith(url)):
                filename = file
                print(filename)
                break