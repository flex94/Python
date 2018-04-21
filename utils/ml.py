import pandas as pd
import numpy as np

def sklearnDatasetToDf(dataset):
    """
    Take a dataset from sklearn and return a pandas DataFrame.

    datasets: e.g. sklearn.datasets.load_iris()
    """
    return pd.DataFrame(
        columns=dataset.feature_names + ['target'],
        data=np.c_[dataset.data, dataset.target]
    )
