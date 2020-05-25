from fury import window, actor
import numpy as np
scene = window.Scene()
centers = np.random.rand(3, 3) * 10
directions = np.random.rand(3, 3)
scale = np.random.rand(5)
roundness = np.array([[1, 1], [1, 2], [2, 1]])
sq_actor = actor.superquadric(centers, roundness=roundness,
                              directions=directions,
                               scale=scale)
scene.add(sq_actor)
# window.show(scene)