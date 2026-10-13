"""Plain-language explanation PDFs for Assignment 4 and Assignment 5."""

from pathlib import Path

import matplotlib
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
FONT_DIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
PLOTS4 = ROOT / "plots" / "assignment_4"
PLOTS5 = ROOT / "plots" / "assignment_5"


class Guide(FPDF):
    def __init__(self, header_label):
        super().__init__()
        self.header_label = header_label
        self.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSans.ttf"))
        self.add_font("DejaVu", "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"))
        self.add_font("DejaVu", "I", str(FONT_DIR / "DejaVuSans-Oblique.ttf"))
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, self.header_label, align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def footer(self):
        self.set_y(-14)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")

    def cover(self, title, subtitle, blurb):
        self.add_page()
        self.ln(28)
        self.set_font("DejaVu", "B", 22)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 11, title, align="C")
        self.ln(4)
        self.set_font("DejaVu", "", 13)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 7, subtitle, align="C")
        self.ln(10)
        self.set_font("DejaVu", "", 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6.5, blurb, align="C")
        self.ln(16)
        self.set_font("DejaVu", "", 10)
        self.set_text_color(80, 80, 80)
        self.multi_cell(
            0,
            6,
            "SVNIT  ·  Department of Artificial Intelligence\nMachine Learning  ·  u24ai028",
            align="C",
        )

    def h1(self, text):
        self.ln(3)
        self.set_font("DejaVu", "B", 15)
        self.set_text_color(0, 70, 130)
        self.set_x(self.l_margin)
        self.multi_cell(0, 8, text)
        self.ln(1)

    def h2(self, text):
        self.ln(2)
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin)
        self.multi_cell(0, 7, text)
        self.ln(0.5)

    def p(self, text):
        self.set_font("DejaVu", "", 10.5)
        self.set_text_color(25, 25, 25)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.6, text)
        self.ln(1.2)

    def say(self, text):
        self.set_font("DejaVu", "I", 10.5)
        self.set_text_color(40, 70, 40)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.6, "Say this: " + text)
        self.ln(1.5)

    def bullet(self, text):
        self.set_font("DejaVu", "", 10.5)
        self.set_text_color(25, 25, 25)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.6, "   •  " + text)
        self.ln(0.4)

    def formula(self, text):
        self.set_font("DejaVu", "", 10.5)
        self.set_text_color(20, 20, 20)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, "    " + text)
        self.ln(1)

    def row(self, cols, widths, bold=False):
        self.set_font("DejaVu", "B" if bold else "", 8.5)
        self.set_text_color(20, 20, 20)
        self.set_x(self.l_margin)
        for col, w in zip(cols, widths):
            self.cell(w, 6.5, col, border=1)
        self.ln()

    def figure(self, path, caption, width=165):
        if self.get_y() > 200:
            self.add_page()
        self.image(str(path), w=width)
        self.ln(1)
        self.set_font("DejaVu", "I", 9)
        self.set_text_color(80, 80, 80)
        self.set_x(self.l_margin)
        self.multi_cell(0, 4.8, caption)
        self.ln(2)


