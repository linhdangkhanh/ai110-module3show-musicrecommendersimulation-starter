# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder generates song recommendations from an 18-song catalog based on four user preferences: genre, mood, energy level, and acoustic vs. electronic taste.

It assumes the user can say what they want to hear — a genre label, a mood, an energy level, and whether they prefer acoustic or electronic sound.

This is designed for classroom exploration and learning about how recommender systems work. It is not intended for real streaming platforms or production use.

---

## 3. How the Model Works  

Each song in the catalog has 10 attributes, but only 4 are used for scoring: genre, mood, energy, and acousticness. The user provides 4 preferences that map directly to those attributes.

Every song earns up to 1.0 points total, split across four components:

- **Genre match (0.30 points):** If the song's genre matches the user's preferred genre, it gets the full 0.30. Otherwise it gets zero. This is the biggest single signal because genre defines the musical structure.
- **Mood match (0.25 points):** If the song's mood matches the user's preferred mood, it gets 0.25. Otherwise zero. Mood captures the emotional feel — happy, chill, intense, etc.
- **Energy proximity (0.25 points):** The closer the song's energy level is to the user's target, the more points it gets. A perfect match (e.g., song energy = 0.4, target = 0.4) scores 0.25. A big gap (e.g., song energy = 0.9, target = 0.4) scores much less.
- **Acoustic match (0.20 points):** If the user likes acoustic, songs with high acousticness score better. If the user likes electronic, songs with low acousticness score better.

After every song is scored, the system sorts them from highest to lowest and returns the top 5. Each recommendation comes with a human-readable explanation listing which components matched.

---

## 4. Data  

The catalog contains 18 songs — 10 from the original starter file and 8 added to increase diversity.

**Genres represented (15):** pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, electronic, blues, classical, hip-hop, reggae, metal, folk

**Moods represented (13):** happy, chill, intense, relaxed, moody, focused, romantic, energetic, sad, nostalgic, angry, uplifting, dark

**Numerical features:** energy (0.28–0.97), valence (0.25–0.90), danceability (0.30–0.91), acousticness (0.02–0.95), tempo (60–165 BPM)

**What's missing:** lyrics, release date, language, artist popularity, listener history, playlist co-occurrence data. The catalog is small and hand-curated — not representative of a real streaming service with millions of tracks.

---

## 5. Strengths  

The system works well when genre and mood both match the user's preferences. For example, a chill lofi listener gets Library Rain and Midnight Coding as top picks — both are lofi, chill, and acoustic, which is exactly right.

It handles impossible preference combinations gracefully. When a user asks for "metal + relaxed + low energy," no songs in the catalog match all three. Instead of crashing or returning random results, the system falls back to energy proximity and acoustic preference, returning the closest available matches (folk and jazz tracks with low energy and acoustic sound).

Every recommendation comes with a human-readable explanation. You can trace exactly why each song was recommended — which features matched and which didn't.

The system is fully transparent. There is no hidden model or training process. Every point in every score can be traced to a specific feature comparison, making the logic easy to inspect and understand.

---

## 6. Limitations and Bias 

The system over-prioritizes genre because a genre match alone awards 0.30 points — more than any other single component. This means a song that perfectly matches mood, energy, and acousticness but has the wrong genre will lose to a genre-matching song that scores poorly on everything else. For example, Gym Hero (pop, intense, energy=0.93) beats Storm Runner (rock, intense, energy=0.91) for a "high-energy pop" user even though Storm Runner's energy is nearly identical — solely because Gym Hero gets the genre bonus. Mood is treated as a hard binary (exact match or zero), so closely related moods like "chill" and "focused" are treated as total mismatches even though they describe similar listening contexts. The catalog also skews toward lofi (3 of 18 songs) and pop (2 of 18), while metal, classical, and reggae have only one song each, making recommendations for those genres less diverse. Finally, the binary `likes_acoustic` preference forces users to choose between acoustic and electronic, when many listeners enjoy both depending on context.

---

## 7. Evaluation

I tested five distinct user profiles: Chill Lofi, High-Energy Pop, Deep Intense Rock, Sad Acoustic, and a Conflicting profile (metal + relaxed + low energy). Each profile was designed to stress-test a different aspect of the scoring logic.

**Chill Lofi vs High-Energy Pop:** These two profiles produce completely different top-5 lists, which is correct. Chill Lofi gets Library Rain (0.96) and Midnight Coding (0.94) — both lofi, chill, and acoustic. High-Energy Pop gets Sunrise City (0.96) — pop, happy, and electronic. The system successfully differentiates when genre and mood align with the user's preferences.

