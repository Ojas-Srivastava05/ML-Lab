"""Create the commented Assignment 8 notebook."""

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


cells = []
cells.append(md("""
# Assignment 8 — Neural network for handwritten digits (MNIST)

**SVNIT — Department of Artificial Intelligence**

**Question sheet:** `assignment-8.pdf`

**Dataset:** `../data/mnist.npz` (the official MNIST file: 60,000 train images and 10,000 test images, 28×28 grayscale digits 0–9)

TensorFlow and PyTorch are not installed in this lab environment. The network is `sklearn.neural_network.MLPClassifier`, which is a feed-forward artificial neural network. For 10 classes it uses a softmax output and minimises cross-entropy, and `solver="adam"` is the Adam optimiser the question asks for.

Plots are saved to `../plots/assignment_8/`. Comments in the code explain each step.
"""))

cells.append(code(r'''
import warnings
from pathlib import Path

import matplotlib
# Save figures to files instead of embedding large PNGs in the notebook.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings("ignore")
pd.set_option("display.float_format", lambda x: f"{x:,.4f}")
pd.set_option("display.width", 120)


def find_project_root():
    """Find the repo that contains data/mnist.npz, whatever the kernel cwd is."""
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
            if (p / "data" / "mnist.npz").exists():
                return p
    raise FileNotFoundError("Could not find data/mnist.npz")


ROOT = find_project_root()
DATA = ROOT / "data"
PLOTS = ROOT / "plots" / "assignment_8"
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


def scores(y_true, y_pred):
    """Accuracy, plus precision and recall averaged across the 10 digits.

    'macro' gives each digit the same weight, so a model that fails on one
    rare-looking digit is not hidden by the other nine.
    """
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="macro", zero_division=0),
    }


print("Project root:", ROOT)
'''))

cells.append(md("## Load, normalise, and look at the digits"))

cells.append(code(r'''
section("Load and preprocess MNIST")

# The npz already contains the official 60k/10k split. We do not reshuffle it,
# so the test score is comparable with published MNIST numbers.
with np.load(DATA / "mnist.npz") as mnist:
    x_train_img = mnist["x_train"]
    y_train = mnist["y_train"]
    x_test_img = mnist["x_test"]
    y_test = mnist["y_test"]

print(f"Train images: {x_train_img.shape}   labels: {y_train.shape}")
print(f"Test images:  {x_test_img.shape}   labels: {y_test.shape}")
print(f"Pixel range before scaling: {x_train_img.min()} to {x_train_img.max()}")
print("Label counts (train):")
print(pd.Series(y_train).value_counts().sort_index().to_string())

# Pixels are stored as integers 0..255. A neural net trains more stably when
# inputs are small and on a similar scale, so divide by 255 to get 0..1.
# Flatten 28x28 into 784 numbers: the input layer has one unit per pixel.
# A CNN would keep the grid; this assignment asks for an ANN, which wants a vector.
x_train = x_train_img.reshape(len(x_train_img), -1).astype("float32") / 255.0
x_test = x_test_img.reshape(len(x_test_img), -1).astype("float32") / 255.0
print(f"\nEach image is now a vector of length {x_train.shape[1]}")
print(f"Pixel range after scaling: {x_train.min():.1f} to {x_train.max():.1f}")

# One row of example digits, so the task is visible before any model runs.
fig, axes = plt.subplots(2, 10, figsize=(10, 2.6))
for digit in range(10):
    index = int(np.where(y_train == digit)[0][0])
    axes[0, digit].imshow(x_train_img[index], cmap="gray")
    axes[0, digit].set_title(str(digit), fontsize=9)
    axes[0, digit].axis("off")
    axes[1, digit].imshow(x_train_img[index + 1], cmap="gray")
    axes[1, digit].axis("off")
fig.suptitle("Example MNIST digits (two of each)")
save_plot("example_digits.png")
'''))

cells.append(md("""
**Example digits**

![Example MNIST digits](../plots/assignment_8/example_digits.png)
"""))

cells.append(md("""
## The network

The layers are:

1. **Input layer** — 784 units, one per pixel. This layer does not learn; it only holds the image.
2. **Hidden layers** — each unit computes `relu(w · x + b)`. ReLU is `max(0, z)`. It lets the network stack non-linear steps, which a single logistic regression cannot do.
3. **Output layer** — 10 units, one per digit. Softmax turns those 10 scores into probabilities that add up to 1. The predicted digit is the largest probability.

Training minimises **cross-entropy**: it punishes a confident wrong answer more than a hesitant one. **Adam** chooses the step size for each weight from how noisy that weight's gradient has been, instead of using one learning rate for every weight.
"""))

