#! /bin/usr/python3.6

from lxml import etree
from os import listdir, path
from os.path import isfile
from util import timed
from database import Database
from multiprocessing import Pool

################################################################
####                    GENERIC LOADER                      ####
################################################################

class GenericReader():

    def __init__(self):
        # self.loaded = Queue(maxsize=0)
        pass

    ##
    # Method to load a file of this type.
    # NOTE: this should append to self.loaded.
    def load_file(self, file, index=None):
        raise NotImplementedError

    ##
    #
    def load_files(self, files, indexes=None):
        return_val = {}
        if indexes:
            for index, file in zip(indexes, files):
                out = self.load_file(file, index)
                return_val[index] = out
        else:
            for file in files:
                out = self.load_file(file)
                return_val[file] = out
        return return_val

    ##
    #
    def load_folder(self, folder):
        files = self.__get_files__(folder)
        return self.load_files(files)

    ##
    # Method to load a folder of folder.
    def load_directory(self, directory):
        return_val = []
        for folder in listdir(directory):
            out = self.load_folder(directory + '/' + folder)
            return_val.append(out)
        return return_val
    
    ##
    #
    def __get_files__(self, folder):
        #for file in listdir(folder):
        #    if isfile(folder + '/' + file:
        #
        return [folder + '/' + file for file in listdir(folder) if isfile(folder + '/' + file) and not file.startswith('.')]


#################################################################
####                    LOCATION DATA                       ####
################################################################

##
# Meant to be used by calling load_files(name_file, corr_file)
# Returns a dataframe with location information.
class LocationReader(GenericReader): # GenericReader inheritance - don't forget it!

    def load_file(self, file, index=None):
        self.load_files(file, 'poiNameCorrespondences.txt')

    ##
    # Loads the location file using location and name_correlation files.
    def load_files(self, name_file, corr_file):
        name_corr = self.load_name_corr(corr_file)
        return self.load_locations(name_file, name_corr)

    ##
    # Create dictionary of title > Location
    def load_locations(self, file, name_correlation):

        if not isfile(file):
            raise OSError('The location data could not be loaded as the provided file was invalid: ' + str(file))
        if not type(name_correlation) is dict:
            raise TypeError('Name correlation was not of the appropriate dictionary type: ' + str(type(name_correlation)))
        
        tree = etree.parse(file)
        root = tree.getroot()
        rows = list()

        for location in root:
            # Load all data from branch.
            locationid = int(location.find('number').text)
            title = location.find('title').text
            name = name_correlation[title]
            latitude = float(location.find('latitude').text)
            longitude = float(location.find('longitude').text)
            wiki = location.find('wiki').text
            rows.append([locationid, title, name, latitude, longitude, wiki])
        return rows

    ##
    # Load title > name correlations
    def load_name_corr(self, file):
        if not isfile(file):
            raise OSError('The name correlation dictionary could not be created as the provided parameter was not a vaild file: ' + str(file))

        name_correlation = {}
        with open(file) as f:
            for line in f:
                name, title = line.strip('\n').split('\t')
                name_correlation[title] = name

        return name_correlation


################################################################
####                   VISUAL DESC LOADER                   ####
################################################################

class VisualDescriptionReader(GenericReader):

    def load_file(self, file):
        # Just accrue list of csv files to load into the database.
        #   Little wasteful, but it allows the existing code to create
        #   the list desired.
        return file


################################################################
####                    Load All Data                       ####
################################################################
class Loader():

    @staticmethod
    @timed
    def make_database(folder):

        db = Database()
        # p = P ool(processes=3)
        
        # Load location data for associating the id's to the names.
        loc_files = (folder + '/devset_topics.xml', folder + '/poiNameCorrespondences.txt')
        location_dict = LocationReader().load_files(*loc_files)
        db.add_locations(location_dict)
        
        # Load visual description data.
        files = VisualDescriptionReader().load_folder(folder + '/descvis/img/')
        db.add_visual_descriptors(files)

        return db