def build_assignment_4():
    pdf = Guide("Assignment 4 explained  ·  u24ai028")
    pdf.cover(
        "Assignment 4, explained",
        "California Housing — from split to Random Forest",
        "A plain-language walkthrough of every question,\nwith the numbers from the solution notebook.",
    )

    pdf.add_page()
    pdf.h1("The whole assignment in one page")
    pdf.p(
        "You are given about 20,640 districts from the 1990 California census. "
        "Each row is one district, not one house. The job is to predict median_house_value "
        "from location, age, rooms, population, income, and how close the district is to the ocean."
    )
    pdf.p(
        "The work has three stages. First, split the data so the test set looks like the real world. "
        "Second, clean the columns (fill missing numbers, scale them, turn ocean_proximity into 0/1 columns) "
        "and try three models. Third, tune the best model, score it once on the test set, "
        "and also solve a tiny linear regression by hand with the Normal Equation."
    )
    pdf.h2("Columns")
    for line in [
        "longitude, latitude — where the district is",
        "housing_median_age — typical age of houses there",
        "total_rooms, total_bedrooms, population, households — size of the district",
        "median_income — typical income, in units of $10,000",
        "ocean_proximity — text: <1H OCEAN, INLAND, ISLAND, NEAR BAY, NEAR OCEAN",
        "median_house_value — the number you predict",
    ]:
        pdf.bullet(line)
    pdf.ln(1)
    pdf.p(
        "One warning you will see in the plots: house values are capped at $500,001. "
        "Anything more expensive was recorded as that number. The model cannot learn prices above the cap."
    )

    pdf.h1("Q1. Split by income, not at random")
    pdf.p(
        "A random 80/20 split can, by luck, put too many rich districts in the test set. "
        "Income is the strongest clue about price, so the test set must have the same mix of incomes as the full data."
    )
    pdf.p(
        "median_income is a continuous number, and stratified splitting needs groups. "
        "So you cut it into 5 bins called income_cat:"
    )
    pdf.formula("bins:  0 – 1.5 – 3.0 – 4.5 – 6.0 – infinity     labels: 1, 2, 3, 4, 5")
    pdf.p(
        "StratifiedShuffleSplit(test_size=0.2, random_state=42) then keeps each bin's share almost identical in train and test."
    )
    pdf.row(["income_cat", "Train count", "Test count", "Share"], [40, 40, 40, 40], bold=True)
    for row in [
        ("1  (poorest)", "657", "165", "about 4%"),
        ("2", "5,265", "1,316", "about 32%"),
        ("3", "5,789", "1,447", "about 35%"),
        ("4", "2,911", "728", "about 18%"),
        ("5  (richest)", "1,890", "472", "about 11%"),
    ]:
        pdf.row(row, [40, 40, 40, 40])
    pdf.ln(1.5)
    pdf.p("Train has 16,512 districts. Test has 4,128. After the split, income_cat is dropped. It was only a tool for splitting. The model still sees the original median_income.")
    pdf.say("I stratified on income bins so the test set has the same rich/poor mix as the full data. A plain random split might not.")

    pdf.h1("Q2. One pipeline, two kinds of columns")
    pdf.p(
        "Models need numbers, and they need every row filled in. total_bedrooms is missing for 158 training districts. "
        "ocean_proximity is text. A ColumnTransformer sends each kind of column down its own path."
    )
    pdf.h2("Numeric path (8 columns)")
    pdf.bullet("SimpleImputer(strategy=\"median\") fills blanks with the median. The median is not pulled around by a few huge districts.")
    pdf.bullet("StandardScaler subtracts the mean and divides by the standard deviation, so every column is on a similar scale.")
    pdf.h2("Category path (ocean_proximity)")
    pdf.bullet("OneHotEncoder makes 5 columns, one per category. A district near the bay is [0, 0, 0, 1, 0], not the number 3.")
    pdf.bullet("handle_unknown=\"ignore\" means a brand-new category at test time becomes all zeros instead of crashing. ISLAND is very rare, so this matters.")
    pdf.p("Resulting training array: shape (16512, 13). That is 16,512 rows and 13 columns = 8 scaled numbers + 5 one-hot columns.")
    pdf.p(
        "fit_transform is used on the training set only. The test set gets transform. "
        "The median and the mean/std must be learned from training rows. If you compute them on the test set too, the test set has leaked into the preprocessing."
    )
    pdf.say("13 columns: 8 scaled numeric features plus 5 yes/no ocean categories. I fit the imputer and scaler on train only.")

    pdf.h1("Q3. Three models, scored with 5-fold CV")
    pdf.p(
        "Cross-validation cuts the training set into 5 folds. Each model is trained on 4 folds and scored on the leftover fold, five times. "
        "The reported number is the average RMSE, plus how much that score wobbles (the std)."
    )
    pdf.p("RMSE is the typical prediction error in dollars. Lower is better. sklearn returns the negative of RMSE because it always tries to maximise a score. The notebook flips the sign back.")
    pdf.row(["Model", "CV RMSE"], [110, 60], bold=True)
    for row in [
        ("Linear regression", "$69,218  ±  $690"),
        ("Decision tree", "$70,629  ±  $1,448"),
        ("Random forest (100 trees)", "$49,942  ±  $761"),
    ]:
        pdf.row(row, [110, 60])
    pdf.ln(1.5)
    pdf.bullet("Linear regression draws one flat relationship. Price depends on location and income in curves and jumps, so a straight fit leaves about $69k of error.")
    pdf.bullet("One decision tree can memorise the training districts. On a new fold it is worse than the straight line, and its score jumps around (largest std).")
    pdf.bullet("A random forest averages many trees. Each tree sees a random sample of rows and a random subset of columns. Averaging cancels the wild mistakes. It wins, at about $50k typical error.")
    pdf.say("The forest wins because averaging trees cuts the overfitting that kills a single tree, and the splits capture patterns a straight line misses.")

    pdf.h1("Q4. Grid search on the forest")
    pdf.p(
        "Two knobs are tried. n_estimators is how many trees (50, 100, or 200). "
        "max_features is how many columns a split is allowed to look at (2, 4, 6, or 8). "
        "That is 3 × 4 = 12 combinations. Each one is scored with 5-fold CV, so the search trains 60 forests."
    )
    pdf.p("Best combination: n_estimators = 200, max_features = 8. Best CV RMSE = $49,015.")
    pdf.p(
        "More trees make the average steadier. The gain from 100 to 200 trees is only about $140, so extra trees help a little and then flatten out. "
        "max_features = 2 makes each tree too weak (RMSE around $51–52k). Allowing 8 features at each split was best inside this grid."
    )
    pdf.p(
        "200 and 8 are both at the edge of the grid. The true best setting might be a bit higher. "
        "A follow-up search would try max_features of 8, 10, and 12."
    )
    pdf.say("GridSearchCV tried every pair of tree-count and feature-count, kept the one with the lowest cross-validated RMSE, then refit that forest on all of the training data.")

    pdf.h1("Q5. One honest score on the test set")
    pdf.p("The tuned forest is used once on the 4,128 districts it has never seen. Mean test house value is about $206,258.")
    pdf.row(["Metric", "Value", "In words"], [40, 45, 95], bold=True)
    for row in [
        ("Test RMSE", "$46,564", "typical error, 22.6% of the mean price"),
        ("Test MAE", "$30,806", "average absolute error, 14.9% of the mean"),
        ("Test R²", "0.8336", "83% of the price variation is explained"),
    ]:
        pdf.row(row, [40, 45, 95])
    pdf.ln(1.5)
    pdf.p(
        "RMSE is larger than MAE because squaring punishes the big misses. Those big misses sit near the $500,001 cap, "
        "where the true price was chopped off. Test RMSE ($46.6k) is close to the CV RMSE ($49.0k), so the tuning did not cheat by fitting the test set."
    )
    pdf.say("On new districts the forest is typically about $47k off, and it explains 83% of the variation in price.")

    pdf.h1("Q6. The Normal Equation, with only NumPy")
    pdf.p(
        "Linear regression has a closed-form answer. You do not have to search. "
        "With a column of 1s added for the intercept, the best weights are:"
    )
    pdf.formula("θ  =  (Xᵀ X)⁻¹  Xᵀ y")
    pdf.p(
        "Here X has only two columns from the training set: median_income and housing_median_age, plus the column of 1s. "
        "The same two columns are given to sklearn's LinearRegression. The two answers match to many decimal places. "
        "The tiny percent difference (about 10⁻¹¹ %) is rounding error. Both methods minimise the same squared error."
    )
    pdf.row(["Parameter", "Value", "Meaning"], [55, 40, 85], bold=True)
    for row in [
        ("θ0  intercept", "−10,706.89", "baseline value"),
        ("θ1  median_income", "43,041.08", "per +1 income unit"),
        ("θ2  housing_median_age", "1,776.05", "per extra year of age"),
    ]:
        pdf.row(row, [55, 40, 85])
    pdf.ln(1.5)
    pdf.formula("value  =  −10,706.89  +  43,041.08 × income  +  1,776.05 × age")
    pdf.p(
        "median_income is in units of $10,000. So a $10,000 rise in typical household income goes with about $43,000 more in median house value, if age stays the same."
    )
    pdf.p(
        "The Normal Equation is the right tool when there are few columns. Inverting XᵀX gets slow as the number of columns grows, "
        "and it fails if two columns are copies of each other. Then you use gradient descent instead. That is Assignment 5."
    )
    pdf.say("NumPy and sklearn solve the same least-squares problem, so θ matches. The income slope is about $43k of house value per income unit.")

    pdf.add_page()
    pdf.h1("Q7. Where the expensive districts are")
    pdf.p(
        "Each point is one district. Horizontal position is longitude, vertical is latitude, so the cloud is the shape of California. "
        "Bigger dots mean more people (dot size = population / 100). Colour is median house value. alpha=0.4 lets overlapping dots show through."
    )
    pdf.figure(
        PLOTS4 / "geographic_scatter.png",
        "Coast and bay districts (Bay Area, Los Angeles, San Diego) are the expensive ones. Inland districts are cheaper. Location should matter in the model.",
    )

    pdf.h1("Q8. The shape of house values")
    pdf.p(
        "Mean value is $206,856. Median is $179,700. The mean is higher because a long right tail of expensive districts pulls it up. Skewness is 0.98, so the distribution is right-skewed. "
        "The tall bar at the far right is the $500,001 cap, not a real pile of houses that all cost exactly that."
    )
    pdf.figure(
        PLOTS4 / "median_house_value_hist.png",
        "Most districts sit between about $100k and $250k. The spike at $500,001 is the census cap.",
    )

    pdf.h1("Q9. Predicted vs actual")
    pdf.p(
        "Each point is one test district. The horizontal axis is the real median value. The vertical axis is the forest's prediction. "
        "The red dashed line is perfect prediction: predicted = actual. Points near that line are good. "
        "A vertical strip at $500,001 is the cap: those districts were worth more, but the data says 500001, so the forest predicts below the line."
    )
    pdf.figure(
        PLOTS4 / "pred_vs_actual.png",
        "Tight to the diagonal in the middle. The big misses are the capped expensive districts.",
    )

    pdf.h1("Q10. Which columns the forest uses")
    pdf.p(
        "Feature importance is how much a column reduces error across all the splits in all the trees. "
        "The numbers add up to 1. They say \"this column was useful,\" not \"this column causes higher prices.\""
    )
    pdf.row(["Rank", "Feature", "Share"], [25, 80, 40], bold=True)
    for row in [
        ("1", "median_income", "44.4%"),
        ("2", "ocean_proximity = INLAND", "15.1%"),
        ("3", "longitude", "11.4%"),
        ("4", "latitude", "10.4%"),
        ("5", "housing_median_age", "4.9%"),
    ]:
        pdf.row(row, [25, 80, 40])
    pdf.ln(1.5)
    pdf.p("Income plus location (inland flag, longitude, latitude) is almost the whole model. The top 10 features hold 99% of the importance. That matches the map: coast vs inland, and richer districts.")
    pdf.figure(
        PLOTS4 / "feature_importances.png",
        "median_income alone is 44% of the forest's importance.",
    )
    pdf.say("The forest mostly uses income and location. Inland districts get their own strong signal, which matches the map.")

    pdf.h1("Short answers if you are asked")
    for line in [
        "Why stratify? So the test set has the same income mix as the full data.",
        "Why median impute? It is not dragged by extreme districts.",
        "Why scale? Rooms are in the thousands, income is around 1–15. Linear models care about that.",
        "Why one-hot, not 0,1,2,3? Those numbers would pretend INLAND < NEAR BAY.",
        "Why is the tree worse than linear regression? It memorises and then fails on new folds.",
        "Why does the forest win? Many trees, averaged, keep the useful splits and cancel the noise.",
        "What is RMSE vs MAE? Both are in dollars. RMSE punishes large errors more.",
        "What is R² = 0.83? 83% of the variation in price is explained.",
        "Why do NumPy and sklearn match in Q6? They minimise the same squared error.",
        "What is wrong with this data? It is from 1990, values are capped at $500,001, and each row is a district average.",
    ]:
        pdf.bullet(line)

    out = ROOT / "Assignment 4" / "u24ai028_Assignment_4_Explained.pdf"
    pdf.output(str(out))
    return out


