"""Generate ML Lab study guide PDF for all 3 assignments."""

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ML_Lab_Study_Guide.pdf"


class GuidePDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "ML Lab Study Guide - SVNIT", align="R", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def cover(self, title, subtitle):
        self.add_page()
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(20, 20, 20)
        self.ln(40)
        self.multi_cell(0, 12, title, align="C")
        self.ln(8)
        self.set_font("Helvetica", "", 14)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 8, subtitle, align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 7, "Department of Artificial Intelligence\nSVNIT, Surat\nMachine Learning Lab", align="C")

    def part_title(self, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 70, 130)
        self.multi_cell(0, 9, text)
        self.ln(2)

    def section(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin)
        self.multi_cell(0, 8, text)
        self.ln(1)

    def subsection(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.set_x(self.l_margin)
        self.multi_cell(0, 7, text)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(20, 20, 20)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, f"  - {text}")
        self.ln(0.5)

    def table_row(self, cols, widths, bold=False):
        style = "B" if bold else ""
        self.set_font("Helvetica", style, 9)
        self.set_x(self.l_margin)
        for col, w in zip(cols, widths):
            self.cell(w, 7, col, border=1)
        self.ln()


def build():
    pdf = GuidePDF()
    pdf.set_auto_page_break(auto=True, margin=18)

    pdf.cover(
        "ML Lab Study Guide",
        "From Basics to All 3 Assignments",
    )

    # ========== FOUNDATIONS ==========
    pdf.add_page()
    pdf.part_title("Part 0: Foundations (Read This First)")
    pdf.body(
        "Before any assignment, understand the ML workflow:\n\n"
        "1. Get data\n"
        "2. Explore it (EDA)\n"
        "3. Clean it (missing values, outliers)\n"
        "4. Prepare features (encode, scale)\n"
        "5. Train a model\n"
        "6. Evaluate and interpret results\n\n"
        "Every assignment follows some version of this pipeline."
    )

    pdf.section("Key vocabulary")
    pdf.table_row(["Term", "Meaning"], [55, 135], bold=True)
    rows = [
        ("Feature (X)", "Input column used to make predictions"),
        ("Target (y)", "Output you want to predict"),
        ("Regression", "Predict a number (price, temperature)"),
        ("Classification", "Predict a category (disease / no disease)"),
        ("Train set", "Data used to teach the model"),
        ("Test set", "Unseen data used to check performance"),
        ("EDA", "Exploratory Data Analysis - understand data first"),
        ("Imputation", "Filling missing values"),
        ("Encoding", "Converting text categories to numbers"),
        ("Scaling", "Putting numeric features on similar scale"),
    ]
    for r in rows:
        pdf.table_row(list(r), [55, 135])

    pdf.section("Regression vs Classification")
    pdf.body(
        "Assignment 1 and 2 use REGRESSION because SalePrice is a continuous number.\n"
        "Assignment 3 uses CLASSIFICATION because heart disease is yes/no (0 or 1).\n\n"
        "Regression metrics: R2, MSE, RMSE, MAE\n"
        "Classification metrics: Accuracy, Precision, Recall, F1, AUC"
    )

    pdf.section("Common Python tools used")
    pdf.bullet("pandas: load and manipulate tables")
    pdf.bullet("numpy: numerical arrays and math")
    pdf.bullet("matplotlib / seaborn: plots")
    pdf.bullet("sklearn: models, metrics, preprocessing")
    pdf.bullet("scipy.stats: t-tests and statistical tests")

    # ========== ASSIGNMENT 1 ==========
    pdf.add_page()
    pdf.part_title("Assignment 1: House Prices Lab")
    pdf.body(
        "PDF: Labassignment-1.pdf\n"
        "Notebook: Assignment 1/Labassignment_1_Solutions.ipynb\n"
        "Dataset: data/train.csv (Kaggle House Prices, Ames Iowa)\n"
        "Target: SalePrice (house price in dollars)\n"
        "Features: about 79 columns (size, quality, neighborhood, etc.)"
    )

    pdf.section("What problem are you solving?")
    pdf.body(
        "You are preparing house data for price prediction. The assignment teaches the FULL "
        "data science pipeline: inspect, explore, clean, encode, scale, then fit linear regression."
    )

    pdf.subsection("Part A - Data Loading and Basic Inspection")
    pdf.body("Goal: Understand what data you have before touching models.")
    pdf.bullet("Load train.csv into a DataFrame")
    pdf.bullet("Show first 10 rows")
    pdf.bullet("Count rows and columns (~1460 rows, ~81 columns)")
    pdf.bullet("Separate numerical vs categorical columns")
    pdf.bullet("Fix wrong datatypes (MSSubClass looks numeric but is categorical)")
    pdf.body(
        "Why MSSubClass matters: values like 20, 60, 70 are class codes, not quantities. "
        "Treating them as numbers would mislead the model."
    )

    pdf.subsection("Part B - Univariate Analysis (one variable at a time)")
    pdf.body("Goal: Understand each feature individually.")
    pdf.bullet("Histograms for LotArea, GrLivArea, SalePrice, YearBuilt, OverallQual")
    pdf.bullet("Check skewness: right-skewed means long tail on the right (common for price)")
    pdf.bullet("Bar charts for Neighborhood, HouseStyle, BldgType")
    pdf.bullet("Find most common and rare categories")
    pdf.bullet("Top 10 most frequent categories across all categorical columns")
    pdf.bullet("Find imbalanced features where one category dominates (>80%)")
    pdf.body(
        "Intuition: SalePrice is usually right-skewed (few very expensive homes). "
        "Imbalanced categories (e.g. almost all paved streets) give little predictive power."
    )

    pdf.subsection("Part C - Bivariate Analysis (relationships between two variables)")
    pdf.body("Goal: See how features relate to SalePrice.")
    pdf.bullet("Scatter GrLivArea vs SalePrice -> positive trend (bigger area, higher price)")
    pdf.bullet("Boxplot SalePrice by OverallQual -> higher quality, higher price")
    pdf.bullet("Correlation heatmap for top 10 features vs SalePrice")
    pdf.bullet("Compare two neighborhoods (e.g. NAmes vs NoRidge) using mean price + t-test")
    pdf.bullet("Compare new homes (YearBuilt >= 2000) vs old using boxplot + t-test")
    pdf.body(
        "Correlation (r): near +1 = move together, near -1 = opposite, near 0 = weak link.\n"
        "T-test p-value < 0.05 means the difference in means is statistically significant."
    )

    pdf.add_page()
    pdf.subsection("Part D - Missing Value Treatment")
    pdf.body("Goal: No missing values before modeling.")
    pdf.bullet("List top 5 columns with most missing values (PoolQC, Alley, Fence often top)")
    pdf.bullet("Numerical columns -> fill with median")
    pdf.bullet("Categorical columns -> fill with mode or 'Missing'")
    pdf.bullet("LotFrontage -> fill with median grouped by Neighborhood")
    pdf.bullet("Verify zero missing values remain")
    pdf.body(
        "Why median for LotFrontage by neighborhood? Frontage depends on area. "
        "Houses in the same neighborhood have similar lot sizes."
    )

    pdf.subsection("Part E - Outlier Detection (IQR method)")
    pdf.body("Goal: Handle extreme values in LotArea and GrLivArea.")
    pdf.bullet("IQR = Q3 - Q1")
    pdf.bullet("Outlier if value < Q1 - 1.5*IQR or > Q3 + 1.5*IQR")
    pdf.bullet("Count outliers in each feature")
    pdf.bullet("Cap (winsorize) or remove outliers - capping keeps all rows")
    pdf.bullet("Replot GrLivArea vs SalePrice scatter - relationship should look clearer")
    pdf.body(
        "Why cap instead of delete? You keep sample size. Extreme lots/areas won't "
        "distort the model as much after capping."
    )

    pdf.subsection("Part F - Feature Encoding and Scaling")
    pdf.body("Goal: Convert data into model-ready numeric form.")
    pdf.bullet("One-Hot Encoding: create 0/1 columns for categories (Neighborhood, RoofStyle)")
    pdf.bullet("Label Encoding: map categories to 0,1,2,... (high-cardinality columns)")
    pdf.bullet("StandardScaler: scale numeric features to mean 0, std 1")
    pdf.bullet("Save as outputs/house_prices_clean.csv")
    pdf.body(
        "Why encode? Models need numbers, not strings.\n"
        "Why scale? LotArea (thousands) should not dominate OverallQual (1-10) just because of units."
    )

    pdf.subsection("Part G - Linear Regression")
    pdf.body("Goal: Predict SalePrice using cleaned features.")
    pdf.bullet("Model: y = b0 + b1*x1 + b2*x2 + ... + error")
    pdf.bullet("Split train/test (e.g. 80/20)")
    pdf.bullet("Report R2, MSE, RMSE")
    pdf.bullet("Plot residuals and actual vs predicted")
    pdf.body(
        "R2 = fraction of price variance explained (e.g. 0.64 = 64%).\n"
        "RMSE = typical prediction error in dollars.\n"
        "High train R2 but lower test R2 = overfitting."
    )

    # ========== ASSIGNMENT 2 ==========
    pdf.add_page()
    pdf.part_title("Assignment 2: Linear Regression")
    pdf.body(
        "PDF: Assignment-2.pdf\n"
        "Notebook: Assignment 2/Assignment_2_Solutions.ipynb\n"
        "Dataset: data/train.csv (same House Prices data)\n"
        "Focus: Simple vs Multiple Linear Regression with proper evaluation"
    )

    pdf.section("Basics: What is Linear Regression?")
    pdf.body(
        "Linear regression finds the best straight-line (or hyperplane) relationship "
        "between features and a numeric target.\n\n"
        "Simple (1 feature):\n"
        "  SalePrice = beta0 + beta1 * GrLivArea + error\n\n"
        "Multiple (3+ features):\n"
        "  SalePrice = beta0 + b1*GrLivArea + b2*OverallQual + b3*GarageCars + error\n\n"
        "beta0 = intercept (baseline price)\n"
        "beta1, beta2... = how much target changes when that feature increases by 1"
    )

    pdf.subsection("Part A - Exploratory Data Analysis")
    pdf.bullet("Load dataset and inspect target SalePrice")
    pdf.bullet("Plot distribution (histogram) and comment on skewness")
    pdf.bullet("Correlation heatmap - which features correlate most with SalePrice?")
    pdf.body(
        "Expected: SalePrice is right-skewed. OverallQual and GrLivArea usually "
        "have strong positive correlation with price."
    )

    pdf.subsection("Part B - Simple Linear Regression")
    pdf.bullet("Pick one predictor (GrLivArea)")
    pdf.bullet("Write hypothesis: y = beta0 + beta1*x + epsilon")
    pdf.bullet("Fit model, report intercept and slope")
    pdf.bullet("Scatter plot with regression line")
    pdf.bullet("Interpret slope: +1 sq ft -> how much price increases")
    pdf.body(
        "Example interpretation: beta1 = 102 means each extra sq ft of living area "
        "is associated with about $102 higher SalePrice on average."
    )

    pdf.subsection("Part C - Multiple Linear Regression")
    pdf.bullet("Use at least 3 predictors (GrLivArea, OverallQual, GarageCars)")
    pdf.bullet("Write fitted equation with all coefficients")
    pdf.bullet("Interpret one coefficient (e.g. OverallQual)")
    pdf.bullet("Evaluate: R2, MSE, RMSE")
    pdf.bullet("Compare with simple model - which is better and why?")
    pdf.body(
        "Multiple regression usually wins because it uses more information.\n\n"
        "Metrics in plain English:\n"
        "  R2 = % of variance explained (higher is better)\n"
        "  MSE = average squared error (lower is better)\n"
        "  RMSE = typical error in dollars (lower is better)\n"
        "  RMSE as % of mean price = easier to interpret (e.g. 25% error)\n\n"
        "Example from your notebook:\n"
        "  Simple:  R2 ~ 55%, RMSE ~ 33% of mean price\n"
        "  Multiple: R2 ~ 76%, RMSE ~ 24% of mean price"
    )

    pdf.section("Residuals (important for viva)")
    pdf.body(
        "Residual = actual - predicted.\n"
        "Plot predicted vs residuals: points should scatter randomly around 0.\n"
        "Patterns in residuals mean the model is missing something (non-linearity, etc.)."
    )

    # ========== ASSIGNMENT 3 ==========
    pdf.add_page()
    pdf.part_title("Assignment 3: Decision Tree - Heart Disease")
    pdf.body(
        "PDF: Assignment 3/LAB ASSIGNMENT.pdf\n"
        "Notebook: Assignment 3/Assignment_3_Solutions.ipynb\n"
        "Dataset: data/heart_disease.csv (270 patients)\n"
        "Features: age, sex, BP, cholestrol\n"
        "Target: heart_disease (0 = no, 1 = yes)"
    )

    pdf.section("Basics: Classification vs Regression")
    pdf.body(
        "This is CLASSIFICATION, not regression. You predict a label (disease or not), "
        "not a number.\n\n"
        "Decision Tree: a flowchart of if-then rules.\n"
        "  Example: if sex <= 0.5 then go left, else go right\n"
        "           if BP <= 167 then ...\n"
        "At each leaf, majority vote decides the class."
    )

    pdf.subsection("Part A - Basic Implementation")
    pdf.bullet("Train DecisionTreeClassifier on heart data")
    pdf.bullet("Report train accuracy and test accuracy")
    pdf.bullet("Visualize tree and interpret first two splits")
    pdf.body(
        "Train accuracy >> test accuracy usually means overfitting.\n"
        "First splits tell you the most important features for separation."
    )

    pdf.subsection("Part B - Model Evaluation")
    pdf.bullet("Confusion matrix (TP, TN, FP, FN)")
    pdf.bullet("Classification report: precision, recall, F1")
    pdf.bullet("ROC curve and AUC score")
    pdf.body(
        "Confusion matrix layout:\n"
        "                 Predicted No   Predicted Yes\n"
        "  Actual No          TN              FP\n"
        "  Actual Yes         FN              TP\n\n"
        "Precision = TP / (TP + FP)  -> of predicted diseased, how many correct?\n"
        "Recall = TP / (TP + FN)     -> of actual diseased, how many caught?\n"
        "F1 = balance of precision and recall\n"
        "AUC = area under ROC curve (1.0 = perfect, 0.5 = random guessing)"
    )

    pdf.subsection("Part C - Hyperparameter Tuning")
    pdf.bullet("Vary max_depth, min_samples_split, min_samples_leaf")
    pdf.bullet("Compare train vs test accuracy for each setting")
    pdf.bullet("Use GridSearchCV to find best combination")
    pdf.body(
        "Overfitting: high train acc, lower test acc (tree too complex)\n"
        "Underfitting: both train and test acc low (tree too simple)\n"
        "GridSearchCV tries many combinations and picks the best via cross-validation."
    )

    pdf.subsection("Part D - Error Analysis")
    pdf.bullet("Find misclassified patients (rows where prediction != actual)")
    pdf.bullet("Compare mean features of misclassified vs correctly classified")
    pdf.bullet("Describe patterns (e.g. borderline cases near decision boundary)")
    pdf.body(
        "Misclassified patients often have moderate values - not clearly healthy or clearly sick. "
        "They sit near the tree's decision thresholds."
    )

    pdf.subsection("Part E - Class Imbalance")
    pdf.bullet("Check class distribution (disease vs no disease counts and %)")
    pdf.bullet("Use balanced accuracy if imbalanced")
    pdf.bullet("Try SMOTE (oversample minority class) or undersampling")
    pdf.body(
        "Accuracy alone can mislead with imbalanced data.\n"
        "Example: 90% class A -> always predicting A gives 90% accuracy but is useless.\n"
        "Balanced accuracy averages recall across classes.\n"
        "SMOTE creates synthetic minority samples to balance training data."
    )

    # ========== COMPARISON & EXAM PREP ==========
    pdf.add_page()
    pdf.part_title("Quick Comparison of All 3 Assignments")
    pdf.table_row(["", "Assignment 1", "Assignment 2", "Assignment 3"], [30, 55, 55, 55], bold=True)
    comp = [
        ("Type", "Regression", "Regression", "Classification"),
        ("Target", "SalePrice ($)", "SalePrice ($)", "heart_disease (0/1)"),
        ("Main goal", "Full pipeline + LR", "Simple vs Multiple LR", "Decision Tree"),
        ("Key plots", "Histograms, scatter", "Regression line", "Tree, ROC curve"),
        ("Key metrics", "R2, RMSE", "R2, MSE, RMSE", "Accuracy, AUC, F1"),
        ("Preprocessing", "Heavy (A-F)", "Light (EDA only)", "Minimal"),
    ]
    for row in comp:
        pdf.table_row(list(row), [30, 55, 55, 55])

    pdf.section("Formulas to remember")
    pdf.body(
        "Skewness: |skew| < 0.5 ~ normal; > 0.5 right-skewed\n\n"
        "IQR outlier: x < Q1 - 1.5*IQR  or  x > Q3 + 1.5*IQR\n\n"
        "R2 = 1 - (MSE / Var(y))  -> fraction of variance explained\n\n"
        "RMSE = sqrt(MSE)  -> error in same units as target\n\n"
        "RMSE % = (RMSE / mean(y)) * 100\n\n"
        "Precision = TP / (TP + FP)\n"
        "Recall = TP / (TP + FN)\n"
        "F1 = 2 * (Precision * Recall) / (Precision + Recall)"
    )

    pdf.section("Viva questions and answers")
    qa = [
        ("Why convert MSSubClass to categorical?", "It is a house type code, not a numeric quantity."),
        ("Why median imputation?", "Median is robust to outliers unlike mean."),
        ("Why cap outliers instead of deleting?", "Keeps all rows; reduces extreme influence."),
        ("Why one-hot encode?", "Categories have no natural order; avoids fake ordering."),
        ("Why scale features?", "Prevents large-scale features from dominating."),
        ("What does R2 = 0.76 mean?", "Model explains 76% of target variance."),
        ("Simple vs multiple regression?", "Multiple uses more features, usually better R2."),
        ("What is overfitting?", "Model memorizes training data, poor on test data."),
        ("What is AUC?", "Probability model ranks a random positive above a random negative."),
        ("Why SMOTE?", "Handles class imbalance by balancing training set."),
    ]
    for q, a in qa:
        pdf.subsection(f"Q: {q}")
        pdf.body(f"A: {a}")

    pdf.section("How to study with your notebooks")
    pdf.body(
        "1. Read this PDF section for an assignment\n"
        "2. Open the matching *_Solutions.ipynb\n"
        "3. Run cells one Part at a time\n"
        "4. For each Part, say: What did I do? Why? What does the output mean?\n"
        "5. Practice explaining plots and metrics without looking at code"
    )

    pdf.output(str(OUT))
    print(f"Created: {OUT}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    build()
