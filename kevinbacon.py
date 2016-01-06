import os, json

class Actor:
    def __init__(self, name):
        self.name = name
        self.adjacent_actors = {}
        
    def update_adjacent_actors(self, cast_list, film):
        for cast in cast_list:
            cast_name = cast["name"]
            if cast_name != self.name and cast_name not in self.adjacent_actors:
                self.adjacent_actors[cast_name] = film


actors = {}

def process_film(film_object):
    film_name = film_object["film"]["name"]
    cast_list = film_object["cast"]
    
    for cast in cast_list:
        #actor_name = actor["name"].lower().replace(" ", "")
        cast_name = cast["name"]
        if cast_name not in actors:
            actors[cast_name] = Actor(cast_name)
            
        actors[cast_name].update_adjacent_actors(cast_list, film_name)

def read_json():
    path_to_json = 'films/'
    json_files = [json_file for json_file in os.listdir(path_to_json) if json_file.endswith('.json')]
    for js in json_files:
        with open(os.path.join(path_to_json, js)) as json_file:
            process_film(json.load(json_file))
            

def find_path(input_name):
    queue = [("Kevin Bacon", [])]
    visited = {}
    while queue:
        (current_actor, current_path) = queue.pop(0)
        if current_actor in visited:
            continue
        
        visited[current_actor] = 1
        if current_actor == input_name:
            return current_path
        
        for actor in actors[current_actor].adjacent_actors.keys():          
            if actor not in visited:
                path = current_path + [(current_actor, actors[current_actor].adjacent_actors[actor])]
                queue.append((actor, path))
                
    return None

def print_pretty_path(path, input_actor):
    current_actor = input_actor
    
    for i in range(len(path)-1, -1, -1):
        print current_actor + " -(" + path[i][1] + ")->",
        current_actor = path[i][0]
        
    print "Kevin Bacon"
        
if __name__ == "__main__":
    read_json()
    
    while(True):
        input_name = raw_input("Please enter an actor's name: ")
        if input_name not in actors:
            print "Sorry! That actor is not in our data"
            continue
        
        path = find_path(input_name)
        
        if path is None:
            print "Sorry! Could not find a path to Kevin Bacon"
            continue
        
        print_pretty_path(path, input_name)