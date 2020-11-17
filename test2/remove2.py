import os
import time
import glob
import re

current_time = time.time()

numbers = re.compile(r'(\d+)')

def numericalSort(value):
	parts = numbers.split(value)
	parts[1::2] = map(int, parts[1::2])
	return parts

def remove():
	while True:
		path = '/home/mooc/image2/*.jpg'
		path_name = '/home/mooc/image2/'
		for f in sorted(glob.glob(os.path.join(path)), key = numericalSort):
			creation_time = os.path.getctime(f)
			if (current_time - creation_time) // 1 >= 1:
				os.unlink(f)
				time.sleep(0.4)
				print('{} remove'.format(f))
		if len(os.listdir(path_name)) == 0:
			print('the directory is empty')
			break
		else:
			continue

if __name__ == '__main__':
	remove()
