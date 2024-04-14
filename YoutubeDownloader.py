import os
from pytube import YouTube
from tkinter import * 
from tkinter import ttk
import subprocess
import sys

def get_exe_directory():
    """Function to get the directory of the exe file."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.realpath(__file__))

def YoutubeDownloadMP4():
    exe_directory = get_exe_directory()
    mp4_output_path = os.path.join(exe_directory, 'Mp4 Files')
    if not os.path.exists(mp4_output_path):
        os.mkdir(mp4_output_path)
    try:
        ytLink = Entry.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution() 
        video.download(output_path=mp4_output_path) 
        displayPER.config(fg="green")
    except Exception as e:
        PER.set("Download failed. Please try again")
        displayPER.config(fg="red")

def YoutubeDownloadMP3():
    exe_directory = get_exe_directory()
    mp3_output_path = os.path.join(exe_directory, 'Mp3 Files')
    if not os.path.exists(mp3_output_path):
        os.mkdir(mp3_output_path)
    try:
        ytLink = Entry.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_audio_only() 
        downloaded_file = video.download(output_path=mp3_output_path)
        output_mp3_file_path = os.path.join(mp3_output_path, f'{ytObject.title}.mp3')
        subprocess.run(['ffmpeg', '-i', downloaded_file, output_mp3_file_path], capture_output=True)
        os.remove(downloaded_file)
        displayPER.config(fg="green")
    except Exception as e:
        PER.set("Download failed. Please try again")
        displayPER.config(fg="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = (bytes_downloaded / total_size) * 100
    PER.set(str(int(percentage_of_completion)))
    loadingBar['value'] = percentage_of_completion
    PER.set(f"Download Complete")
    
def clear():
    loadingBar['value'] = 0
    Entry.delete(0, END)
    displayPER.config(fg="black")
    PER.set("")

window = Tk()
window.title("Youtube Converter")

titleLabel = Label(window, font=("Arial", 50, "bold"), text="Youtube Converter")
titleLabel.grid(row=0, column=1, columnspan=3, pady=20, padx=20)

image = PhotoImage(file='C:\\Users\\Admin\\Desktop\\pythonProjects\\Youtube Converter\\Logo.png')
image_Label = Label(window, image=image)
image_Label.grid(row=1, column=1, columnspan=3, pady=20) 
ico_image = "C:\\Users\\Admin\\Desktop\\pythonProjects\\Youtube Converter\\icon.ico"
window.iconbitmap(ico_image)

Entry = Entry(window, font=("Arial", 30, "italic"))
Entry.grid(row=2, column=1, columnspan=3, pady=20)

PER = StringVar()
displayPER = Label(window, textvariable=PER,font=('Arial',12,'bold'))
displayPER.grid(row=3, column=1, columnspan=3, pady=10)

loadingBar = ttk.Progressbar(window, orient=HORIZONTAL, length=500)
loadingBar.grid(row=4, column=1, columnspan=3)

Button(window, font=('Arial', 15, "bold"), text="Convert MP4", command=YoutubeDownloadMP4).grid(row=5, 
column=1, columnspan=1, pady=10,padx=5)
Button(window, font=('Arial', 15, "bold"), text="CLEAR", command=clear).grid(row=5, 
column=1, columnspan=3 ,pady=10, padx=10)
Button(window, font=('Arial', 15, "bold"), text="Convert MP3", command=YoutubeDownloadMP3).grid(row=5, 
column=2, columnspan=4, pady=10,padx=10)

window.mainloop()
