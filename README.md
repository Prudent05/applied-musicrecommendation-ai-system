# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This simulator builds a transparent, content-based music recommender that scores each song against a user taste profile, then ranks songs from best match to weakest match. It uses interpretable features from the catalog (genre, mood, energy, tempo, valence, danceability, acousticness) so we can see exactly why a song is recommended. The goal is not to copy Spotify scale, but to model the same core idea: convert taste signals into a numeric score and use that score to produce personalized suggestions.

---

## How The System Works

Explain your design in plain language.

Real platforms usually combine two strategies. Collaborative filtering predicts what you might like from behavior patterns of similar users (for example, co-listens, likes, skips, playlist overlap). Content-based filtering predicts from item attributes (for example, genre, mood, tempo, energy). This project prioritizes content-based logic so recommendations can be directly explained from song attributes.

In this simulator, each song gets a single compatibility score made from weighted feature matches. Exact matches on genre and mood get strong boosts, while numeric attributes use a distance rule: songs closer to the user's target value score higher, and songs farther away score lower. For energy-like features, a simple closeness term such as $1 - |x - t|$ (with values normalized to $[0,1]$) rewards "near the target" instead of simply "higher" or "lower." Acoustic preference is handled as a conditional bonus depending on whether the user prefers acoustic sound.

Scoring and ranking are separate on purpose. The scoring rule answers "How good is this one song for this one user?" The ranking rule answers "Out of all songs, which are best?" by sorting by score and returning the top $k$. This separation makes the system easier to debug, tune, and explain.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

Feature choices for this simulation:

- `Song` features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- `UserProfile` features: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

Algorithm recipe (high level):

- Add a weighted bonus for matching `genre`
- Add a weighted bonus for matching `mood`
- Add closeness points for `energy` using a distance-based score
- Add smaller closeness points for `tempo_bpm`, `valence`, and `danceability`
- Add or subtract points from `acousticness` based on `likes_acoustic`
- Sort songs by total score (highest first) and return top recommendations

Final weighted scoring recipe used in implementation:

- `+2.0` for genre match (or custom weight override)
- `+1.2` for mood match
- `energy_score = 1.5 * (1 - abs(song_energy - target_energy))`
- `tempo_score = 0.6 * (1 - min(abs(song_tempo - target_tempo) / 100, 1))`
- `valence_score = 0.5 * (1 - abs(song_valence - target_valence))`
- `danceability_score = 0.4 * (1 - abs(song_danceability - target_danceability))`
- acoustic preference bonus: `+0.5 * acousticness` if `likes_acoustic=True`, else `+0.5 * (1 - acousticness)`

Default user profile examples used in evaluation:

- High-Energy Pop: `{"genre": "pop", "mood": "happy", "energy": 0.85, "tempo_bpm": 125, "valence": 0.8, "danceability": 0.82, "likes_acoustic": False}`
- Chill Lofi: `{"genre": "lofi", "mood": "chill", "energy": 0.35, "tempo_bpm": 78, "valence": 0.58, "danceability": 0.58, "likes_acoustic": True}`
- Deep Intense Rock: `{"genre": "rock", "mood": "intense", "energy": 0.92, "tempo_bpm": 148, "valence": 0.45, "danceability": 0.62, "likes_acoustic": False}`

Data flow map:

```mermaid
flowchart LR
  A[Input: User Preferences] --> B[Load songs.csv]
  B --> C[Loop through each song]
  C --> D[Compute weighted score + reasons]
  D --> E[Store song, score, explanation]
  E --> F[Rank all songs by score descending]
  F --> G[Output top K recommendations]
```

Potential bias note:

This system can over-prioritize exact genre matches, which may hide strong cross-genre songs that match mood and energy very well.

You can include a simple diagram or bullet list if helpful.

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

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

What I tested:

- Added 8 new songs (IDs 11-18) to expand genre/mood diversity (classical, hip hop, metal, country, reggae, techno, rnb, folk).
- Ran 3 profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock).
- Ran a sensitivity experiment where energy weight was doubled and genre weight was halved.

Observed behavior:

- High-Energy Pop: `Sunrise City` ranked first, with `Gym Hero` and `Rooftop Lights` near the top.
- Chill Lofi: lofi tracks (`Library Rain`, `Midnight Coding`, `Focus Flow`) dominated as expected.
- Deep Intense Rock: `Storm Runner` ranked first due to direct genre/mood match and close energy.
- Weight-shift experiment changed ranking order by moving `Rooftop Lights` above `Gym Hero`, showing the recommender is sensitive to weight choices.

**Terminal output (`python -m src.main`):**

