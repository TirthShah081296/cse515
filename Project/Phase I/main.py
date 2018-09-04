# The main class for executing phase I.
import sys
import loader, vectorize

def main(*argv):
    if len(argv) < 2:
        raise ValueError('No folder argument was found in args ' + str(argv))
    
    folder = argv[1]

    # load the data (Takes a while)
    location_map, images, users = loader.load_data_timed(folder)
    # Make vectors out of the data.



if __name__ == '__main__':
    #main(sys.argv)
    main(None, '/home/crosleyzack/Documents/CSE 515/repo/Project/Dataset')