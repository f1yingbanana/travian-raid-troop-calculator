import math

class Farm:
  def __init__(self, location, production):
    """
    Initializes a Farm with the given location and production.

    location: an int tuple, e.g. (12, 34)
    production: The resource production per hour, e.g. 70
    """
    self.location = location
    self.production = production


class Oasis(Farm):
  LUMBER = 71
  LUMBER_CROP = 101
  LUMBER_LUMBER = 111
  CLAY = 71
  CLAY_CROP = 101
  CLAY_CLAY = 111
  IRON = 71
  IRON_CROP = 101
  IRON_IRON = 111
  CROP = 71
  CROP_CROP = 111

  def __init__(self, location, type):
    """
    Initializes an oasis at the given location.

    location: an int tuple, e.g. (12, 34)
    type: The type of the oasis, see constants in the class
    """
    Farm.__init__(self, location, type)


class Troop:
  def __init__(self, speed, carrying_capacity, cost, upkeep, research_cost):
    """
    Initializes a troop.
    """
    self.speed = speed
    self.carrying_capacity = carrying_capacity
    self.cost = cost
    self.upkeep = upkeep
    self.research_cost = research_cost


Troop.LEGIONNAIRE = Troop(6, 50, 400, 1, 0)
Troop.EQUITES_IMPERATORIS = Troop(14, 100, 1410, 3, 8780)
Troop.CLUBSWINGER = Troop(7, 60, 250, 1, 0)
Troop.PHALANX = Troop(7, 35, 315, 1, 0)
Troop.THEUTATES_THUNDER = Troop(19, 75, 1090, 2, 6660)


class Map:
  def __init__(self, farms, self_location):
    """
    Initializes a map containing farms and our own location.

    farms: a list of Farm objects
    self_location: an int tuple, e.g. (12, 34)
    """
    self.farms = farms
    self.self_location = self_location


  def print_stats(self):
    """
    Prints stats about the farms around self.
    """
    sorted_farms = sorted(self.farms, key=lambda farm: math.dist(farm.location, self.self_location))
    current_distance = 0
    current_production = 0
    current_count = 0
    BUCKET = 5
    for farm in sorted_farms:
      distance = math.dist(farm.location, self.self_location)
      if distance < current_distance + BUCKET:
        current_production += farm.production
        current_count += 1
      else:
        if current_count > 0:
          print(f'{current_count} oases within {current_distance}-{current_distance + BUCKET}, maximum farm {current_production}/h.')
        current_distance += BUCKET
        current_count = 0
        current_production = 0
