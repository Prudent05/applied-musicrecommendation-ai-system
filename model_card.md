# Model Card: VibeFinder CLI 2.0

## 1. Model Name

VibeFinder CLI 2.0 (Explainable Content-Based Music Recommender)

## 2. Intended Use

This system recommends top songs from a local catalog based on a user profile containing genre, mood, and numeric preference targets.

Intended users:
- students learning applied AI system design,
- instructors evaluating reliability and explainability,
- portfolio reviewers assessing practical AI engineering workflow.

Out of scope:
- production use at large scale,
- high-stakes use cases,
- personalized recommendations based on private behavioral history.

## 3. System Type and AI Behavior

This is a **specialized rule-based AI recommender** with explicit weighted scoring.

Behavior summary:
- categorical matching: genre and mood boosts,
- numeric closeness scoring: energy, tempo, valence, danceability,
- preference logic: acoustic vs non-acoustic bonus,
- ranked top-k outputs with human-readable explanations.

## 4. Data

Source: `data/songs.csv`

Dataset properties:
- 18 songs total,
- multiple genres and moods,
- structured numeric features normalized to recommender expectations.

Known data limitations:
- small catalog size,
- no lyrics/language/cultural metadata,
- no user interaction history,
- no external knowledge retrieval.

## 5. Evaluation and Reliability

Evaluation methods used:
- automated unit tests (`python -m pytest -q`),
- reliability harness (`python -m src.evaluate`) with predefined checks,
- out-of-range input test for guardrail validation.

Latest observed results:
- unit tests: 2/2 passed,
- reliability checks: 4/4 passed,
- average confidence: about 0.80.

Reliability interpretation:
- the model is consistent on representative profiles,
- confidence is useful as an internal stability signal,
- confidence is **not** equivalent to objective user satisfaction.

## 6. Guardrails and Safety

Implemented guardrails:
- clamp normalized numeric values to `[0,1]`,
- enforce non-negative tempo values,
- deterministic ranking and safe behavior for invalid `k`.

Operational controls:
- local-only data processing,
- transparent explanation strings per recommendation,
- reproducible test/evaluation scripts.

## 7. Limitations and Bias Risks

1. Feature bias
The model only optimizes the features it sees; unmodeled factors (lyrics, context, language preference) are ignored.

2. Catalog bias
Small and imbalanced catalogs can over-represent certain genres/artists in top-k outputs.

3. Filter bubble risk
Exact-match boosts can repeatedly reinforce similar music and reduce exploration.

4. Weight sensitivity
Small changes in weights can shift ranking order substantially.

## 8. Misuse Risks and Mitigations

Potential misuse:
- presenting this classroom system as a production-grade recommendation engine,
- overstating confidence as a guarantee of recommendation quality,
- using narrow profiles to justify exclusionary content decisions.

Mitigations:
- clear intended-use statement in documentation,
- explicit limitation and confidence caveats,
- transparent feature-level explanations for auditability,
- recommendation to add diversity constraints before broader deployment.

## 9. Reflection on Testing and Surprises

What surprised me:
- rankings changed more than expected from modest weight changes,
- deterministic outputs still required evaluation because intuitive expectations can be wrong.

Main takeaway:
- reliable AI systems need both algorithm design and systematic testing artifacts.

## 10. Collaboration with AI During Development

Helpful AI suggestion:
- AI suggested adding a dedicated reliability harness script that runs fixed scenarios and reports pass/fail plus confidence. This improved the project from "demo only" to "measurable system behavior."

Flawed AI suggestion:
- AI initially suggested running plain `pytest`, which failed in this environment due to module path resolution (`ModuleNotFoundError: src`). The corrected command `python -m pytest -q` worked. This reinforced the need to verify AI suggestions in the real runtime environment.
