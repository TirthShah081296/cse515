from collections import Counter
from loader import User, Photo

class Vectorizer():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    def vectorize(self, item):
        raise NotImplementedError



class UserVectorizer(Vectorizer):

    def vectorize(self, item):
        if not isinstance(item, User):
            raise TypeError('UserVectorizer can only vectorize items of type User, but was given item of type ' + str(type(item)))

        vector = Counter()
        photo_vectorizer = PhotoVectorizer()
        for photo in item.photos:
            vector += photo_vectorizer.vectorize(photo)
        
        return vector



##
# NOTE: This vectorizer is for the photo items underneath the user item,
#   not for images themselves.
# TODO: Think of a better name to make this clear!
class PhotoVectorizer(Vectorizer):

    def vectorize(self, item):

        tag_vector = self.vectorize_by_image_tags(item)
        name_vector = self.vectorize_by_image_name(item)
        return tag_vector + name_vector


    def vectorize_by_image_tags(self, item):

        if not isinstance(item, Photo):
            raise TypeError('PhotoVectorizer can only vectorize items of type Photo, but was given item of type ' + str(type(item)))

        vector = Counter(item.tags)
        
        return vector

    
    def vectorize_by_image_name(self, item):

        if not isinstance(item, Photo):
            raise TypeError('PhotoVectorizer can only vectorize items of type Photo, but was given item of type ' + str(type(item)))

        vector = Counter(item.title.split(' '))
        
        return vector