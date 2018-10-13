from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD as SVD


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
    def decompose(term_space, k, method, database):
        table = database.get_txt_desc_table(term_space)
        
        if method == 'pca':
            f = Decompose.pca
        elif method == 'svd':
            f = Decompose.svd
        elif method == 'lda':
            f = Decompose.lda
        
        returnval = f(table, k, database)
        return returnval