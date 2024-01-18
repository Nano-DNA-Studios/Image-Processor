import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance, ImageOps
import random

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

def ProcessShapes (input_image_path: [str], output_image_path: [str]):
    
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

    #Make 10 edited copies 
    for i in range(20):
        #Make 10 copies
        edge_copy = edges.copy()

        #Get random values
        angle = random.uniform(-40, 40)
        scale = random.uniform(0.5, 1.4)
        offsetX = random.randint(-4, 4)
        offsetY = random.randint(-4, 4)

        #Rotate the Image
        rotated_image = edge_copy.rotate(angle, expand=False)

        #Scale Image
        scale_image = ImageOps.scale(rotated_image, scale, resample=Image.Resampling.BILINEAR)

        #Generate a new Image for Offset
        offset_image = Image.new('L', edge_copy.size)

        #Offset the image
        offset_image.paste(scale_image, (offsetX, offsetY))

        #Get Noise image
        noise = Image.effect_noise(edge_copy.size, 60)

        #Mix original and the noise
        noise_image = Image.blend(offset_image, noise, 0.1) #Change this Alpha value

        #Get new Save path
        edited_path = output_image_path.replace(".", f"_{i}.")

        # Save the Edited image
        noise_image.save(edited_path, 'PNG')

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
    for subdirs, dirs, files in os.walk(input_dir):
        #Copy Folder Structure
        for dir in dirs:
            #Gets the Output folder
            structure_output = os.path.join(output_dir, dir)
            structure_input = os.path.join(input_dir, dir)

            if os.path.isdir(structure_input):
                #Make the new Directory
                if not os.path.isdir(structure_output):
                    os.makedirs(structure_output)

                #Go to the next level
                RecursiveImageProcessing(structure_input, structure_output, processImage)

                print(f"Completed {dir}")

        #Process Images
        for file in files:
            #Save paths
            image_path = os.path.join(input_dir, file)
            image_output_path = os.path.join(output_dir, file)

            #Check if it's a real file 
            if os.path.isfile(image_path):
                #Check if the file is an 'Image'
                if file.lower().endswith(('.png', '.jpeg', '.jpg')):
                    processImage(image_path, image_output_path)

#Sets up the folder
root = tk.Tk()
root.withdraw()

Folder_Path = GetFolderPath()

Output_Path = GetFolderPath()

RecursiveImageProcessing(Folder_Path, Output_Path, ProcessShapes)

print(Folder_Path + "  -->  " + Output_Path)

print("Finished")
