from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD as SVD
from pandas import DataFrame
from util import timed
from functools import wraps



def reindex(f):
    """
    Wrapper to grab indexes from initial table and add them to the reduced table.
    """
    @wraps(f)
    def wrapper(table, k):
        indexes = table.index
        out = f(table, k)
        return DataFrame(out, index=indexes)
    return wrapper

class Decompose():

    @staticmethod
    @reindex
    def svd(table, k):
        """
        Decompose table into matrices U . S . V = table.
        :param DataFrame table: table to decompose.
        :param int k: number of components to get from decomposition.
        :return DataFrame reduced matrix.
        """
        matrix = SVD(n_components=k)
        out = matrix.fit_transform(table)
        return out

    @staticmethod
    @reindex
    def pca(table, k):
        """
        Decompose table into matrices V . L . V^{T} = table and returns the obj matrix.
        :param DataFrame table: table to decompose.
        :param int k: number of components to get from decomposition.
        :return DataFrame reduced matrix.
        """
        matrix = PCA(n_components=k)
        out = matrix.fit_transform(table)
        return out


    @staticmethod
    @reindex
    def lda(table, k):
        """
        Decompose table into matrices U . S . V^{T} = table and returns the obj matrix.
        :param DataFrame table: table to decompose.
        :param int k: number of components to get from decomposition.
        :return DataFrame reduced matrix.
        """
        matrix = LDA(n_components=k)
        out = matrix.fit_transform(table)
        return out

    
    @staticmethod
    def switchboard(table, k, method):
        """
        Selects the method to run based on the method name. Useful for every
        :param DataFrame table: the table to reduce.
        :param int k: The number of latent semantics to use.
        :param str method: The method of decomposition to use (pca, lda, svd)
        :return DataFrame with reduced objects.
        """
        if method == 'pca':
            f = Decompose.pca
        elif method == 'svd':
            f = Decompose.svd
        elif method == 'lda':
            f = Decompose.lda
        else:
            raise ValueError("Invalid decomposition method specified: " + method)

        return f(table, k)


    @staticmethod
    def txt_latent_semantics(term_space, k, method, database):
        """
        Used by task1 - Identifies the first k latent semantics
        :param str term_space: The type of term space to grab. (user, photo, location)
        :param int k: The number of latent semantics to use.
        :param str method: The method of decomposition to use (pca, lda, svd)
        :return DataFrame with reduced objects.
        """
        table = database.get_txt_desc_table(term_space)
        # Takes transpose of table to find the latent semantic vectors, instead of object vectors.
        reduced_table = Decompose.switchboard(table.T, k, method)
        return reduced_table


    @staticmethod
    def decompose_text(term_space, k, method, database):
        """
        Used by task2.
        :param str term_space: The type of term space to grab. (user, photo, location)
        :param int k: The number of latent semantics to use.
        :param str method: The method of decomposition to use (pca, lda, svd)
        :return DataFrame with reduced objects.
        """
        table = database.get_txt_desc_table(term_space)
        return Decompose.switchboard(table, k, method)


    @staticmethod
    def decompose_vis(model, k, method, database):
        table = database.get_vis_table(model=model)
        return Decompose.switchboard(table, k, method)
    

    @staticmethod
    def decompose_loc_vis(model, k, method, locationid, database):
        table = database.get_vis_table(model=model, locationid=locationid)
        return Decompose.switchboard(table, k, method)
    

    @staticmethod
    def decompose_loc(k, method, locationid, database):
        table = database.get_vis_table(locationid=locationid)
        return Decompose.switchboard(table, k, method)