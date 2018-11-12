#! /bin/usr/python3.6
from loader import Loader
from distance import Similarity
from graph import Graph
from os.path import abspath, isdir
import argparse
from util import timed


class Interface():

    def __init__(self):
        self.__database__ = None
        self.__graph__ = None 
        self.__valid_types__ = ['photo', 'user', 'poi']
        self.__vis_models__ = ['CM', 'CM3x3', 'CN', 'CN3x3',
                'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        self.__io__()
    

    def __io__(self):
        print("Welcome to the CSE 515 data software. Please enter a command.\
              \nEnter \"help\" for a list of commands.")

        def __filepath__(parser, arg):
            if not isdir(arg):
                parser.error("The directory %s doesn't exist." %arg)
            else:
                return True

        parser = argparse.ArgumentParser()
        parser.add_argument('-task', type=int, choices=range(1,6), required=True, metavar='#')
        parser.add_argument('--k', type=int, metavar='#')
        parser.add_argument('--visualize', action='store_true', default=True)
        parser.add_argument('--load', type=str, metavar='filepath')
        parser.add_argument('--layers', type=int, metavar='L')
        parser.add_argument('--hashes', type=int, metavar='k')
        parser.add_argument('--cluster', type=int, metavar='c')
        parser.add_argument('--vectors', type=list) # Not sure how this works still.
        while True:
            user_input = input("\nEnter a Command:$ ")
            user_input = user_input.split(' ')
            args = parser.parse_args(user_input)

            # call load if indicated in the command.
            if args.load:
                self.load(args)

            # Get method with this name - makes it easy to create new interface methods 
            #   without having to edit this method.
            try:
                method = getattr(self, 'task' + str(args.task))
            except AttributeError:
                print('The command specified was not a valid command.\n')
            
            try:
                method(args)
            except Exception as e:
                print('Something went wrong while executing ' + str(method.__name__))
                print(str(e))



    def help(self, args):
        """
        Command:\   thelp
        Description:\tPrints the interface information about the program.
        """

        print("The following are valid commands to the program.")
        for item in dir(self):
            if not item.startswith('__'):
                method = getattr(self, item)
                print(method.__doc__)
        


    # takes a single argument - file to load.
    def load(self, args):
        """
        Command:\tload <filepath>
        Description:\tLoads the database at that file path. If the file does not exist, will prompt to create a new database using the folder of a users choice.
        Arguments:
        \t<filepath> - A valid file path in the system.
        """
        
        folder = abspath(args.load)

        if not isdir(folder):
            print("[ERROR] The provided path was not a folder, and therefore not a valid data directory.")
            return
        
        self.__database__ = Loader.make_database(folder)
        print("Database loaded successfully.")



    @timed
    def task1(self, args):
        if args.k == None:
            raise ValueError('Parameter K must be defined for task 1.')
        if args.load:
            all_photos = self.__database__.get_vis_table()
            print("All Photos w/ all models collected.")
            similarity = Similarity.cosine_similarity(all_photos, all_photos)
            print("Similarity matrix created.")
            self.__graph__ = Graph(similarity=similarity)
            print("Graph loaded.")
            self.__graph__.save('graph.pickle')
        # Get subgraph
        k = int(args.k)
        # visualize graph.


    def quit(self, *args):
        """
        Command:\tquit
        Description:\tExits the program and performs necessary cleanup.
        """
        exit(1)

if __name__ == '__main__':
    Interface()
