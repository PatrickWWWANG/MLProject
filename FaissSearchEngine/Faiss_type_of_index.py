import faiss
import numpy as np

d = 64
nb = 10000
np.random.seed(42)
data = np.random.random((nb, d)).astype('float32')

# Index Flat
index_flat = faiss.IndexFlatL2(d)
index_flat.add(data)

# Index IVF
ncluster = 100
quantizer = faiss.IndexFlatL2(d)
index_ivf = faiss.IndexIVFFlat(quantizer, d, ncluster, faiss.METRIC_L2)

# Train Index
index_ivf.train(data)
index_ivf.add(data)

# Index PQ
m = 8
index_pq = faiss.IndexPQ(d, m, 8)
index_pq.train(data)
index_pq.add(data)

# Search
nq = 5
np.random.seed(42)
query_vectors = np.random.random((nq, d)).astype('float32')

k = 4
distance_flat, indices_flat = index_flat.search(query_vectors, k)
distance_ivf, indices_ivf = index_ivf.search(query_vectors, k)
distance_pq, indices_pq = index_pq.search(query_vectors, k)

print('Flat Distance: \n', distance_flat)
print('Flat Indices: \n', indices_flat)
print()
print('IVF Distance: \n', distance_ivf)
print('IVF Indices: \n', indices_ivf)
print()
print('PQ Distance: \n', distance_pq)
print('PQ Indices: \n', indices_pq)

# Save index
faiss.write_index(index_pq, 'my_index.faiss')

# Read Index
index_pq = faiss.read_index('my_index.faiss')
