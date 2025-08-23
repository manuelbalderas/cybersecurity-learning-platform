import pandas as pd
from sentence_transformers import SentenceTransformer
import json

df = pd.read_csv('data/glossary.csv')

model = SentenceTransformer('all-MiniLM-L6-v2')

definitions = df['Definition'].tolist()
embeddings = model.encode(definitions, show_progress_bar=True)
df['Embedding'] = [embedding.tolist() for embedding in embeddings]

import numpy as np

embedding_matrix = np.array(df['Embedding'].tolist())

from sklearn.decomposition import PCA
pca = PCA(n_components=50)  # Reduce to 50 dimensions
reduced_embeddings = pca.fit_transform(embedding_matrix)

# Clustering the embeddings using KMeans
from sklearn.cluster import KMeans
n_clusters = 24
kmeans = KMeans(n_clusters=n_clusters)
df['Cluster'] = kmeans.fit_predict(reduced_embeddings)

# for i in range(n_clusters):
#     print(f"\nCluster {i}")
#     print(df[df['Cluster'] == i][['Term', 'Definition']].head(5))

clustered_data = {}

for i in range(n_clusters):
    cluster_df = df[df['Cluster'] == i][['Term', 'Definition']]
    items = cluster_df.to_dict(orient='records')
    clustered_data[f'Cluster {i}'] = items
    
with open('data/clustered_glossary.json', 'w', encoding='utf-8') as f:
    json.dump(clustered_data, f, ensure_ascii=False, indent=2)
    
flat_data = df[['Term', 'Definition', 'Cluster']].to_dict(orient='records')

with open('data/all_terms_with_clusters.json', 'w') as f:
    json.dump(flat_data, f, ensure_ascii=False, indent=2)

    
# Using DBSCAN for clustering (optional, uncomment to use)

# from sklearn.cluster import DBSCAN

# dbscan = DBSCAN(eps=1.5, min_samples=5)
# labels = dbscan.fit_predict(reduced_embeddings)

# df['Cluster'] = labels
# print(df['Cluster'].value_counts())



# TEST



# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt

# inertia = []
# cluster_range = range(2, 30)

# for k in cluster_range:
#     kmeans = KMeans(n_clusters=k)
#     kmeans.fit(reduced_embeddings)
#     inertia.append(kmeans.inertia_)

# plt.figure(figsize=(8, 5))
# plt.plot(cluster_range, inertia, marker='o')
# plt.title('Elbow Method for Optimal k')
# plt.xlabel('Number of clusters')
# plt.ylabel('Inertia (Within-cluster sum of squares)')
# plt.grid(True)
# plt.savefig('elbow_method_reducted_dimentionality_50.png')

# from sklearn.metrics import silhouette_score

# silhouette_scores = []
# for k in range(2, 30):
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     labels = kmeans.fit_predict(reduced_embeddings)
#     score = silhouette_score(reduced_embeddings, labels)
#     silhouette_scores.append(score)

# plt.plot(range(2, 30), silhouette_scores, marker='o')
# plt.title('Silhouette Score vs Number of Clusters')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Silhouette Score')
# plt.grid(True)
# plt.savefig('silhouette_scores_reduced_dimensionality_50.png')