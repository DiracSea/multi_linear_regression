import numpy as np

def shuffle_data(X,y):#randomize X and y,testing
    seed = random.random()
    random.seed(seed)
    random.shuffle(X.tolist())
    random.seed(seed)
    random.shuffle(y.tolist())
    X = np.array(X)
    y = np.array(y)
    return X,y

def shuffle_index(inputs):
    indices = np.arange(inputs.shape[0])
    np.randpm.shuffle(indices)
    return indices