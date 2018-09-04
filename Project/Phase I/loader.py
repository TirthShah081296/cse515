# CSE 515
# Project Phase 1
#
# TODO Do we need to load anything from desctext, descvis, gt?
# TODO Create utilities to:
#   1. Find user who took an image based on img id.
#   2. Get 

from lxml import etree
import sys
from os import listdir
from os.path import isfile
from dateutil.parser import parse
import inspect
from cv2 import cv2
import multiprocessing
from queue import Queue
from copyreg import pickle
import time # for testing efficiency.

################################################################
####                    GENERIC LOADER                       ####
################################################################

class GenericLoader:

    def __init__(self):
        self.loaded = Queue(maxsize=0)

    ##
    # Method to load a file of this type.
    # NOTE: this should append to self.loaded.
    def load_file(self, file):
        raise NotImplementedError
    
    ##
    # Method to load a folder of files.
    def load_folder(self, folder):

        items = list()
        if isfile(folder):
            return items
        
        files = [file for file in listdir(folder) if isfile(folder + '/' + file)]

        num_cpus = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(num_cpus)
        pool.map(self.load_file, files)

        return self.loaded

        # for file in listdir(folder):
        #     item = self.load_file(folder + "/" + file)
        #     if not item is None:
        #         items.append(item)
        
        # return items
    
    ##
    # Method to load a folder of folder.
    def load_directory(self, directory):
        image_map = {}
        for folder in listdir(directory):
            image_map[folder] = self.load_folder(directory + '/' + folder)
        return image_map


################################################################
####                    LOCATION DATA                       ####
################################################################

class LocationEntry:

    def __init__(self, id = None, title = None, name=None, latitude = None, longitude = None, wiki = None):
        self.id = int(id)
        self.title = title
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.wiki = wiki

##
# NOTE: There are 593 user files, each with a ton of images. This loader
#   takes a while to run.
class LocationReader(GenericLoader):

    ##
    #
    def load_file(self, file):
        self.load_files(file, 'poiNameCorrespondences.txt')

    ##
    # Loads the location file using location and name_correlation files.
    def load_files(self, name_file, corr_file):
        name_corr = self.load_name_corr(corr_file)
        locations = self.load_locations(name_file, name_corr)
        self.loaded.put(locations)

    ##
    # Create dictionary of title > Location
    def load_locations(self, file, name_correlation):

        if not isfile(file):
            raise FileNotFoundError('The location data could not be loaded as the provided file was invalid: ' + str(file))
        if not type(name_correlation) is dict:
            raise TypeError('Name correlation was not of the appropriate dictionary type: ' + str(type(name_correlation)))

        try:
            tree = etree.parse(file)
        except IOError as e:
            print ("File " + file + " not found. " +str(e))

        root = tree.getroot()
        return_val = {}

        for child in root:
            # Load all data from branch.
            child_id = child.find('number').text
            title = child.find('title').text
            latitude = child.find('latitude').text
            longitude = child.find('longitude').text
            wiki = child.find('wiki').text
            location_name = name_correlation[title]
            # Create dictionary entry.
            dict_entry = LocationEntry(id=child_id, name=location_name, title=title, latitude=latitude, longitude=longitude, wiki=wiki)
            # create mapping.
            return_val[title] = dict_entry
        
        return return_val

    ##
    # Load title > name correlations
    def load_name_corr(self, file):

        if not isfile(file):
            raise FileNotFoundError('The name correlation dictionary could not be created as the provided parameter was not a vaild file: ' + str(file))
        
        name_correlation = {}
        with open(file) as f:
            for line in f:
                name, title = line.strip('\n').split('\t')
                name_correlation[title] = name
        
        return name_correlation


class UserCred():

    def __init__(self, visualScore=None, faceProportion=None, tagSpecificity=None,
                locationSimilarity=None, photoCount=None, uniqueTags=None,
                uploadFrequency=None, bulkProportion=None):
        self.visualScore = visualScore
        self.faceProportion = faceProportion
        self.tagSpecificity = tagSpecificity
        self.locationSimilarity = locationSimilarity
        self.photoCount = photoCount
        self.uniqueTags = uniqueTags
        self.uploadFrequency = uploadFrequency
        self.bulkProportion = bulkProportion

