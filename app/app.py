import os
import time
import webbrowser
from threading import Timer

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from flask import Flask, render_template, request
from sentence_transformers import SentenceTransformer
import pandas as pd

from src.job_parser.job_parser import parse_job_description
from src.ranking.ranker import rank_candidates

app = Flask(__name__)

print("Loading candidate database...")
df = pd.read_parquet("data/embeddings.parquet")
print(f"Loaded {len(df):,} candidates")

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Ready!")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    job_description = request.form["job_description"]

    # ----------------------------------------
    # Parse Job Description
    # ----------------------------------------
    start = time.time()

    parsed = parse_job_description(job_description)
    print(parsed)

    print(f"Parsing Time: {time.time() - start:.2f} seconds")

    # ----------------------------------------
    # Build Search Query
    # ----------------------------------------
    query = " ".join(parsed["required_skills"])

    if parsed["title"]:
        query = parsed["title"] + " " + query

    # ----------------------------------------
    # Generate Embedding
    # ----------------------------------------
    start = time.time()

    job_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    print(f"Embedding Time: {time.time() - start:.2f} seconds")

    # ----------------------------------------
    # Rank Candidates
    # ----------------------------------------
    start = time.time()

    # Use a smaller candidate pool for faster demo performance
    candidate_pool = df.sample(
        n=10000,
        random_state=42
    )

    ranked = rank_candidates(
        candidate_pool,
        job_embedding,
        parsed
    )

    print(f"Ranking Time: {time.time() - start:.2f} seconds")

    # ----------------------------------------
    # Top Results
    # ----------------------------------------
    top10 = ranked.head(10)

    results = top10[
        [
            "rank",
            "candidate_id",
            "current_title",
            "years_of_experience",
            "open_to_work",
            "github_activity_score",
            "recruiter_response_rate",
            "interview_completion_rate",
            "notice_period_days",
            "search_appearance",
            "score",
            "reasoning",
        ]
    ].to_dict(orient="records")

    return render_template(
        "index.html",
        results=results,
        parsed=parsed,
        job_description=job_description,
        required_skills=parsed.get("required_skills", [])
    )


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)