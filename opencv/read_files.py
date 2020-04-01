import os
import glob
import cv2
from tools import quadtree_split


def generate_images(folder_name, file_extension):
	image_paths = map(os.path.abspath, glob.glob(f'./{folder_name}/*.{file_extension}'))
	yield from map(cv2.imread, image_paths)

def display_image(image, window_name = 'image'):
	cv2.imshow(window_name, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	image_iterator = generate_images('images', 'jpg')
	quad_iterator = quadtree_split(next(image_iterator), 3)
	for image_no, image in enumerate(quad_iterator):
		cv2.imwrite(f'sample{image_no}.jpg', image)

	#list(map(lambda image: display_image(image, 'image'), generate_images('images', 'jpg')))