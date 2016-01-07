import os, json, sys, time

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
            if cast_name != self.name and cast_name not in self.adjacent_actors:
                self.adjacent_actors[cast_name] = film



# Dictionary to store all actors read in from JSON files
# Key = name of actor, value = Actor object
actors = {}

'''
Input: Parsed JSON object containing film information
Adds each cast member to the actors dictionary and updates the actors' adjacent actors
'''
def process_film(film_object):
    film_name = film_object["film"]["name"]
    cast_list = film_object["cast"]
    
    for cast in cast_list:
        cast_name = cast["name"]
        
        # Create new Actor object if first time seeing this cast member
        if cast_name not in actors:
            actors[cast_name] = Actor(cast_name)
            
        actors[cast_name].update_adjacent_actors(cast_list, film_name)

'''
Reads and processes every JSON file in the films folder
''' 
def read_json():
    path_to_json = 'films/'
    json_files = [json_file for json_file in os.listdir(path_to_json) if json_file.endswith('.json')]
    for js in json_files:
        with open(os.path.join(path_to_json, js)) as json_file:
            process_film(json.load(json_file))
            

'''
Input: Name of actor

Performs BFS to find shortest path from Kevin Bacon to actor

Returns: Path to actor (if found), None otherwise
'''
def find_path(input_name):
    queue = [("Kevin Bacon", [])] # List of tuples: ("Actor Name", [Path so far])
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
def print_pretty_path(path, input_actor):
    current_actor = input_actor
    
    for i in range(len(path)-1, -1, -1):
        print current_actor + " -(" + path[i][1] + ")->",
        current_actor = path[i][0]
        
    print "Kevin Bacon"
        
if __name__ == "__main__":
    read_json()
    
    try:
        while(True):
            input_name = raw_input("Please enter an actor's name: ")
            if input_name not in actors:
                print "Sorry! That actor is not in our data"
                continue
            
            start = time.time()
            path = find_path(input_name)
            end = time.time()
            print "Elapsed time: %.3fs" % (end - start)
            if path is None:
                print "Sorry! Could not find a path to Kevin Bacon"
                continue
            
            print_pretty_path(path, input_name)
            
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)