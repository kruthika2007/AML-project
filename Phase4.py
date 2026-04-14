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
# HELPER — compute per-group hybrid scores
# =====================================================
def top_movies_for_group(group_data, n=20):
    stats = group_data.groupby("title").agg(
        avg_user_rating=("rating", "mean"),
        rating_count=("rating", "count"),
        rating_std=("rating", "std"),
    ).reset_index()
    stats.fillna(0, inplace=True)

    # Drop movies with too few ratings within this group
    min_votes = max(5, int(stats["rating_count"].quantile(0.40)))
    stats = stats[stats["rating_count"] >= min_votes]
    stats = stats[stats["avg_user_rating"] > 3.0]

    if stats.empty:
        return stats

    C = stats["avg_user_rating"].mean()
    m = stats["rating_count"].quantile(0.60)

    stats["weighted_rating"] = stats.apply(
        lambda r: (r["rating_count"] / (r["rating_count"] + m) * r["avg_user_rating"])
                  + (m / (r["rating_count"] + m) * C),
        axis=1,
    )
    stats["popularity_score"] = stats["avg_user_rating"] * np.log1p(stats["rating_count"])
    stats["consistency_score"] = 1 / (1 + stats["rating_std"])

    for col in ["weighted_rating", "popularity_score", "consistency_score"]:
        rng = stats[col].max() - stats[col].min()
        stats[col] = (stats[col] - stats[col].min()) / rng if rng > 0 else 0.0

    stats["hybrid_score"] = (
        0.5 * stats["weighted_rating"]
        + 0.3 * stats["popularity_score"]
        + 0.2 * stats["consistency_score"]
    )

    return stats.sort_values("hybrid_score", ascending=False).head(n)


# =====================================================
# SEGMENT RECOMMENDATIONS (per-cluster scores)
# =====================================================
print("\nGenerating segment recommendations...")

segment_outputs = []
for cl in sorted(data["cluster"].unique()):
    top = top_movies_for_group(data[data["cluster"] == cl])
    top["recommended_for_cluster"] = cl
    top["reason"] = "Popular & highly rated within this segment"
    segment_outputs.append(top)

segment_df = pd.concat(segment_outputs)
segment_df.to_csv("segment_movie_recommendations.csv", index=False)
print("Segment recommendations saved.")

# =====================================================
# AGE GROUP RECOMMENDATIONS (per-age-group scores)
# =====================================================
print("\nGenerating age group recommendations...")

age_outputs = []
for age in sorted(data["age_group"].unique()):
    top = top_movies_for_group(data[data["age_group"] == age])
    top["recommended_for_age_group"] = age
    top["reason"] = "Trending among this age group"
    age_outputs.append(top)

age_df = pd.concat(age_outputs)
age_df.to_csv("age_group_recommendations.csv", index=False)
print("Age group recommendations saved.")

# =====================================================
# GLOBAL TOP MOVIES
# =====================================================
print("\nGenerating global top movies...")

global_top = top_movies_for_group(data, n=30)
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
plt.scatter(global_top["avg_rating"], global_top["rating_count"])
plt.title("Rating vs Popularity")
plt.xlabel("Average Rating")
plt.ylabel("Number of Ratings")

# Plot 2 – Hybrid Score Distribution
plt.subplot(2,2,2)
plt.hist(global_top["hybrid_score"], bins=30)
plt.title("Hybrid Score Distribution")
plt.xlabel("Hybrid Score")
plt.ylabel("Movies")

# Plot 3 – Popularity Distribution
plt.subplot(2,2,3)
plt.hist(global_top["rating_count"], bins=30)
plt.title("Movie Popularity Distribution")
plt.xlabel("Number of Ratings")
plt.ylabel("Movies")

# Plot 4 – Rating Distribution
plt.subplot(2,2,4)
plt.hist(global_top["avg_rating"], bins=30)
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