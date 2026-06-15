import os
import yt_dlp
import imageio_ffmpeg

def download_youtube_video(video_url):
    output_folder = "downloads"
    
    # 1. Check and create directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
    
    # Get the exact physical path where imageio-ffmpeg saved the engine executable
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    # 2. Configure downloader options for absolute player compatibility
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg_path,
        
        # ◄── NEW: Forces FFmpeg to re-encode the audio track to universal AAC format ──►
        'postprocessor_args': [
            '-c:a', 'aac',         # Audio codec: Advanced Audio Coding (AAC)
            '-b:a', '192k'         # Audio bitrate: Crystal clear 192kbps high quality
        ],
    }
    
    # 3. Safe Execution (Error Handling)
    try:
        print("Connecting to YouTube... please wait...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download complete! Your file is safe inside the 'downloads' folder.")
        
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    link = input("Paste your YouTube link here: ")
    download_youtube_video(link)