from os.path import isfile, abspath, isdir
from loader import Loader
from database import Database
from neighbor import Neighbor
from decompose import Decompose
from distance import Scoring
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD as SVD
import numpy as np
from pandas import DataFrame as df
import xml.etree.ElementTree as ET
from operator import itemgetter

class Interface():

    def __init__(self):
        self.__database__ = None
        self.__valid_types__ = ['photo', 'user', 'poi']
        self.__vis_models__ = ['CM', 'CM3x3', 'CN', 'CN3x3',
                'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        self.__io__()

    

    def __print_latent_semantics__(self, table):
        """
        Pretty prints out the latent semantics.
        :param DataFrame table: The latent semantic vectors. Columns are individual vectors, rows are features.
        """
        for i, col_id in enumerate(table):
            column = table[col_id]
            column = column.sort_values(ascending=False)
            print('-'*50)
            print("LATENT SEMANTIC " + str(i))
            print('-'*50)
            print(column)



    def __io__(self):
        print("Welcome to the CSE 515 data software. Please enter a command.\
              \nEnter \"help\" for a list of commands.")
        while True:
            user_input = input("\nEnter a Command:$ ")
            user_input = user_input.split(' ')
            command = user_input[0]
            command.replace('_', '')
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

        response = Decompose.txt_latent_semantics(term_space, k, method.lower(), self.__database__)
        self.__print_latent_semantics__(response)



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

        reduced_table = Decompose.decompose_text(term_space, k, method.lower(), self.__database__)
        # Get nearest items from latent semantics. Neighbor.knn may be useful for you.
        pass



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
        reduced_table = Decompose.decompose_vis(vis_model, k, method, self.__database__) # Get latent semantics.
        # Get nearest items from latent semantics. Neighbor.knn may be useful for you.
        pass



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
        reduced_table = Decompose.decompose_loc_vis(vis_model, k, method, locationid, self.__database__) # Get latent semantics.
        # Get nearest 5 locations from latent semantics. Neighbor.knn may be useful for you.
        pass


    
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
        reduced_table = Decompose.decompose_loc(k, method, locationid, self.__database__) # Get latent semantics.
        reduced_table.to_csv('Image-semantic_task5.csv')
        reducedLocations = dict()  # A dictionary that has locationid as the key and the reduced tables as the values.
        # reducedLocations[locationid] = reduced_table
        similarityScore = dict()
        for i in [x for x in range(1,31)]:
            if i == locationid:
                reducedLocations[i] = reduced_table
            else:
                reducedLocations[i] = Decompose.decompose_loc(k, method, i, self.__database__)
            sim = cosine_similarity(reduced_table,reducedLocations[i])
            # The dot_similarity (matrix, matrix) returns a 2D array that has ids of one location as rows, and another location's id as columns.
            # The values are the similarity between each id (Just like a similarity matrix).

            similarityScore[i] = Scoring.score_matrix(sim)
        orderedSimilarityList = sorted(similarityScore, key=similarityScore.__getitem__) # returns a list containing the Locations ids in the increasing order of the similarity
        orderedSimilarityList.reverse()  # Reverse the list to get it in the decreasing order
        print (similarityScore)
        print("The most related 5 locations are:")
        for i in range(5):
            print("Id: ", orderedSimilarityList[i], "Score: ", similarityScore[orderedSimilarityList[i]])
        # sim = cosine_similarity(reduced_table, reducedLocations[1])
        # numpy.savetxt("similarity.csv", sim, delimiter= ",")
        # sim.to_csv('similarity.csv')
        # reduced_table.iloc[0].to_csv('row.csv')
        # reducedLocations[1].to_csv('thetable.csv')


        # print ("Score ", similarityScore)

        # csv_out = csv.writer(open("dictionary.csv", "w"))
        # pickle.dump(reducedLocations, pickle_out)
        # pickle_out.close()
        # for key, val in reducedLocations.items():
        #     csv_out.writerow([key, val])
        # Get nearest 5 locations by latent semantics. Neighbor.knn may be useful for you.
        # pass
    


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

        # First getting all the location tables having all the visual discriptors.

        # IMP NOTE: Remember to change all the static values after the test data arrives.
        all_location_tables = dict()
        for id in range(1,31):
            all_location_tables[id] = Database.get_vis_table(self.__database__,locationid=id)
        # print(all_location_tables.keys(), len(all_location_tables))
        # all_location_tables[2].to_csv('atable.csv')

        # Start finding the similarity between each pair of locations and store the results into a dictionary.
        if isfile('./all_similarities.npy'):
            all_similarities = np.load('all_similarities.npy').item()
        else:
            all_similarities = dict()
            for i in range(1,31):
                for j in range(i,31):
                    cos_sim = cosine_similarity(all_location_tables[i], all_location_tables[j])
                    all_similarities[(i, j)] = Scoring.score_matrix(cos_sim)
                    all_similarities[(j, i)] = all_similarities[(i, j)]
            np.save('all_similarities.npy', all_similarities)

        # print(all_similarities)
        # print(len(all_similarities))
        similarity_matrix = df(index=range(1,31),columns=range(1,31))
        for i in range(1,31):
            sim_list = list()
            for j in range(1,31):
                sim_list.append(all_similarities[(i, j)])
            similarity_matrix.loc[i] = sim_list
        similarity_matrix.to_csv('Task6_SimilarityMatrix.csv')
        print("Location-Location Similarity matrix created...")

        reduced = SVD(n_components=k)
        reduced_table = reduced.fit_transform(similarity_matrix)
        VTranspose = df(data=reduced.components_, index=range(1,k+1),columns=range(1,31))
        # reduced_table.to_csv('task6reducedtable.csv')
        # np.savetxt("task6reducedtable.csv", reduced_table, delimiter=",")
        VTranspose.to_csv('task6transposetable.csv')
        # np.savetxt("task6transposetable.csv", VTranspose, delimiter=",")

        filename = './devset_topics.xml'
        tree = ET.parse(filename)
        root = tree.getroot()
        location_name = dict()
        location_dict = dict()
        i = 0

        while i < len(root):
            v1 = int(root[i][0].text)
            v2 = root[i][1].text
            location_name[v1] = v2
            i += 1

        print("Top k latent semantics in form of their location-weight pair are:")
        for index, row in VTranspose.iterrows():
            for j in range(1, 31):
                loc = location_name[j]
                location_dict[loc] = row[j]
            sorted_location_dict = sorted(location_dict.items(), key=itemgetter(1), reverse=True)

            print("latent semantic " + str(index) + " : " + str(sorted_location_dict))

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

        # First getting the terms of all the user ids, image ids and location ids into dictionaries.
        # A very naive code implementation.
        # Add these files to the PhaseII folder, or mention the path to the files.
        userFile = './devset_textTermsPerUser.txt'
        imageFile = './devset_textTermsPerImage.txt'
        locationFile = './devset_textTermsPerPOI.wFolderNames.txt'

        userDictionary = dict()  # contains userid as the key and terms as its terms as the value.
        imageDictionary = dict()  # contains imageid as the key and terms as its terms as the value.
        locationDictionary = dict()  # contains locationid as the key and terms as its terms as the value.

        uflag = 1
        utermlist = list()
        uturnon = 0
        ucurrent_id = ""
        with open(userFile, encoding = 'latin-1') as f:
            for line in f:
                for word in line.split():
                    if uflag == 1:
                        if not word.startswith('"'):
                            if uturnon:
                                userDictionary[ucurrent_id] = utermlist
                                utermlist.clear()
                            ucurrent_id = word
                            uturnon = 1
                            continue
                        utermlist.append(word)
                        uflag = 2
                        continue
                    if uflag == 2:
                        uflag = 3
                        continue
                    if uflag == 3:
                        uflag = 4
                        continue
                    if uflag == 4:
                        uflag = 1
                        continue
        userDictionary[ucurrent_id] = utermlist

        iflag = 1
        itermlist = list()
        iturnon = 0
        icurrent_id = ""
        with open(imageFile, encoding='latin-1') as f:
            for line in f:
                for word in line.split():
                    if iflag == 1:
                        if not word.startswith('"'):
                            if iturnon:
                                imageDictionary[icurrent_id] = itermlist
                                itermlist.clear()
                            icurrent_id = word
                            iturnon = 1
                            continue
                        itermlist.append(word)
                        iflag = 2
                        continue
                    if iflag == 2:
                        iflag = 3
                        continue
                    if iflag == 3:
                        iflag = 4
                        continue
                    if iflag == 4:
                        iflag = 1
                        continue
        imageDictionary[icurrent_id] = itermlist
        # print(userDictionary)
        # print(len(imageDictionary.keys()))
        # print(len(userDictionary.keys()))

        locNames = dict()
        tree = ET.parse('./devset_topics.xml')
        root = tree.getroot()
        for elem1 in root:
            locNames[elem1[1].text] = int(elem1[0].text)

        # print (locNames)
        lflag = 1
        ltermlist = list()
        lturnon = 0
        lcurrent_id = ""
        with open(locationFile, encoding='utf8') as f:
            for line in f:
                for word in line.split():
                    if lflag == 1:
                        if word.startswith('"'):
                            ltermlist.append(word)
                            # current_term = word
                            lflag = 2
                            continue
                        if lturnon:
                            locationDictionary[lcurrent_id] = ltermlist
                            ltermlist.clear()
                        lcurrent_id = locNames[word]
                        lturnon = 1
                        # idlist.append(current_id)
                        # if turnon == 1:
                        #     turnon = 0
                        # else:
                        #     if current_id == int(sys.argv[1]):
                        #         turnon = 1
                        lflag = 5
                        continue
                    elif lflag == 2:
                        # tflist.append(word)
                        # main_dict[(current_id, current_term, 'TF')] = float(word)
                        lflag = 3
                        continue
                    elif lflag == 3:
                        # dflist.append(word)
                        # main_dict[(current_id, current_term, 'DF')] = float(word)
                        lflag = 4
                        continue
                    elif lflag == 4:
                        # idflist.append(word)
                        # print current_id, current_term
                        # main_dict[(current_id, current_term, 'TF-IDF')] = float(word)
                        lflag = 1
                        continue
                    elif lflag == 5:
                        if word.startswith('"'):
                            ltermlist.append(word)
                            # if turnon == 1:
                            #     reqTermList.append(word)
                            # current_term = word
                            lflag = 2
                            continue
                        continue
        locationDictionary[lcurrent_id] = ltermlist

        # print(len(locationDictionary))
        # print(len(userDictionary))
        # print(len(imageDictionary))

        # At this point the dictionaries have a list of terms for each ids


    def quit(self, *args):
        """
        Command:\tquit
        Description:\tExits the program and performs necessary cleanup.
        """
        exit(1)

if __name__ == '__main__':
    Interface()