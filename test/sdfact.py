from fury import actor, window

#Basic script to render SDF actor

scene = window.Scene()
scene.background((1.0, 0.8, 0.8))
center=([5, 0, 0])
sdfactor = actor.sdf(center = center)
scene.add(sdfactor)

scene.add(actor.axes())
window.show(scene, size=(1920,1080))
