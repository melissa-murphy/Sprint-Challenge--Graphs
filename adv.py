from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# reverse direction
reverse_path = []
# dict for room ref
rooms = {}
reverse_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# # start in room 0 and return exits
rooms[0] = player.current_room.get_exits()

# # while there are unvisited rooms
while len(rooms) < len(room_graph) - 1:
    # if the room the player is in is not in rooms dict:
    if player.current_room.id not in rooms:
        # get exits and add to rooms
        rooms[player.current_room.id] = player.current_room.get_exits()
        # define previous room reverse_path[-1]
        previous_room = reverse_path[-1]
        # remove previous room from rooms
        rooms[player.current_room.id].remove(previous_room)

    # while rooms dict is empty:
    while len(rooms[player.current_room.id]) < 1:
        # pop last from reverse_path
        reverse = reverse_path.pop()
        # add to traversal_path
        traversal_path.append(reverse)
        # player travels in reverse
        player.travel(reverse)

    # find exit direction from last entry in rooms dict
    exit_direction = rooms[player.current_room.id].pop(0)
    # add exit direction to traversal_path
    traversal_path.append(exit_direction)
    # add reverse_direction to reverse path
    reverse_path.append(reverse_direction[exit_direction])
    # player travels in reverse
    player.travel(exit_direction)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
