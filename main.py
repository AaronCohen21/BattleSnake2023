# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import serealize
import math

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Aaron, Quinn, Jaden, and Scott",  # TODO: Your Battlesnake Username
        "color": "#864C00",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def print_array(arr):
  print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in arr]))

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

  def get_grid():
    # create empty 2d array
    grid = []
    grid = [[0 for i in range(game_state['board']['height'])] for i in range(game_state['board']['width'])]

    # fill grid with own snake data
    grid[game_state['you']['head']['x']][game_state['you']['head']['y']] = 1
    for tail in game_state['you']['body']:
      grid[tail['x']][tail['y']] = 1
    
    # fill grid with opponent snake data
    for snake in game_state['board']['snakes']:
      grid[snake['head']['x']][snake['head']['y']] = 1
      for tail in snake['body']:
        grid[tail['x']][tail['y']] = 1
    
    return grid

  # print_array(get_grid())
  # print("\n\n")

  is_move_safe = {
    "up": True, 
    "down": True, 
    "left": True, 
    "right": True
  }

  # We've included code to prevent your Battlesnake from moving backwards
  my_head = game_state["you"]["body"][0]  # Coordinates of your head
  my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

  if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
      is_move_safe["left"] = False

  elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
      is_move_safe["right"] = False

  elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
      is_move_safe["down"] = False

  elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
      is_move_safe["up"] = False

  # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

