# 🌱 AgriGuard AI – Crop Disease Detection System

AgriGuard AI is an AI-powered crop disease detection system that uses deep learning to identify tomato leaf diseases from uploaded images. It helps users recognize potential plant diseases and access relevant information and agricultural advice.

## 🚀 Features

- **AI-Based Disease Detection:** Predicts tomato leaf diseases from leaf images using a trained deep learning model.
- **Five-Class Classification:** Identifies healthy tomato leaves, bacterial spot, early blight, late blight, and leaf mold.
- **Confidence Score:** Displays the model's prediction confidence.
- **Disease Information:** Provides information about detected diseases.
- **Agricultural Advice:** Offers relevant guidance to help users understand possible next steps.
- **Interactive Web Interface:** Simple and user-friendly frontend for uploading leaf images and viewing predictions.
- **REST API:** FastAPI backend for image processing and model predictions.

## 🛠️ Technologies Used

- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** Python, FastAPI
- **Deep Learning:** TensorFlow, Keras, MobileNetV2
- **Image Processing:** Pillow
- **Model Training:** Transfer Learning
- **Version Control:** Git and GitHub

## 🍅 Supported Tomato Classes

1. Tomato Healthy
2. Tomato Bacterial Spot
3. Tomato Early Blight
4. Tomato Late Blight
5. Tomato Leaf Mold

## 🏗️ Project Structure

```text
agriguard-ai-core/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── ml/
│   ├── train.py
│   ├── evaluate.py
│   └── prepare_dataset.py
├── models/
│   ├── crop_disease.keras
│   ├── class_names.json
│   └── history.json
├── data/
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sanjai-A-07/Agriguard-ai.git
cd Agriguard-ai
```

### 2. Set up the Python backend

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the backend from the project root:

```bash
python -m uvicorn app.main:app --app-dir backend --reload
```

The API documentation will be available at:

`http://127.0.0.1:8000/docs`

### 3. Set up the frontend

Open another terminal and run:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your terminal.

## 🧠 Model Training

AgriGuard AI uses MobileNetV2 transfer learning to classify tomato leaf images.

The model can be trained using the prepared dataset:

```bash
python ml/train.py --data data/tomato_split --out models --batch 16 --epochs 5
```

The trained model and class-name mapping are stored in the `models/` directory.

## 📊 Initial Training Results

The model achieved the following results during an initial five-epoch training run:

- **Training Accuracy:** 88.95%
- **Validation Accuracy:** 89.41%
- **Validation Loss:** 0.3000

These are initial training results, not independently verified test-set performance. Further evaluation on unseen images is recommended.

## 🔮 Future Enhancements

- Support for additional crops and plant diseases.
- Improve model accuracy using further training and evaluation.
- Add multilingual support for farmers.
- Integrate weather and environmental information.
- Deploy the application online for wider accessibility.

## ⚠️ Disclaimer

AgriGuard AI is an educational AI project. Its predictions are not a substitute for professional agricultural diagnosis. For important crop-management decisions, consult a qualified agricultural expert.

## 👨‍💻 Developer

**Sanjai A**

B.E. Computer Science and Engineering – Artificial Intelligence and Machine Learning

GitHub: [Sanjai-A-07](https://github.com/Sanjai-A-07)

## 📄 License

A license has not yet been specified for this project. Please add an appropriate license before allowing others to reuse or distribute the code.

---

⭐ If you find this project interesting, consider starring the repository!
