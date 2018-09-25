
def split_num(batchsize):
    train_num = int(batchsize*7/10+1/2)
    valid_num = batchsize - train_num
    return train_num, valid_num