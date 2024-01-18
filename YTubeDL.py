from pytube import YouTube
import os, re


default_path = os.getcwd().replace('\\', '/')
ffmpeg_path = default_path + "/ffmpeg/bin/ffmpeg.exe"
while True:
    destination_path = input("Enter the desired folder path (or leave blank for default): ").replace("\\", "/")
    destination_path = destination_path.strip()  

    if destination_path:
        if os.path.exists(destination_path):
            folder_path = destination_path
            print("\n Using specified path:", folder_path)
            break
        else:
            print("\n Invalid path. Please enter a valid path or leave blank for default.")
    else:
        folder_path = default_path + "/output"
        os.makedirs(folder_path, exist_ok=True)
        print("\nCreated default directory:", folder_path)
        break         

def getTitle(link):
    global title, youtubeObject, vid, audio
    youtubeObject = YouTube(link, on_progress_callback=on_progress)
    title = youtubeObject.title
    title = re.sub(r'[<>:"/\|?!*]', "", title).replace("  ", " ")
    vid = youtubeObject.streams.filter(only_video=True)
    audio = youtubeObject.streams.filter(only_audio=True).order_by('abr').desc().first()
    os.system('cls' if os.name == 'nt' else 'clear')

def on_progress(stream, chunk, bytes_remaining):
    total_size_bytes = stream.filesize
    bytes_downloaded = total_size_bytes - bytes_remaining
    total_size_mb = int(total_size_bytes / (1024 * 1024)) 
    bytes_downloaded_mb = bytes_downloaded / (1024 * 1024)
    percent = round((bytes_downloaded / total_size_bytes) * 100, 2)
    print(f"\n{bytes_downloaded_mb} MB of {total_size_mb} MB downloaded ({percent}%)")

def getChoose(choose):
    global extension, output_file, output_path
    match choose:
        case "video":
            extension = ".mp4"
        case "audio":
            extension = ".mp3"
    output_file = f"{title}{extension}"
    output_path = f"{folder_path}/{output_file}"
def delete():
    os.rename(output_file, output_path)
    end(title, output_path)

def end(title, output_path):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n Output Path", output_path)
    print(f"\n Finished Downloaded: {title}")

while True:
    link = input("\n Youtube Link --> URL: ")
    
    if not link: 
        print("\n Please enter a Youtube link.\n")
        continue  

    if "youtu.be" not in link and "youtube.com" not in link: 
        print("\n Invalid YouTube link. Please try again.\n")
        continue
    else:
        getTitle(link)
        print(f"\nTitle: {title}\n")
        while True:
            choose = input("Video or Audio?: ").lower()
            if choose not in ("video", "audio"):
                print("\n Invalid! Audio and Video only")
                pass
            else:
                getChoose(choose)
                if os.path.exists(output_path):
                    print(f"\nThe video '{title}{extension}' already exists in the output folder.")
                    break
                else:
                    if choose == "audio":
                        audio.download(filename="audio.m4a")
                        os.system(fr'{ffmpeg_path} -i "audio.m4a" "{title}{extension}" && del audio.m4a')
                    else:
                        format_info = []
                        for i, stream in enumerate(vid):
                            file_size_mb = round(stream.filesize_approx / (1024 * 1024), 2)  
                            format_info.append((i, stream, f"{file_size_mb} MB"))  

                        for i, stream, file_size in format_info:
                            print(f"{i}. ({file_size}) {stream.resolution}")

                        while True:
                            try:
                                strm = int(input(f"0 - {len(vid) - 1}: "))
                                if 0 <= strm < len(vid):
                                    audio.download(filename="audio.m4a")
                                    vid[strm].download(filename="video.mp4")

                                    os.system(fr'{ffmpeg_path} -i video.mp4 -i audio.m4a -c:v copy -c:a aac -strict experimental "{title}{extension}" && del video.mp4 audio.m4a')
                                    break
                                else:
                                    print(f"\n Please enter a number between 0 and {len(vid) - 1} \n Option Above ")
                            except:
                                print("\n Invalid input. Please enter a whole number.\n")
                    delete()
                    break
