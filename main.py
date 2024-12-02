import tkinter as tk
from tkinter import Canvas, Button, Label, Scale, Frame, LEFT, RIGHT, TOP, BOTTOM
import numpy as np
import random

class DataGenerator:
    def __init__(self, seed):
        random.seed(seed)
    
    def generateSandPlot(self, size):
        # Simple sand plot generation
        data = np.random.rand(size, size)
        return data
    
    def generateMNISTData(self, size):
        # Placeholder for MNIST-like data
        data = np.zeros((size, size))
        # Add some random noise
        data += np.random.rand(size, size) * 0.1
        return data
    
    def dataToImageData(self, data, size):
        # Normalize data to 0-255
        img_data = (data * 255).astype(np.uint8).flatten()
        return img_data

class TrainingEnvironment(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Training Environment")
        self.seed = 1337
        self.imageSize = 256
        self.mode = 'sandplot'
        self.isTraining = False
        self.iteration = 0
        self.canvasRefs = [None] * 8  # References to canvas widgets
        
        self.initializeUI()
        self.bindEvents()
        self.generateImages()

    def initializeUI(self):
        main_frame = Frame(self)
        main_frame.pack(padx=10, pady=10)
        
        control_frame = Frame(main_frame)
        control_frame.pack(side=TOP, fill=tk.X, padx=5, pady=5)
        
        self.train_button = Button(control_frame, text="Start Training", command=self.toggleTraining)
        self.train_button.pack(side=LEFT)
        
        self.mode_button = Button(control_frame, text=f"Mode: {self.mode}", command=self.toggleMode)
        self.mode_button.pack(side=LEFT)
        
        self.size_scale = Scale(control_frame, from_=28, to=512, resolution=4, orient=tk.HORIZONTAL, label="Image Size", command=self.updateImageSize)
        self.size_scale.set(self.imageSize)
        self.size_scale.pack(side=LEFT)
        
        self.iteration_label = Label(control_frame, text=f"Iteration: {self.iteration}")
        self.iteration_label.pack(side=RIGHT)
        
        canvas_frame = Frame(main_frame)
        canvas_frame.pack(side=BOTTOM, padx=5, pady=5)
        
        for i in range(4):
            original_canvas = Canvas(canvas_frame, width=self.imageSize, height=self.imageSize, bg='gray')
            original_canvas.grid(row=i, column=0)
            self.canvasRefs[i*2] = original_canvas
            
            reconstructed_canvas = Canvas(canvas_frame, width=self.imageSize, height=self.imageSize, bg='gray')
            reconstructed_canvas.grid(row=i, column=1)
            self.canvasRefs[i*2 + 1] = reconstructed_canvas

    def bindEvents(self):
        self.train_button.configure(command=self.toggleTraining)
        self.mode_button.configure(command=self.toggleMode)
        self.size_scale.configure(command=self.updateImageSize)

    def toggleTraining(self):
        self.isTraining = not self.isTraining
        if self.isTraining:
            self.train_button.config(text="Stop Training")
            self.trainingLoop()
        else:
            self.train_button.config(text="Start Training")

    def toggleMode(self):
        self.mode = 'mnist' if self.mode == 'sandplot' else 'sandplot'
        self.mode_button.config(text=f"Mode: {self.mode}")
        self.generateImages()

    def updateImageSize(self, value):
        self.imageSize = int(value)
        self.generateImages()

    def trainingLoop(self):
        if self.isTraining:
            self.seed += 1
            self.iteration += 1
            self.iteration_label.config(text=f"Iteration: {self.iteration}")
            self.generateImages()
            self.after(100, self.trainingLoop)  # Adjust delay as needed

    def renderToCanvas(self, canvas, imageData, size):
        canvas.delete("all")
        for y in range(size):
            for x in range(size):
                color = "#{:02x}{:02x}{:02x}".format(imageData[y*size+x], imageData[y*size+x], imageData[y*size+x])
                canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline="")
    
    def generateImages(self):
        generator = DataGenerator(self.seed)
        for i, ref in enumerate(self.canvasRefs):
            if ref:
                data = generator.generateSandPlot(self.imageSize) if self.mode == 'sandplot' else generator.generateMNISTData(self.imageSize)
                imageData = generator.dataToImageData(data, self.imageSize)
                self.renderToCanvas(ref, imageData, self.imageSize)

if __name__ == "__main__":
    app = TrainingEnvironment()
    app.mainloop()