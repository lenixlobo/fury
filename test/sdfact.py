from fury import actor, window
import numpy as np
#Basic script to render SDF actor

scene = window.Scene()
scene.background((1.0, 0.8, 0.8))
dirs = np.random.rand(7, 3)
#centers = np.random.rand(7,3)
colors = np.random.rand(7,3) * 255
centers = np.array([[2, 0, 0], [0, 0, 0], [-2, 0, 0], [0, 2, 0],[0, -2, 0],[0, 0, -2],[0, 0, 2]])
sdfactor = actor.sdf(centers = centers, directions = dirs,colors = colors)
scene.add(sdfactor)

scene.add(actor.axes())
window.show(scene, size=(1920,1080))