# Gets the loaction of the head x and y coordinates and compares it to the walls' max and min coordinates, assuming standard size 11x11 board. Height[0][11] and Width[0][11]
  
  if( my_head["y"] == board_height-1 ):
    # print(my_head["y"] +1)
    # print("Avoided roof")
    is_move_safe["up"] = False
  if(my_head["y"] -1 < 0):
    # print(my_head["y"] -1)
    # print("Avoided floor")
    is_move_safe["down"] = False
  if( my_head["x"] == board_width -1):
    # print(my_head["x"] -1)
    # print("Avoided right")
    is_move_safe["right"] = False
  if(my_head["x"] -1 < 0):
    # print(my_head["x"] -1)
    # print("Avoided left")
    is_move_safe["left"] = False

  # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
  def adjacent_coord(direction1, direction2="null", amount1=1, amount2=1):
    modification = [0,0]

    if (direction1 == "right"): modification[0] += amount1
    if (direction1 == "left"): modification[0] += -1*amount1
    if (direction1 == "up"): modification[1] += amount2
    if (direction1 == "down"): modification[1] += -1*amount2

    if (direction2 == "right"): modification[0] += amount1
    if (direction2 == "left"): modification[0] += -1*amount1
    if (direction2 == "up"): modification[1] += amount2
    if (direction2 == "down"): modification[1] += -1*amount2
    
    return {"x" : my_head["x"] + modification[0], "y" : my_head["y"] + modification[1]}

  
  def check_collision(snake, is_self):
    directions = {
      "up",
      "down",
      "left",
      "right"
    }
    
    # Head Collision
    if not is_self:
      for direction in directions:
        if adjacent_coord(direction) == snake['head']:
          is_move_safe[direction] = False
    
    # Body Collision (omitting  tail of self only)
    for idx in range(len(snake['body'])-(1 if is_self else 0)):
      snake_bit = snake['body'][idx]
      for direction in directions:
        if adjacent_coord(direction) == snake_bit:
          is_move_safe[direction] = False



  # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes 
  check_collision(game_state['you'], True)

  # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
  opponents = game_state['board']['snakes']
  for snake in opponents:
    check_collision(snake, False)

  # Snake logic (pseudo-safe squares)
  pseudo_safe_moves = {
    "up": is_move_safe["up"],
    "down": is_move_safe["down"],
    "left": is_move_safe["left"],
    "right": is_move_safe["right"]
  }

  for snake in opponents:
    my_length = len(game_state['you']['body']) + 1
    opp_length = len(snake['body']) + 1
    play_agro = my_length > opp_length
    
    # Case 1: Top Left
    if (is_move_safe["up"] and is_move_safe["right"] and adjacent_coord("up", "right") == snake['head']):
      pseudo_safe_moves["down"] = not play_agro
      pseudo_safe_moves["right"] = play_agro
      pseudo_safe_moves["up"] = play_agro
      
    # Case 2: Top Middle
    if (is_move_safe["down"] and adjacent_coord("down", "null", 2) == snake['head']):
      pseudo_safe_moves["down"] = play_agro
      pseudo_safe_moves["up"] = not play_agro
      pseudo_safe_moves["right"] = not play_agro

    # Case 3: Top Right
    if (is_move_safe["down"] and is_move_safe["right"] and adjacent_coord("down", "right") == snake['head']):
      pseudo_safe_moves["down"] = play_agro
      pseudo_safe_moves["right"] = play_agro
      pseudo_safe_moves["left"] = not play_agro

  # Finds shortest distance between two points
  food = game_state['board']['food']  


  food_directions = {
    "up": is_move_safe["up"],
    "down": is_move_safe["down"],
    "left": is_move_safe["left"],
    "right": is_move_safe["right"]
  }

  def get_distance(point_1, point_2):
   distance = abs(point_2['x'] - point_1['x']) + abs(point_2['y'] - point_1['y'])
   return distance

  #Find shortest distance to food


  def move_to_closest_foo():
   
    shortest_distance = 35 # large value that gets smaller as it is updated

    #figure out if closest_food is already targetted
    closest_food = food[0]
    targeted = False
    # if (Path("./target.txt").is_file()):
    #   targeted = True
    #   closest_food = serealize.load("target")
    #   if (closest_food not in game_state['board']['food']):
    #     targeted = False
    #     os.remove("./target.txt")

    if not targeted:
      for i in food:
        if(get_distance(my_head, i) < shortest_distance):
          shortest_distance = get_distance(my_head, i)
          closest_food = i

      serealize.write(closest_food, "target")
      # print("locked onto target: " + str(closest_food))

    # Closest food is a struct with the position of the closest food

    def make_one_true(dict, direction):
      for d, isTrue in dict.items():
        dict[d] = False
      dict[direction] = True
    
    
    dx = math.fabs(closest_food['x'] - my_head['x'])
    dy = math.fabs(closest_food['y'] - my_head['y'])

    moving_x = dx >= dy

    if moving_x:
      if closest_food['x'] < my_head['x'] and is_move_safe['left']:
        make_one_true(food_directions, "left")
      elif is_move_safe['right']:
        make_one_true(food_directions, "right")
      elif closest_food['y'] < my_head['y'] and is_move_safe['down']:
        make_one_true(food_directions, "down")
      else:
        make_one_true(food_directions, "up")
    else:
      if closest_food['y'] < my_head['y'] and is_move_safe['down']:
        make_one_true(food_directions, "down")
      elif is_move_safe['up']:
        make_one_true(food_directions, "up")
      elif closest_food['x'] < my_head['x'] and is_move_safe['left']:
        make_one_true(food_directions, "left")
      else:
        make_one_true(food_directions, "right")
        
      
    
    # if(is_move_safe['right'] == True and (my_head['x'] < closest_food['x'])):
      
    #   make_one_true(food_directions, "right")
      
    # elif(is_move_safe['left'] == True and (my_head['x'] > closest_food['x'])):
      
    #   make_one_true(food_directions, "left")
      
    # elif(is_move_safe['up'] == True and (my_head['y'] < closest_food['y'])):
      
    #   make_one_true(food_directions, "up")
      
    # elif(is_move_safe['down'] == True and (my_head['y'] > closest_food['y'])):
      
    #   make_one_true(food_directions, "down")

    # print (closest_food)


  move_to_closest_foo()



  # Flood Stuff
  def new_area(grid, x, y, empty, filled):
    width = board_width
    height = board_height
    area = 0
    if x < 0 or x >= width or y < 0 or y >= height or grid[x][y] == filled:
      return 0
    else:
      grid[x][y] = filled
      area += 1
      area += new_area(grid, x+1, y, empty, filled)
      area += new_area(grid, x-1, y, empty, filled)
      area += new_area(grid, x, y+1, empty, filled)
      area += new_area(grid, x, y-1, empty, filled)
    
    #print(area)
    return area
  
  areas_list = []
  areas_list.append(new_area(get_grid(), my_head['x'] +1 , my_head['y'], 0, 1))#area for movement to the right
  areas_list.append(new_area(get_grid(), my_head['x'] -1 , my_head['y'], 0, 1))#area for movement to the left
  areas_list.append(new_area(get_grid(), my_head['x']  , my_head['y'] +1, 0, 1))#area for movement up
  areas_list.append(new_area(get_grid(), my_head['x']  , my_head['y'] +1, 0, 1))#area for movement down
  
  moves_list = ["right", "left", "up", "down"]
  valid_moves_base_on_area = []
  areavalue = 0
  for i,k in enumerate(areas_list):
    if k > areavalue:
      areavalue = k
  for i,k in enumerate(areas_list):
    if k == areavalue:
      valid_moves_base_on_area.append(moves_list[i])
  best_move = random.choice(valid_moves_base_on_area)
  # End Flood Stuff
  
  # Cull pseudo_safe_moves
  for move, isSafe in pseudo_safe_moves.items():
    if is_move_safe[move] == False and isSafe == True:
      pseudo_safe_moves[move] = False
  
  # Test to make sure a move towards food is pseudo_safe_moves
  for move, is_in_food_dir in food_directions.items():
    if is_in_food_dir and pseudo_safe_moves[move] == True:
      for bmove in valid_moves_base_on_area:
        if bmove == move:
          return {"move": move}
      # if it is safe move the snake in that direction

  # Moving to food is not pseudo_safe, move to a random pseudo_safe square
  safe_moves = []
  for move, isSafe in pseudo_safe_moves.items():
      if isSafe:
          safe_moves.append(move)

  if len(safe_moves) == 0:
      print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
      return {"move": "down"}

  # Choose a random move from the safe ones
  for move in safe_moves:
    for bmove in valid_moves_base_on_area:
      if bmove == move: return {"move": bmove}
  next_move = random.choice(safe_moves)
  return {"move": next_move}
  

  # def go_to_closest_food(closest_food):
  #   if(is_move_safe['right'] == True and my_head['x'] < closest_food["x"]):
  #     is_move_safe['right'] == True
  #   elif(is_move_safe['left'] == True and my_head['x'] > closest_food["x"]):
  #     move ['left']
  #   elif(is_move_safe['up'] == True and my_head['y'] < closest_food["y"]):
  #     move ['up']
  #   elif(is_move_safe['down'] == True and my_head['y'] < closest_food["y"]):
  #     move ['down']
      
  # body = game_state['you']['health']


