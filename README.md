# AgriGuard AI (core detection workflow)

Tomato leaf disease check: upload a photo, get a prediction with an honest confidence/uncertainty status and curated guidance. Preliminary only; it never replaces an agricultural expert.

## Status

| Done | Not built yet |
|---|---|
| Backend: `/health`, `/api/crops`, `/api/advice/{class}`, `/api/predict` | Tamil UI and Tamil advice text |
| Upload validation (content check, size, dimensions, blur/light warnings) | Scan history, delete, `/api/history*` (needs DB + auth) |
| Uncertainty logic (confidence threshold + margin) | Analytics dashboard, `/api/analytics` |
| ML scripts: prepare, train, evaluate | Disease library page, Settings/Help, auth |
| React: Home, Detect (upload, preview, results, advice) | Frontend tests, Docker, deployment |
| 15 backend tests with a mocked model | Real measured model metrics (you must train it) |

`scan_id` is generated per request but **nothing is stored yet**.

## Run (Windows PowerShell)

    # 1. Dataset + model (Colab is fine for training; copy models/ back afterwards)
    python -m venv .venv; .\.venv\Scripts\Activate.ps1
    pip install -r backend\requirements.txt matplotlib scikit-learn
    git clone --depth 1 https://github.com/spMohanty/PlantVillage-Dataset data\PlantVillage-Dataset
    python ml\prepare_dataset.py --source data\PlantVillage-Dataset\raw\color --out data\tomato_split
    python ml\train.py --epochs 15 --finetune-epochs 5
    python ml\evaluate.py

    # 2. Backend
    cd backend; copy .env.example .env
    uvicorn app.main:app --reload        # http://localhost:8000/docs

    # 3. Frontend (new terminal)
    cd frontend; copy .env.example .env; npm install; npm run dev

Without a trained model the app still starts; `/health` shows `model_available: false` and `/api/predict` returns 503.

## Tests

    cd backend; pytest

## Important notes

- Set `CONFIDENCE_THRESHOLD` / `MIN_MARGIN` from the threshold sweep printed by `evaluate.py`, not the defaults.
- PlantVillage photos are lab-style; test scores will likely overstate field performance. Test with real field photos before claiming anything.
- `disease_information.json` is marked `draft_needs_expert_review`: sources name institutions only, with no URLs or review dates. Verify against TNAU/ICAR material and fill in `last_reviewed` before any public use. It deliberately contains no pesticide names or dosages.
