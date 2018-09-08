##
#

class Distance():

    @staticmethod
    def get_feature_set(vector1, vector2):
        return list(set(vector1) | set(vector2))

    @staticmethod
    def l_n_distance(n, vector1, vector2):
        feature_set = Distance.get_feature_set(vector1, vector2)

        distance = 0
        for item in feature_set:
            distance += (abs(vector1[item] - vector2[item]))**n
        
        return distance ** (1/n)        
    
    @staticmethod
    def l_2_distance(vector1, vector2):
        return Distance.l_n_distance(2, vector1, vector2)