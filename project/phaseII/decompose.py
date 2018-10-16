from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD as SVD
from sklearn.preprocessing import StandardScaler
from pandas import DataFrame
from util import timed

class Decompose():

    @staticmethod
    def svd(table, k, database):
        matrix = SVD(n_components=k)
        out = matrix.fit_transform(table)
        return out


    @staticmethod
    def pca(table, k, database):
        matrix = PCA(n_components=k)
        out = matrix.fit_transform(table)
        return out


    @staticmethod
    def lda(table, k, database):
        matrix = LDA(n_components=k)
        out = matrix.fit_transform(table)
        return out


    @staticmethod
    def decompose_text(term_space, k, method, database):
        table = database.get_txt_desc_table(term_space)
        
        if method == 'pca':
            f = Decompose.pca
        elif method == 'svd':
            f = Decompose.svd
        elif method == 'lda':
            f = Decompose.lda
        
        # put table in appropriate format - transpose and standardize.
        indexes = table.columns
        table = table.T
        table = StandardScaler().fit_transform(table)

        out = f(table, k, database)
        return DataFrame(out, index=indexes)


    @staticmethod
    @timed
    def decompose_vis(model, k, method, database):
        table = database.get_vis_table(model=model)
        raise NotImplementedError # TASK 3 IMPLEMENT
    

    @staticmethod
    @timed
    def decompose_loc_vis(model, k, method, locationid, database):
        table = database.get_vis_table(model=model, locationid=locationid)
        raise NotImplementedError # TASK 4 IMPLEMENT
    

    @staticmethod
    @timed
    def decompose_loc(k, method, locationid, database):
        table = database.get_vis_table(locationid=locationid)
        raise NotImplementedError # TASK 5 IMPLEMENT