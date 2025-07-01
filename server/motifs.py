import turtle
import tkinter as tk
from PIL import ImageGrab
import time

def generate_pattern_and_save(sides, depth, size, angle, color, filename="motif.png"):
    # Crée une fenêtre Tkinter
    root = tk.Tk()
    root.title("Générateur de motifs")
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()
    
    # Configure Turtle
    screen = turtle.TurtleScreen(canvas)
    t = turtle.RawTurtle(screen)
    t.hideturtle()
    t.speed(0)
    t.color(color)
    
    # Dessine le motif
    for _ in range(depth):
        for _ in range(sides):
            t.forward(size)
            t.right(360 / sides)
        t.right(angle)
        size *= 0.95
    
    # Met à jour la fenêtre
    root.update()
    time.sleep(0.5)  # Laisse le temps au rendu
    
    # Capture uniquement la zone du canvas
    x0 = root.winfo_rootx() + canvas.winfo_x()
    y0 = root.winfo_rooty() + canvas.winfo_y()
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()
    
    ImageGrab.grab().crop((x0, y0, x1, y1)).save(filename)
    root.destroy()
