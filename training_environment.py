import tkinter as tk
from tkinter import Canvas, Button, Label, Scale, Frame, LEFT, RIGHT, TOP, BOTTOM
import numpy as np
from PIL import Image, ImageTk
from data_generator import DataGenerator

class TrainingEnvironment(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Training Environment")
        self.seed = 1337
        self.image_size = 256
        self.mode = 'sandplot'
        self.is_training = False
        self.iteration = 0
        self.canvases = []  # List to hold canvas widgets
        
        self.initialize_ui()
        self.bind_events()
        self.generate_images()

    def initialize_ui(self):
        main_frame = Frame(self)
        main_frame.pack(padx=10, pady=10)
        
        control_frame = Frame(main_frame)
        control_frame.pack(side=TOP, fill=tk.X, padx=5, pady=5)
        
        self.train_button = Button(control_frame, text="Start Training", command=self.toggle_training)
        self.train_button.pack(side=LEFT)
        
        self.mode_button = Button(control_frame, text=f"Mode: {self.mode}", command=self.toggle_mode)
        self.mode_button.pack(side=LEFT)
        
        self.size_scale = Scale(control_frame, from_=28, to=512, resolution=4, orient=tk.HORIZONTAL, label="Image Size", command=self.update_image_size)
        self.size_scale.set(self.image_size)
        self.size_scale.pack(side=LEFT)
        
        self.iteration_label = Label(control_frame, text=f"Iteration: {self.iteration}")
        self.iteration_label.pack(side=RIGHT)
        
        canvas_frame = Frame(main_frame)
        canvas_frame.pack(side=BOTTOM, padx=5, pady=5)
        
        for _ in range(4):
            original_canvas = Canvas(canvas_frame, width=self.image_size, height=self.image_size)
            original_canvas.grid(row=_//2, column=_%2)
            self.canvases.append(original_canvas)
    
    def bind_events(self):
        self.train_button.configure(command=self.toggle_training)
        self.mode_button.configure(command=self.toggle_mode)
        self.size_scale.configure(command=self.update_image_size)

    def toggle_training(self):
        self.is_training = not self.is_training
        if self.is_training:
            self.train_button.config(text="Stop Training")
            self.after(100, self.training_loop)  # Start the training loop
        else:
            self.train_button.config(text="Start Training")

    def toggle_mode(self):
        self.mode = 'mnist' if self.mode == 'sandplot' else 'sandplot'
        self.mode_button.config(text=f"Mode: {self.mode}")
        self.generate_images()

    def update_image_size(self, value):
        self.image_size = int(value)
        self.generate_images()

    def training_loop(self):
        if self.is_training:
            self.seed += 1
            self.iteration += 1
            self.iteration_label.config(text=f"Iteration: {self.iteration}")
            self.generate_images()
            self.after(100, self.training_loop)  # Schedule the next iteration

    def render_to_canvas(self, canvas, image_data, size):
        # Convert flat list to 2D array
        pixels = [image_data[i:i+3] for i in range(0, len(image_data), 3)]
        image = Image.new("RGB", (size, size))
        image.putdata(pixels)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        canvas.image = photo  # Keep a reference to prevent garbage collection

    def generate_images(self):
        generator = DataGenerator(self.seed)
        for canvas in self.canvases:
            data = generator.generate_sand_plot(self.image_size) if self.mode == 'sandplot' else generator.generate_mnist_data(self.image_size)
            image_data = generator.data_to_image_data(data, self.image_size)
            self.render_to_canvas(canvas, image_data, self.image_size)

if __name__ == "__main__":
    app = TrainingEnvironment()
    app.mainloop()