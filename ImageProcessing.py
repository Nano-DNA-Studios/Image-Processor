import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageFilter, ImageOps

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

def ResizeImage (input_image_path: [str], output_image_path: [str]):

    # Open the image
    img = Image.open(input_image_path)

    # Resize the image
    resized_img = img.resize([28, 28])

    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(resized_img)

    inverse = ImageOps.invert(gray_image)

    # Apply edge detection
    edges = inverse.filter(ImageFilter.FIND_EDGES)

    # Save the resized image as PNG
    edges.save(output_image_path, 'PNG')

def RecursiveImageProcessing (input_dir: str , output_dir : str, processImage):

    #Get the List of Directories and the files
    for subdirs, dirs, images in os.walk(input_dir):
        #Copy Folder Structure
        for dir in dirs:
            #Gets the Output folder
            structure_output = os.path.join(output_dir, dir)
            structure_input = os.path.join(input_dir, dir)

            if os.path.isdir(structure_input):
                # print(f"Dir:{dir}")
                # print(f"Input: {structure_input}")
                # print(f"Output: {structure_output}")

                #Make the new Directory
                if not os.path.isdir(structure_output):
                    os.makedirs(structure_output)

                #Go to the next level
                RecursiveImageProcessing(structure_input, structure_output, processImage)

                print(f"Completed {dir}")

        #Process Images
        for image in images:

            image_path = os.path.join(input_dir, image)
            image_output_path = os.path.join(output_dir, image)
            
            if os.path.isfile(image_path):
                if image.lower().endswith(('.png', '.jpeg', '.jpg')):
                    processImage(image_path, image_output_path)

        



#Sets up the folder
root = tk.Tk()
root.withdraw()

Folder_Path = GetFolderPath()

Output_Path = GetFolderPath()

RecursiveImageProcessing(Folder_Path, Output_Path, ResizeImage)

# Images = GetImages(Folder_Path)

# for image in Images:
#     ResizeImage(Folder_Path + "/" + image, [28, 28], Output_Path + "/Test/" + image)

print(Folder_Path + "  -->  " + Output_Path)

print("Finished")
