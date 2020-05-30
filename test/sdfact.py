from fury import actor, window

scene = window.Scene()
center=([5, 0, 0])
sdfactor = actor.sdf(center = center)
scene.add(sdfactor)

window.show(scene)
