import cv2
import datamodels as dm
import numpy as np
import os

OASIS_ICONS_PATH = 'oasis-icons'

def parse_map(filepath, size, bottom_left_location):
  """
  Parses a Travian map block located at the given filepath for oases using CV.

  filepath: the string containing the path to the map image
  size: an int tuple of the grid size shown in the map, e.g. (20, 20)
  bottom_left_location: an int tuple of the location of the bottom-left grid
  """
  map_image = cv2.imread(filepath)

  if map_image is None:
    print('Bad map image, refresh your JWT cookie.')
    return []

  threshold = .8
  h, w, c = map_image.shape
  oases = []

  for template_path in os.listdir(OASIS_ICONS_PATH):
    path = f'{OASIS_ICONS_PATH}/{template_path}'
    oasis_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    template = oasis_image[:,:,:3]
    mask = oasis_image[:,:,3]
    result = cv2.matchTemplate(map_image, template, cv2.TM_CCOEFF_NORMED, None, mask)
    locations = np.where(result >= threshold)

    for x, y in zip(*locations[::-1]):
      # Some values can be out of range. We skip these.
      if result[y, x] > 1 or result[y, x] < 0:
        continue

      # Flip y coordinate as image y-axis is inverted.
      cx = int(bottom_left_location[0] + x // (w / size[0]))
      cy = int(bottom_left_location[1] + (h - y) // (h / size[1]))

      oasis_type = 0
      if template_path =='lumber.png':
        oasis_type = dm.Oasis.LUMBER
      elif template_path =='lumber-crop.png':
        oasis_type = dm.Oasis.LUMBER_CROP
      elif template_path =='lumber-lumber.png':
        oasis_type = dm.Oasis.LUMBER_LUMBER
      elif template_path =='clay.png':
        oasis_type = dm.Oasis.CLAY
      elif template_path =='clay-crop.png':
        oasis_type = dm.Oasis.CLAY_CROP
      elif template_path =='clay-clay.png':
        oasis_type = dm.Oasis.CLAY_CLAY
      elif template_path =='iron.png':
        oasis_type = dm.Oasis.IRON
      elif template_path =='iron-crop.png':
        oasis_type = dm.Oasis.IRON_CROP
      elif template_path =='iron-iron.png':
        oasis_type = dm.Oasis.IRON_IRON
      elif template_path =='crop.png':
        oasis_type = dm.Oasis.CROP
      elif template_path =='crop-crop.png':
        oasis_type = dm.Oasis.CROP_CROP

      oases.append(dm.Oasis((cx, cy), oasis_type))

  return oases
