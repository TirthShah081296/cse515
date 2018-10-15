from os.path import isfile, abspath, isdir
from loader import Loader
from database import Database
from neighbor import Neighbor
from decompose import Decompose

class Interface():

    def __init__(self):
        self.__database__ = None
        self.__valid_types__ = ['photo', 'user', 'poi']
        self.__vis_models__ = ['CM', 'CM3x3', 'CN', 'CN3x3',
                'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        self.__io__()



    def __io__(self):
        print("Welcome to the CSE 515 data software. Please enter a command.\
              \nEnter \"help\" for a list of commands.")
        while True:
            user_input = input("\nEnter a Command:$ ")
            user_input = user_input.split(' ')
            command = user_input[0]
            # Get method with this name - makes it easy to create new interface methods 
            #   without having to edit this method.
            try:
                method = getattr(self, command)
            except AttributeError:
                print('The command specified was not a valid command.\n')
            
            try:
                method(*user_input[1:])
            except Exception as e:
                print('Something went wrong while executing ' + str(method.__name__))
                print(str(e))



    def help(self, *args):
        """
        Command:\thelp
        Description:\tPrints the interface information about the program.
        """

        print("The following are valid commands to the program.")
        for item in dir(self):
            if not item.startswith('__'):
                method = getattr(self, item)
                print(method.__doc__)
        


    # takes a single argument - file to load.
    def load(self, *args):
        """
        Command:\tload <filepath>
        Description:\tLoads the database at that file path. If the file does not exist, will prompt to create a new database using the folder of a users choice.
        Arguments:
        \t<filepath> - A valid file path in the system.
        """

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
        
        self.__database__ = Loader.make_database(folder)
        print("Database loaded successfully.")



    # For calculating the latent semantics of the data (Task I)
    def task1(self, *args):
        """
        Command:\ttask1 <term space> <k> <method>
        Description:\tCalculates the top k latent semantics in the term space given a \
        methodology. Latent semantics will be presented in term-weight pairs.
        Arguments:
        \tTerm Space - What text description type to pull. (user, photo, location)
        \tK - Number of latent semantics to return.
        \tMethod - The decomposition method to use. (PCA, SVD, LDA)
        """

        if len(args) < 3:
            print("[ERROR] Not enough args were provided. Expected 3 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if len(args) > 3:
            print("[ERROR] Too many arguments were provided. Expected 3 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if not self.__database__:
            print("[ERROR] The Database must be loaded before this can be run.")
            print("\tCommand: load <filepath>")
            return
        
        try:
            term_space = args[0]
            k = int(args[1])
            method = args[2]
        except:
            print("[ERROR] One or more arguments could not be parsed: " + str(args))


        response = Decompose.decompose_text(term_space, k, method.lower(), self.__database__)
        print(response)


    # TODO - this should be implemented so it can follow Task 1, not be restarted
    #   from scratch.
    def task2(self, *args):
        """
        Command:\ttask2 <term space> <k> <method> <j> <id>
        Description:\tIdentifies the top k latent semantics uses an id in the term \
        space to identify the most related j ids.
        Arguments:
        \tTerm Space - What text description type to pull. (user, photo, location).
        \tK - Number of latent semantics to return.
        \tMethod - The decomposition method to use. (PCA, SVD, LDA).
        \tJ - Number of nearest terms to find.
        \tID - The id to find nearest neighbors to using the latent semantics.
        """
        if len(args) < 5:
            print("[ERROR] Not enough args were provided. Expected 5 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if len(args) > 5:
            print("[ERROR] Too many arguments were provided. Expected 5 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if not self.__database__:
            print("[ERROR] The Database must be loaded before this can be run.")
            print("\tCommand: load <filepath>")
            return
        
        try:
            term_space = args[0]
            k = int(args[1])
            method = args[2]
            j = int(args[3])
            anid = args[4]
        except:
            print("[ERROR] One or more arguments could not be parsed: " + str(args))

        # YOUR FUNCTION HERE. #####################################################
        



    # TODO - This should also be reimplemented so the query for j nearest can be done
    #   after the initial query, rather than from scratch.
    def task3(self, *args):
        """
        Command:\ttask3 <vis model> <k> <method> <j> <id>
        Description:\tIdentifies k latent semantics using model and methodology. Given an \
        id, finds the top j most related items to that id.
        Arguments:
        \tVisual Space - What visual description model to pull. ('CM', 'CM3x3', 'CN', \
        'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3')
        \tK - Number of latent semantics to return.
        \tMethod - The decomposition method to use. (PCA, SVD, LDA).
        \tJ - Number of nearest terms to find.
        \tID - The id to find nearest neighbors to using the latent semantics.
        """
        if len(args) < 5:
            print("[ERROR] Not enough args were provided. Expected 5 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if len(args) > 5:
            print("[ERROR] Too many arguments were provided. Expected 5 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if not self.__database__:
            print("[ERROR] The Database must be loaded before this can be run.")
            print("\tCommand: load <filepath>")
            return
        
        try:
            vis_model = args[0]
            k = int(args[1])
            method = args[2]
            j = int(args[3])
            anid = args[4]
        except:
            print("[ERROR] One or more arguments could not be parsed: " + str(args))

        # WRITE CODE IN THESE FUNCTIONS #####################################################
        Decompose.decompose_vis(vis_model, k, method, self.__database__) # Get latent semantics.
        # Get nearest items from latent semantics. Neighbor.knn may be useful for you.




    def task4(self, *args):
        """
        Command:\ttask4 <locationid> <vis model> <k> <method>
        Description:\tIdentifies the top k latent semantics for the given location \
        and lists the five most related locations.
        Arguments:
        \tLocation Id - A valid location id. (1 - 30)
        \tVisual Space - What visual description model to pull. ('CM', 'CM3x3', 'CN', \
        'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3').
        \tK - Number of latent semantics to identify.
        \tMethod - The decomposition method to use. (PCA, SVD, LDA).
        """
        if len(args) < 4:
            print("[ERROR] Not enough args were provided. Expected 4 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if len(args) > 4:
            print("[ERROR] Too many arguments were provided. Expected 4 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if not self.__database__:
            print("[ERROR] The Database must be loaded before this can be run.")
            print("\tCommand: load <filepath>")
            return
        
        try:
            locationid = int(args[0])
            vis_model = args[1]
            k = int(args[2])
            method = args[3]
        except:
            print("[ERROR] One or more arguments could not be parsed: " + str(args))

        # WRITE CODE IN THESE FUNCTIONS #####################################################
        Decompose.decompose_loc_vis(vis_model, k, method, locationid, self.__database__) # Get latent semantics.
        # Get nearest 5 locations from latent semantics. Neighbor.knn may be useful for you.


    
    def task5(self, *args):
        """
        Command:\ttask5 <locationid> <k> <method>
        Description:\tIdentifies the top k latent semantics for the location id \
        across all models and identifies the top 5 related locations to the \
        latent semantics.
        Arguments:
        \tLocation Id - A valid location id. (1 - 30)
        \tK - Number of latent semantics to identify.
        \tMethod - The decomposition method to use. (PCA, SVD, LDA).
        """
        if len(args) < 3:
            print("[ERROR] Not enough args were provided. Expected 3 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if len(args) > 3:
            print("[ERROR] Too many arguments were provided. Expected 3 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if not self.__database__:
            print("[ERROR] The Database must be loaded before this can be run.")
            print("\tCommand: load <filepath>")
            return
        
        try:
            locationid = int(args[0])
            k = int(args[1])
            method = args[2]
        except:
            print("[ERROR] One or more arguments could not be parsed: " + str(args))

        # WRITE CODE IN THESE FUNCTIONS #####################################################
        Decompose.decompose_loc(k, method, locationid, self.__database__) # Get latent semantics.
        # Get nearest 5 locations by latent semantics. Neighbor.knn may be useful for you.

    


    def task6(self, *args):
        """
        Command:\ttask6 <k>
        Description:\tCreates a location - location similarity matrix, performs SVD, \
        and reports the top k latent semantics.
        Arguments:
        \tK - Number of latent semantics to identify.
        """
        if len(args) < 1:
            print("[ERROR] Not enough args were provided. Expected 1 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if len(args) > 1:
            print("[ERROR] Too many arguments were provided. Expected 1 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if not self.__database__:
            print("[ERROR] The Database must be loaded before this can be run.")
            print("\tCommand: load <filepath>")
            return
        
        try:
            k = int(args[0])
        except:
            print("[ERROR] One or more arguments could not be parsed: " + str(args))

        # YOUR FUNCTION HERE. #####################################################

    


    def task7(self, *args):
        """
        Command:\ttask7 <k>
        Description:\tCreates a user-image-location tensor, performs rank k CP \
        decomposition of this tensor, and creates k non-overalapping groups of \
        users, images, and locations based on the discovered latent semantics.
        Arguments:
        \tK - Number of non-overlapping groups to create.
        """
        if len(args) < 1:
            print("[ERROR] Not enough args were provided. Expected 1 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if len(args) > 1:
            print("[ERROR] Too many arguments were provided. Expected 1 but got " + str(len(args)))
            print("\targs = " + str(args))
            return
        if not self.__database__:
            print("[ERROR] The Database must be loaded before this can be run.")
            print("\tCommand: load <filepath>")
            return
        
        try:
            k = int(args[0])
        except:
            print("[ERROR] One or more arguments could not be parsed: " + str(args))

        # YOUR FUNCTION HERE. #####################################################




    def quit(self, *args):
        """
        Command:\tquit
        Description:\tExits the program and performs necessary cleanup.
        """
        exit(1)

if __name__ == '__main__':
    Interface()