from collections import defaultdict
from database import SQLDatabase

class Vectorizer():

    @staticmethod
    def create_description_vector(id, database, model, item_type):
        if item_type == 'photo':
            return Vectorizer.create_photo_term_vector(id, database, model)
        elif item_type == 'user':
            return Vectorizer.create_user_term_vector(id, database, model)
        elif item_type == 'poi':
            return Vectorizer.create_location_term_vector(id, database, model)
        else:
            raise ValueError('[ERROR] The provided type was invalid.\ntype = ' + str(item_type))

    @staticmethod
    def create_vector_from_desc_list(desc, model):

        vector = defaultdict(int)
        for _, term, tf, idf, tfidf in desc:
            if model == 'tf':
                vector[term] = tf
            elif model == 'idf':
                vector[term] = idf
            elif model == 'tf-idf':
                vector[term] = tfidf
            else:
                raise ValueError('[ERROR] The value provided for model was not valid.\nmodel = ' + str(model))
        return vector


    @staticmethod
    def create_user_term_vector(id, database, model):
        desc = database.get_user_desc(id)
        return Vectorizer.create_vector_from_desc_list(desc, model)
    
    @staticmethod
    def create_location_term_vector(id, database, model):
        desc = database.get_loc_desc(id)
        return Vectorizer.create_vector_from_desc_list(desc, model)
    
    @staticmethod
    def create_photo_term_vector(id, database, model):
        desc = database.get_photo_desc(id)
        return Vectorizer.create_vector_from_desc_list(desc, model)