```
Loaded songs: 18

=== Profile: High-Energy Pop ===
 1. Sunrise City by Neon Echo | score=6.49
    reasons: genre match (+2.0); mood match (+1.2); energy closeness (+1.46); tempo closeness (+0.56); valence closeness (+0.48); danceability closeness (+0.39); non-acoustic preference (+0.41)
 2. Gym Hero by Max Pulse | score=5.27
    reasons: genre match (+2.0); energy closeness (+1.38); tempo closeness (+0.56); valence closeness (+0.48); danceability closeness (+0.38); non-acoustic preference (+0.47)
 3. Rooftop Lights by Indigo Parade | score=4.38
    reasons: mood match (+1.2); energy closeness (+1.36); tempo closeness (+0.59); valence closeness (+0.49); danceability closeness (+0.40); non-acoustic preference (+0.33)
 4. Neon Circuit by Vector Bloom | score=3.16
    reasons: energy closeness (+1.35); tempo closeness (+0.53); valence closeness (+0.44); danceability closeness (+0.37); non-acoustic preference (+0.46)
 5. Street Cipher by Nova Verse | score=3.00
    reasons: energy closeness (+1.33); tempo closeness (+0.43); valence closeness (+0.41); danceability closeness (+0.40); non-acoustic preference (+0.43)

=== Profile: Chill Lofi ===
 1. Library Rain by Paper Lanterns | score=6.58
    reasons: genre match (+2.0); mood match (+1.2); energy closeness (+1.50); tempo closeness (+0.56); valence closeness (+0.49); danceability closeness (+0.40); acoustic preference (+0.43)
 2. Midnight Coding by LoRoom | score=6.42
    reasons: genre match (+2.0); mood match (+1.2); energy closeness (+1.40); tempo closeness (+0.60); valence closeness (+0.49); danceability closeness (+0.38); acoustic preference (+0.35)
 3. Focus Flow by LoRoom | score=5.29
    reasons: genre match (+2.0); energy closeness (+1.42); tempo closeness (+0.59); valence closeness (+0.49); danceability closeness (+0.39); acoustic preference (+0.39)
 4. Spacewalk Thoughts by Orbit Bloom | score=4.34
    reasons: mood match (+1.2); energy closeness (+1.40); tempo closeness (+0.49); valence closeness (+0.46); danceability closeness (+0.33); acoustic preference (+0.46)
 5. Old Photo Roads by Maple Thread | score=3.32
    reasons: energy closeness (+1.47); tempo closeness (+0.59); valence closeness (+0.49); danceability closeness (+0.36); acoustic preference (+0.41)

=== Profile: Deep Intense Rock ===
 1. Storm Runner by Voltline | score=6.58
    reasons: genre match (+2.0); mood match (+1.2); energy closeness (+1.48); tempo closeness (+0.58); valence closeness (+0.48); danceability closeness (+0.38); non-acoustic preference (+0.45)
 2. Gym Hero by Max Pulse | score=4.30
    reasons: mood match (+1.2); energy closeness (+1.48); tempo closeness (+0.50); valence closeness (+0.34); danceability closeness (+0.30); non-acoustic preference (+0.47)
 3. Iron Pulse by Granite Sky | score=3.22
    reasons: energy closeness (+1.43); tempo closeness (+0.48); valence closeness (+0.45); danceability closeness (+0.38); non-acoustic preference (+0.48)
 4. Neon Circuit by Vector Bloom | score=3.11
    reasons: energy closeness (+1.46); tempo closeness (+0.53); valence closeness (+0.38); danceability closeness (+0.29); non-acoustic preference (+0.46)
 5. Night Drive Loop by Neon Echo | score=2.84
    reasons: energy closeness (+1.24); tempo closeness (+0.37); valence closeness (+0.48); danceability closeness (+0.36); non-acoustic preference (+0.39)

=== Experiment: Energy x2, Genre x0.5 (High-Energy Pop) ===
 1. Sunrise City by Neon Echo | score=6.95
    reasons: genre match (+1.0); mood match (+1.2); energy closeness (+2.91); tempo closeness (+0.56); valence closeness (+0.48); danceability closeness (+0.39); non-acoustic preference (+0.41)
 2. Rooftop Lights by Indigo Parade | score=5.74
    reasons: mood match (+1.2); energy closeness (+2.73); tempo closeness (+0.59); valence closeness (+0.49); danceability closeness (+0.40); non-acoustic preference (+0.33)
 3. Gym Hero by Max Pulse | score=5.65
    reasons: genre match (+1.0); energy closeness (+2.76); tempo closeness (+0.56); valence closeness (+0.48); danceability closeness (+0.38); non-acoustic preference (+0.47)
```

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

See `model_card.md` for the full model documentation and `reflection.md` for profile-by-profile comparison notes.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

