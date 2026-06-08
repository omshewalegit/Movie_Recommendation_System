<div align="center">

<img src="https://img.shields.io/badge/CINESEARCH-RECOMMENDER-E50914?style=for-the-badge&labelColor=141414&color=E50914" alt="CineSearch Recommender"/>

# CineSearch 🎬

**Your Personal Movie Matchmaker**<br/>
Find movies similar to what you love — powered by TF-IDF and cosine similarity

Built with Scikit-learn · Streamlit · OMDB API · Python

[![Python](https://img.shields.io/badge/Python-3.10+-3B82F6?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML_Engine-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-EF4444?style=flat-square)](https://streamlit.io)
[![OMDB API](https://img.shields.io/badge/OMDB_API-Posters_%26_Metadata-F5C518?style=flat-square&labelColor=1a1a1a)](https://www.omdbapi.com)
[![Dataset](https://img.shields.io/badge/Dataset-5000%2B_Movies-16A34A?style=flat-square)](https://www.kaggle.com)
[![License](https://img.shields.io/badge/License-MIT-6366F1?style=flat-square)](LICENSE)

</div>

---

## What is CineSearch?

CineSearch is a content-based movie recommendation system that suggests films similar to a given title by analyzing metadata — genres, keywords, and plot features — using TF-IDF vectorization and cosine similarity.

Built for movie lovers, students, and developers who want a simple, explainable recommender that's easy to run and extend.

> **Example:** Input `Inception (2010)` → Top result: `Shutter Island (2010)` — similar themes, psychological thriller elements, and overlapping keywords.

---

## Highlights

- **Content-based recommendations** using TF-IDF and cosine similarity
- **5,000+ movies** processed with multi-feature extraction from genres and keywords
- **Interactive Streamlit UI** with real-time movie poster integration via the OMDB API
- **Top 10 matches** returned with title, year, brief overview, and poster
- **Explainability** — inspect which features drove each recommendation

---

## How It Works

```
Input Movie Title
       │
       ▼
┌─────────────────────┐
│  Dataset Preprocess │  Clean text, normalize genres/keywords, fill missing values
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Feature Builder    │  Combine genres + keywords + plot fields into one text vector
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  TF-IDF Vectorizer  │  Convert combined text into numeric feature vectors
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Cosine Similarity  │  Compute pairwise similarity across all 5,000+ movies
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Rank & Return      │  Sort by similarity score → return top 10 matches
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Streamlit UI       │  Fetch posters from OMDB API → display results
└─────────────────────┘
```

---

## Features

- **Fast similarity lookup** — compute and show top 10 matches for any input movie
- **Multi-feature blending** — genres, keywords, and plot-related text fused into a single vector
- **Poster previews** — movie posters fetched in real-time from the OMDB API
- **Clean, minimal UI** — powered by Streamlit for easy demos and testing
- **Modular pipeline** — swap TF-IDF with sentence embeddings or BERT at any time

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Data processing and model logic |
| Data Handling | Pandas | Dataset loading and preprocessing |
| ML Engine | Scikit-learn | TF-IDF vectorizer and cosine similarity |
| Frontend | Streamlit | Interactive web app UI |
| Enrichment | OMDB API | Movie posters and metadata |

---

## Project Structure

```
CineSearch/
├── data/
│   ├── raw/                 # Original dataset CSVs
│   └── cleaned/             # Preprocessed, feature-engineered CSVs
├── notebooks/
│   └── eda_preprocessing.ipynb   # Exploratory analysis and feature extraction steps
├── src/
│   ├── __init__.py
│   ├── preprocess.py        # Text cleaning, normalization, missing value handling
│   ├── features.py          # Feature builder — genre + keyword + plot fusion
│   ├── vectorizer.py        # TF-IDF vectorization logic
│   └── similarity.py        # Cosine similarity computation and top-k ranking
├── .env                     # OMDB API key (not committed)
├── .gitignore
├── requirements.txt
└── app.py                   # Streamlit entry point
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- OMDB API key — free at [omdbapi.com](https://www.omdbapi.com/apikey.aspx)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cinesearch.git
cd cinesearch

# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
OMDB_API_KEY=your_omdb_api_key_here
```

### Run

```bash
streamlit run app.py
```

Application available at `http://localhost:8501`

---

## Example Output

```
🔍 Input:  Inception (2010)

Top 10 Recommendations:
──────────────────────────────────────────────────────
 #   Title                        Year   Similarity
──────────────────────────────────────────────────────
 1   Shutter Island               2010   ████████░░  High
 2   The Prestige                 2006   ███████░░░  High
 3   Memento                      2000   ██████░░░░  Medium
 4   Interstellar                 2014   ██████░░░░  Medium
 5   The Matrix                   1999   █████░░░░░  Medium
...
──────────────────────────────────────────────────────
```

---

## Metrics

- Processed **5,000+ movies** from an OMDB-style dataset
- Returns **top 10** relevant movies with qualitative validation against human judgments
- UI enables **instant manual verification** via poster and short overview

---

## Use Cases

- **Movie fans** — find similar films to watch next based on a title you loved
- **Portfolio / interviews** — demonstrates practical ML + web integration in one project
- **Educational** — explains how content-based recommenders work, step by step

---

## Future Scope

- [ ] Hybrid recommender — combine collaborative filtering with content signals
- [ ] User profiles and session-based personalization
- [ ] Upgrade feature extraction to sentence embeddings or BERT
- [ ] Filters by year, language, or minimum rating
- [ ] Cloud deployment with poster request caching for faster loads

---

## Screenshots

<img width="1844" height="896" alt="image" src="https://github.com/user-attachments/assets/782f5c4a-d210-44ba-adc8-411cda961816" />
<img width="1759" height="866" alt="image" src="https://github.com/user-attachments/assets/c7571a9e-a445-45cc-915a-1410049173f9" />
<img width="1760" height="880" alt="image" src="https://github.com/user-attachments/assets/8bc6ce90-285b-4790-91cb-06236968b5de" />



---

## Notes for Reviewers

- Dataset preprocessing code and notebooks are included for full reproducibility
- Similarity pipeline is modular — TF-IDF can be swapped with any embedding model without touching the rest of the codebase
- OMDB API calls are made at render time; results are not cached between sessions in the current version

---

## Disclaimer

CineSearch uses publicly available movie metadata for educational and demonstration purposes only. All movie titles, posters, and related content belong to their respective rights holders.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  Developed May 2025 · <strong>Om Shewale</strong>
</div>