**High-Energy Pop vs Deep Intense Rock:** Both profiles want high energy, but their genre preferences pull different songs to the top. Pop gets Sunrise City first (genre match), rock gets Storm Runner first (genre match). Gym Hero appears in both top-5 lists because its high energy (0.93) makes it a strong energy-proximity match for any high-energy profile, even when the mood doesn't match (intense ≠ happy). This revealed that energy proximity can override mood mismatches for high-energy songs.

**Sad Acoustic:** Whiskey Blues dominates at 0.95 because it matches all four components: blues genre, sad mood, low energy (0.45 ≈ 0.4 target), and high acousticness (0.82). The remaining top-5 slots are filled by songs that match energy and acousticness but not genre or mood — showing the system correctly falls back to proximity scoring when exact matches don't exist.

**Conflicting metal + relaxed + low energy:** This was the most interesting test. No metal songs have a "relaxed" mood or low energy in the catalog, so the genre and mood components score 0.0 for every song. The system correctly falls back to energy proximity and acoustic preference, returning Porch Swing Evenings (folk, relaxed, energy=0.38) and Coffee Shop Stories (jazz, relaxed, energy=0.37) as the best available matches. This shows the system handles impossible preference combinations gracefully rather than crashing or returning random results.

**Weight shift experiment:** I temporarily doubled the energy weight (0.25 → 0.50) and halved the genre weight (0.30 → 0.15). The most notable change was Spacewalk Thoughts jumping from #4 to #3 in the Chill Lofi profile — its energy (0.28) is very close to the target (0.4), so the increased energy weight boosted its score. The Conflicting profile scores jumped from 0.67 to 0.80 because energy proximity became the dominant signal, making the impossible genre match less punishing. This confirmed that genre weight is the main reason some profiles feel "locked in" to specific genres.

**Surprise finding:** The same song (Spacewalk Thoughts) appeared in four of five profiles' top-5 lists. Its low energy (0.28) and high acousticness (0.92) make it a universal fallback for any low-energy or acoustic preference, regardless of genre. This is a feature, not a bug — it shows proximity scoring works — but it also means the system may over-recommend a small set of "versatile" songs across unrelated profiles.

---

## 8. Future Work  

**Mood similarity scoring:** Right now, "chill" and "focused" are treated as total mismatches even though they describe similar listening contexts. I would add mood similarity using word embeddings or a hand-crafted similarity matrix so that closely related moods get partial credit.

**Diversity enforcement:** The top-5 results sometimes repeat the same genre and mood. I would add a rule that limits how many songs from the same genre or mood can appear in the top results, forcing the system to surface more variety.

**Expanded catalog:** With only 18 songs, a few "versatile" tracks appear in almost every profile. Growing the catalog to 100+ songs would reduce this problem and make the recommendations feel more personalized.

---

## 9. Personal Reflection  

**Biggest learning moment:** I was surprised that a simple weighted sum — just four numbers multiplied and added together — can produce recommendations that actually feel reasonable. I expected to need something much more complex. The key insight was that the weights matter more than the algorithm: changing genre from 0.30 to 0.15 completely changed which songs ranked first, even though the code stayed the same.

**How AI tools helped:** AI helped me design the initial scoring formula, explained the difference between cosine similarity and proximity scoring, and suggested adversarial test profiles I wouldn't have thought of (like "metal + relaxed + low energy"). I needed to double-check the weight balance — AI initially suggested equal weights for all components, but testing showed that genre needed to be slightly higher to anchor the recommendations. AI also helped me identify that Spacewalk Thoughts was appearing in too many profiles, which led me to discover the "universal fallback" problem.

**What surprised me:** How much the catalog shape matters. With only 18 songs, the system's behavior is heavily influenced by which songs exist — not just by the scoring logic. A larger catalog would make the same algorithm feel much more personalized. I also surprised myself by how much the explanation strings changed my perception of the recommendations. Seeing "Matches your love of lofi; Has the chill vibe you enjoy" makes the system feel intelligent, even though it's just reporting what the math found.

**What I'd try next:** I would add collaborative filtering using playlist co-occurrence data — if users frequently put two songs on the same playlist, those songs are similar regardless of their audio features. I would also build a Streamlit UI so users could adjust their preferences with sliders and see recommendations update in real time.
