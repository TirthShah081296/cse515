#! /bin/usr/python3.6

import igraph
from os.path import isfile
from util import timed

class Graph():

    def __init__(self, graph=None, similarity=None):
        if graph:
            self.__graph__ = graph
        else:
            self.__graph__ = igraph.Graph(directed=True)

        if not similarity is None:
            self.add_similarity(similarity)


    def add_edge(self, tx, start_node, end_node, edge_weight):
        """
        Creates an edge from one photo to another with a defined edge weight.
        :param int start: Id of photo for out edge.
        :param float weight: Weight of edge. In this case, similarity value.
        :param int end: Id of photo for in edge.
        """
        pass


    @timed 
    def add_similarity(self, similarity):
        """
        Adds similarity matrix information to database. Adds all ~8900 photos and the weighted edges
        to their k most similar partners.
        :param Pandas.Dataframe similarity: photo-photo similarity matrix
        """
        assert(all(similarity.index == similarity.columns))
        # TODO photo too large for C int, breaks igraph lib.
        photos = similarity.index
        self.__graph__.add_vertices(photos)
        # get the nearest neighbors similarity wise to each image and add to database.
        for photo in photos:
            photo = int(photo)
            row = similarity.loc[photo].sort_values(ascending=False)
            edges = [(photo, int(other)) for other in row.index]
            weights = [other for other in row]
            self.__graph__.add_edges(edges)
            self.__graph__.es['weight'] = weights
        
        return
        


    def edge(self, src, end):
        """
        """
        return self.__graph__.es.find(_source=src, _target=end)



    def edge_weight(self, edge=None, source=None, end=None):
        """
        """
        if source and end:
            edge = self.edge(source, end)
        return edge['weight']



    def subgraph(self, out_degree):
        """
        Returns a subgraph of the main graph with max out degree of k.
        When removing edges it keeps the largest k.
        :param int out_degree: number of out edges for each vertex.
        """
        subgraph = self.__graph__.copy()
        for vertex in subgraph.vs:
            edges = [subgraph.es[i] for i in subgraph.incident(vertex, mode=igraph.OUT)]
            while vertex.outdegree > out_degree:
                # find and remove edge with smallest weight.
                # NOTE: Removing edge is simple as getting the object and calling .delete()
                min_edge = min(edges, key=lambda a: a['weight'])
                min_edge.delete()
        return subgraph

    
    def neighbors(self, node):
        """
        Returns the neighboring nodes to this one with the edge weight between them.
        :param int node: id of node to find neighbors of.
        """
        pass

    
    def specify_cluster(self, node, cluster):
        """
        Adds cluster label to the node.
        :param int node: node id to add label to.
        :param str cluster: cluster identifier to add to node.
        """
        pass
    

    def drop(self):
        """
        Deletes all graph data. Use with Caution!
        """
        pass

    
    def save(self, location):
        """
        Saves graph to binary for easy loading later.
        :param path location: location to save to.
        """
        if not isfile(location):
            raise FileNotFoundError('The location specified does not exist: %s' % location)
        self.__graph__.write_pickle(fname=location) 
    

    def load(self, location):
        """
        Load graph from binary.
        :param path location: location to read from. 
        """
        if not isfile(location):
            raise FileNotFoundError('The location specified does not exist: %s' % location)
        self.__graph__ = igraph.Graph.Read_Pickle(fname=location) 