from fury import actor, window, ui
import numpy as np
import itertools


tb = ui.TextBlock2D(font_size=20, color=(1, 0.5, 1))
panel = ui.Panel2D(position=(400,400), size = (500, 150))
panel.add_element(tb, (0.2, 0.5))


scene = window.Scene()
scene.background((1.0, 0.8, 0.8))
# dirs = np.random.rand(7, 3)
# colors = np.random.rand(7, 3) * 255
# centers = np.array([[2, 0, 0], [0, 0, 0], [-2, 0, 0], [0, 2, 0], [0, -2, 0],
#                     [0, 0, -2], [0, 0, 2]])
centers = np.array([[0, 0, 0]])
sdfactor = actor.sdf_sh(centers=centers)

fpss = []

counter = itertools.count()
showm = window.ShowManager(scene, reset_camera=False )

showm.initialize()


scene.add(sdfactor)
scene.add(panel)


def timer_callback(_obj, _event):
	cnt = next(counter)
	showm.render()

	if cnt % 1 == 0:
		fps = scene.frame_rate
		fpss.append(fps)
		msg = "FPS: " + str(fps) 
		tb.message = msg
		
	if(cnt==2000):
		showm.exit()




showm.add_timer_callback(True, 10, timer_callback)
showm.start()
