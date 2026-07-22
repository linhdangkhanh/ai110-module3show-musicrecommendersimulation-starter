# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

The system over-prioritizes genre because a genre match alone awards 0.30 points — more than any other single component. This means a song that perfectly matches mood, energy, and acousticness but has the wrong genre will lose to a genre-matching song that scores poorly on everything else. For example, Gym Hero (pop, intense, energy=0.93) beats Storm Runner (rock, intense, energy=0.91) for a "high-energy pop" user even though Storm Runner's energy is nearly identical — solely because Gym Hero gets the genre bonus. Mood is treated as a hard binary (exact match or zero), so closely related moods like "chill" and "focused" are treated as total mismatches even though they describe similar listening contexts. The catalog also skews toward lofi (3 of 18 songs) and pop (2 of 18), while metal, classical, and reggae have only one song each, making recommendations for those genres less diverse. Finally, the binary `likes_acoustic` preference forces users to choose between acoustic and electronic, when many listeners enjoy both depending on context.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

I tested five distinct user profiles: Chill Lofi, High-Energy Pop, Deep Intense Rock, Sad Acoustic, and a Conflicting profile (metal + relaxed + low energy). Each profile was designed to stress-test a different aspect of the scoring logic.

**Chill Lofi vs High-Energy Pop:** These two profiles produce completely different top-5 lists, which is correct. Chill Lofi gets Library Rain (0.96) and Midnight Coding (0.94) — both lofi, chill, and acoustic. High-Energy Pop gets Sunrise City (0.96) — pop, happy, and electronic. The system successfully differentiates when genre and mood align with the user's preferences.

**High-Energy Pop vs Deep Intense Rock:** Both profiles want high energy, but their genre preferences pull different songs to the top. Pop gets Sunrise City first (genre match), rock gets Storm Runner first (genre match). Gym Hero appears in both top-5 lists because its high energy (0.93) makes it a strong energy-proximity match for any high-energy profile, even when the mood doesn't match (intense ≠ happy). This revealed that energy proximity can override mood mismatches for high-energy songs.

**Sad Acoustic:** Whiskey Blues dominates at 0.95 because it matches all four components: blues genre, sad mood, low energy (0.45 ≈ 0.4 target), and high acousticness (0.82). The remaining top-5 slots are filled by songs that match energy and acousticness but not genre or mood — showing the system correctly falls back to proximity scoring when exact matches don't exist.

**Conflicting metal + relaxed + low energy:** This was the most interesting test. No metal songs have a "relaxed" mood or low energy in the catalog, so the genre and mood components score 0.0 for every song. The system correctly falls back to energy proximity and acoustic preference, returning Porch Swing Evenings (folk, relaxed, energy=0.38) and Coffee Shop Stories (jazz, relaxed, energy=0.37) as the best available matches. This shows the system handles impossible preference combinations gracefully rather than crashing or returning random results.

**Weight shift experiment:** I temporarily doubled the energy weight (0.25 → 0.50) and halved the genre weight (0.30 → 0.15). The most notable change was Spacewalk Thoughts jumping from #4 to #3 in the Chill Lofi profile — its energy (0.28) is very close to the target (0.4), so the increased energy weight boosted its score. The Conflicting profile scores jumped from 0.67 to 0.80 because energy proximity became the dominant signal, making the impossible genre match less punishing. This confirmed that genre weight is the main reason some profiles feel "locked in" to specific genres.

**Surprise finding:** The same song (Spacewalk Thoughts) appeared in four of five profiles' top-5 lists. Its low energy (0.28) and high acousticness (0.92) make it a universal fallback for any low-energy or acoustic preference, regardless of genre. This is a feature, not a bug — it shows proximity scoring works — but it also means the system may over-recommend a small set of "versatile" songs across unrelated profiles.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
