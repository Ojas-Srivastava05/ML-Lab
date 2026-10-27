"""Create commented solution notebooks for Assignments 6 and 7."""

import uuid
from pathlib import Path

import nbformat
from nbformat import v4 as nbf

ROOT = Path("/Users/ojas/Desktop/ML Lab")


def nid():
    return str(uuid.uuid4())


def md(text):
    cell = nbf.new_markdown_cell(text.strip() + "\n")
    cell["id"] = nid()
    return cell


def code(text):
    cell = nbf.new_code_cell(text.strip() + "\n")
    cell["id"] = nid()
    cell["execution_count"] = None
    cell["outputs"] = []
    return cell


def notebook(cells):
    nb = nbf.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    nb["cells"] = cells
    return nb


def write_a6():
    cells = []
    cells.append(md("""
# Assignment 6 — Class imbalance, hypothesis tests, and Naive Bayes

**SVNIT — Department of Artificial Intelligence**

**Question sheet:** `LAB ASSIGNMENT-6.pdf`

Two separate problems:

1. **Credit-card fraud** (`../data/creditcard.csv`, 284,807 transactions). Class `1` is fraud and is about 0.17% of the rows. Parts A–D cover EDA, why imbalance breaks accuracy, under-sampling, over-sampling / SMOTE, and a hypothesis test used as a feature check.
2. **SMS spam** (`../data/sms_spam.tsv`). Clean the text, turn it into numbers, then compare Bernoulli Naive Bayes with Multinomial Naive Bayes.

Plots are saved to `../plots/assignment_6/` and shown under the code that creates them. Every code cell is commented so the *reason* for each step is in the notebook.
"""))

    cells.append(code(r'''
import string
import warnings
from pathlib import Path

import matplotlib
# Agg writes plots to files. That avoids huge inline PNGs in the notebook.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
pd.set_option("display.float_format", lambda x: f"{x:,.4f}")
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)


def find_project_root():
    """Walk upwards until we find the data/ folder, so the notebook runs
    whether the kernel's working directory is the repo or the Assignment 6 folder."""
    starts = [Path.cwd().resolve()]
    for key in ("__vsc_ipynb_file__", "__session__"):
        val = globals().get(key)
        if val:
            starts.append(Path(val).resolve().parent)
    seen = set()
    for start in starts:
        for p in [start, *start.parents]:
            if p in seen:
                continue
            seen.add(p)
            if (p / "data" / "creditcard.csv").exists():
                return p
    raise FileNotFoundError("Could not find data/creditcard.csv")


ROOT = find_project_root()
DATA = ROOT / "data"
PLOTS = ROOT / "plots" / "assignment_6"
PLOTS.mkdir(parents=True, exist_ok=True)


def section(title):
    print("\n" + "=" * 72)
    print(f"  {title}")
    print("=" * 72)


def save_plot(name):
    path = PLOTS / name
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"Saved {path.relative_to(ROOT)}")


def fraud_scores(y_true, y_pred, name):
    """Scores for the fraud class only (label 1).

    Accuracy is printed too, but it is the wrong headline metric here:
    a model that always says "not fraud" is already ~99.8% accurate.
    Precision = of the alarms we raised, how many were real fraud.
    Recall    = of the real frauds, how many we caught.
    F1        = the harmonic mean of those two. It is low if either is low.
    """
    row = {
        "model": name,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
    }
    return row


print("Project root:", ROOT)
'''))

    cells.append(md("""
## Problem 1 — Credit card fraud

The file is the well-known European card-transaction dataset. `Time` is seconds since the first transaction. `V1`–`V28` are already principal components of the original (confidential) features. `Amount` is the transaction value. `Class` is 0 for a normal payment and 1 for fraud.
"""))

    cells.append(code(r'''
section("Part A: EDA")

fraud = pd.read_csv(DATA / "creditcard.csv")

# Nothing should be missing in this file. We check anyway, because a later
# scaler or hypothesis test would silently drop or crash on NaN.
print(f"Rows: {len(fraud):,}    Columns: {fraud.shape[1]}")
print("Columns:", list(fraud.columns))
print(f"Missing values: {int(fraud.isna().sum().sum())}")

class_counts = fraud["Class"].value_counts().sort_index()
n_legit = int(class_counts[0])
n_fraud = int(class_counts[1])
fraud_rate = n_fraud / len(fraud)

print(f"\nLegitimate (0): {n_legit:,}")
print(f"Fraud        (1): {n_fraud:,}")
print(f"Fraud rate:        {100 * fraud_rate:.3f}%")
print("\nAmount by class (fraud amounts are not always the huge ones):")
print(fraud.groupby("Class")["Amount"].describe().round(2).to_string())

# Two views of the same fact. The pie makes the imbalance obvious.
# The bar uses a log scale so the 492 frauds are still visible next to 284,315 legitimate rows.
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].pie(
    [n_legit, n_fraud],
    labels=["Legitimate", "Fraud"],
    autopct="%1.2f%%",
    colors=["steelblue", "crimson"],
    startangle=90,
)
axes[0].set_title("Class share")
axes[1].bar(["Legitimate", "Fraud"], [n_legit, n_fraud], color=["steelblue", "crimson"])
axes[1].set_yscale("log")
axes[1].set_ylabel("Count (log scale)")
axes[1].set_title("Class counts")
save_plot("class_distribution.png")

# Amount is heavily skewed. A log x-axis shows whether fraud sits in a different
# dollar range from normal spending. (log1p so a zero-amount row still plots.)
plt.figure(figsize=(8, 4.5))
for label, color, name in [(0, "steelblue", "Legitimate"), (1, "crimson", "Fraud")]:
    values = fraud.loc[fraud["Class"] == label, "Amount"]
    plt.hist(np.log1p(values), bins=40, alpha=0.55, color=color, label=name, density=True)
plt.xlabel("log(1 + Amount)")
plt.ylabel("Density")
plt.title("Transaction amount by class")
plt.legend()
save_plot("amount_by_class.png")
'''))

    cells.append(md("""
**Class balance and amount**

![Class distribution](../plots/assignment_6/class_distribution.png)

![Amount by class](../plots/assignment_6/amount_by_class.png)
"""))

    cells.append(code(r'''
section("Part B: Why imbalance is a problem")

# A useless rule — "always predict legitimate" — gets this accuracy.
# That is the trap. Accuracy rewards the majority class.
always_legit_accuracy = n_legit / len(fraud)
print(f"Accuracy of predicting every row as legitimate: {100 * always_legit_accuracy:.3f}%")
print(f"Recall of that rule on fraud: 0%  (it never catches a fraud)")
print()
print("What goes wrong if we train on the raw data:")
print("  1. The loss is dominated by the 284,315 legitimate rows.")
print("  2. The model can lower the loss by predicting 0 almost everywhere.")
print("  3. Accuracy still looks excellent, while fraud recall is near zero.")
print("  4. The decision threshold 0.5 is then much too high for a rare event.")
print()
print("Fix used below: change the TRAINING set so the two classes have equal")
print("counts, then score the model on the ORIGINAL imbalanced test set.")
print("We never resample the test set. The test set must look like real traffic.")

# Same split for every sampling method, so the comparison is fair.
# stratify=y keeps the 0.17% fraud rate in both sides.
feature_cols = [c for c in fraud.columns if c != "Class"]
X = fraud[feature_cols]
y = fraud["Class"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# V1-V28 are already scaled PCA scores, but Time and Amount are not.
# Logistic regression uses the size of each coefficient, so we put every
# column on a common scale. Fit the scaler on train only.
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

print(f"\nTrain rows: {len(y_train):,}   fraud in train: {int(y_train.sum()):,}")
print(f"Test rows:  {len(y_test):,}   fraud in test:  {int(y_test.sum()):,}")
'''))

    cells.append(code(r'''
section("Part C: Under-sampling, over-sampling, SMOTE")

# All three samplers change ONLY the training matrix.
# random_state=42 makes the random draws repeatable.
samplers = {
    # Throw away legitimate training rows until counts match the fraud count.
    # Fast, but most of the legitimate patterns are discarded.
    "Random under-sampling": RandomUnderSampler(random_state=42),
    # Copy fraud rows until they match the legitimate count.
    # Nothing new is learned; the same frauds are just repeated.
    "Random over-sampling": RandomOverSampler(random_state=42),
    # Invent new fraud rows on the line between a fraud and one of its
    # nearest fraud neighbours. Minority count is brought up to the majority count.
    "SMOTE": SMOTE(random_state=42),
}

# Baseline: train on the imbalanced data, no resampling.
# This is the "do nothing" model the sampling methods have to beat.
models = {
    "No resampling": (X_train_s, y_train.to_numpy()),
}
for name, sampler in samplers.items():
    X_res, y_res = sampler.fit_resample(X_train_s, y_train)
    models[name] = (X_res, y_res)
    print(f"{name:<24} train rows {len(y_res):>8,}   fraud {int((y_res == 1).sum()):>8,}")

print(f"\n{'Model':<24} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10}")
print("-" * 68)
score_rows = []
for name, (X_res, y_res) in models.items():
    # Same classifier everywhere. The only thing that changes is the training mix.
    # max_iter is high because the over-sampled sets are large.
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_res, y_res)
    pred = clf.predict(X_test_s)
    row = fraud_scores(y_test, pred, name)
    score_rows.append(row)
    print(
        f"{name:<24} {100 * row['accuracy']:>9.2f}% {row['precision']:>10.3f} "
        f"{row['recall']:>10.3f} {row['f1']:>10.3f}"
    )

scores = pd.DataFrame(score_rows).set_index("model")
# "Best" is decided by fraud F1, not accuracy. Accuracy stays high for all of them.
best_name = scores["f1"].idxmax()
print(f"\nHighest fraud F1: {best_name}  (F1 = {scores.loc[best_name, 'f1']:.3f})")

plot_df = scores.reset_index().melt(
    id_vars="model", value_vars=["precision", "recall", "f1"],
    var_name="metric", value_name="score",
)
plt.figure(figsize=(9, 4.8))
sns.barplot(data=plot_df, x="model", y="score", hue="metric")
plt.ylim(0, 1)
plt.ylabel("Score on the fraud class")
plt.xlabel("")
plt.xticks(rotation=15, ha="right")
plt.title("Fraud precision, recall, and F1")
save_plot("sampling_comparison.png")
'''))

    cells.append(md("""
**Sampling comparison** (test set is still the real, imbalanced mix)

![Sampling comparison](../plots/assignment_6/sampling_comparison.png)
"""))

    cells.append(code(r'''
section("Part D: Which method, which metric, hypothesis test")

print("1. Which sampling method worked best?")
print(f"   {best_name}, by fraud F1 on the untouched test set.")
print("   Under-sampling raises recall because the model finally sees fraud")
print("   as half the training data, but it throws away legitimate examples,")
print("   so it also raises more false alarms (precision drops).")
print("   Copying fraud rows (random over-sampling) repeats the same points.")
print("   SMOTE fills in between real frauds, so the fraud region is a cloud")
print("   rather than a pile of duplicates. That is why it is the usual choice")
print("   when the minority class is not tiny enough to make the neighbours meaningless.")
print()
print("2. Which metrics matter for fraud?")
print("   Recall first: a missed fraud (false negative) costs the bank real money.")
print("   Precision next: every false alarm is a payment stopped for review.")
print("   F1 is the single number that punishes a model that only does one of those.")
print("   Accuracy is the wrong headline. 99.8% is achievable by catching nothing.")
print()

# Hypothesis test as a feature check, fit on TRAIN only so the test set stays clean.
# Mann-Whitney U asks: does this feature tend to be larger for fraud than for
# legitimate payments? It does not assume a normal distribution. Amount is skewed,
# so a t-test on the raw dollars would be the wrong default.
# With ~200,000 training rows, a tiny shift is "significant". The p-value will be
# ~0 for almost every V-column. The useful number is the effect size
# (rank-biserial correlation): how strongly the feature separates the two classes.
legit_mask = y_train.to_numpy() == 0
fraud_mask = y_train.to_numpy() == 1
records = []
for j, col in enumerate(feature_cols):
    a = X_train_s[legit_mask, j]
    b = X_train_s[fraud_mask, j]
    # alternative='two-sided': we do not assume fraud is always larger.
    u_stat, p_value = stats.mannwhitneyu(b, a, alternative="two-sided")
    # Rank-biserial r is in [-1, 1]. 0 means the two classes are mixed together.
    r_rb = (2 * u_stat) / (a.size * b.size) - 1
    records.append({"feature": col, "p_value": p_value, "effect_r": r_rb, "abs_effect": abs(r_rb)})

tests = pd.DataFrame(records).sort_values("abs_effect", ascending=False)
print("3. Hypothesis testing for feature selection (train set, Mann-Whitney U)")
print("   Top 8 features by |effect size|, not by p-value:")
print(f"   {'feature':<10} {'p-value':>12} {'effect r':>10}")
print("   " + "-" * 34)
for _, row in tests.head(8).iterrows():
    print(f"   {row['feature']:<10} {row['p_value']:>12.2e} {row['effect_r']:>10.3f}")
n_sig = int((tests["p_value"] < 0.05).sum())
print(f"\n   Features with p < 0.05: {n_sig} of {len(tests)}")
print("   How this supports feature selection:")
print("   - Keep features whose class distributions actually differ (large |effect r|).")
print("   - Do not rank features by p-value alone. Here almost every p-value is tiny")
print("     because the sample is huge, even when the shift is too small to help a model.")
print("   - V14, V12, V17 and similar columns (large |r|) are the ones a fraud model")
print("     should be allowed to use. A feature with r near 0 can be dropped.")

top = tests.head(10).iloc[::-1]
plt.figure(figsize=(8, 5))
colors = ["crimson" if v > 0 else "steelblue" for v in top["effect_r"]]
plt.barh(top["feature"], top["effect_r"], color=colors)
plt.axvline(0, color="gray", lw=0.8)
plt.xlabel("Rank-biserial effect (fraud vs legitimate)")
plt.title("Features that separate fraud (train set)")
save_plot("hypothesis_effects.png")
'''))

    cells.append(md("""
**Which features actually differ between fraud and legitimate payments**

![Hypothesis-test effect sizes](../plots/assignment_6/hypothesis_effects.png)
"""))

    cells.append(md("""
## Problem 2 — SMS spam vs ham

Each row is one text message labelled `ham` (normal) or `spam`. A Naive Bayes classifier treats the words as evidence and multiplies their probabilities. Two variants:

- **Bernoulli NB** cares only whether a word appears at least once (binary features).
- **Multinomial NB** cares how many times a word appears (count features).
"""))

    cells.append(code(r'''
section("Problem 2: SMS spam — Bernoulli NB vs Multinomial NB")

sms = pd.read_csv(DATA / "sms_spam.tsv", sep="\t", header=None, names=["label", "text"])
print(f"Messages: {len(sms):,}")
print(sms["label"].value_counts().to_string())
print("\nRaw example:")
print(" ", sms.loc[0, "text"][:140])

# Preprocessing, in the order the question asks for.
# 1. lowercase, so "Free" and "free" are the same word.
# 2. strip punctuation. "free!" and "free" would otherwise be different tokens.
# 3. drop English stop words (the, a, to, ...). They appear in both classes
#    and mostly add noise. sklearn's built-in list is used so we do not need NLTK.
punct_table = str.maketrans("", "", string.punctuation)

def clean_message(text):
    lowered = text.lower().translate(punct_table)
    tokens = [word for word in lowered.split() if word not in ENGLISH_STOP_WORDS and word.isalpha()]
    return " ".join(tokens)

sms["clean"] = sms["text"].map(clean_message)
print("\nCleaned example:")
print(" ", sms.loc[0, "clean"][:140])

# 1 = spam, so precision/recall below are "of the spam class".
y_sms = (sms["label"] == "spam").astype(int)
X_txt_train, X_txt_test, y_txt_train, y_txt_test = train_test_split(
    sms["clean"], y_sms, test_size=0.2, random_state=42, stratify=y_sms
)

# CountVectorizer builds a vocabulary from the TRAINING messages only,
# then counts how often each word appears. binary=True turns every count
# into 0/1, which is exactly the input Bernoulli NB is designed for.
# The default (binary=False) keeps the counts, which is what Multinomial NB expects.
binary_vec = CountVectorizer(binary=True)
count_vec = CountVectorizer(binary=False)
X_bin_train = binary_vec.fit_transform(X_txt_train)
X_bin_test = binary_vec.transform(X_txt_test)
X_cnt_train = count_vec.fit_transform(X_txt_train)
X_cnt_test = count_vec.transform(X_txt_test)
print(f"\nVocabulary size: {len(count_vec.vocabulary_):,} words")
print(f"Train messages: {X_cnt_train.shape[0]:,}    Test messages: {X_cnt_test.shape[0]:,}")

# alpha=1 is Laplace smoothing: pretend we have seen every word once.
# Without it, a word that never appeared in spam would give spam probability 0
# for the whole message, because Naive Bayes multiplies word probabilities.
bern = BernoulliNB(alpha=1.0)
multi = MultinomialNB(alpha=1.0)
bern.fit(X_bin_train, y_txt_train)
multi.fit(X_cnt_train, y_txt_train)

comparisons = []
for name, model, X_te in [
    ("Bernoulli NB (word present/absent)", bern, X_bin_test),
    ("Multinomial NB (word counts)", multi, X_cnt_test),
]:
    pred = model.predict(X_te)
    comparisons.append({
        "model": name,
        "accuracy": accuracy_score(y_txt_test, pred),
        "precision": precision_score(y_txt_test, pred, zero_division=0),
        "recall": recall_score(y_txt_test, pred, zero_division=0),
        "f1": f1_score(y_txt_test, pred, zero_division=0),
    })

comp = pd.DataFrame(comparisons)
print(f"\n{'Model':<40} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10}")
print("-" * 84)
for _, row in comp.iterrows():
    print(
        f"{row['model']:<40} {100 * row['accuracy']:>9.2f}% {row['precision']:>10.3f} "
        f"{row['recall']:>10.3f} {row['f1']:>10.3f}"
    )

winner = comp.loc[comp["f1"].idxmax(), "model"]
print(f"\nBetter spam F1: {winner}")
print()
print("Why the two models want different features:")
print("  Bernoulli NB models each word as a yes/no event, P(word appears | class).")
print("  Repeating 'free free free' is the same evidence as writing 'free' once.")
print("  That matches a binary bag-of-words, and short SMS where presence matters")
print("  more than repetition.")
print("  Multinomial NB models the count of each word, as if the message were a")
print("  bag of tokens drawn with replacement. A word used five times is five")
print("  pieces of evidence. That matches CountVectorizer's raw counts")
print("  (or TF-IDF, which is a weighted count).")
print("  On SMS the counts are usually 0 or 1 anyway, so the two models often")
print("  land close. Multinomial still has the edge when a spam word is repeated.")
'''))

    path = ROOT / "Assignment 6" / "Assignment_6_Solutions.ipynb"
    nbformat.write(notebook(cells), path)
    print("wrote", path)


