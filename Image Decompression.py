import sys
import os.path
#import cv2
import numpy as np
from skimage import io
#import matplotlib.pyplot as plt

if __name__ == "__main__":
	try:
		name, = [x for x in input().split()]
		if (os.path.isfile(name)):
			#opencv reads images in bgr format
			#c = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
			c = io.imread(name, as_gray=True)
		else:
			raise FileNotFoundError
	except ValueError:
		print("Enter _clusters path as 'xyz.png'")
		sys.exit(1)
	except FileNotFoundError:
		print("FileNotFoundError : '" + name + "' was not found!")
		sys.exit(1)
	
	#convert bgr to rgb image
	#c = c[...,::-1]

	basename = name[:name.rfind('_')]
	try:
		μ = np.load(basename + '_means.npy')
	except IOError:
		print("_means should be in the same directory as _clusters!")
		sys.exit(1)
	except ValueError:
		print("the _means file was corrupt!")
		sys.exit(1)
	m, n, p = c.shape[0], c.shape[1], μ.shape[1]
	c = c.reshape((m * n,))
	x = np.ones((m * n, p), dtype=np.uint8)

	for i in range(x.shape[0]):
		x[i] = μ[int(c[i])]
	recovered_img = x.reshape(m, n, p)

	#cv2.imwrite(basename + '_decompressed.png', recovered_img)
	io.imsave(basename + '_decompressed.png', recovered_img)
	#plt.imsave('test_decompressed.png', recovered_img)
