import sys
import json
import turtle
from PIL import Image
import io
import time

def main():
    # Lire les paramètres
    with open(sys.argv[1], 'r') as f:
        params = json.load(f)

    # Configuration Turtle (fenêtre minuscule et hors écran)
    screen = turtle.Screen()
    screen.setup(width=1, height=1, startx=-2000, starty=-2000)  # Place la fenêtre hors de l'écran
    screen.bgcolor("white")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color(params["color"])

    # Paramètres
    sides = params["sides"]
    depth = params["depth"]
    size = params["size"]
    angle = params["angle"]

    # Génération du motif
    for _ in range(depth):
        for _ in range(sides):
            t.forward(size)
            t.right(360 / sides)
        t.right(angle)
        size *= 0.95

    # Rendu final
    screen.update()
    time.sleep(0.2)  # Court délai pour assurer le rendu

    # Capture du canvas
    canvas = screen.getcanvas()
    ps_data = canvas.postscript(colormode='color')

    # Conversion en PNG
    img = Image.open(io.BytesIO(ps_data.encode('utf-8')))
    img.save('output.png', 'PNG')

    # Fermeture propre
    screen.bye()

if __name__ == "__main__":
    main()
