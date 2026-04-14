# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder CLI 1.0

---

## 2. Intended Use

This recommender suggests top songs from a small local CSV catalog using a single user taste profile.
It is designed for classroom exploration of recommender system logic, not for production use.
It assumes users can be represented by a few explicit preferences (genre, mood, energy, tempo, valence, danceability, acoustic preference).

---

## 3. How the Model Works

Each song is compared to user preferences and gets a compatibility score.
If genre matches, it gets a strong bonus. If mood matches, it gets a smaller bonus.
Numeric features (energy, tempo, valence, danceability) are scored by closeness to the user target so near values are rewarded more than simply high values.
Acousticness is handled as a preference bonus (higher if the user likes acoustic, lower otherwise).
After scoring all songs, the recommender sorts by score and returns top-k tracks with explanation strings.

---

## 4. Data

The catalog contains 18 songs in `data/songs.csv`.
I started with the 10-song starter set and added 8 songs.
Genres now include pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip hop, metal, country, reggae, techno, rnb, and folk.
Moods include happy, chill, intense, relaxed, moody, focused, calm, confident, aggressive, warm, uplifting, euphoric, soulful, and nostalgic.
The dataset is still small and does not include lyrics, language, cultural context, or listening history.

---

## 5. Strengths

The recommender works well when the user profile has clear genre and mood targets.
It gave intuitive top picks for the tested profiles:
- High-Energy Pop: Sunrise City and Gym Hero scored high.
- Chill Lofi: Library Rain and Midnight Coding scored high.
- Deep Intense Rock: Storm Runner scored highest.
The explanations make results transparent because each recommendation includes score reasons.

---

## 6. Limitations and Bias

The system can over-prioritize exact genre matching, which can suppress cross-genre discoveries.
Because the catalog is tiny, a few songs can dominate multiple profiles.
The model assumes taste is static and independent of context (time of day, activity, language, social trends).
There is a filter-bubble risk: users may repeatedly get very similar songs due to deterministic ranking.
The model does not include fairness constraints, so representation in top-k results depends heavily on feature distribution in the CSV.

---

## 7. Evaluation

I evaluated the system with three profiles:
- High-Energy Pop
- Chill Lofi
- Deep Intense Rock

I checked whether top recommendations aligned with expected vibe and whether reasons made sense.
I also ran a sensitivity experiment by doubling energy weight and halving genre weight.
In that experiment, Rooftop Lights moved above Gym Hero for the pop profile, showing ranking sensitivity to weight design.
I also ran unit tests (`python -m pytest`), and all tests passed.

---

## 8. Future Work

1. Add diversity constraints so top-k does not over-repeat artist or genre.
2. Add multi-mode scoring (genre-first, mood-first, energy-focused).
3. Add richer features like popularity, release decade, and lyric sentiment.
4. Learn weights from feedback instead of hard-coding them.

---

## 9. Personal Reflection

The biggest learning moment was seeing how much ranking behavior changes from small weight adjustments.
AI tooling was useful for drafting structure quickly, but I had to verify import behavior, run tests, and inspect outputs to ensure the logic really matched expectations.
I was surprised that a simple weighted formula can already feel like a recommender when explanations are shown.
If I extend this project, I would focus on diversity and feedback loops so recommendations stay useful without getting repetitive.
