import bpy
import mathutils
import numpy as np
import cv2
import pickle
import time
import chess
# blender scene.blend -b -P script.py


_fen = "rnbqk2r/1p2bppp/p2ppn2/8/3NP3/P1NB4/1PP2PPP/R1BQ1RK1 b kq - 0 8"
board = chess.Board(fen = _fen)

def converte_notacao_xadrez_afonso(square_number):
    return (63 - square_number)//8, 7 - (63 - square_number)%8


def generate_matrix_board(board):
    tabuleiro = np.array([(converte_notacao_xadrez_afonso(i), x.symbol()) for i, x in board.piece_map().items()])
    matrix = np.chararray((8, 8))
    matrix[:] = "_"

    for i, x in tabuleiro:
        matrix[i[0], i[1]] = x
    return matrix

matrix = generate_matrix_board(board)

dc = {}

for peca, counts in zip(*np.unique(matrix, return_counts = True)):
    for i in range(counts):
        dc[peca.decode("utf-8") + f"{i}"] = np.argwhere(matrix == peca)[i]


path = ""


begin_time = time.time()
for i in range(1):

	img_name = f"{i}_from_FEN"


	###


	bpy.data.scenes["Scene"].render.resolution_x = 1024
	bpy.data.scenes["Scene"].render.resolution_y = 1024

	camera = bpy.data.objects["Camera"]
	camera.location = mathutils.Vector((0., 0., 60.))
	camera.rotation_euler = mathutils.Vector((0., 0., -np.pi/2))

	sun = bpy.data.objects["Empty"]
	sun.rotation_euler = mathutils.Vector((0., 0., 2 * np.pi * np.random.random()))


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


	#f = open(f"Dcs/{img_name}.pkl","wb")
	#pickle.dump(dc,f)
	#f.close()
	
	bpy.data.scenes['Scene'].render.filepath = f'{img_name}.jpg'
	bpy.ops.render.render( write_still=True ) 

print(f"Levou: {time.time() - begin_time}")

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