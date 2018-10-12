##
# Neighbor Calculator for running phase 1.
from vectorize import Vectorizer
from distance import Distance, Similarity
from heapq import heappush, merge, nsmallest
from util import timed
from numpy import union1d
from multiprocessing import Pool
from math import ceil

# A class is implemented for this tuple to ensure that
#   the heapq can compare when appending.
class DistanceMeasure():
    def __init__(self, an_id, distance):
        self.id = an_id
        self.dist = distance

    def __lt__(self, other):
        return self.dist < other.dist
    
    def __str__(self):
        return "( id = " + str(self.id) + ", distance = " + str(self.dist) + ")"
    
    def __repr__(self):
        return self.__str__()


class Neighbor():
    
    # RUNTIME KNN USERS - 58s.
    @staticmethod
    def knn_worker(vector, table):
        vec_indexes = vector.nonzero()[0]
        distances = list()

        for index in table.index:
            # Get common indices between the two vectors.
            other = table.loc[index]
            other_indexes = other.nonzero()[0]
            indexes = union1d(vec_indexes, other_indexes)
            # get only the common indices for the two vectors.
            vec = vector[indexes.tolist()]
            other = other[indexes.tolist()]
            # now calculate distance.
            distance = Distance.l_p_distance(3, vec, other)
            
            heappush(distances, DistanceMeasure(index, distance))
        
        return distances
    

    # RUNTIME KNN USERS - 55s.
    @staticmethod
    def knn_worker_alt2(vector, table):
        distances = list()

        for index in table.index:
            other = table.loc[index]
            # now calculate distance.
            distance = Distance.l_p_distance(3, vector, other)
            
            heappush(distances, DistanceMeasure(index, distance))
        return distances
    

    # RUNTIME KNN USERS - 283s.
    @staticmethod
    def knn_worker_alt(vector, table):
        
        dist_table = Distance.l_p_distance_alt(3, vector, table)
        distances = list()
        for index in dist_table.index:
            heappush(distances, DistanceMeasure(index, dist_table[index]))
        
        return distances
    

    @staticmethod
    @timed
    def knn(k, vector, table, processes=8):

        rows = table.shape[0]
        size = ceil(rows / processes)

        args = []
        for i in range(processes):
            subtable = table.iloc[i * size : (i + 1) * size]
            args.append((vector, subtable))
        
        p = Pool(processes)
        print("Starting threads!")
        out = p.starmap(Neighbor.knn_worker_alt2, args)

        dists = merge(*out)
        nearest = nsmallest(k, dists)
        print('All Distances = ' + str(list(dists)))
        print('Nearest = ' + str(type(nearest)) + " : " + str(list(nearest)))
        return nearest

        """
        vec_indexes = vector.nonzero()[0]

        nearest = {}
        max_min = float('-inf')
        max_id = None

        for index in table.index:
            # Get common indices between the two vectors.
            other = table.loc[index]
            other_indexes = other.nonzero()[0]
            indexes = union1d(vec_indexes, other_indexes)
            # get only the common indices for the two vectors.
            sub_vector = vector[indexes.tolist()]
            other = other[indexes.tolist()]
            # now calculate distance.
            distance = Distance.l_p_distance(3, sub_vector, other)

            if len(nearest) < k:
                nearest[other.name] = distance
                if distance > max_min:
                    max_min = distance
                    max_id = other.name
            elif distance < max_min:
                nearest.pop(max_id)
                nearest[other.name] = distance
                max_min = max(nearest.values())
                max_id = [name for name in nearest.keys() if nearest[name] == max_min][0]

        return nearest
        """


    # KNN Specific method for textual - gets the appropriate table and vector
    #   and then calls generic KNN.
    @staticmethod
    def knn_textual(k, an_id, model, atype, database, processes=8):
        vector = database.get_txt_vector(atype, an_id, model)
        table = database.get_txt_desc_table(atype, model).drop(vector.name)

        return Neighbor.knn(k, vector, table, processes)



    @staticmethod
    @timed
    def knn_textual_2(k, an_id, model, atype, database, vector = None):
        table = database.get_txt_desc_table(atype, model)
        vector = database.get_txt_vector(atype, an_id, model)

        # Get a pandas series of all the distances between the vectors
        distances = Distance.l_p_distance(3, vector, table)

        # sort by ascending distance
        distances.sort_values(axis=0, ascending=True, inplace=True)

        # Our first vector will inevitably be this_vector as the distance will be 0, so we 
        #   will grab 1-k
        return distances.index[1:k]
        


    @staticmethod
    def similarity_by_id(this_vector, ids, database, model, itemtype, k=3):
        other_vectors =[Vectorizer.text_vector(an_id, database, model, itemtype) for an_id in ids]
        return Neighbor.similarity_contribution(this_vector, other_vectors, k)


    @staticmethod
    def similarity_contribution(an_id, other_ids, k=3):
        pass


    ###############################################################################################

"""
    @staticmethod
    def knn_visual(k, locationid, model, database, this_vector=None):
        nearest = {}
        if not this_vector:
            this_vector = Vectorizer.visual_vector(locationid, database, model)
        
        others = database.get_location_ids()
        others.remove(locationid)
        # Get distance to each other vecctor and add to nearest if it is less than the
        #   distance to an existing vector.
        for other in others:
            other_vector = Vectorizer.visual_vector(other, database, model)
            distance = Distance.l_p_distance(3, this_vector, other_vector, positional=True)

            if len(nearest) < k:
                largest_key, largest_best = None, inf
            else:
                largest_key, largest_best = max(nearest.items(), key=itemgetter(1))
    
            if distance < largest_best:
                if largest_key:
                    nearest.pop(largest_key)
                nearest[other] = distance
        
        return nearest


    @staticmethod
    def knn_visual_all(k, locationid, models, database, this_vector=None):
        nearest = {}
        others = database.get_location_ids()
        others.remove(locationid)

        # Calculate this_vector
        if not this_vector:
            this_vector = Vectorizer.visual_vector_multimodel(locationid, database, models)

        # Make a vector where each item is an average for that model
        for other in others:
            other_vector = Vectorizer.visual_vector_multimodel(locationid, database, models)
            # get distance between vectors
            distance = Distance.l_p_distance(3, this_vector, other_vector)
            
            if len(nearest) < k:
                largest_key, largest_best = None, inf
            else:
                largest_key, largest_best = max(nearest.items(), key=itemgetter(1))
    
            if distance < largest_best:
                if largest_key:
                    nearest.pop(largest_key)
                nearest[other] = distance
        
        return nearest
                

    
    @staticmethod
    def visual_sim_contribution(this_vector, ids, database, model, k=3):
        other_vectors = [Vectorizer.visual_vector(locid, database, model) for locid in ids]
        return Neighbor.similarity_contribution(this_vector, other_vectors, k, positional=True)
    

    @staticmethod
    def visual_sim_multimodal(this_vector, ids, database, models, k=3):
        other_vectors = [Vectorizer.visual_vector_multimodel(locid, database, models) for locid in ids]
        return Neighbor.similarity_contribution(this_vector, other_vectors, k, positional=True)
        """