cells.append(code(r'''
section("Train the main network")

# hidden_layer_sizes=(128, 64) means two hidden layers, 128 units then 64.
# The input size (784) and the output size (10) are inferred from X and y.
# activation='relu' is the hidden-unit function. The output is softmax because
# there are more than two classes and the loss is cross-entropy (log-loss).
# solver='adam' is the optimiser named in the question.
# max_iter is the number of passes over the 60,000 training images.
main_net = MLPClassifier(
    hidden_layer_sizes=(128, 64),
    activation="relu",
    solver="adam",
    learning_rate_init=0.001,
    max_iter=20,
    random_state=42,
)
main_net.fit(x_train, y_train)

print("Architecture:")
print("  input 784  ->  hidden 128 (ReLU)  ->  hidden 64 (ReLU)  ->  softmax 10")
print(f"Passes over the training set: {main_net.n_iter_}")
print(f"Final training loss (cross-entropy): {main_net.loss_:.4f}")

y_pred = main_net.predict(x_test)
main_scores = scores(y_test, y_pred)
print(f"\nTest accuracy:  {main_scores['accuracy']:.4f} ({100 * main_scores['accuracy']:.2f}%)")
print(f"Test precision: {main_scores['precision']:.4f}  (macro, each digit weighted equally)")
print(f"Test recall:    {main_scores['recall']:.4f}  (macro)")
print()
print(classification_report(y_test, y_pred, digits=3))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(7, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.xlabel("Predicted digit")
plt.ylabel("True digit")
plt.title("Test confusion matrix — 784-128-64-10")
save_plot("confusion_matrix.png")

# The loss curve shows whether 20 passes were enough. It should fall and then flatten.
plt.figure(figsize=(7, 4))
plt.plot(np.arange(1, len(main_net.loss_curve_) + 1), main_net.loss_curve_, color="steelblue")
plt.xlabel("Pass over the training set")
plt.ylabel("Training cross-entropy")
plt.title("Adam training loss")
save_plot("loss_curve.png")
'''))

cells.append(md("""
**Confusion matrix and training loss**

![Confusion matrix](../plots/assignment_8/confusion_matrix.png)

![Training loss](../plots/assignment_8/loss_curve.png)
"""))

cells.append(code(r'''
section("Hyperparameters and a benchmark")

# Three changes, one at a time, so the effect of each choice is visible.
#   1. A single hidden layer of 64 units: less capacity.
#   2. The main net: 128 then 64, learning rate 0.001.
#   3. The same shape with a 10x larger Adam step (0.01): steps can overshoot.
# Logistic regression is the benchmark without hidden layers: one softmax,
# no ReLU stack. Published MNIST numbers for context are printed after the table.
configs = [
    ("Logistic regression (no hidden layer)", None),
    ("ANN 64, lr 0.001", dict(hidden_layer_sizes=(64,), learning_rate_init=0.001)),
    ("ANN 128-64, lr 0.001", dict(hidden_layer_sizes=(128, 64), learning_rate_init=0.001)),
    ("ANN 128-64, lr 0.01", dict(hidden_layer_sizes=(128, 64), learning_rate_init=0.01)),
]

rows = []
for name, params in configs:
    if params is None:
        model = LogisticRegression(max_iter=200, random_state=42)
        model.fit(x_train, y_train)
    else:
        model = MLPClassifier(
            activation="relu",
            solver="adam",
            max_iter=20,
            random_state=42,
            **params,
        )
        model.fit(x_train, y_train)
    pred = model.predict(x_test)
    row = scores(y_test, pred)
    row["model"] = name
    rows.append(row)
    print(f"{name:<42} accuracy {100 * row['accuracy']:6.2f}%")

table = pd.DataFrame(rows).set_index("model")
print(f"\n{'Model':<42} {'Accuracy':>10} {'Precision':>10} {'Recall':>10}")
print("-" * 76)
for name, row in table.iterrows():
    print(
        f"{name:<42} {100 * row['accuracy']:>9.2f}% {row['precision']:>10.3f} {row['recall']:>10.3f}"
    )

best = table["accuracy"].idxmax()
print(f"\nBest of these four: {best}")
print()
print("How the knobs matter:")
print("  A hidden layer beats plain logistic regression, because a digit is not")
print("  a straight cut in pixel space. Two hidden layers beat one.")
print("  Learning rate 0.01 is a bigger Adam step than 0.001. On this data it")
print("  still learns, but it is less accurate: the steps are too coarse.")
print()
print("Published context (not trained here):")
print("  Linear classifier on MNIST is typically about 92%.")
print("  A fully connected network of this size is typically 97-98%.")
print("  A convolutional net, which uses the 2D grid, is typically above 99%.")
print("  This ANN does not see neighbouring pixels as neighbours, so it should")
print("  land near the fully-connected benchmark, not the convolutional one.")

plot_names = list(table.index)
plt.figure(figsize=(8, 4.5))
plt.barh(plot_names[::-1], 100 * table.loc[plot_names[::-1], "accuracy"], color="steelblue")
plt.xlabel("Test accuracy (%)")
plt.xlim(90, 100)
plt.title("Effect of hidden layers and learning rate")
save_plot("hyperparameter_comparison.png")
'''))

cells.append(md("""
**Hidden layers and learning rate**

![Hyperparameter comparison](../plots/assignment_8/hyperparameter_comparison.png)
"""))

nb = nbf.new_notebook()
nb["metadata"] = {
    "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "pygments_lexer": "ipython3"},
}
nb["cells"] = cells
path = ROOT / "Assignment 8" / "Assignment_8_Solutions.ipynb"
nbformat.write(nb, path)
print("wrote", path)
