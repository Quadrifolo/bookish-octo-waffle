import os
import requests
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from PIL import Image, ImageTk


class ImageDownloader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Image Downloader")
        self.master.geometry("600x400")

        self.search_label = ttk.Label(self.master, text="Search Term:")
        self.search_label.pack()
        self.search_term = ttk.Entry(self.master, width=40)
        self.search_term.pack()

        self.folder_label = ttk.Label(self.master, text="Folder Path:")
        self.folder_label.pack()
        self.folder_path = ttk.Entry(self.master, width=40)
        self.folder_path.pack()

        self.download_button = ttk.Button(
            self.master, text="Download Images", command=self.download_images)
        self.download_button.pack()

        self.status = tk.StringVar()
        self.status.set("Ready")
        self.status_label = ttk.Label(self.master, textvariable=self.status)
        self.status_label.pack()

        self.image_frame = ttk.Frame(self.master)
        self.image_frame.pack(pady=10)

        self.images = []

    def download_images(self):
        self.status.set("Downloading Images...")
        search_term = self.search_term.get()
        folder_path = self.folder_path.get()
        url = f"https://www.google.com/search?q={search_term}&source=lnms&tbm=isch"
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        img_tags = soup.find_all("img")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for i, img_tag in enumerate(img_tags):
            img_url = img_tag["src"]
            try:
                response = requests.get(img_url)
                filename = os.path.join(folder_path, f"{search_term}_{i}.jpg")
                with open(filename, "wb") as f:
                    f.write(response.content)
                # Open the image file and add it to the images list
                image = Image.open(filename)
                self.images.append(image)
            except:
                pass

        # Clear any previously displayed images
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Display the downloaded images in the GUI
        row = 0
        col = 0
        for i, image in enumerate(self.images):
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(self.image_frame, image=photo)
            label.image = photo
            label.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                row += 1
                col = 0

        self.status.set("Download Complete")


root = tk.Tk()
app = ImageDownloader(root)
app.mainloop()
