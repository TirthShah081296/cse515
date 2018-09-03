# CSE 515
# Project Phase 1
#
# TODO Do we need to load anything from desctext, descvis, gt?
#

import xml.etree.ElementTree as ElementTree
from os import listdir
from os.path import isfile
import inspect

################################################################
####                    LOCATION DATA                       ####
################################################################
class LocationEntry:

    def __init__(self, id = None, name = None, latitude = None, longitude = None, wiki = None):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.wiki = wiki


class LocationReader:

    def __init__(self):
        self.name_title_dict = None
    
    ##
    # Create dictionary of title > 
    def parse_xml(self, file):
        
        if self.name_title_dict is None:
            print("Tried to parse xml without name-title mappings.")
            return None
        
        try:
            tree = ElementTree.parse(file)
        except IOError as e:
            print ("File " + file + " not found. " +str(e))

        root = tree.getroot()
        return_val = {}

        for child in root():
            # Load all data from branch.
            child_id = child.find('number').text
            title = child.find('title').text
            latitude = child.find('latitude').text
            longitude = child.find('longitude').text
            wiki = child.find('wiki').text
            # Create dictionary entry.
            dict_entry = LocationEntry(id=child_id, name=title, latitude=latitude, longitude=longitude, wiki=wiki)
            location_name = self.name_title_dict[title]
            # create mapping.
            return_val[location_name] = dict_entry
        
        return return_val
    

    ##
    # Load title > name correlations
    def parse_name_corr(self, file):
        
        # Create dictionary if not already created. The main reason
        #   to do this here is so we can check if no names have been
        #   loaded when we run the parse_xml method and throw an error.
        if self.name_title_dict is None:
            self.name_title_dict = {}

        with open(file) as f:
            for line in f:
                name, title = line.split('\t')
                self.name_title_dict[title] = name


class UserCred():

    def __init__(self, visualScore=None, faceProportion=None, tagSpecificity=None,
                locationSimilarity=None, photoCount=None, uniqueTags=None,
                uploadFrequency=None, bulkProportion=None, **kwargs):
        # set properties dynamically
        for name, value in locals().copy().items():
            setattr(self, name, value)

################################################################
####                     USER LOADER                        ####
################################################################

class Photo():

    def __init__(self, date_taken=None, id=None, tags=None, title=None, url_b=None, userid=None, views=None):
        # set properties dynamically
        for name, value in locals().copy().items():
            setattr(self, name, value)


class User():

    def __init__(self, credibility=None, photos=None, id=None):
        self.credibility = credibility
        self.photos = photos
        self.id = id


class UserLoader():
    
    ##
    # Load all users from a directory.
    # @returns list of user objects.
    @staticmethod
    def load_users(folder):

        users = []

        for file in listdir(folder):
            user = UserLoader.load_user(folder + '/' + file)
            if not user is None:
                users.append(user)

        return users
    
    ##
    # load user from file.
    @staticmethod
    def load_user(file):
        
        if not isfile(file):
            return None
        
        try:
            tree = ElementTree.parse(file)
        except IOError as e:
            print("Could not parse user file " + str(file) + "; " + str(e))
            return None
        
        # get the two main sections of the xml file
        root = tree.getroot()
        user_id = root.get('user')
        credibility = root.find('credibilityDescriptors')
        photos = root.find('photos')

        # load in separate function
        cred = UserLoader.__load_credibility__(credibility)
        pics = UserLoader.__load_photos__(photos)

        return User(credibility=cred, photos=pics, id=user_id)

    ## 
    # Load information from the credibility section of the user
    #   xml.
    @staticmethod
    def __load_credibility__(credibility_root):
        
        children = credibility_root.iter()
        # Load packed values.
        kwargs = {}
        for child in children:
            kwargs[child.tag] = child.text
        
        return UserCred(**kwargs)

    ##
    # Load the photos from the user.
    @staticmethod
    def __load_photos__(photos_root):

        photos = []
        for photo in photos_root.iterfind('photo'):
            photos.append(Photo(date_taken=photo.get('date_taken'), 
                            id=photo.get('id'),
                            tags=photo.get('tags').split(' '),
                            title=photo.get('title'),
                            url_b=photo.get('url_b'),
                            userid=photo.get('userid'),
                            views=photo.get('views')))
        return photos



################################################################
####                     IMAGE LOADER                       ####
################################################################


class ImageLoader():

    @staticmethod
    def load_image(file):
        
        if not isfile(file):
            return None
        
        # TODO: Load File
        raise NotImplementedError
    
    @staticmethod
    def load_image_folder(folder):

        images = list()
        if isfile(folder):
            return images
        
        for file in listdir(folder):
            img = ImageLoader.load_image(file)
            if img:
                images.append(img)
        
        return images
    
    @staticmethod
    def load_image_directory(directory):
        image_map = {}
        for folder in listdir(directory):
            folder_name = None # get directory name
            image_map[folder_name] = ImageLoader.load_image_folder(directory + '/' + folder)
        return image_map
        


################################################################
####                    Load All Data                       ####
################################################################

def load_data(data_folder):

    users = UserLoader.load_users(data_folder + '/desccred')
    loc_reader = LocationReader()
    loc_reader.parse_name_corr(data_folder + '/poiNameCorrespondences.txt')
    location_map = loc_reader.parse_xml(data_folder + '/devset_topics.xml')

users = UserLoader.load_users("../Dataset/desccred")