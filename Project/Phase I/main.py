# The main class for executing phase I.
#
# TODO
#   1. Figure how to get the terms w/ highest similarity contribution.
#   2. Ask if 'Nearest' is calculated using a distance measure of our choice.
#   3. Where does data come from for 4, 5.
#
#
import sys
from os.path import isfile, abspath
from functools import wraps
from neighbor import Neighbor
from vectorize import Vectorizer
from loader import Loader, SQLDatabase

class Interface():

    def __init__(self):
        self.database = None
        self.valid_types = ['photo', 'user', 'poi']
        self.valid_txt_models = ['tf', 'idf', 'tf-idf']
        self.valid_vis_models = ['CM', 'CM3x3', 'CN', 'CN3x3',
                'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        self.loader = Loader()
        self.io()
    
    def io(self):
        
        print("Welcome to the CSE 515 data software. Please enter a command.\
              \nEnter \"help\" for a list of commands.")
        while True:
            user_input = input("\nEnter a Command:$ ")
            user_input = user_input.split(' ')

            if user_input[0] == 'help':
                self.help()
            elif user_input[0] == 'load':
                self.load(*user_input[1:])
            elif user_input[0] == 'get':
                self.get(*user_input[1:])
            elif user_input[0] == 'quit':
                self.quit()
            elif user_input[0] == 'nearest-text':
                self.nearest_text(*user_input[1:])
            elif user_input[0] == 'nearest-visual':
                raise NotImplementedError('This functionality hasn\'t been added yet.')
            else:
                raise ValueError('The command specified was not a valid command.')

    ##
    # takes no arguments. Doesn't fail on any argument input.
    def help(self):
        print("The following are valid commands to the program.\
                \n\tload <filepath>\
                \n\tLoads the database at that file path. If the file does not exist, will prompt to create a new database using the folder of a users choice.\
                \n\t\t<filepath> - A valid file path in the system. \
                \n\tget <item type> <item>\
                \n\tGets the data from the database related to the item specified.\
                \n\t\t<item type> - The type of item we are looking for neighbors to. Valid options include 'photo', 'user', and 'poi'.\
                \n\t\t<item> - The id of the item in question. This is either a user id, photo id, and point of interest id.\
                \n\tnearest-text k <item type> <item> <model>\
                \n\tcalculates the nearest k items to the specified item using textual descriptors. If the item type, item, or model aren't valid it will return an error message.\
                \n\t\t<item type> - The type of item we are looking for neighbors to. Valid options include 'photo', 'user', and 'poi'.\
                \n\t\t<item> - The id of the item in question. This is either a user id, photo id, and point of interest id.\
                \n\t\t<model> - The distance method to use. Valid options include 'tf', 'idf', and 'tf-idf'.\
                \n\tnearest-visual k <item type> <item> <model>\
                \n\tCalculates the nearest k items to the specified item using visual descriptors. If the item type, item, or model aren't valid it will return an error message.\
                \n\t\t<item type> - The type of item we are looking for neighbors to. Valid options include 'photo', 'user', and 'poi'.\
                \n\t\t<item> - The id of the item in question. This is either a user id, photo id, and point of interest id.\
                \n\t\t<model> - The distance method to use. Valid options include 'CM', 'CM3x3', 'CN', 'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', and 'LBP3x3'.\
                \n\tquit\
                \n\t\texits the program and performs necessary cleanup.\
                \n\n")

    ##
    # takes a single argument - file to load.
    def load(self, *args):

        if len(args) < 1:
            print("[ERROR] Not enough args given to load parameter.")
            print("\targs = " + str(args))
            return
        if len(args) >= 2:
            print("[ERROR] Too many args given to load parameter.")
            print("\targs = " + str(args))
            return
        
        filename = abspath(args[0])

        if not isfile(filename):
            print("[WARNING] The file provided does not exist.")
            user_input = input("Would you like to create and load it? (y/n):$ ")
            if user_input.lower()[0] == 'n':
                return
            elif user_input.lower()[0] == 'y':
                user_input = input("Please specify the directory of the dataset file to load:$ ")
                self.database = self.loader.make_database(filename)
                self.loader.load_database(user_input, self.database, num_threads=0)
            else:
                print("[ERROR] Please enter a valid input.")
        else:
            self.database = self.loader.make_database(filename)

    ##
    # retrieve an item from the database.
    def get(self, *args):

        if not self.database:
            print("[ERROR] The database must be loaded for this action.")
            return

        if not len(args) is 2:
            print("Get expected 2 arguments but got " + str(len(args)) + ".")
            print("\targs = " + str(args))
            return
        
        item_type = args[0]
        if item_type == 'photo':
            item = self.database.get_photo(args[1])
            cols = self.database.get_photo_cols()
        elif item_type == 'user':
            item = self.database.get_user(args[1])
            cols = self.database.get_user_cols()
        elif item_type == 'poi':
            item = self.database.get_location(args[1])
            cols = self.database.get_location_cols()
        else:
            print("[ERROR] Type specified was invalid.")
        
        if item is None:
            print("No value could be found in the database matching those parameters.")
            return

        # Clean up cols - Returns as huge set of tuples we want to remove.
        cols = [col[0] for col in cols.description]

        for i, tple in enumerate(item):
            print(str(i) + ").")
            for name, value in zip(cols, tple):
                print("\t" + str(name) + '\t' + str(value))

    ##
    # 
    def quit(self, *args):
        self.database.commit()
        self.database.close()
        exit()

    ##
    # Takes a value for k, <item type>, <item>, <model>
    def nearest_text(self, *args):
        
        if not self.database:
            print("[ERROR] The database must be loaded for this action.")
            return

        if not len(args) is 4:
            print("Nearest Text expected 4 arguments but got " + str(len(args)) + ".")
            print("\targs = " + str(args))
            return

        # Get the first argument
        try:
            k = int(args[0])
        except:
            print("[ERROR] K Value provided is invalid.")
            print("\tk = " + str(args[0]))
            return
        
        # Get the type of item we are considering.
        item_type = args[1]
        if not item_type in self.valid_types:
            print("[ERROR] Item Type value provided was invalid.")
            print("\tItem Type = " + str(args[1]))
            return
        
        # Get the model to use. We do this before the item as it is easier
        #   to differentiate valid from invalid
        model_type = args[3]
        if not model_type in self.valid_txt_models:
            print("[ERROR] Model Type value provided was invalid.")
            print("\tModel Type = " + str(args[3]))
            return
        
        nearest = Neighbor.get_nearest_neighbors(k, args[2], model_type, item_type, self.database)


    def nearest_visual(self, *args):
        
        if not self.database:
            print("[ERROR] The database must be loaded for this action.")
            return


if __name__ == '__main__':
    Interface()