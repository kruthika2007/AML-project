# =====================================================
# PHASE 4 – ADVANCED MOVIE RECOMMENDATION ENGINE
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("\nLoading datasets...")

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
customers = pd.read_csv("customer_segments_final.csv")

ratings.rename(columns={"userId":"user_id"}, inplace=True)

print("Merging datasets...")
data = ratings.merge(movies, on="movieId")
data = data.merge(customers[['user_id','cluster','age_group']], on="user_id")

# =====================================================
# MOVIE STATISTICS
# =====================================================
print("Calculating movie statistics...")

movie_stats = data.groupby("title").agg(
    avg_rating=("rating","mean"),
    rating_count=("rating","count"),
    rating_std=("rating","std")
).reset_index()

movie_stats.fillna(0, inplace=True)

C = movie_stats["avg_rating"].mean()
m = movie_stats["rating_count"].quantile(0.60)

def weighted_rating(row):
    v = row["rating_count"]
    R = row["avg_rating"]
    return (v/(v+m)*R) + (m/(m+v)*C)

movie_stats["weighted_rating"] = movie_stats.apply(weighted_rating, axis=1)

# Remove weak movies
movie_stats = movie_stats[movie_stats["rating_count"] > 20]
movie_stats = movie_stats[movie_stats["avg_rating"] > 3.2]

# Popularity + Consistency scores
movie_stats["popularity_score"] = movie_stats["avg_rating"] * np.log1p(movie_stats["rating_count"])
movie_stats["consistency_score"] = 1 / (1 + movie_stats["rating_std"])

# Normalize scores
for col in ["weighted_rating","popularity_score","consistency_score"]:
    movie_stats[col] = (movie_stats[col]-movie_stats[col].min())/(movie_stats[col].max()-movie_stats[col].min())

# Final Hybrid Score
movie_stats["hybrid_score"] = (
      0.5 * movie_stats["weighted_rating"]
    + 0.3 * movie_stats["popularity_score"]
    + 0.2 * movie_stats["consistency_score"]
)

data = data.merge(movie_stats, on="title")

# =====================================================
# SEGMENT RECOMMENDATIONS
# =====================================================
print("\nGenerating segment recommendations...")

segment_outputs = []
clusters = sorted(data["cluster"].unique())

for cl in clusters:
    seg_data = data[data["cluster"] == cl]

    top_movies = (
        seg_data.groupby("title")
        .agg(
            avg_user_rating=("rating","mean"),
            rating_count=("rating_count","first"),
            hybrid_score=("hybrid_score","mean")
        )
        .reset_index()
        .sort_values("hybrid_score", ascending=False)
        .head(20)
    )

    top_movies["recommended_for_cluster"] = cl
    top_movies["reason"] = "Popular & highly rated within this segment"
    segment_outputs.append(top_movies)

segment_df = pd.concat(segment_outputs)
segment_df.to_csv("segment_movie_recommendations.csv", index=False)
print("Segment recommendations saved.")

# =====================================================
# AGE GROUP RECOMMENDATIONS
# =====================================================
print("\nGenerating age group recommendations...")

age_outputs = []
ages = sorted(data["age_group"].unique())

for age in ages:
    age_data = data[data["age_group"] == age]

    top_movies = (
        age_data.groupby("title")
        .agg(
            avg_user_rating=("rating","mean"),
            rating_count=("rating_count","first"),
            hybrid_score=("hybrid_score","mean")
        )
        .reset_index()
        .sort_values("hybrid_score", ascending=False)
        .head(20)
    )

    top_movies["recommended_for_age_group"] = age
    top_movies["reason"] = "Trending among this age group"
    age_outputs.append(top_movies)

age_df = pd.concat(age_outputs)
age_df.to_csv("age_group_recommendations.csv", index=False)
print("Age group recommendations saved.")

# =====================================================
# GLOBAL TOP MOVIES
# =====================================================
print("\nGenerating global top movies...")

global_top = movie_stats.sort_values("hybrid_score", ascending=False).head(30)
global_top["reason"] = "Top movies overall"
global_top.to_csv("global_top_movies.csv", index=False)
print("Global recommendations saved.")

# =====================================================
# BIG INSIGHT FIGURE (FOR REPORT)
# =====================================================
print("\nGenerating recommendation insights figure...")

plt.figure(figsize=(14,10))

# Plot 1 – Rating vs Popularity
plt.subplot(2,2,1)
plt.scatter(movie_stats["avg_rating"], movie_stats["rating_count"])
plt.title("Rating vs Popularity")
plt.xlabel("Average Rating")
plt.ylabel("Number of Ratings")

# Plot 2 – Hybrid Score Distribution
plt.subplot(2,2,2)
plt.hist(movie_stats["hybrid_score"], bins=30)
plt.title("Hybrid Score Distribution")
plt.xlabel("Hybrid Score")
plt.ylabel("Movies")

# Plot 3 – Popularity Distribution
plt.subplot(2,2,3)
plt.hist(movie_stats["rating_count"], bins=30)
plt.title("Movie Popularity Distribution")
plt.xlabel("Number of Ratings")
plt.ylabel("Movies")

# Plot 4 – Rating Distribution
plt.subplot(2,2,4)
plt.hist(movie_stats["avg_rating"], bins=30)
plt.title("Average Rating Distribution")
plt.xlabel("Average Rating")
plt.ylabel("Movies")

plt.tight_layout()
plt.savefig("phase4_recommendation_insights.png")
plt.close()

print("\n==============================")
print("PHASE 4 COMPLETED SUCCESSFULLY")
print("==============================")
print("Files generated:")
print("• segment_movie_recommendations.csv")
print("• age_group_recommendations.csv")
print("• global_top_movies.csv")
print("• phase4_recommendation_insights.png")
print("==============================\n")