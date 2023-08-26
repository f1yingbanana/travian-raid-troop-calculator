import mapparser
import math
import os
import requests

BLOCK_SIZE = 10 # this can either be 10 or 20, depending on the oasis-images

def get_map_block(server, jwt, folder, block):
  """
  Travian stores maps in pre-rendered blocks. This script grabs a single block
  and store it to a folder.

  server: the server that we are grabbing from. E.g. ts2.x1.america.travian.com
  jwt: the JWT found in the cookie after login
  folder: the output folder
  block: which block to get, e.g. (20, 30)
  """
  print(f'Processing block {block}...')

  i = block[0] // BLOCK_SIZE * BLOCK_SIZE
  j = block[1] // BLOCK_SIZE * BLOCK_SIZE

  cookies = {'JWT': jwt}
  filename = f'{i}.{j}.{i + BLOCK_SIZE - 1}.{j + BLOCK_SIZE - 1}.png'
  path = f'https://{server}/map/block/{filename}'
  response = requests.get(path, cookies=cookies, stream=True)

  if response.status_code == 200:
    map_path = f'{folder}/{filename}'
    with open(map_path, 'wb') as file:
      for chunk in response.iter_content(chunk_size=1024):
        file.write(chunk)
    return mapparser.parse_map(map_path, (BLOCK_SIZE, BLOCK_SIZE), (i, j))
  else:
    print(f'Bad server response: {response.status_code}')
    return []


def get_map_circle(server, jwt, folder, center, radius):
  """
  Travian stores maps in pre-rendered blocks. This script grabs all of these
  blocks and store these to a folder.

  server: the server that we are grabbing from. E.g. ts2.x1.america.travian.com
  jwt: the JWT found in the cookie after login
  folder: the output folder
  center: the center of the circle of blocks to get
  radius: the radius of the circle of blocks to get, inclusive
  """
  farms = []
  for i in range(-200, 200, BLOCK_SIZE):
    if i + BLOCK_SIZE - 1 < center[0] - radius or i > center[0] + radius:
      continue
    for j in range(-200, 200, 10):
      if j + BLOCK_SIZE - 1 < center[1] - radius or j > center[1] + radius:
        continue
      if math.dist((i + BLOCK_SIZE / 2, j + BLOCK_SIZE / 2), center) > radius + BLOCK_SIZE:
        continue
      farms += get_map_block(server, jwt, folder, (i, j))
  return farms
