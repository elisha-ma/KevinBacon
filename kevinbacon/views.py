import requests, os, json, sys, time
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')

def input(request):
    actors = read_json()
    input_name = request.POST.get('actorname')
    
    input_name_lower = input_name.lower()
    if input_name_lower not in actors:
        return render(request, "index.html", {"message" : "Sorry! That actor is not in our data"})
        
    start = time.time()
    path = find_path(input_name_lower, actors)
    end = time.time()
    elapsed = "%.3fs" % (end - start)
    if path is None:
        return render(request, "index.html", {"message" : "Sorry! Could not find a path to Kevin Bacon"})
                
    path_string = print_pretty_path(path, input_name_lower, actors)
    
    context = {"path" : path_string, "time" : elapsed}
    return render(request, 'input.html', context)
        
'''
Input: Name of actor

Performs BFS to find shortest path from Kevin Bacon to actor

Returns: Path to actor (if found), None otherwise
'''
def find_path(input_name, actors):
    queue = [("kevin bacon", [])] # List of tuples: ("Actor Name", [Path so far])
    visited = {} # Track which actors have already been visited
    
    while queue:
        (current_actor, current_path) = queue.pop(0)
        if current_actor in visited:
            continue
        
        visited[current_actor] = 1
        if current_actor == input_name:
            return current_path
        
        # Add the current actor and the adjacent film to the next path
        # Enqueue the adjacent actor plus the path
        for actor in actors[current_actor].adjacent_actors.keys():          
            if actor not in visited:
                next_film = actors[current_actor].adjacent_actors[actor]
                path = current_path + [(current_actor, next_film)]
                queue.append((actor, path))
                
    return None
'''
Prints the path by printing each Actor in the path followed by the Film they shared
with the next Actor up to Kevin Bacon
'''
def print_pretty_path(path, input_actor, actors):
    current_actor = actors[input_actor].name
    
    path_list = []
    
    for i in range(len(path)-1, -1, -1):
        path_list.append(current_actor)
        path_list.append( " -(" + str(path[i][1]) + ")->")
        current_actor = actors[path[i][0]].name
        
    path_list.append("Kevin Bacon")
    
    return "".join(path_list)

class Actor:
    '''
    Object to store name of actor and a list of adjacent actors
    name: string
    adjacent_actors: dictionary with key = name of actor and value = film they were in together
    '''
    def __init__(self, name):
        self.name = name
        self.adjacent_actors = {}
    
    '''
    Adds each new actor from the cast list to the adjacent_actors dictionary
    '''    
    def update_adjacent_actors(self, cast_list, film):
        for cast in cast_list:
            cast_name = cast["name"]
            cast_name_lower = cast_name.lower()
            if cast_name != self.name and cast_name_lower not in self.adjacent_actors:
                self.adjacent_actors[cast_name_lower] = film



'''
Reads and processes every JSON file in the films folder
''' 
def read_json():
    # Dictionary to store all actors read in from JSON files
    # Key = name of actor, value = Actor object
    actors = {}
    path_to_json = 'films/'
    json_files = [json_file for json_file in os.listdir(path_to_json) if json_file.endswith('.json')]
    for js in json_files:
        with open(os.path.join(path_to_json, js)) as json_file:
            process_film(json.load(json_file), actors)
    
    return actors
            
            
'''
Input: Parsed JSON object containing film information
Adds each cast member to the actors dictionary and updates the actors' adjacent actors
'''
def process_film(film_object, actors):
    film_name = film_object["film"]["name"]
    cast_list = film_object["cast"]
    
    for cast in cast_list:
        cast_name = cast["name"]
        cast_name_lower = cast_name.lower()
        
        # Create new Actor object if first time seeing this cast member
        if cast_name_lower not in actors:
            actors[cast_name_lower] = Actor(cast_name)
            
        actors[cast_name_lower].update_adjacent_actors(cast_list, film_name)