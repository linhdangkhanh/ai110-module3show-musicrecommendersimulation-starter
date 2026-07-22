"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def run_profile(name, user_prefs, songs, k=5):
    """Run one profile and print labeled results."""
    print(f"\n{'='*60}")
    print(f"Profile: {name}")
    print(f"  genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, acoustic={user_prefs['likes_acoustic']}")
    print(f"{'='*60}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"  {i}. {song['title']} ({song['artist']}) - Score: {score:.2f}")
        print(f"     Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs\n")

    profiles = [
        {"name": "Chill Lofi",
         "genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True},

        {"name": "High-Energy Pop",
         "genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},

        {"name": "Deep Intense Rock",
         "genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},

        {"name": "Sad Acoustic",
         "genre": "blues", "mood": "sad", "energy": 0.4, "likes_acoustic": True},

        {"name": "Conflicting: metal + relaxed + low energy",
         "genre": "metal", "mood": "relaxed", "energy": 0.3, "likes_acoustic": True},
    ]

    for profile in profiles:
        name = profile.pop("name")
        run_profile(name, profile, songs)


if __name__ == "__main__":
    main()
