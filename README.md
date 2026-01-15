# 🎓 Student Exam Score Predictor AI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **End-to-End Machine Learning System to Predict Student Performance & Exam Scores.**

## 🔍 Overview
**Student Exam Score Predictor AI** is a full-stack machine learning application designed to help educators and students understand the key factors driving academic success. 

Unlike simple scripts, this is a **production-ready system** that includes:
-   **Automated Data Pipeline:** Cleans, scales, and processes raw CSV data automatically.
-   **Robust Regression Model:** Trained on 20,000+ records to predict scores with **73%+ accuracy**.
-   **Interactive Web Dashboard:** A beautiful Dark Mode UI built with **Next.js**.
-   **Explainable AI (XAI):** Visualizes *exactly* why a specific score was predicted (e.g., "High study hours increased score by 15%").

## 🌟 Key Features
*   **🧠 AI-Powered Predictions:** Uses advanced Linear Regression to forecast exam results.
*   **📊 Dynamic Insights:** Interactive charts powered by `recharts` to show feature importance.
*   **⚡ High Performance:** Backend powered by **FastAPI** for sub-millisecond inference.
*   **🎨 Premium UI/UX:** Fully responsive, modern design with smooth animations.
*   **🐳 Dockerized:** One-command deployment using `docker-compose`.

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **ML Core** | Python, Scikit-Learn, Pandas, NumPy, Joblib |
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | Next.js 14 (React), CSS Modules, Recharts |
| **DevOps** | Docker, Docker Compose |
| **Analysis** | Matplotlib, Seaborn, Jupyter |

## 🚀 Quick Start (Docker)
The best way to run this project is with Docker.

```bash
# 1. Clone the repository
git clone https://github.com/anish-devgit/student-performance-predictor-ai.git
cd student-performance-predictor-ai

# 2. Start the application
docker-compose up --build
```

*   **Frontend:** [http://localhost:3000](http://localhost:3000)
*   **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

## 💻 Manual Installation
<details>
<summary>Click to expand</summary>

### Backend
```bash
cd app/backend
pip install -r ../../requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd app/frontend
npm install
npm run dev
```
</details>

## 📊 Model Performance
The model was trained and evaluated on a dataset of 20,000 students.
*   **RMSE (Root Mean Square Error):** 9.77
*   **R² Score:** 0.733
*   **Top Predictors:** `class_attendance`, `study_hours`, `previous_scores`.

## 👥 Author
**Anish Raj**
*   **GitHub:** [@anish-devgit](https://github.com/anish-devgit)
*   **Sponsor:** [Sponsor Me](https://github.com/sponsors/anish-devgit)

---
*Made with ❤️ for the Open Source Community.*
