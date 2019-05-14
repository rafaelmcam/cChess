import bpy
import mathutils
import numpy as np
import cv2
import pickle

# blender scene.blend -b -P script.py

path = ""

for i in range(5):

	img_name = f"{i}"

	arr = np.array([[b'r', b'n', b'b', b'q', b'k', b'b', b'n', b'r'],
		[b'p', b'p', b'p', b'p', b'p', b'p', b'p', b'p'],
		[b'_', b'_', b'_', b'_', b'_', b'_', b'_', b'_'],
		[b'_', b'_', b'_', b'_', b'_', b'_', b'_', b'_'],
		[b'_', b'_', b'_', b'_', b'_', b'_', b'_', b'_'],
		[b'_', b'_', b'_', b'_', b'_', b'_', b'_', b'_'],
		[b'P', b'P', b'P', b'P', b'P', b'P', b'P', b'P'],
		[b'R', b'N', b'B', b'Q', b'K', b'B', b'N', b'R']], dtype = np.object_)

	final = np.random.permutation(arr.ravel()).reshape(8, 8)

	dc = {}
	for peca, counts in zip(*np.unique(final, return_counts = True)):
		for i in range(counts):
			dc[peca.decode("utf-8") + f"{i}"] = np.argwhere(final == peca)[i]

	print(final)

	###


	bpy.data.scenes["Scene"].render.resolution_x = 1024
	bpy.data.scenes["Scene"].render.resolution_y = 1024

	camera = bpy.data.objects["Camera"]
	camera.location = mathutils.Vector((0., 0., 60.))
	camera.rotation_euler = mathutils.Vector((0., 0., -np.pi/2))


	for peca, pos in dc.items():
		if peca[0]!= "_":
			print(peca, pos)
			cube = bpy.data.objects[peca]
			cube.rotation_euler = mathutils.Vector((0., 0., 2 * np.pi * np.random.random()))
			if peca[0].islower():
				cube.location = mathutils.Vector((-21.0 + pos[0] * 6.0 - 0.3 + np.random.normal(0, 0.5), - 21.0 + pos[1] * 6.0 + 0.4 + np.random.normal(0, 0.5), 0.0))
			else:
				cube.location = mathutils.Vector((21.0 - pos[0] * 6.0 , 21.0 - pos[1] * 6.0 , 0.0))
			#cube.rotation_euler = mathutils.Vector((0., 0., 10 * np.random.random()))

	#cube = bpy.data.objects["P0"]
	#cube.location = mathutils.Vector((-21.0, -21.0, 10.0))

	for peca, pos in dc.items():
		if peca[0]!= "_":
			print(peca, pos)


	f = open(f"Dcs/{img_name}.pkl","wb")
	pickle.dump(dc,f)
	f.close()
	
	bpy.data.scenes['Scene'].render.filepath = f'Boards/{img_name}.jpg'
	bpy.ops.render.render( write_still=True ) 



#img = cv2.imread('/home/rcampello/Desktop/image.png', 0)
#print(img)
#print(img.shape)
#cv2.imshow("imagem", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# one blender unit in x-direction
#vec = mathutils.Vector((10.0, 0.0, 0.0))
#inv = cube.matrix_world.copy()
#inv.invert()
# vec aligned to local axis
#vec_rot = vec * inv
#cube.location = cube.location + vec_rot