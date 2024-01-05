import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def GetFolderPath ():
    folder_path = filedialog.askdirectory()

    return folder_path

def GetImages  (folder_path: [str]):

    image_files = []

    print(folder_path)

    for file in os.listdir(folder_path):
        # Check if the file is a PNG or JPEG
        if file.lower().endswith(('.png', '.jpeg', '.jpg')):
            image_files.append(file)

    return image_files

def ResizeImage (input_image_path: [str], new_size: [int, int], output_image_path: [str]):

    # Open the image
    img = Image.open(input_image_path)

    # Resize the image
    resized_img = img.resize(new_size)

    # Save the resized image as PNG
    resized_img.save(output_image_path, 'PNG')


#
# Replace everything with custom image processing settings
#

#Sets up the folder
root = tk.Tk()
root.withdraw()

Folder_Path = GetFolderPath()

Output_Path = GetFolderPath()

Images = GetImages(Folder_Path)

for image in Images:
    ResizeImage(Folder_Path + "/" + image, [28, 28], Output_Path + "/" + image)

print(Folder_Path + "  -->  " + Output_Path)

print("Finished")
