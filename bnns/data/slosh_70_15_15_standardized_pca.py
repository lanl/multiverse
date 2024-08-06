
import numpy as np
import torch
import os
from quality_of_life.my_torch_utils import convert_Tensors_to_Dataset
from quality_of_life.my_base_utils import find_root_dir_of_repo

#
# ~~~ Establish the path to the folder `bnns/data`
root = find_root_dir_of_repo()
PATH = os.path.join( root, "bnns", "data" )

try:
    #
    # ~~~ Load the processed data
    U = torch.load(os.path.join( PATH, "slosh_standardized_U.pt"))
    s = torch.load(os.path.join( PATH, "slosh_standardized_s.pt"))
    V = torch.load(os.path.join( PATH, "slosh_standardized_V.pt"))
except:
    #
    # ~~~ Load the unprocessed data
    from bnns.data.slosh_70_15_15 import coords_np, inputs_np, out_np
    data_matrix = torch.from_numpy( (out_np - np.mean(out_np,axis=0)) / (np.std(out_np,axis=0)+1e-10) )
    #
    # ~~~ Process the data (do SVD)
    evals, evecs = torch.linalg.eigh(data_matrix@data_matrix.T)
    s_squared = evals.flip(dims=(0,)) # ~~~ the squared singular values of `data_matrix`
    percentage_of_variance_explained = s_squared.cumsum(dim=0)/s_squared.sum()
    r = (percentage_of_variance_explained<.99).int().argmin().item()    # ~~~ the first index at which percentage_of_variance_explained>=.99
    U, s, V = torch.linalg.svd( data_matrix, full_matrices=False )
    # #
    # # ~~~ Question to self, why doesn't this seem to work?
    # U = evecs.flip(dims=(0,))
    # s = torch.where( s_squared>=s_squared[r], (s_squared+1e-10).sqrt(), 0. )  # ~~~ adding an epsilon before taking the sqrt in order to avoid nan's (this is hacky)
    # V = ( torch.where(s>0,1/s,0.).diag() @ U.T @ data_matrix ).T
    # ((data_matrix-U@s.diag()@V.T)**2).mean()  # ~~~ should be small, like of the order 0.01
    #
    # ~~~ Save the processed data
    torch.save( U, os.path.join( PATH, "slosh_standardized_U.pt" ))
    torch.save( s, os.path.join( PATH, "slosh_standardized_s.pt" ))
    torch.save( V, os.path.join( PATH, "slosh_standardized_V.pt" ))

#
# ~~~ Compute indices for a train/val/test split (same code as in slosh_70_15_15.py)
np.random.seed(2024)
n_train = 2600
n_test = 700
n_val = 700
n = len(inputs_np)
assert len(inputs_np) == 4000 == len(out_np)
assert n_train + n_test + n_val == n
idx = np.random.permutation(n)
idx_train, idx_test, idx_val = np.split( idx, [n_train,n_train+n_test] )

#
# ~~~ Use indices for a train/val/test split
x_train = torch.from_numpy(inputs_np[idx_train])
x_test = torch.from_numpy(inputs_np[idx_test])
x_val = torch.from_numpy(inputs_np[idx_val])
y_train = U[idx_train]
y_test = U[idx_test]
y_val = U[idx_val]

#
# ~~~ Finally, package as objects of class torch.utils.data.Dataset
D_train = convert_Tensors_to_Dataset(x_train,y_train)
D_test = convert_Tensors_to_Dataset(x_test,y_test)
D_val = convert_Tensors_to_Dataset(x_val,y_val)