'''



def new_area(grid, x, y, empty, filled):
  width = board_width
  height = board_height
  area = 0
  if x < 0 or x >= width or y < 0 or y >= height or grid[x][y] == filled:
    return 0
  else:
    grid[x][y] = filled
    area += 1
    area += new_area(grid, x+1, y, empty, filled)
    area += new_area(grid, x-1, y, empty, filled)
    area += new_area(grid, x, y+1, empty, filled)
    area += new_area(grid, x, y-1, empty, filled)
  
  print(area)
  return area

areas_list = []
areas_list.append(new_area(get_grid(), my_head['x'] +1 , my_head['y'], 0, 1))#area for movement to the right
areas_list.append(new_area(get_grid(), my_head['x'] -1 , my_head['y'], 0, 1))#area for movement to the left
areas_list.append(new_area(get_grid(), my_head['x']  , my_head['y'] +1, 0, 1))#area for movement down
areas_list.append(new_area(get_grid(), my_head['x']  , my_head['y'] +1, 0, 1))#area for movement up

index = -1
areavalue = 0
for i,k in enumerate(areas_list):
  if k > areavalue:
    areavalue = k
    index = i
moves_list = ["right", "left", "down", "up"]
best_move = moves_list[index]


'''









  
  


      
      # if(is_move_safe['left'] == True && my_head['x'] -1 < 
      #    get_distance(my_head['x'], closest_food))
           
        
       
      
    

    

    
    

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
  # food = game_state['board']['food']

    #find the closest food on the board
    # distances = []
    # for apple in food:
    #   a = 1

  


    # print(f"MOVE {game_state['turn']}: {next_move}")


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
