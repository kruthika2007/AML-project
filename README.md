🎬 Customer Segmentation using Clustering Algorithms

An end-to-end Applied Machine Learning project that segments customers into meaningful groups using unsupervised learning, then delivers personalized movie recommendations through a content-based filtering engine and a live web application.


📌 Problem Statement
Generic recommendation systems treat all users the same — leading to poor engagement and irrelevant suggestions. This project solves that by automatically grouping customers into distinct segments based on their profiles, then tailoring movie recommendations to each segment using a hybrid scoring approach.

🗂️ Project Structure
AML-project/
├── Phase2.py                          # Data preprocessing & feature engineering
├── Phase3.py                          # Clustering & segment analysis
├── Phase4.py                          # Recommendation engine
├── app.py                             # Flask REST API backend
├── building_a_content_based_         
│   recommendation_system.ipynb        # Jupyter notebook walkthrough
├── frontend/                          # React + Vite frontend
├── Customers_data.csv                 # Core customer dataset
├── movies.csv                         # Movie catalog
├── ratings.csv                        # User-movie ratings
├── global_top_movies.csv              # Globally trending movies
├── customer_segments_final.csv        # Final cluster assignments
├── segment_insights_summary.csv       # Per-segment analytics
├── segment_movie_recommendations.csv  # Recommendations per segment
├── age_group_recommendations.csv      # Recommendations per age group
└── *.png                              # Visualizations

🔄 Pipeline Overview
Phase 1 — Data Collection
Raw customer data collected covering demographics, viewing behavior, and preferences.
Phase 2 — Preprocessing

Handle missing values and remove duplicates
Feature engineering: age group binning, hybrid score computation
Normalize features for distance-based clustering

Phase 3 — Clustering & Segmentation

Applied K-Means Clustering on customer features
Used the Elbow Method to determine optimal K = 4
Identified 4 customer segments:
SegmentAge RangeKids5 – 12Teens13 – 17Young Adults18 – 35Adults35+


Phase 4 — Recommendation System

Built a content-based filtering engine
Computed hybrid scores per movie per segment:

  hybrid_score = α × content_similarity + β × avg_rating + γ × global_popularity

Weights (α, β, γ) tuned per age segment to reflect differing preferences


🌐 Web Application
A full-stack web app where users enter their name and age and instantly receive top 10 personalized movie recommendations.
Backend: Flask (Python) — REST API at /api/result
Frontend: React + Vite
How it works

User submits name + age via the React UI
Flask classifies the user into an age segment
Top 10 movies are ranked by hybrid score for that segment
Results returned and displayed in the UI


🚀 Running Locally
Prerequisites

Python 3.8+
Node.js 16+

Backend (Flask)
bashpip install flask flask-cors pandas
python app.py
# Runs on http://localhost:5000
Frontend (React)
bashcd frontend
npm install
npm run dev
# Runs on http://localhost:5173

📊 Key Results

Young Adults (18–35) form the largest segment (~40% of users)
Animation & Drama score highest in average ratings across all segments
Hybrid scoring outperforms pure content-based filtering for cross-age groups
Elbow Method converged clearly at K = 4, validating the age-group hypothesis


🛠️ Tech Stack
LayerTechnologyLanguagePythonData ProcessingPandas, NumPyMachine LearningScikit-learnNotebookJupyterBackend APIFlaskFrontendReact, Vite, CSSVisualizationsMatplotlib, Seaborn

📸 Visualizations
Optimal Clusters (Elbow)Customer SegmentsCustomer InsightsShow ImageShow ImageShow Image

🔮 Future Scope

Add collaborative filtering to enrich recommendations
Implement real-time re-clustering as user behavior evolves
Use deep learning embeddings (autoencoders) for richer latent features
Deploy on AWS / GCP with scalable data pipelines


👥 Team
Kruthika Tummala, Isha Deshwal, Yashika, Harsh Yadav

AML Project — Customer Segmentation using Clustering Algorithms
