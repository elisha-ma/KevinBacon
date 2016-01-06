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
        if cast_name not in cast_list:
            actors[cast_name] = Actor(cast_name)
            
        actors[cast_name].update_adjacent_actors(cast_list, film_name)

def read_json():
    path_to_json = 'films/'
    json_files = [json_file for json_file in os.listdir(path_to_json) if json_file.endswith('.json')]
    for js in json_files:
        with open(os.path.join(path_to_json, js)) as json_file:
            process_film(json.load(json_file))
            
if __name__ == "__main__":
    read_json()
    
    while(True):
        input_name = raw_input("Please enter the actor's name: ")
        