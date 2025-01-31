import numpy as np
import faiss

d = 64
nb = 10000
np.random.seed(1234)
db_vectors = np.random.random((nb, d)).astype('float32')

# Build index 
index = faiss.IndexFlatL2(d)

# Add data to index
index.add(db_vectors)

nq = 5
np.random.seed(1234)
query_vectors = np.random.random((nq, d)).astype('float32')

k = 4
distance, indices = index.search(query_vectors, k)

print('Distance: \n', distance)
print('Indices: \n', indices)