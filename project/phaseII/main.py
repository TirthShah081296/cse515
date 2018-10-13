# The interface for executing phase I.
#
# TODO
#   1. Figure how to get the terms w/ highest similarity contribution?
#           Term that contributes the least distance / highest similarity.
#   2. Ask if 'Nearest' is calculated using a distance measure of our choice?
#           Yes, but justify your selection.
#   3. Where does data come from for 4, 5?
#           NOTE: P5 is aggregating all 10 models of P4.

from os.path import isfile, abspath, isdir
from loader import Loader
from database import Database
from vectorize import Vectorizer
from neighbor import Neighbor
from decompose import Decompose

class Interface():

    def __init__(self):
        self.database = None
        self.valid_types = ['photo', 'user', 'poi']
        self.valid_txt_models = ['tf', 'df', 'tf-idf']
        self.valid_vis_models = ['CM', 'CM3x3', 'CN', 'CN3x3',
                'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3', 'ALL']
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
            elif user_input[0] == 'vector-space':
                self.vector_space(*user_input[1:])
            else:
                raise ValueError('The command specified was not a valid command.')

    ##
    # takes no arguments. Doesn't fail on any argument input.
    def help(self):
        print("The following are valid commands to the program.\
                \n\tload <filepath>\
                \n\tLoads the database at that file path. If the file does not exist, will prompt to create a new database using the folder of a users choice.\
                \n\t\t<filepath> - A valid file path in the system. \
                \n\tvector-space <>\
                \n\t\tTerm Space - (user, photo, location)\
                \n\t\tK - number of latent semantics to return\
                \n\t\tMethod - (PCA, SVD, LDA)\
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
        
        folder = abspath(args[0])

        if not isdir(folder):
            print("[ERROR] The provided path was not a folder, and therefore not a valid data directory.")
            return
        
        self.database = self.loader.make_database(folder)

    
    def vector_space(self, *args):

        if len(args) < 3:
            print("[ERROR] Not enough args were provided.")
            print("\targs = " + str(args))
            return
        if len(args) > 3:
            print("[ERROR] Too many arguments were provided.")
            print("\targs = " + str(args))
            return

        if not self.database:
            print("[ERROR] The Database must be loaded before this can be run.")
            return
        
        term_space = args[0]
        k = int(args[1])
        method = args[2]

        response = Decompose.decompose(term_space, k, method.lower(), self.database)
        


if __name__ == '__main__':
    Interface()