class Distance():
    
    @staticmethod
    def mahalonobis(vector1, table):
        # Create Covariance Matrix
        #   calculate covariance between each feature.
        # sqrt((v1-v2)*covariance*(v1-v2)^T)
        pass


    @staticmethod
    def quadratic(vector, table):
        # Calculate similarity matrix
        #   caluclate similarity between each feature.
        # sqrt((v1-v2)*covariance*(v1-v2)^T)
        pass


    @staticmethod
    def l_p_distance(p, vector, table, positional=False):

        distances = table.sub(vector, axis='columns').abs().pow(p).sum(1).pow(1/p)
        return distances

##
# Default Similarity class which uses dictionary keys (feature ids) to compare two vectors. Should
#   be used as the default similarity measure.
class Similarity():
    
    @staticmethod
    def intersection():
        pass
    
    @staticmethod
    def cosine_similarity():
        pass
    
    @staticmethod
    def dot_similarity(vector, table):
        return table.dot(vector.T)