################################################################
####                     USER LOADER                        ####
################################################################

class Photo():

    def __init__(self, date_taken=None, id=None, tags=None, title=None, url_b=None, userid=None, views=None):
        self.date_taken = date_taken
        self.id = id
        self.tags = tags
        self.title = title
        self.url_b = url_b
        self.userid = userid
        self.views = views

class User():

    def __init__(self, credibility=None, photos=None, id=None):
        self.credibility = credibility
        self.photos = photos
        self.id = id


class UserLoader(GenericLoader):

    ##
    # load user from file.
    def load_file(self, file):
        
        if not isfile(file):
            raise FileNotFoundError('File from which to load user could not be found: ' + str(file))
        
        try:
            tree = etree.parse(file)
        except IOError as e:
            print("Could not parse user file " + str(file) + "; " + str(e))
            return None
        
        # get the two main sections of the xml file
        root = tree.getroot()
        user_id = root.get('user')
        credibility = root.find('credibilityDescriptors')
        photos = root.find('photos')

        # load in separate function
        cred = self.__load_credibility__(credibility)
        pics = self.__load_photos__(photos)

        # return User(credibility=cred, photos=pics, id=user_id)
        self.loaded.put(User(credibility=cred, photos=pics, id=user_id))

    ## 
    # Load information from the credibility section of the user
    #   xml.
    def __load_credibility__(self, credibility_root):
        
        children = credibility_root.iter()
        
        for child in children:
            visualScore = float(child.get('visualScore').text)
            faceProportion = float(child.get('faceProportion').text)
            tagSpecificity = float(child.get('tagSpecificity').text)
            locationSimilarity = float(child.get('locationSimilarity').text)
            photoCount = int(child.get('photoCount').text)
            uniqueTags = float(child.get('uniqueTags').text)
            uploadFrequency = float(child.get('uploadFrequency').text)
            bulkProportion = float(child.get('bulkProportion').text)
        
        return UserCred(visualScore, faceProportion, tagSpecificity, locationSimilarity,
                        photoCount, uniqueTags, uploadFrequency, bulkProportion)

    ##
    # Load the photos from the user.
    def __load_photos__(self, photos_root):

        photos = []
        for photo in photos_root.iterfind('photo'):
            try:
                photos.append(Photo(date_taken=parse(photo.get('date_taken')), 
                            id=int(photo.get('id')),
                            tags=photo.get('tags').split(' '),
                            title=photo.get('title'),
                            url_b=photo.get('url_b'),
                            userid=photo.get('userid'),
                            views=int(photo.get('views'))))
            except Exception as e:
                print('An exception occured when appending photo ' + photo.get('title') + ': ' + str(e))
        return photos


################################################################
####                     IMAGE LOADER                       ####
################################################################


class ImageLoader(GenericLoader):

    ##
    # Load the image into a numpy array.
    def load_file(self, file):
        image = cv2.imread(file)
        self.loaded.put(image)


################################################################
####                    Load All Data                       ####
################################################################

def load_data_timed(folder):
    start_time = time.time()
    location_map, images, users = load_data(folder)
    elapsed = start_time - time.time()
    print("Loading images, location, and users took " + str(elapsed) + " time.")
    return location_map, images, users


##
# Takes about 25 seconds to load location_map and images
# Takes [a long time]
def load_data(folder):
    # Load locations
    loc_reader = LocationReader()
    loc_reader.load_files(folder + '/devset_topics.xml',
               folder + '/poiNameCorrespondences.txt')
    location_map = loc_reader.loaded
    users = UserLoader().load_folder(folder + '/desccred')
    images = ImageLoader().load_directory(folder + '/img') # About 4GB when loaded. VERY large.
    return location_map, images, users