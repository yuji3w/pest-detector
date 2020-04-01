import cv2
import numpy as np

''' Returns color IMG broken into BLOCK_DIMS[0]xBLOCK_DIMS[1] 
    sub-rectangles as 5-dimensional array of NEW_X, NEW_Y, X,
    Y, CHANNEL. '''
def partition_image(img, block_dims = (4,4)):
  if (len(img.shape) == 2):
    return partition_gray(img, block_dims)
  x_len, y_len, channels = img.shape
  x_block, y_block = block_dims
  blocks = []
  for x in range(0, x_len - x_len % x_block, x_block):
    blocks.append([])
    for y in range(0, y_len - y_len % y_block, y_block):
      blocks[x // x_block].append(
        img[x : x + x_block, y : y + y_block, :])
  # todo: integrate np for speedup
  return blocks

''' Returns cv2 grayscale IMG broken into BLOCK_DIMS[0]x
    BLOCK_DIMS[1] sub-rectangles as 4-dimensional array 
    of NEW_X, NEW_Y, X, Y. '''
def partition_gray(img, block_dims = (4,4)):
  x_len, y_len = img.shape
  x_block, y_block = block_dims
  blocks = []
  for x in range(0, x_len - x_len % x_block, x_block):
    blocks.append([])
    for y in range(0, y_len - y_len % y_block, y_block):
      blocks[x // x_block].append(
        img[x : x + x_block, y : y + y_block])
  # todo: integrate np for speedup
  return blocks

''' Yields 4^depth color sub-IMG, in up-down, 
    left-right order.'''
def quadtree_split(img, depth = 1):
  assert depth >= 0, 'invalid args'
  assert hasattr(img, 'shape'), 'invalid'
  if(len(img.shape) == 2):
    yield from gray_quadtree_split(img, depth)
    return
  if (depth == 0):
    yield img
  else:
    y1x1 = quadtree_split(image_quarter(img, 0), depth - 1)
    y2x1 = quadtree_split(image_quarter(img, 1), depth - 1)
    for y in range(0, 2 ** (depth - 1)):
      yield from yield_until(y1x1, 2 ** (depth - 1))
      yield from yield_until(y2x1, 2 ** (depth - 1))
    y1x2 = quadtree_split(image_quarter(img, 2), depth - 1)
    y2x2 = quadtree_split(image_quarter(img, 3), depth - 1)
    for y in range(0, 2 ** (depth - 1)):
      yield from yield_until(y1x2, 2 ** (depth - 1))
      yield from yield_until(y2x2, 2 ** (depth - 1))

''' Returns a quarter of IMG up-down, left-right'''
def image_quarter(img, number):
  x_len, y_len, channels = img.shape
  if (number == 0):
    return img[0 : x_len // 2, 0 : y_len // 2, :]
  elif (number == 1):
    return img[x_len // 2 : x_len - x_len % 2, 
    0 : y_len // 2, :]
  elif (number == 2):
    return img[0 : x_len // 2, y_len // 2 :
    y_len - y_len % 2, :]
  else:
    return img[x_len // 2 : x_len - x_len % 2,
    y_len // 2 : y_len - y_len % 2, :]

''' Yield from ITER LIMIT times. '''
def yield_until(iter, limit):
  for i in range(limit):
    yield next(iter)