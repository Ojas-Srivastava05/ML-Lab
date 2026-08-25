# ML Lab — SVNIT

Machine Learning lab assignments for the Department of Artificial Intelligence.

## Quick start

```bash
cd "ML Lab"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Open the notebook for the assignment you need:

| Assignment | Notebook |
|---|---|
| Assignment 1 | `Assignment 1/Assignment_1_Solutions.ipynb` |
| Assignment 2 | `Assignment 2/Assignment_2_Solutions.ipynb` |
| Assignment 3 | `Assignment 3/Assignment_3_Solutions.ipynb` |

```bash
jupyter notebook "Assignment 1/Assignment_1_Solutions.ipynb"
```

## Project structure

```
ML Lab/
├── requirements.txt
├── data/
│   ├── train.csv
│   └── heart_disease.csv
├── outputs/
│   └── house_prices_clean.csv
├── plots/
│   ├── house_prices/
│   ├── assignment_2/
│   └── assignment_3/
├── Assignment 1/
│   ├── Assignment_1_Solutions.ipynb
│   ├── ML-1.pdf
│   ├── Labassignment.pdf
│   └── Graded+Quiz+*.ipynb
├── Assignment 2/
│   ├── Assignment_2_Solutions.ipynb
│   └── Assignment-2.pdf
└── Assignment 3/
    ├── Assignment_3_Solutions.ipynb
    ├── LAB ASSIGNMENT.pdf
    └── heart_v2.pdf
```

## What's in each notebook

| Notebook | Topics |
|---|---|
| Assignment 1 | Python/NumPy (ML-1) + House Prices EDA, preprocessing, KNN |
| Assignment 2 | Simple & multiple linear regression |
| Assignment 3 | Decision tree, ROC/AUC, GridSearchCV, SMOTE |