def write_a7():
    cells = []
    cells.append(md("""
# Assignment 7 — Abalone classification: logistic regression, PCA, SVM

**SVNIT — Department of Artificial Intelligence**

**Question sheet:** `Assignment-7.pdf`

**Dataset:** `../data/abalone.data` (UCI Abalone, 4,177 animals)

`Rings` is a count, not a category. The lab asks for classification, so rings are turned into three age groups before any model is trained. That rule is fixed in the code and explained where the target is built.

The same 80/20 split (`random_state=42`) is used for logistic regression and SVM, with and without PCA, so the comparison is fair. The scaler and the PCA are fit on the training set only.

Plots go to `../plots/assignment_7/`.
"""))

    cells.append(code(r'''
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC

warnings.filterwarnings("ignore")
pd.set_option("display.float_format", lambda x: f"{x:,.4f}")
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

# UCI file has no header row. These names are the official column order.
COLUMNS = [
    "Sex",             # M, F, or I (infant)
    "Length",          # longest shell measurement (mm, already scaled in the file)
    "Diameter",
    "Height",
    "Whole_weight",    # whole animal
    "Shucked_weight",  # meat only
    "Viscera_weight",  # gut weight
    "Shell_weight",
    "Rings",           # +1.5 gives a rough age in years. This becomes the target.
]
NUM_COLS = [c for c in COLUMNS if c not in ("Sex", "Rings")]


def find_project_root():
    starts = [Path.cwd().resolve()]
    for key in ("__vsc_ipynb_file__", "__session__"):
        val = globals().get(key)
        if val:
            starts.append(Path(val).resolve().parent)
    seen = set()
    for start in starts:
        for p in [start, *start.parents]:
            if p in seen:
                continue
            seen.add(p)
            if (p / "data" / "abalone.data").exists():
                return p
    raise FileNotFoundError("Could not find data/abalone.data")


ROOT = find_project_root()
DATA = ROOT / "data"
PLOTS = ROOT / "plots" / "assignment_7"
PLOTS.mkdir(parents=True, exist_ok=True)


def section(title):
    print("\n" + "=" * 72)
    print(f"  {title}")
    print("=" * 72)


def save_plot(name):
    path = PLOTS / name
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"Saved {path.relative_to(ROOT)}")


def age_group(rings):
    """Turn the ring count into a class.

    Cuts sit on the quartiles of this file (25th ≈ 8, 50th ≈ 9, 75th ≈ 11),
    which also makes the three classes similar in size:
      young  : 8 or fewer rings
      medium : 9 or 10 rings
      old    : 11 or more rings
    Rings itself is NOT used as a feature. Otherwise the model would be
    predicting a label that was copied from one of its inputs.
    """
    if rings <= 8:
        return "young"
    if rings <= 10:
        return "medium"
    return "old"


def evaluate(name, model, X_test, y_test, labels):
    """Accuracy, confusion matrix, and the full per-class report."""
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred, labels=labels)
    print(f"\n{name}")
    print(f"Test accuracy: {acc:.4f} ({100 * acc:.2f}%)")
    print("Confusion matrix (rows = true class, columns = predicted class)")
    print("Labels order:", labels)
    print(pd.DataFrame(cm, index=labels, columns=labels).to_string())
    print(classification_report(y_test, pred, labels=labels, digits=3))
    return acc, pred


print("Project root:", ROOT)
'''))

    cells.append(md("## Part A — Inspect the table and make a class label"))

    cells.append(code(r'''
section("A1–A3: Load, EDA, encode the target")

abalone = pd.read_csv(DATA / "abalone.data", header=None, names=COLUMNS)
print(f"Rows: {len(abalone):,}    Columns: {abalone.shape[1]}")
print("Dtypes:")
print(abalone.dtypes.to_string())
print("\nMissing values:", int(abalone.isna().sum().sum()))
print("\nNumeric summary:")
print(abalone[NUM_COLS + ["Rings"]].describe().round(3).to_string())
print("\nSex counts (I = infant, not a third adult sex):")
print(abalone["Sex"].value_counts().to_string())

abalone["AgeGroup"] = abalone["Rings"].map(age_group)
# Fixed order so confusion matrices always read young / medium / old.
CLASS_ORDER = ["young", "medium", "old"]
print("\nAge groups created from Rings:")
print(abalone["AgeGroup"].value_counts().reindex(CLASS_ORDER).to_string())

# Distributions of the measurements the model will actually see.
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
for ax, col in zip(axes.ravel(), NUM_COLS):
    ax.hist(abalone[col], bins=30, color="steelblue", edgecolor="white")
    ax.set_title(col, fontsize=9)
fig.suptitle("Measurement distributions")
save_plot("eda_histograms.png")

# Length, diameter and the four weights move together. PCA will collapse
# that shared "overall size" direction into the first component.
plt.figure(figsize=(8, 6))
sns.heatmap(abalone[NUM_COLS].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation of the physical measurements")
save_plot("eda_correlation.png")

plt.figure(figsize=(8, 4.5))
sns.boxplot(data=abalone, x="AgeGroup", y="Shell_weight", order=CLASS_ORDER, color="steelblue")
plt.title("Shell weight rises with the age group")
save_plot("eda_shell_by_age.png")
'''))

    cells.append(md("""
**EDA plots**

![Histograms](../plots/assignment_7/eda_histograms.png)

![Correlation](../plots/assignment_7/eda_correlation.png)

![Shell weight by age](../plots/assignment_7/eda_shell_by_age.png)
"""))

    cells.append(code(r'''
section("A4–A7: Split, scale, logistic regression")

# Features: sex + the 7 physical measurements. Rings is excluded on purpose.
X = abalone[["Sex"] + NUM_COLS]
y = abalone["AgeGroup"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {len(X_train):,}    Test: {len(X_test):,}")

# Sex is text. One-hot makes two 0/1 columns (drop='first' removes one of the
# three, because M+F+I would always equal 1 and PCA would see a useless direction).
# Unknown categories are not expected; the file only contains M, F, I.
sex_encoder = OneHotEncoder(drop="first", sparse_output=False)
sex_train = sex_encoder.fit_transform(X_train[["Sex"]])
sex_test = sex_encoder.transform(X_test[["Sex"]])
sex_names = list(sex_encoder.get_feature_names_out(["Sex"]))

# Glue the numeric measurements next to the sex dummies, THEN standardize.
# Standardization (zero mean, unit variance) is required before PCA and before
# logistic regression, because both treat a large column as a large effect.
# Fit on train, transform test. Test rows must not change the means.
X_train_raw = np.hstack([X_train[NUM_COLS].to_numpy(), sex_train])
X_test_raw = np.hstack([X_test[NUM_COLS].to_numpy(), sex_test])
feature_names = NUM_COLS + sex_names

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train_raw)
X_test_s = scaler.transform(X_test_raw)
print("Scaled feature matrix:", X_train_s.shape, "(rows, features)")
print("Feature order:", feature_names)

# Multinomial logistic regression: one linear score per class, then softmax
# turns the scores into probabilities that add up to 1.
# sklearn 1.8+ does this automatically for 3 classes (the old multi_class
# argument has been removed).
logit = LogisticRegression(max_iter=1000, random_state=42)
logit.fit(X_train_s, y_train)
acc_logit, pred_logit = evaluate(
    "Logistic regression on the 9 standardized features",
    logit, X_test_s, y_test, CLASS_ORDER,
)

plt.figure(figsize=(5.5, 4.5))
cm = confusion_matrix(y_test, pred_logit, labels=CLASS_ORDER)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=CLASS_ORDER, yticklabels=CLASS_ORDER)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Logistic regression — test confusion matrix")
save_plot("logit_confusion.png")
'''))

    cells.append(md("""
**Logistic regression confusion matrix**

![Logistic regression confusion matrix](../plots/assignment_7/logit_confusion.png)
"""))

    cells.append(code(r'''
section("A8–A12: PCA, then logistic regression on the components")

# PCA rotates the standardized features into new axes (components) that are
# uncorrelated. The first axis is the direction of greatest variance.
# explained_variance_ratio_[i] is the fraction of total variance on axis i.
pca_full = PCA(random_state=42)
pca_full.fit(X_train_s)
ratio = pca_full.explained_variance_ratio_
cumulative = np.cumsum(ratio)

print("explained_variance_ratio_:")
print(np.array2string(ratio, precision=4))
print(f"\n{'PC':<6} {'Variance share':>16} {'Cumulative':>12}")
print("-" * 36)
for i, (share, cum) in enumerate(zip(ratio, cumulative), start=1):
    print(f"PC{i:<4} {100 * share:>15.2f}% {100 * cum:>11.2f}%")

# "Selected" components = the smallest set that still keeps 95% of the variance.
# Fewer axes means a simpler model. The leftover 5% is mostly noise and
# duplicate size information (length and diameter are almost the same fact).
n_keep = int(np.searchsorted(cumulative, 0.95) + 1)
print(f"\nComponents kept for 95% variance: {n_keep} of {len(ratio)}")

pca = PCA(n_components=n_keep, random_state=42)
X_train_pca = pca.fit_transform(X_train_s)
X_test_pca = pca.transform(X_test_s)

logit_pca = LogisticRegression(max_iter=1000, random_state=42)
logit_pca.fit(X_train_pca, y_train)
acc_logit_pca, pred_logit_pca = evaluate(
    f"Logistic regression on the first {n_keep} principal components",
    logit_pca, X_test_pca, y_test, CLASS_ORDER,
)

# coef_ has shape (n_classes, n_components).
# Entry [class, k] is the weight of PCk in that class's log-odds.
# A large positive weight means "this component pushes the prediction toward this class".
coef = pd.DataFrame(
    logit_pca.coef_,
    index=logit_pca.classes_,
    columns=[f"PC{i}" for i in range(1, n_keep + 1)],
)
coef = coef.reindex(CLASS_ORDER)
print("\nLogistic coefficients on the principal components:")
print(coef.round(3).to_string())

plt.figure(figsize=(8, 3.2))
sns.heatmap(coef, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Logistic regression weights on each principal component")
plt.ylabel("Class")
save_plot("pca_coefficient_heatmap.png")

plt.figure(figsize=(5.5, 4.5))
cm = confusion_matrix(y_test, pred_logit_pca, labels=CLASS_ORDER)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=CLASS_ORDER, yticklabels=CLASS_ORDER)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("PCA + logistic regression — test confusion matrix")
save_plot("logit_pca_confusion.png")
'''))

    cells.append(md("""
**PCA logistic regression**

![Coefficient heatmap](../plots/assignment_7/pca_coefficient_heatmap.png)

![PCA logistic confusion matrix](../plots/assignment_7/logit_pca_confusion.png)
"""))

    cells.append(md("""
## Part B — Support vector machine

An SVM looks for the boundary with the widest margin between classes. The RBF kernel lets that boundary curve, which a plain logistic regression (a flat boundary in feature space) cannot do. The same split, the same scaler, and the same principal components as Part A are reused.
"""))

    cells.append(code(r'''
section("Part B: SVM, then the comparison")

# Documented settings:
#   kernel='rbf'  — compare each animal with others using a Gaussian similarity.
#   C=1.0         — default penalty on points that fall on the wrong side.
#                   Larger C tries harder to classify every training point.
#   gamma='scale' — kernel width = 1 / (n_features * variance). sklearn's default.
svm = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42)
svm.fit(X_train_s, y_train)
acc_svm, pred_svm = evaluate(
    "SVM (RBF, C=1, gamma='scale') on the 9 standardized features",
    svm, X_test_s, y_test, CLASS_ORDER,
)

svm_pca = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42)
svm_pca.fit(X_train_pca, y_train)
acc_svm_pca, pred_svm_pca = evaluate(
    f"SVM (same kernel) on the first {n_keep} principal components",
    svm_pca, X_test_pca, y_test, CLASS_ORDER,
)

comparison = pd.DataFrame([
    ("Logistic regression", "standardized features", acc_logit),
    ("Logistic regression", f"first {n_keep} PCs", acc_logit_pca),
    ("SVM (RBF)", "standardized features", acc_svm),
    ("SVM (RBF)", f"first {n_keep} PCs", acc_svm_pca),
], columns=["Model", "Features", "Test accuracy"])

print("\nSame split, four models")
print(f"{'Model':<24} {'Features':<28} {'Test accuracy':>14}")
print("-" * 68)
for _, row in comparison.iterrows():
    print(f"{row['Model']:<24} {row['Features']:<28} {100 * row['Test accuracy']:>13.2f}%")

best = comparison.loc[comparison["Test accuracy"].idxmax()]
print(
    f"\nBest on this test set: {best['Model']} using {best['Features']} "
    f"({100 * best['Test accuracy']:.2f}%)."
)
print("PCA usually costs a little accuracy, because the dropped components")
print("still held some age signal, and it buys a smaller, uncorrelated input.")
print("The RBF SVM can bend the boundary, so it is the model to beat the")
print("straight logistic boundary when the classes overlap in size.")

plt.figure(figsize=(8, 4.5))
labels = [f"{m}\n{f}" for m, f in zip(comparison["Model"], comparison["Features"])]
plt.bar(labels, 100 * comparison["Test accuracy"], color=["steelblue", "skyblue", "seagreen", "darkseagreen"])
plt.ylabel("Test accuracy (%)")
plt.ylim(0, 100)
plt.title("Same split: logistic regression vs SVM, with and without PCA")
save_plot("model_comparison.png")

plt.figure(figsize=(5.5, 4.5))
cm = confusion_matrix(y_test, pred_svm, labels=CLASS_ORDER)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
            xticklabels=CLASS_ORDER, yticklabels=CLASS_ORDER)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("SVM — test confusion matrix")
save_plot("svm_confusion.png")
'''))

    cells.append(md("""
**SVM and the four-way comparison**

![Model comparison](../plots/assignment_7/model_comparison.png)

![SVM confusion matrix](../plots/assignment_7/svm_confusion.png)
"""))

    path = ROOT / "Assignment 7" / "Assignment_7_Solutions.ipynb"
    nbformat.write(notebook(cells), path)
    print("wrote", path)


if __name__ == "__main__":
    write_a6()
    write_a7()
