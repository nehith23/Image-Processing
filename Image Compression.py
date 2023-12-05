import sys
import time
import os.path
import itertools
import threading
#import cv2
import numpy as np
from skimage import io
#import matplotlib.pyplot as plt

def assignCentroids(x, μ):
	m = x.shape[0]
	c = np.zeros((m,), dtype=np.uint8)
	k = μ.shape[0]
	for i in range(m):
		min_dist = 1000000
		for j in range(k):
			dist = np.linalg.norm(x[i] - μ[j])
			if (dist < min_dist):
				min_dist = dist
				c[i] = j
	return c

def moveCentroids(x, c, k):
	m = x.shape[0]
	n = x.shape[1]
	μ = np.zeros((k, n))
	for i in range(k):
		tmp = np.array([x[ci] for ci in range(m) if c[ci] == i])
		if (tmp.shape[0] == 0):
			continue
		μ[i] = (tmp.sum(axis=0)) / np.float64(tmp.shape[0])
	return μ

def randomInit(x, k):
	tmp = np.copy(x)
	np.random.shuffle(tmp)
	μ = tmp[:k,:]
	return μ

def formClusters(x, k, max_iters):
	μ = randomInit(x, k)
	for i in range(max_iters):
		c = assignCentroids(x, μ)
		μ = moveCentroids(x, c, k)
	return μ, c

def compress():
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.write('\rrunning k-means ' + c)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rDone!     ')

if __name__ == '__main__':
	try:
		name, n_c = [x for x in input().split()]
		if (os.path.isfile(name)):
			rgb = io.imread(name)
		else:
			raise FileNotFoundError
	except ValueError:
		print("Enter image path and color clusters as 'xyz.png 16'")
		sys.exit(1)
	except FileNotFoundError:
		print("FileNotFoundError : '" + name + "' was not found!")
		sys.exit(1)

	tmp = rgb
	m, n, p = tmp.shape[0], tmp.shape[1], tmp.shape[2]
	x = tmp.reshape((m * n, p))
	done = False
	print('')
	print('This may take a while...Please be patient')
	t = threading.Thread(target=compress)
	t.start()
	μ, c = formClusters(x, int(n_c), 10)
	done = True

	c = c.reshape((m, n))
	#plt.imsave('test_clusters.png', c)
	basename = name[:name.rfind('.')]
	#cv2.imwrite(basename + '_clusters.jpg', c)
	io.imsave(basename + '_clusters.png', c); 
	np.save(basename + '_means.npy', μ) 
	#plt.imshow(recovered_img)
	#plt.show()

