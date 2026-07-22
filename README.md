# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems like Spotify and YouTube use a hybrid approach combining **collaborative filtering** (analyzing patterns across millions of users — "people who listened to X also enjoyed Y") and **content-based filtering** (matching song attributes like tempo, energy, and genre to a listener's taste profile). These systems process billions of daily interactions — skips, saves, playlist additions, listening duration — to build high-dimensional user embeddings that capture nuanced preferences, then rank candidates using machine learning models that balance relevance, freshness, and diversity. This simulation strips away the collaborative layer to focus exclusively on **content-based filtering** using a 10-song catalog with five measurable attributes: genre, mood, energy, acousticness, and valence. The system scores each song by computing how closely its attributes match a user's stated preferences — rewarding exact genre and mood matches, and using proximity scoring for numerical features so that songs closer to the user's target energy and acoustic preferences rank higher. Every recommendation is fully explainable: each score is a weighted sum of transparent feature matches, and each suggestion comes with a human-readable reason, making the logic inspectable in a way that production-scale neural recommenders cannot easily offer.

### Song Features

Each `Song` object in the catalog contains:

| Feature | Type | Role in Scoring |
|---|---|---|
| `id` | `int` | Unique identifier (display only) |
| `title` | `str` | Song name (display only) |
| `artist` | `str` | Artist name (display only) |
| `genre` | `str` | **Categorical match** — exact match = 1.0, no match = 0.0 |
| `mood` | `str` | **Categorical match** — exact match = 1.0, no match = 0.0 |
| `energy` | `float` (0–1) | **Proximity scoring** — closer to target = higher score |
| `tempo_bpm` | `float` | Not scored (too correlated with energy in this dataset) |
| `valence` | `float` (0–1) | Not scored in simple version |
| `danceability` | `float` (0–1) | Not scored in simple version |
| `acousticness` | `float` (0–1) | **Proximity scoring** — mapped via `likes_acoustic` preference |

### UserProfile

Each `UserProfile` stores the user's taste preferences:

| Feature | Type | What It Captures |
|---|---|---|
| `favorite_genre` | `str` | Preferred genre (e.g., "pop", "lofi") |
| `favorite_mood` | `str` | Preferred mood (e.g., "happy", "chill") |
| `target_energy` | `float` (0–1) | Desired energy level (e.g., 0.8 for upbeat) |
| `likes_acoustic` | `bool` | Whether the user prefers acoustic over electronic |

### Scoring Rule (One Song)

Each song is scored against the user profile using a weighted sum of four components:

| Component | Weight | How It Works |
|---|---|---|
| Genre match | 0.30 | Exact match = 1.0, no match = 0.0 |
| Mood match | 0.25 | Exact match = 1.0, no match = 0.0 |
| Energy proximity | 0.25 | `1.0 - abs(target_energy - song_energy)` |
| Acoustic match | 0.20 | If `likes_acoustic=True`: score = acousticness; if `False`: score = `1.0 - acousticness` |

**Final score** = `0.30 * genre + 0.25 * mood + 0.25 * energy_proximity + 0.20 * acoustic_score`

This produces a score between **0.0** (terrible match) and **1.0** (perfect match).

### Ranking Rule (List of Songs)

After every song is scored, the system:

1. Sorts all songs by score in descending order
2. Selects the top-k songs (default: 5)
3. Attaches an explanation string to each recommendation

### Example Flow

```
User Profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False
                              ↓
For each song in catalog:
  → Score genre match (0.30 weight)
  → Score mood match (0.25 weight)
  → Score energy proximity (0.25 weight)
  → Score acoustic preference (0.20 weight)
  → Sum = final score
                              ↓
Sort by score descending → Return top 5
                              ↓
"Sunrise City — Score: 0.96 — Matches your love of pop; Has the happy vibe you enjoy"
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



