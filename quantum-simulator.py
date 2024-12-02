import tkinter as tk
from tkinter import Canvas, Button, Label, Scale, Frame, LEFT, RIGHT, TOP, BOTTOM
import numpy as np
import math
import random
import time

class QuantumPoint:
    def __init__(self, x, y, angle, radius, channel):
        self.x = x
        self.y = y
        self.angle = angle
        self.radius = radius
        self.channel = channel
        self.energy = 1.0

class QuantumPacket:
    def __init__(self, channel, packet_type, progress=0):
        self.channel = channel
        self.type = packet_type  # 'original' or 'reconstructed'
        self.progress = progress
        self.energy = random.random() * 0.3 + 0.7
        self.id = time.time() + random.random()
    
    def update(self, delta_time):
        self.progress += delta_time * 0.02
        return self.progress <= 1

class QuantumCore:
    def __init__(self):
        self.rotation = 0
        self.energy_level = 0.5
        self.packets = []
        self.spiral_points = self.generate_spiral_points(24)
    
    def generate_spiral_points(self, count):
        points = []
        for i in range(count):
            angle = (i / count) * math.pi * 8
            radius = 48 - (i / count) * 40
            x = 50 + math.cos(angle) * radius
            y = 50 + math.sin(angle) * radius
            points.append(QuantumPoint(x, y, angle, radius, i % 4))
        return points
    
    def update(self, delta_time):
        # Update core rotation
        self.rotation = (self.rotation + delta_time * 2) % 360
        
        # Update energy level with quantum oscillation
        self.energy_level += math.sin(time.time()) * 0.1 * delta_time
        self.energy_level = max(0, min(1, self.energy_level))
        
        # Generate new packets
        if random.random() > 0.6:
            channel = random.randint(0, 3)
            pair_offset = random.random() * 0.1
            
            self.packets.append(QuantumPacket(channel, 'original'))
            self.packets.append(QuantumPacket(channel, 'reconstructed', pair_offset))
        
        # Update existing packets
        self.packets = [p for p in self.packets if p.update(delta_time)]
        
        return self.get_state()
    
    def get_state(self):
        return {
            'rotation': self.rotation,
            'energy_level': self.energy_level,
            'packet_count': len(self.packets),
            'packets': [{
                'x': self.spiral_points[int(p.progress * (len(self.spiral_points) - 1))].x,
                'y': self.spiral_points[int(p.progress * (len(self.spiral_points) - 1))].y,
                'channel': p.channel,
                'type': p.type,
                'energy': p.energy
            } for p in self.packets]
        }

class QuantumTrainingEnvironment(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quantum Training Environment")
        self.quantum_size = 400
        self.mode = 'sandplot'
        self.is_training = False
        self.iteration = 0
        self.quantum_core = QuantumCore()
        
        self.initialize_ui()
        self.bind_events()
        
        # Add color mappings for quantum visualization
        self.channel_colors = [
            '#06B6D4',  # cyan
            '#10B981',  # green
            '#6366F1',  # indigo
            '#EC4899'   # pink
        ]
    
    def initialize_ui(self):
        main_frame = Frame(self)
        main_frame.pack(padx=10, pady=10)
        
        # Control frame
        control_frame = Frame(main_frame)
        control_frame.pack(side=TOP, fill=tk.X, padx=5, pady=5)
        
        self.train_button = Button(control_frame, text="Start Training", command=self.toggle_training)
        self.train_button.pack(side=LEFT)
        
        self.mode_button = Button(control_frame, text=f"Mode: {self.mode}", command=self.toggle_mode)
        self.mode_button.pack(side=LEFT)
        
        self.iteration_label = Label(control_frame, text=f"Iteration: {self.iteration}")
        self.iteration_label.pack(side=RIGHT)
        
        # Quantum visualization canvas
        self.quantum_canvas = Canvas(main_frame, width=self.quantum_size, height=self.quantum_size, bg='#111827')
        self.quantum_canvas.pack(side=TOP, padx=5, pady=5)
    
    def bind_events(self):
        self.train_button.configure(command=self.toggle_training)
        self.mode_button.configure(command=self.toggle_mode)
    
    def toggle_training(self):
        self.is_training = not self.is_training
        if self.is_training:
            self.train_button.config(text="Stop Training")
            self.training_loop()
        else:
            self.train_button.config(text="Start Training")
    
    def toggle_mode(self):
        self.mode = 'mnist' if self.mode == 'sandplot' else 'sandplot'
        self.mode_button.config(text=f"Mode: {self.mode}")
    
    def training_loop(self):
        if self.is_training:
            self.iteration += 1
            self.iteration_label.config(text=f"Iteration: {self.iteration}")
            
            # Update quantum simulation
            state = self.quantum_core.update(0.1)
            self.render_quantum_state(state)
            
            self.after(50, self.training_loop)
    
    def render_quantum_state(self, state):
        self.quantum_canvas.delete("all")
        
        # Draw quantum field layers
        center_x = self.quantum_size / 2
        center_y = self.quantum_size / 2
        
        # Draw background circles
        for i, color in enumerate(['#06B6D4', '#10B981', '#6366F1']):
            radius = (self.quantum_size * 0.45) - (i * 20)
            self.quantum_canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=color, width=2, fill='', stipple='gray50'
            )
        
        # Draw spiral paths
        for channel in range(4):
            points = []
            for point in self.quantum_core.spiral_points:
                if point.channel == channel:
                    x = center_x + (point.x - 50) * self.quantum_size / 100
                    y = center_y + (point.y - 50) * self.quantum_size / 100
                    points.extend([x, y])
            
            if points:
                self.quantum_canvas.create_line(
                    points, 
                    fill=self.channel_colors[channel], 
                    width=1, 
                    stipple='gray50'
                )
        
        # Draw packets
        for packet in state['packets']:
            x = center_x + (packet['x'] - 50) * self.quantum_size / 100
            y = center_y + (packet['y'] - 50) * self.quantum_size / 100
            color = self.channel_colors[packet['channel']]
            
            # Draw packet with glow effect
            size = 6 if packet['type'] == 'original' else 4
            for i in range(3):
                self.quantum_canvas.create_oval(
                    x - size - i*2, y - size - i*2,
                    x + size + i*2, y + size + i*2,
                    fill=color if i == 0 else '',
                    outline=color,
                    stipple='gray50' if i > 0 else ''
                )
        
        # Draw quantum core
        core_size = 30
        rotation = state['rotation']
        
        # Core layers
        for i, color in enumerate(['#06B6D4', '#10B981', '#6366F1', '#FFFFFF']):
            size = core_size - (i * 6)
            x0 = center_x - size
            y0 = center_y - size
            x1 = center_x + size
            y1 = center_y + size
            
            # Rotate the core elements
            self.quantum_canvas.create_oval(
                x0, y0, x1, y1,
                fill=color, stipple='gray50'
            )
        
        # Update the display
        self.update_idletasks()

if __name__ == "__main__":
    app = QuantumTrainingEnvironment()
    app.mainloop()