def build_assignment_5():
    pdf = Guide("Assignment 5 explained  ·  u24ai028")
    pdf.cover(
        "Assignment 5, explained",
        "Gradient descent, polynomials, and regularisation",
        "A plain-language walkthrough of every question,\nwith the numbers from the solution notebook.",
    )

    pdf.add_page()
    pdf.h1("The whole assignment in one page")
    pdf.p(
        "Assignment 4 used sklearn to fit models. This assignment asks you to see how a model actually moves toward the answer, "
        "and what happens when the model is too simple or too flexible."
    )
    pdf.bullet("Q1–Q3 use made-up data: y = 4 + 3x + noise. You walk θ toward the best line three ways: batch, stochastic, and mini-batch gradient descent.")
    pdf.bullet("Q4 uses a curve, y = 0.5 x² + x + 2 + noise. A degree-1 line underfits. A degree-300 polynomial overfits. Degree 2 matches the truth.")
    pdf.bullet("Q5–Q6 use real red-wine data. Ridge, Lasso, and Elastic Net predict the quality score. Then logistic regression predicts \"good wine\" (score 7 or more).")
    pdf.bullet("Q7 uses the Iris flowers. Logistic regression draws the boundary between three species from petal length and petal width.")
    pdf.p("Random draws use seed 42, so a re-run gives the same θ.")

    pdf.h1("The one idea behind Q1–Q3")
    pdf.p(
        "A line is y = θ0 + θ1 x. θ0 is the intercept, θ1 is the slope. "
        "The error of a guess is the mean squared error:"
    )
    pdf.formula("MSE  =  average of (prediction − actual)²")
    pdf.p(
        "Gradient descent starts at a random θ and repeatedly steps downhill on that error. "
        "The gradient is the slope of the error. The learning rate η says how big the step is."
    )
    pdf.formula("θ_new  =  θ_old  −  η × gradient")
    pdf.p(
        "The data is X = 2 × random(100, 1) and y = 4 + 3X + noise, so the true line is θ = [4, 3]. "
        "Noise means the best fit on these 100 points is a bit off that. "
        "The Normal Equation on the same points gives θ0 = 4.2151 and θ1 = 2.7701, with MSE = 0.8066. "
        "That is the target the gradient methods are walking toward. The starting θ was random: about [0.01, 1.45]."
    )

    pdf.h1("Q1. Batch gradient descent")
    pdf.p(
        "Every step uses all 100 rows at once. Learning rate is 0.1. There are 1,000 iterations, so 1,000 parameter updates. "
        "The gradient of the MSE is:"
    )
    pdf.formula("gradient  =  (2 / m)  Xᵀ (Xθ − y)")
    pdf.p(
        "The 2 appears because the derivative of (error)² brings down a 2. m is 100. "
        "A column of 1s is glued onto X so θ0 has something to multiply."
    )
    pdf.p(
        "After 1,000 steps, batch GD lands on θ0 = 4.2151 and θ1 = 2.7701. That is the same answer as the Normal Equation, so it has fully converged. "
        "Training MSE ends at 0.8066. The MSE drops below 1.0 at epoch 22. "
        "One epoch here is one pass over the data, which for batch GD is one iteration."
    )
    pdf.figure(
        PLOTS5 / "q1_batch_gd_mse.png",
        "The error falls almost immediately, then the line is flat. Extra iterations after that do not change θ.",
    )
    pdf.say("Batch GD uses every row on every step. With η = 0.1 it reaches the least-squares line, the same θ as the Normal Equation.")

    pdf.h1("Q2. Stochastic gradient descent")
    pdf.p(
        "Stochastic means random. Each step uses one random row, not all 100. "
        "The step size shrinks over time so the path can settle:"
    )
    pdf.formula("η  =  t0 / (t + t1)    with t0 = 5, t1 = 50")
    pdf.p(
        "t starts at 0 and goes up by 1 on every row. Early on, η = 5/50 = 0.1, the same size as batch GD. Later the steps get smaller."
    )
    pdf.p(
        "50 epochs × 100 rows = 5,000 updates. Batch GD only did 1,000. "
        "SGD's final θ is 4.2151 and 2.7535, and the final MSE is 0.8069. Almost the same place as batch GD, with a slightly different slope because the path is noisy. "
        "MSE is already under 1.0 after the first epoch, because that epoch contains 100 updates."
    )
    pdf.figure(
        PLOTS5 / "q2_batch_vs_sgd_mse.png",
        "Blue is batch GD (1,000 updates). Orange dots are SGD, measured after each epoch. Both sit on the same low error. SGD just keeps taking small noisy steps out to 5,000 updates.",
    )
    pdf.say("SGD updates once per row, 5,000 times in total. Batch GD updates once per full pass, 1,000 times. They finish at almost the same θ.")

    pdf.h1("Q3. Mini-batch, and the comparison table")
    pdf.p(
        "Mini-batch is the middle ground. Each step uses 20 rows (batch_size = 20), in random order. "
        "The question does not give a separate learning rate, so the notebook uses the same decaying schedule as SGD, η = 5 / (t + 50). "
        "50 epochs × (100 / 20) = 250 updates."
    )
    pdf.p("Final mini-batch θ is 4.1349 and 2.8384. Final MSE is 0.8085. It crosses MSE < 1.0 at epoch 6.")
    pdf.row(["Method", "θ0", "θ1", "Epochs to MSE<1", "Updates"], [38, 28, 28, 42, 32], bold=True)
    for row in [
        ("Batch GD", "4.2151", "2.7701", "22", "1,000"),
        ("Stochastic GD", "4.2151", "2.7535", "1", "5,000"),
        ("Mini-batch GD", "4.1349", "2.8384", "6", "250"),
    ]:
        pdf.row(row, [38, 28, 28, 42, 32])
    pdf.ln(1.5)
    pdf.p(
        "Read the \"epochs\" column carefully. An epoch is one pass over the 100 rows. "
        "SGD looks fastest in epochs only because each epoch hides 100 updates. "
        "Mini-batch does the fewest updates overall (250) and still lands near the same error. "
        "Batch GD takes the most epochs, but every step is exact, which is why it matches the Normal Equation digit for digit."
    )
    pdf.say("All three land near θ = [4.22, 2.77] and MSE ≈ 0.81. They differ in how many rows they use per step, and therefore in how many steps they take.")

    pdf.h1("Q4. Too simple, just right, too flexible")
    pdf.p(
        "New data: 100 x-values spread from −3 to 3, and y = 0.5 x² + x + 2 + noise. The truth is a parabola. "
        "PolynomialFeatures builds columns x, x², x³, … up to the degree you ask for. LinearRegression then fits a weight on each column."
    )
    pdf.row(["Degree", "Train RMSE", "What you see"], [30, 40, 100], bold=True)
    for row in [
        ("1", "1.74", "a straight line through a curve"),
        ("2", "0.88", "the true shape, error ≈ the noise"),
        ("300", "2.20", "a curve that shoots off at the edges"),
    ]:
        pdf.row(row, [30, 40, 100])
    pdf.ln(1.5)
    pdf.p(
        "Degree 1 cannot bend, so it misses the dip in the middle. That is underfitting: both training and validation error stay high, and they stay close to each other (about 1.74). "
        "Degree 2 is the degree the data was built from, so the leftover error is basically the noise. "
        "Degree 300 has far more knobs than data points. On the learning curve its validation RMSE is about 11,500 while training RMSE is about 2.2. That gap is overfitting. "
        "The right-hand plot uses a log scale because the validation error is thousands of times larger than the training error."
    )
    pdf.figure(
        PLOTS5 / "q4_polynomial_fits.png",
        "Blue line underfits. Green curve follows the points. Red degree-300 curve is flat in the middle and explodes at x = −3 and x = 3.",
    )
    pdf.figure(
        PLOTS5 / "q4_learning_curves.png",
        "Left: degree 1, train and validation error stay together and high. Right: degree 300, validation error (orange) stays far above training error.",
    )
    pdf.say("Degree 1 underfits because a line cannot make a parabola. Degree 300 overfits because it has more coefficients than points, so it fails on new x values.")

    pdf.add_page()
    pdf.h1("Q5. Ridge, Lasso, and Elastic Net on red wine")
    pdf.p(
        "The file is winequality-red.csv, semicolon-separated, 1,599 wines and 11 chemical measurements. "
        "The target is quality, a score. The split is 80/20 with random_state=42: 1,279 train, 320 test. "
        "Every model is a pipeline: StandardScaler, then the regressor. Scaling matters because alpha penalises the size of the coefficients, and that penalty is only fair if the columns share a scale."
    )
    pdf.h2("What the three penalties do")
    pdf.bullet("Ridge adds α × (sum of squared coefficients). Coefficients get small, but they rarely become exactly 0. Every feature stays in the model.")
    pdf.bullet("Lasso adds α × (sum of |coefficients|). Coefficients can become exactly 0, so Lasso deletes features.")
    pdf.bullet("Elastic Net is both penalties at once. sklearn's default mix is l1_ratio = 0.5, half Lasso and half Ridge.")
    pdf.p("α is tried at 0.001, 0.01, 0.1, 1, and 10. Bigger α means a stronger penalty and a simpler model. The table is test RMSE. Lower is better.")
    pdf.row(["Model", "0.001", "0.01", "0.1", "1", "10"], [36, 26, 26, 26, 26, 26], bold=True)
    for row in [
        ("Ridge", "0.6245", "0.6245", "0.6245", "0.6245", "0.6246"),
        ("Lasso", "0.6249", "0.6269", "0.6627", "0.8107", "0.8107"),
        ("Elastic Net", "0.6247", "0.6263", "0.6441", "0.8107", "0.8107"),
    ]:
        pdf.row(row, [36, 26, 26, 26, 26, 26])
    pdf.ln(1.5)
    pdf.p(
        "The best score in the table is Ridge at α = 0.001, RMSE 0.6245. Ridge barely changes as α grows, because shrinking coefficients a bit does not hurt this dataset. "
        "Lasso and Elastic Net get worse once α reaches 1. At α = 1 and α = 10 their RMSE is 0.8107, which is what you get from predicting the average quality for every wine: the penalty has wiped the model out."
    )
    pdf.h2("Which Lasso coefficient hits zero first?")
    pdf.p(
        "On the five required alphas, three features are already 0 at α = 0.01 and still nonzero at α = 0.001: citric acid, residual sugar, and density. "
        "A finer sweep between 0.001 and 0.01 separates them:"
    )
    pdf.bullet("residual sugar reaches 0 first, at about α = 0.0027")
    pdf.bullet("density is next, at about α = 0.0033")
    pdf.bullet("citric acid follows, at about α = 0.0057")
    pdf.p("alcohol, volatile acidity, and sulphates survive the longest. They only hit zero at α = 1. Those are the measurements the model most wants to keep.")
    pdf.figure(
        PLOTS5 / "q5_lasso_coefficients.png",
        "Each line is one feature. As alpha grows, every line is pulled to 0. The lines that touch 0 earliest are the ones Lasso drops first.",
    )
    pdf.say("Ridge is the most stable across alpha. Lasso starts deleting features as alpha grows, and residual sugar is the first coefficient to hit exactly zero.")

    pdf.h1("Q6. Is the wine good? Logistic regression")
    pdf.p(
        "quality is turned into two classes: good if the score is 7 or more, not good otherwise. "
        "There are 217 good wines and 1,382 not-good wines, so \"good\" is only about 14% of the data. "
        "The split is 80/20, stratified, so the test set keeps that 14%."
    )
    pdf.p(
        "Logistic regression does not predict the class directly. It predicts a probability with the sigmoid function, "
        "and the usual cutoff is 0.5. Features are scaled first, same reason as Q5."
    )
    pdf.row(["Metric", "Score", "Plain meaning"], [35, 30, 115], bold=True)
    for row in [
        ("Accuracy", "89.38%", "overall fraction correct"),
        ("Precision", "69.57%", "of wines called good, this fraction really is"),
        ("Recall", "37.21%", "of truly good wines, this fraction was caught"),
        ("F1", "48.48%", "balance of precision and recall"),
    ]:
        pdf.row(row, [35, 30, 115])
    pdf.ln(1.5)
    pdf.p(
        "Accuracy looks strong because always saying \"not good\" would already be about 86% right. "
        "Recall of 37% means the model misses most of the good wines. "
        "That is the number to talk about, not the accuracy."
    )
    pdf.say("Accuracy is 89% partly because good wines are rare. Recall is only 37%, so most good wines are missed.")

    pdf.h1("Q7. Iris: a picture of the decision boundary")
    pdf.p(
        "Only two columns are used: petal length and petal width. There are three species: setosa, versicolor, virginica. "
        "LogisticRegression on 3 classes fits the multinomial (softmax) model, which is what multi_class=\"multinomial\" used to request. "
        "Current sklearn does that by default, and the old argument has been removed."
    )
    pdf.p(
        "The filled colours are the model's prediction at every point in the plane. "
        "The boundary is where two class probabilities are equal. The dots are the 150 training flowers. "
        "Training accuracy is 96.67%. Setosa separates cleanly. Versicolor and virginica share a fuzzy border, which is where the few mistakes are."
    )
    pdf.figure(
        PLOTS5 / "q7_iris_decision_boundary.png",
        "Green is setosa, orange is versicolor, blue is virginica. Two petal measurements are enough to separate them.",
    )
    pdf.say("With only petal length and petal width, multinomial logistic regression separates the three species at 96.7% training accuracy. Setosa is the easy one.")

    pdf.h1("Short answers if you are asked")
    for line in [
        "What is a gradient? The slope of the error. We step in the opposite direction.",
        "What does the learning rate do? It sets the step size. Too big overshoots. Too small takes forever.",
        "Batch vs SGD vs mini-batch? All rows, one row, or a small group of rows, per update.",
        "Why does SGD's learning rate shrink? So the late steps stop bouncing around the minimum.",
        "Why does batch GD match the Normal Equation? Both minimise squared error, and 1,000 steps were enough to arrive.",
        "Underfitting vs overfitting? High error on both train and val, versus low train error and much higher val error.",
        "Why is degree 2 the right one? The data was built from a quadratic. Degree 1 cannot bend. Degree 300 has more weights than points.",
        "Ridge vs Lasso? Ridge shrinks coefficients. Lasso can set them to exactly 0 and drop features.",
        "Why scale before Ridge/Lasso? Alpha penalises coefficient size. Unscaled columns would be penalised unfairly.",
        "Why is wine accuracy misleading? Only 14% of wines are \"good\", so a model can look accurate while missing most of them.",
    ]:
        pdf.bullet(line)

    out = ROOT / "Assignment 5" / "u24ai028_Assignment_5_Explained.pdf"
    pdf.output(str(out))
    return out


if __name__ == "__main__":
    for path in (build_assignment_4(), build_assignment_5()):
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size / 1024:.0f} KB")
