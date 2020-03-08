# CSE515
Code developed for CSE 515 class.

The code was written using Python 3.7.0, but any recent Python 3 version should work.

This code has the following python-library dependencies:
  1. numpy 1.15.2
  2. pandas 0.23.4
  3. lxml 4.2.5
  4. scikit-learn 0.20.0
  5. python-igraph 0.7.1
  6. pycairo 1.18.0
      Requires cairo intallation. See https://www.cairographics.org/download/
  7. pillow 5.3.0

## Phase 1
The first phase of the project had every member of the group set up, individually, the basic functionality which will be necessary for later phases. The requirements included parsing the data from the files and using similarity and distance measures to find users, images, and locations that are similar based on term vectors. For my implementation, I produced a SQL Database to read the data into for efficient retrieval. Loader and Reader class operates on the data set folder to fill the SQL database. I also generated a database interface in python to provide abstraction from the direct database structure. Separate classes allow for creating vectors from the database, measuring distance between vectors, and evaluating similarity between vectors. A Neighbors class finds the k nearest vectors to one provided by using the aforementioned vector creation, distance, and similarity classes. Finally, an interface class provides a means for users to enter commands to load the database, retrieve entries, and get nearest neighbors to a vector.

## Phase 2
Phase 2 of the project included 7 major tasks.
1. Command at Prompt: task1 <term space> <k> <method>
Term Space: String text description type (user, photo, poi)
		K - Int number of latent semantics to return.
Method - Decomposition to run (PCA, SVD, LDA)
2. Command at Prompt: task2 <term space> <k> <method> <j> <id>
Term Space: String text description type (user, photo, poi)
K - Int number of latent semantics to return.
Method - Decomposition to run (PCA, SVD, LDA)
J - Int number of nearest terms to find.
ID - String id to find nearest neighbors for (id type depends on term space selected).
3. Command at Prompt: task3 <visual model> <k> <method>  <id>
Visual Model - String visual description model to use (CM, CM3x3, CN, CN3x3, CSD, GLRLM, GLRLM3x3, HOG, LBP, LBP3x3)
K - Int number of latent semantics to return.
Method - Decomposition to run (PCA, SVD, LDA)
ID - Int image id to find nearest neighbors for.
4. Command at Prompt: task4 <location id> <visual model> <k> <method>
	Location ID - Int location id to find semantics for.
Visual Model - String visual description model to use (CM, CM3x3, CN, CN3x3, CSD, GLRLM, GLRLM3x3, HOG, LBP, LBP3x3)
K - Int number of latent semantics to return.
Method - Decomposition to run (PCA, SVD, LDA)
5. Command at Prompt: task5 <location id> <k> <method>
Location ID - Int location id to find semantics for.
K - Int number of latent semantics to return.
Method - Decomposition to run (PCA, SVD, LDA)
6. Command at Prompt: task6 <k>
K - Int number of latent semantics to identify.
7. Command at Prompt: task7 <k>
K - Int number of non-overlapping groups to create.

## Phase 3
1. Command at Prompt: -task 1 --load <dataset location> --k #
Load: Location of the dataset.
K - Int number of similar images to maintain edges to in graph.
2. Command at Prompt: -task 2 --k #
K - Int number of clusters to form.
3. Command at Prompt: -task 3 --k #
K - Int number of dominant images to find.
4. Command at Prompt: -task 4 --k # --imgs image1 image2 image3
K - Int number of relevant images to find.
Imgs - list of space delimited images by int id to use.
5. Command at Prompt: -task 5 --layers # --hashes # --k # --imageId imageid
Layers - Int number of layers to create.
Hashes - Int number of hashes to create per layer for hash.
K - Int number of similar images to find.
ImageId - Int id of image to find nearest images to.
6. Command at Prompt: -task 6 --alg algorithm # --file filename
Alg - Algorithm to run.
File - The file containing the sample image Id and the labels assigned to it.

## Big shoutout to Zack, Tithi, Dhiren, Riddhi, Tithi Patel for the successful implementation.
