import os
import glob
import cv2
from tools import *

def generate_images(folder_name, file_extension):
	image_paths = map(os.path.abspath, glob.glob(f'./{folder_name}/*.{file_extension}'))
	yield from map(cv2.imread, image_paths)

def display_image(image, window_name = 'image'):
	cv2.imshow(window_name, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	image_iterator = generate_images('images', 'jpeg')
	only_image = next(image_iterator)
	filtered_image = frame_hue_bounded(only_image)
	cv2.imwrite('filtered.jpg', filtered_image)
	filtered_black_image = frame_hue_bounded(only_image,
		np.array([0, 5, 50]), np.array([179, 50, 255]))
	contoured = draw_contours(filtered_black_image)
	cv2.imwrite('contoured.jpg', contoured)

if __name__ == '__main__':
	image_iterator = generate_images('images', 'jpg')
	only_image = next(image_iterator)
	filtered_image = frame_hue_bounded(only_image)
	cv2.imwrite('filtered.jpg', filtered_image)
	corners = detect_corners(filtered_image)
	roi = transform_frame(only_image, corners)
	cv2.imwrite('only_flypaper.jpg', roi)
	roi_detected_black = frame_hue_bounded(roi,
		np.array([0, 5, 50]), np.array([179, 50, 255]))
	cv2.imwrite('black_roi.jpg', roi_detected_black)
	blurred_roi = kernel_blur(roi)