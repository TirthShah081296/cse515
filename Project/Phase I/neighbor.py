##
# Neighbor Calculator for running phase 1.
from vectorize import Vectorizer
from distance import Distance
from math import inf
from operator import itemgetter 

class Neighbor():
    
    @staticmethod
    def get_nearest_neighbors(k, id, model, item_type, database):

        nearest = {}

        # get vector representing item associated w/ id
        this_vector = Vectorizer.create_description_vector(id, database, model, item_type)

        # Get the id's for all items of the same type.
        if item_type == 'photo':
            others = database.get_photo_ids()
        elif item_type == 'user':
            others = database.get_user_ids()
        elif item_type == 'poi':
            others = database.get_location_ids()
        else:
            raise ValueError('[ERROR] The provided type was invalid.\ntype = ' + str(item_type))

        # This is not a list of tuples. Clean to make a list of ids.
        others = [other[0] for other in others]
        
        # remove this id from the list
        others.remove(id)

        # for each other one, get their vector and calculate distance.
        for other in others:
            
            other_vector = Vectorizer.create_description_vector(other, database, model, item_type)

            distance = Distance.l_2_distance(this_vector, other_vector)

            if len(nearest) < k:
                largest_key, largest_best = None, inf
            else:
                largest_key, largest_best = max(nearest.items(), key=itemgetter(1))

            if distance < largest_best:
                # remove the key with the largest distance if it exists
                if largest_key:
                    nearest.pop(largest_key)
                
                nearest[other] = distance
        
        # Return your K nearest
        return nearest



