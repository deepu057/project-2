from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from pytube import YouTube
import threading
import os
from kivymd.toast import toast

class VideoDownloaderApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.root = Builder.load_string(
            '''
BoxLayout:
    orientation: "vertical"
    spacing: "10dp"
    padding: "10dp"
    MDLabel:
        text: "JAYDEEP OMPRAKASH SHARMA'S Video Downloader"
        halign: "center"
        font_style: "H5"
    MDTextField:
        id: url_entry
        hint_text: "YouTube URL"
        size_hint_x: None
        width: "250dp"
    MDBoxLayout:
        spacing: "5dp"
        MDDropDownItem:
            id: resolution_combobox
            text: "Resolution"
            width: "200dp"
            menu: [{"text": "Highest"}, {"text": "720p"}, {"text": "480p"}, {"text": "360p"}]
    MDRectangleFlatButton:
        text: "Download"
        on_press: app.download_video()
    MDProgressBar:
        id: progress_bar
        size_hint_y: None
        height: "20dp"
        indeterminate: True
'''
        )
        return self.root

    def download_video(self):
        url = self.root.ids.url_entry.text
        resolution = self.root.ids.resolution_combobox.text

        if not url:
            toast("Please enter a YouTube URL.")
            return

        self.root.ids.progress_bar.start()

        def download():
            try:
                yt = YouTube(url)
                if resolution == "Highest":
                    stream = yt.streams.get_highest_resolution()
                else:
                    stream = yt.streams.filter(res=resolution).first()

                # Specify the desktop directory for saving the downloaded videos
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                download_path = os.path.join(desktop_path, "downloaded_videos")
                os.makedirs(download_path, exist_ok=True)

                # Download the video to the specified directory
                stream.download(output_path=download_path)

                toast("Video downloaded successfully!")
            except Exception as e:
                toast(f"An error occurred: {str(e)}")
            finally:
                self.root.ids.progress_bar.stop()

        threading.Thread(target=download).start()

if __name__ == "__main__":
    VideoDownloaderApp().run()
