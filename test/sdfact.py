from fury import actor, window

scene = window.Scene()
center=([5, 0, 0])
sdfactor = actor.sdf(center = center)
scene.add(sdfactor)

scene.add(actor.axes())
window.show(scene, size=(1920,1080))
