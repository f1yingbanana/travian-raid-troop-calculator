import datamodels as dm
import mapgetter as mg
import math
import os

# Calculates ROI (return of investment) for each troop built, given the list of
# farms (oases).

# Prepopulate these in to skip options.
server = None # e.g. 'ts1.x1.america.travian.com'
jwt = None # find in your browser cookie
unit = None # look at constants in datamodels.py. E.g. dm.Troop.CLUBSWINGER
target_roi = None # return of investment in hours, e.g. 48
efficiency = None # how efficient you are at farming, from 0-1
location = None # location of your village

def calculate_roi_distance(unit, target_roi, efficiency):
  """
  When we fix ROI, we can calculate the maximum distance the unit can travel to
  make that ROI from how fast is the unit and how many trips it must make to
  gather its production cost.
  """
  return efficiency * target_roi * unit.speed * unit.carrying_capacity / (2 * unit.cost + 2 * target_roi * unit.upkeep)


def calculate_units(farm_map, unit, target_roi, efficiency, include_research):
  """
  Each farm can support a finite number of units per hour, determined by the
  unit's carrying capacity and the farm's production. The further a farm is, the
  larger is its ROI. We calculate the number of units required to saturate all
  farms up to the distance determined by the ROI.
  """
  units_to_build = 0
  farm_rate = 0
  roi_distance = calculate_roi_distance(unit, target_roi, efficiency)

  for farm in farm_map.farms:
    farm_distance = math.dist(farm.location, farm_map.self_location)
    if farm_distance <= roi_distance:
      capacity = 2 * farm.production * farm_distance / (unit.speed * unit.carrying_capacity)
      units_to_build += capacity
      farm_rate += farm.production * efficiency

  print(f'Given your efficiency is {efficiency}, to reach a target ROI of {target_roi}h, you should build {math.ceil(units_to_build)} units and farm within {round(roi_distance, 2)} of your village {farm_map.self_location}.')
  print(f'Your projected farm rate is {round(farm_rate, 2)}/h.')

  # Now we calculate how long it takes for the above units to farm reserach cost
  if include_research and unit.research_cost > 0:
    research_time = unit.research_cost / farm_rate
    print(f'Research costs {round(research_time, 2)} additional farm hours.')


def run_calculator(unit, target_roi, efficiency, location, server, jwt):
  if unit == None:
    units = [
      dm.Troop.LEGIONNAIRE,
      dm.Troop.EQUITES_IMPERATORIS,
      dm.Troop.CLUBSWINGER,
      dm.Troop.PHALANX,
      dm.Troop.THEUTATES_THUNDER
    ]
    unit = units[int(input('Farm unit is (enter number):\n(0) Legionnaire\n(1) Equites Imperatoris\n(2) Clubswinger\n(3) Phalanx\n(4) Theutates Thunder\n'))]
  if target_roi == None:
    target_roi = max(1, float(input('Enter your desired ROI (return on investment) in hours:\n')))
  if efficiency == None:
    efficiency = max(0.01, min(1, float(input('Enter your farming efficiency from 0-1, with 0 being getting no farm and 1 being resources never overflow in oases and no one else farms them:\n'))))
  distance = calculate_roi_distance(unit, target_roi, efficiency)
  if location == None:
    location = tuple(map(int, input('Enter your village location (e.g. 23, 45):\n').split(',')))
  if server == None:
    server = input('Enter your server (e.g. ts1.x1.america.travian.com):\n')
  if jwt == None:
    jwt = input('Enter your JWT (found in browser cookies):\n')

  TEMP_FOLDER = 'temp'
  if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)
  farms = mg.get_map_circle(server, jwt, TEMP_FOLDER, location, distance)
  farm_map = dm.Map(farms, location)
  farm_map.print_stats()
  calculate_units(farm_map, unit, target_roi, efficiency, True)


if __name__ == '__main__':
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  run_calculator(unit, target_roi, efficiency, location, server, jwt)
