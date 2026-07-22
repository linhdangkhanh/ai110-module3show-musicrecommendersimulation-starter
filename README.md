# 🎵 Music Recommender Simulation

## Project Summary

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems like Spotify and YouTube use a hybrid approach combining **collaborative filtering** (analyzing patterns across millions of users — "people who listened to X also enjoyed Y") and **content-based filtering** (matching song attributes like tempo, energy, and genre to a listener's taste profile). These systems process billions of daily interactions — skips, saves, playlist additions, listening duration — to build high-dimensional user embeddings that capture nuanced preferences, then rank candidates using machine learning models that balance relevance, freshness, and diversity. This simulation strips away the collaborative layer to focus exclusively on **content-based filtering** using an 18-song catalog with five measurable attributes: genre, mood, energy, acousticness, and valence. The system scores each song by computing how closely its attributes match a user's stated preferences — rewarding exact genre and mood matches, and using proximity scoring for numerical features so that songs closer to the user's target energy and acoustic preferences rank higher. Every recommendation is fully explainable: each score is a weighted sum of transparent feature matches, and each suggestion comes with a human-readable reason, making the logic inspectable in a way that production-scale neural recommenders cannot easily offer.

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

Each song is scored against the user profile using a **weighted sum** of four components. The weights were chosen to balance structural identity (genre, mood) against continuous preference (energy, acousticness):

| Component | Weight | Points | How It Works |
|---|---|---|---|
| Genre match | 0.30 | +0.30 max | Exact match = 1.0, no match = 0.0 |
| Mood match | 0.25 | +0.25 max | Exact match = 1.0, no match = 0.0 |
| Energy proximity | 0.25 | +0.25 max | `1.0 - abs(target_energy - song_energy)` |
| Acoustic match | 0.20 | +0.20 max | If `likes_acoustic=True`: score = acousticness; if `False`: score = `1.0 - acousticness` |

**Final score** = `0.30 * genre + 0.25 * mood + 0.25 * energy_proximity + 0.20 * acoustic_score`

This produces a score between **0.0** (terrible match) and **1.0** (perfect match).

#### Why These Weights?

- **Genre (30%)** — strongest categorical signal; defines the musical structure and sonic palette. A genre match is a hard filter that anchors the recommendation.
- **Mood (25%)** — core "vibe" dimension; captures emotional feel. Cross-genre (e.g., "chill" applies to lofi, ambient, jazz), so it connects songs that genre alone would miss.
- **Energy (25%)** — continuous precision within genre/mood clusters. Differentiates "chill lofi for studying" (energy=0.35) from "chill lofi for a party" (energy=0.60).
- **Acousticness (20%)** — texture preference. Maps directly to the `likes_acoustic` boolean; rewards organic/acoustic sound or electronic/synthetic sound based on user preference.

### Ranking Rule (List of Songs)

After every song is scored, the system:

1. Sorts all songs by score in descending order
2. Selects the top-k songs (default: 5)
3. Attaches an explanation string to each recommendation

### Example Flow

```
User Profile: genre=lofi, mood=chill, energy=0.4, likes_acoustic=True
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
 "Library Rain — Score: 0.96 — Matches your love of lofi; Has the chill vibe you enjoy;
 Energy level (0.35) fits your preference; Is acoustic like you prefer"
```

### Algorithm Recipe (Finalized)

The system uses a two-step process — **Scoring Rule** (one song) and **Ranking Rule** (list of songs) — to produce recommendations.

**Step 1: Score each song individually (Scoring Rule)**

Each song earns up to 1.0 points total, split across four components:

| Component | Points Available | Rule |
|---|---|---|
| Genre match | +0.30 | Exact match = 0.30; no match = 0.0 |
| Mood match | +0.25 | Exact match = 0.25; no match = 0.0 |
| Energy proximity | +0.25 | `0.25 × (1.0 - abs(target_energy - song_energy))` |
| Acoustic match | +0.20 | If `likes_acoustic=True`: `0.20 × acousticness`; if `False`: `0.20 × (1.0 - acousticness)` |

**Maximum possible score:** 1.0 (perfect match on all four components)
**Minimum possible score:** 0.0 (no matches at all)

**Step 2: Rank all songs and return top-k (Ranking Rule)**

1. Score every song in the catalog using the Scoring Rule
2. Sort all songs by score in descending order
3. Select the top-k songs (default: k=5)
4. Attach an explanation string to each recommendation listing which components matched

### Potential Biases

This system, while simple and transparent, has several known biases:

- **Genre over-prioritization:** Genre carries the most weight (30%), so a genre match alone gives a song a significant head start. A song that perfectly matches mood, energy, and acousticness but has the wrong genre will lose to a genre-matching song that scores poorly on everything else. This means great songs outside the user's preferred genre may never surface.
- **Mood as a blunt instrument:** Mood is categorical (exact match or nothing). A song with mood="focused" gets zero mood points for a user who prefers "chill," even though "focused" and "chill" are closely related feelings. The system cannot distinguish near-miss moods from total mismatches.
- **Binary acoustic preference:** The `likes_acoustic` boolean forces a hard split between acoustic and electronic. A user who sometimes likes both cannot express that nuance — they must pick one.
- **No diversity enforcement:** The top-5 results may all be the same genre and mood if the catalog is skewed. There is no mechanism to ensure variety in the recommendations.
- **Catalog bias:** The scoring only works well if the catalog contains songs that match the user's profile. With only 18 songs, some preference combinations (e.g., genre=metal + mood=relaxed) may have no good matches at all.

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

User profile: genre=lofi, mood=chill, energy=0.4, likes_acoustic=True

```
Top recommendations:

Library Rain - Score: 0.96
Because: Matches your love of lofi; Has the chill vibe you enjoy; Energy level (0.35) fits your preference; Is acoustic like you prefer

Midnight Coding - Score: 0.94
Because: Matches your love of lofi; Has the chill vibe you enjoy; Energy level (0.42) fits your preference; Is acoustic like you prefer

Focus Flow - Score: 0.71
Because: Matches your love of lofi; Energy level (0.40) fits your preference; Is acoustic like you prefer

Spacewalk Thoughts - Score: 0.65
Because: Has the chill vibe you enjoy; Energy level (0.28) fits your preference; Is acoustic like you prefer

Porch Swing Evenings - Score: 0.43
Because: Energy level (0.38) fits your preference; Is acoustic like you prefer
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



