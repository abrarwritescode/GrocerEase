

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def generate_item_features(all_items):
   
    item_texts = [
        f"{item.itemtitle} {', '.join(category.categoryname for category in item.category.all())}"
        for item in all_items
    ]

    vectorizer = TfidfVectorizer(stop_words='english')
    features = vectorizer.fit_transform(item_texts)


    print(f"item_texts: {item_texts}")
    print(f"features.shape: {features.shape}")


    return features


def calculate_similarity(features):
   
    similarity_matrix = linear_kernel(features, features)
    print(f"similarity_matrix.shape: {similarity_matrix.shape}")
    return similarity_matrix


def get_recommendations(item_index, items, similarity_matrix, num_recommendations=5):
    print(f"item_index: {item_index}")
    print(f"len(items): {len(items)}")
    print(f"similarity_matrix.shape: {similarity_matrix.shape}")


    if item_index >= similarity_matrix.shape[0]:
        raise IndexError(f"Index {item_index} is out of bounds for axis 0 with size {similarity_matrix.shape[0]}")


   
    similarity_scores = list(enumerate(similarity_matrix[item_index]))


 
    print("Raw Similarity Scores:")
    for idx, score in similarity_scores:
        print(f"Item {idx}: {score}")


    similarity_scores = [(idx, score) for idx, score in similarity_scores if score > 0]
 
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)


 
    print("\nSorted Similarity Scores:")
    for idx, score in similarity_scores:
        print(f"Item {idx}: {score}")


    # the indices of the top similar items 
    similar_item_indices = [i[0] for i in similarity_scores[:num_recommendations] if i[0] != item_index]


    # the actual items based on indices
    recommended_items = [items[i] for i in similar_item_indices] 


    print("\nRecommended Items:")
    for item in recommended_items:
        print(item.itemtitle)


    return recommended_items