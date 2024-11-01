import tkinter as tk
from tkinter import messagebox
from main import SpotifyYouTubeConverter  # Import the main conversion logic


class App:
    def __init__(self, master):
        self.master = master
        master.title("Spotify to YouTube Playlist Converter")

        self.converter = SpotifyYouTubeConverter()

        # Create GUI elements
        self.label = tk.Label(master, text="Enter Spotify Playlist URL:")
        self.label.pack()

        self.playlist_url_entry = tk.Entry(master, width=50)
        self.playlist_url_entry.pack()

        self.convert_button = tk.Button(master, text="Convert to YouTube Playlist", command=self.convert_playlist)
        self.convert_button.pack()

        self.result_label = tk.Label(master, text="", wraplength=300)
        self.result_label.pack()

    def convert_playlist(self):
        playlist_url = self.playlist_url_entry.get()
        if not playlist_url:
            messagebox.showerror("Input Error", "Please enter a Spotify playlist URL.")
            return

        try:
            self.converter.convert_playlist(playlist_url)
            self.result_label.config(text="Playlist converted successfully!")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
