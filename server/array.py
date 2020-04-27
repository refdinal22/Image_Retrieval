import numpy as np
import h5py
from sklearn.metrics.pairwise import cosine_similarity
from numpy import linalg as LA

# feats1 = [1,2,3,4]
# feats2 = [1,3,5,7]
# feats3 = [1,2,9,11]
# feats4 = [1,4,5,13]

# feats1 = feats1/LA.norm(feats1)
# feats2 = feats2/LA.norm(feats2)
# feats3 = feats3/LA.norm(feats3)
# feats4 = feats4/LA.norm(feats4)

# feats = []
# feats.append(feats1)
# feats.append(feats2)
# feats.append(feats3)
# feats.append(feats4)

# id = [1, 2, 3, 4]

# feats = np.array(feats)

# h5py = h5py.File("test.h5", 'w')
# h5py.create_dataset('feats', data = feats)
# h5py.create_dataset('id', data = id)
# h5py.close()

# Read
h5f = h5py.File("test.h5",'r')
feats = h5f['feats'][:]
id = h5f['id'][:]
h5f.close()

print(id)
print(feats)

q_feats = [1,4,5,13]
q_feats = q_feats/LA.norm(q_feats)

# print(q_feats)
# # feats.T = transformasi
scores = np.dot(q_feats, feats.T)
rank_ID = np.argsort(scores)[::-1]

rank_score = scores[rank_ID]
id_rank = id[rank_ID]

rank = np.r_[(rank_score>0.7).nonzero()]

id_rank = id_rank[rank]
rank_score = rank_score[rank]


print(scores)
# print (rank_ID)
print(id_rank)
print (rank_score)
# print(rank)