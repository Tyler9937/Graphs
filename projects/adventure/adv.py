from room import Room
from player import Player
from world import World
import csv

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


switch = True
seed_cache = {}
path_length_cache = {}
seed_var = 90870

# Taking advantage of random path selection to shrink path lenght
while switch is True:

    if seed_var in seed_cache:
        seed_var += 1

    # Initating mutable variables
    player = Player(world.starting_room)
    
    
    traversal_string = ''
    traversal_path = []
    reverese_directions = {'n':'s', 's':'n','e':'w','w':'e'} # Oppistee direction referernce for travaling backwards
    reverse_path = []
    visited = {}

    # Initaiting starting room in visited
    visited[player.current_room.id] = player.current_room.get_exits()

    # Looping till all rooms visited
    while len(visited) < len(room_graph) -1:

        # Adding room to visited
        if player.current_room.id not in visited:
            
            visited[player.current_room.id] = player.current_room.get_exits()
            
            # Remove room that was entered from
            visited[player.current_room.id].remove(reverse_path[-1])


        # If in a dead end
        while len(visited[player.current_room.id]) == 0:

            # Start backtracking
            reverse = reverse_path.pop()
            traversal_path.append(reverse) 
            player.travel(reverse)


        # Adding Randomness to path selection
        choices = visited[player.current_room.id]
        choice = random.choice(choices)
        index = choices.index(choice)
        movement = visited[player.current_room.id].pop(index) # Movement equal to random direction


        # Update paths and move player object
        traversal_path.append(movement)
        reverse_path.append(reverese_directions[movement])
        player.travel(movement)


    path_length = len(traversal_path)
    seed_cache[seed_var] = path_length
    

    # TRAVERSAL TEST
    if path_length < 990 and path_length not in path_length_cache:
        print(str(seed_var) +' '+ str(path_length))
    if path_length < 990:
        print(seed_var)
        visited_rooms = set()
        player.current_room = world.starting_room
        visited_rooms.add(player.current_room)

        for move in traversal_path:
            player.travel(move)
            visited_rooms.add(player.current_room)

        if len(visited_rooms) == len(room_graph):
                switch = False
                
                
 

    path_length_cache[path_length] = seed_var






# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")

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
