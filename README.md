#  ASL Alphabet Classification

> Fine-tuned **ResNet50** · FastAPI Backend · Streamlit Frontend

---

## 📁 Project Structure

```
CNN/
├── asl-alphabet.ipynb            # 📓 Training notebook (Kaggle)
├── requirements.txt              # 📦 Dependencies
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── main.py                   # 🚀 FastAPI entry point
│   ├── routers/
│   │   └── endpoint.py           #    /health, /predict endpoints
│   ├── schema/
│   │   └── schema.py             #    Pydantic response models
│   └── view/
│       └── streamlit_app.py      # 🎨 Streamlit web UI
│
├── models/                       # 💾 Trained model
│   └── asl_resnet50_final.keras
│
├── data/                         # 📂 Dataset (Kaggle)
│   ├── asl_alphabet_train/
│   └── asl_alphabet_test/
│
├── dataflow/                     # 📊 Architecture diagrams
│   └── DataFlow.png
│
└── outputs/                      # � Training plots & reports
    └── acc & loss.png
```

## 🚀 Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Download Dataset

[ASL Alphabet — Kaggle](https://www.kaggle.com/datasets/grassknoted/asl-alphabet) → extract into `data/`

### 3. Train

Open `asl-alphabet.ipynb` in Jupyter/Kaggle and run all cells.

**Pipeline:**
- 📸 87K images, 29 classes (A–Z + del, nothing, space)
- 🔄 Data augmentation (flip, rotate, zoom, brightness)
- 🧊 **Phase 1** — Frozen ResNet50 backbone (feature extraction)
- 🔥 **Phase 2** — Unfreeze top layers (fine-tuning)
- 💾 Saves `.keras` model to `models/`

### 4. Serve (FastAPI)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

📖 Swagger docs → **http://localhost:8000/docs**

| Method | Endpoint        | Description              |
|--------|----------------|--------------------------|
| GET    | `/api/health`  | Health check             |
| POST   | `/api/predict` | Upload image → top-5     |

**Response schema** (`/api/predict`):

```json
{
  "success": true,
  "top_label": "A",
  "top_confidence": 99.87,
  "predictions": [
    { "label": "A", "confidence": 99.87 },
    { "label": "S", "confidence": 0.05 }
  ]
}
```

### 5. Web UI (Streamlit)

```bash
streamlit run app/view/streamlit_app.py
```

🎨 Opens at **http://localhost:8501** — upload a hand sign image and get instant predictions!

> ⚠️ FastAPI must be running (step 4) before using Streamlit.

---

## 🧠 Model Details

| Item              | Detail                                          |
|-------------------|------------------------------------------------|
| **Base Model**    | ResNet50 (ImageNet pre-trained)                 |
| **Input Size**    | 224 × 224 × 3                                  |
| **Classes**       | 29 (A–Z + space + delete + nothing)             |
| **Phase 1**       | Frozen backbone, LR = 1e-3                      |
| **Phase 2**       | Unfreeze layer 140+, LR = 1e-5 (fine-tuning)   |
| **Augmentation**  | Flip, Rotation, Zoom, Translation, Brightness   |
| **Model Format**  | `.keras` (trainable weights preserved)           |

## 🛠️ Tech Stack

| Layer        | Technology                           |
|--------------|--------------------------------------|
| **DL Framework** | TensorFlow / Keras               |
| **API**      | FastAPI + Uvicorn                    |
| **Frontend** | Streamlit                            |
| **Schemas**  | Pydantic                             |
| **Image Processing** | Pillow, NumPy               |
| **Visualization** | Matplotlib, Seaborn             |

## 📜 License

This project was built as a **graduation project** for ASL alphabet recognition.
