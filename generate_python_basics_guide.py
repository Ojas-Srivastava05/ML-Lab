"""Generate Python Basics Reference PDF."""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent / "Python_Basics_Reference.pdf"


class BasicsPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "Python Basics Reference", align="R", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def cover(self):
        self.add_page()
        self.set_font("Helvetica", "B", 26)
        self.ln(45)
        self.cell(0, 12, "Python Basics Reference", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)
        self.set_font("Helvetica", "", 14)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, "Elementary Scripts, Syntax, and Use Cases", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(20)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 7, "Covers: variables, None/null checks, collections,\nconditionals, loops, functions, files,\npandas & numpy essentials for ML labs.", align="C")

    def h1(self, text):
        self.ln(4)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(0, 70, 130)
        self.multi_cell(0, 8, text)
        self.ln(2)

    def h2(self, text):
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def usecase(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 5, f"Use case: {text}")
        self.ln(1)

    def body(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 5.2, text)
        self.ln(1)

    def code(self, text):
        self.set_x(self.l_margin + 2)
        self.set_font("Courier", "", 9)
        self.set_fill_color(245, 245, 245)
        for line in text.split("\n"):
            self.cell(0, 5, "  " + line, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

    def note(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(150, 80, 0)
        self.multi_cell(0, 5, f"Note: {text}")
        self.ln(1)


def build():
    pdf = BasicsPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.cover()

    # ========== 1. BASICS ==========
    pdf.add_page()
    pdf.h1("1. Variables and Data Types")
    pdf.body("Python is dynamically typed. You do not declare types explicitly.")
    pdf.code(
        "name = 'Ojas'          # str\n"
        "age = 20               # int\n"
        "height = 5.9           # float\n"
        "is_student = True      # bool\n"
        "nothing = None         # NoneType (Python's null)"
    )
    pdf.usecase("Store different kinds of values in variables.")

    pdf.h2("Check type")
    pdf.code("type(age)           # <class 'int'>\nisinstance(age, int) # True")
    pdf.usecase("Verify what kind of data you are working with.")

    pdf.h2("Convert types")
    pdf.code(
        "int('42')      # 42\n"
        "float('3.14')  # 3.14\n"
        "str(100)       # '100'\n"
        "bool(0)        # False\n"
        "bool(1)        # True\n"
        "list('abc')    # ['a', 'b', 'c']"
    )
    pdf.usecase("Convert user input or file data to the type you need.")

    # ========== 2. NONE / NULL ==========
    pdf.h1("2. None (Null) Checks")
    pdf.body("Python uses None, not null. Always compare with 'is' or 'is not'.")
    pdf.code(
        "x = None\n\n"
        "if x is None:\n"
        "    print('x is null')\n\n"
        "if x is not None:\n"
        "    print('x has a value')"
    )
    pdf.usecase("Check if a variable has no value yet.")
    pdf.note("Use 'is None', NOT 'x == None'. 'is' checks identity correctly.")

    pdf.h2("Default values for None")
    pdf.code(
        "def greet(name=None):\n"
        "    if name is None:\n"
        "        name = 'Guest'\n"
        "    return f'Hello, {name}'\n\n"
        "value = some_var if some_var is not None else 0"
    )
    pdf.usecase("Provide fallback when input is missing.")

    pdf.h2("Safe access")
    pdf.code(
        "data = {'score': None}\n"
        "score = data.get('score')       # None if missing\n"
        "score = data.get('score', 0)    # 0 if missing\n\n"
        "name = user.get('name') or 'Unknown'"
    )
    pdf.usecase("Avoid KeyError and handle missing dictionary keys.")

    # ========== 3. STRINGS ==========
    pdf.h1("3. Strings")
    pdf.code(
        "s = 'hello'\n"
        "s.upper()           # 'HELLO'\n"
        "s.lower()           # 'hello'\n"
        "s.strip()           # remove spaces\n"
        "s.replace('l', 'L') # 'heLLo'\n"
        "s.split(',')        # split by comma\n"
        "','.join(['a','b']) # 'a,b'\n"
        "'age' in s          # True/False\n"
        "len(s)              # 5"
    )
    pdf.usecase("Clean and format text data.")

    pdf.h2("f-strings (formatted strings)")
    pdf.code(
        "name = 'Ojas'\n"
        "score = 95.5\n"
        "f'Name: {name}, Score: {score:.1f}%'\n"
        "f'Price: ${1000:,.2f}'   # $1,000.00"
    )
    pdf.usecase("Print readable output with variables embedded.")

    # ========== 4. LISTS ==========
    pdf.add_page()
    pdf.h1("4. Lists")
    pdf.code(
        "nums = [1, 2, 3, 4, 5]\n"
        "nums[0]        # first item: 1\n"
        "nums[-1]       # last item: 5\n"
        "nums[1:3]      # slice: [2, 3]\n"
        "nums.append(6) # add to end\n"
        "nums.insert(0, 0)\n"
        "nums.remove(3) # remove value\n"
        "nums.pop()     # remove last\n"
        "len(nums)\n"
        "3 in nums      # membership check"
    )
    pdf.usecase("Store ordered collections that can change.")

    pdf.h2("List comprehension")
    pdf.code(
        "squares = [x**2 for x in range(1, 6)]\n"
        "evens = [x for x in nums if x % 2 == 0]\n"
        "pairs = [a+b for a in 'abc' for b in 'def']"
    )
    pdf.usecase("Create new lists in one line (Assignment 1 Q4).")

    # ========== 5. DICTS & SETS ==========
    pdf.h1("5. Dictionaries and Sets")
    pdf.code(
        "student = {'name': 'Ojas', 'age': 20}\n"
        "student['name']          # get value\n"
        "student.get('grade', 'N/A')\n"
        "student.keys()\n"
        "student.values()\n"
        "student.items()\n"
        "student['grade'] = 9\n"
        "'name' in student        # key exists?\n\n"
        "a = {1, 2, 3}\n"
        "b = {3, 4, 5}\n"
        "a & b    # intersection: {3}\n"
        "a | b    # union: {1,2,3,4,5}\n"
        "a - b    # difference: {1, 2}"
    )
    pdf.usecase("Dicts for key-value data (Netflix views). Sets for unique items and set math (Q1 sports).")

    pdf.h2("Dictionary comprehension")
    pdf.code("{x: x**3 for x in range(1, 101) if x % 3 == 0}")
    pdf.usecase("Build dictionaries quickly (Assignment 1 Q3).")

    # ========== 6. CONDITIONALS ==========
    pdf.h1("6. Conditionals (if / elif / else)")
    pdf.code(
        "if score >= 90:\n"
        "    grade = 'A'\n"
        "elif score >= 75:\n"
        "    grade = 'B'\n"
        "else:\n"
        "    grade = 'C'\n\n"
        "# one-liner\n"
        "status = 'pass' if score >= 40 else 'fail'"
    )
    pdf.usecase("Make decisions based on conditions.")

    pdf.h2("Truthy and Falsy values")
    pdf.body("Falsy: None, 0, 0.0, '', [], {}, set(), False\nEverything else is truthy.")
    pdf.code(
        "if my_list:\n"
        "    print('list is not empty')\n\n"
        "if not name:\n"
        "    print('name is empty or None')"
    )
    pdf.usecase("Quick checks without writing 'is not None' every time.")

    # ========== 7. LOOPS ==========
    pdf.h1("7. Loops")
    pdf.code(
        "for i in range(5):       # 0,1,2,3,4\n"
        "    print(i)\n\n"
        "for item in my_list:\n"
        "    print(item)\n\n"
        "for key, val in student.items():\n"
        "    print(key, val)\n\n"
        "count = 0\n"
        "while count < 5:\n"
        "    count += 1\n\n"
        "for i in range(10):\n"
        "    if i == 3:\n"
        "        continue   # skip\n"
        "    if i == 7:\n"
        "        break      # stop loop"
    )
    pdf.usecase("Repeat actions over data.")

    pdf.h2("enumerate and zip")
    pdf.code(
        "for i, val in enumerate(['a', 'b', 'c']):\n"
        "    print(i, val)   # 0 a, 1 b, 2 c\n\n"
        "for a, b in zip([1,2], ['x','y']):\n"
        "    print(a, b)     # 1 x, 2 y"
    )
    pdf.usecase("Loop with index, or combine two lists together.")

    # ========== 8. FUNCTIONS ==========
    pdf.add_page()
    pdf.h1("8. Functions")
    pdf.code(
        "def add(a, b):\n"
        "    return a + b\n\n"
        "def greet(name='Guest'):\n"
        "    return f'Hello, {name}'\n\n"
        "def stats(nums):\n"
        "    return min(nums), max(nums), sum(nums)/len(nums)\n\n"
        "lo, hi, avg = stats([1, 2, 3, 4, 5])"
    )
    pdf.usecase("Reusable blocks of code. Default args handle missing inputs.")

    pdf.h2("Lambda (small one-line functions)")
    pdf.code(
        "square = lambda x: x**2\n"
        "sorted(words, key=lambda x: len(x))\n"
        "df['LotFrontage'].fillna(df.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.median()))"
    )
    pdf.usecase("Quick functions for sorting or pandas group operations.")

    # ========== 9. FILES ==========
    pdf.h1("9. File Handling")
    pdf.code(
        "# Read text file\n"
        "with open('file.txt', 'r') as f:\n"
        "    content = f.read()\n\n"
        "# Write text file\n"
        "with open('out.txt', 'w') as f:\n"
        "    f.write('Hello')\n\n"
        "# Read CSV with pandas\n"
        "import pandas as pd\n"
        "df = pd.read_csv('data/train.csv')\n"
        "df.to_csv('output.csv', index=False)"
    )
    pdf.usecase("Load datasets and save results. 'with' auto-closes the file.")

    # ========== 10. ERRORS ==========
    pdf.h1("10. Error Handling")
    pdf.code(
        "try:\n"
        "    value = int(user_input)\n"
        "except ValueError:\n"
        "    print('Not a valid number')\n"
        "except KeyError:\n"
        "    print('Key not found')\n"
        "else:\n"
        "    print('Success:', value)\n"
        "finally:\n"
        "    print('Always runs')"
    )
    pdf.usecase("Handle bad input or missing data without crashing.")

    # ========== 11. PANDAS NULL ==========
    pdf.h1("11. Pandas: Null / Missing Values")
    pdf.body("In pandas, missing values are NaN (Not a Number), not None.")
    pdf.code(
        "import pandas as pd\n"
        "import numpy as np\n\n"
        "df.isnull()          # True where missing\n"
        "df.notnull()         # True where present\n"
        "df.isna()            # same as isnull()\n"
        "df.notna()           # same as notnull()\n\n"
        "df.isnull().sum()    # count missing per column\n"
        "df.isnull().sum().sum()  # total missing\n\n"
        "df['col'].isnull().any()  # any missing in column?\n"
        "df['col'].notna().all()   # all values present?"
    )
    pdf.usecase("Find missing data before modeling (Assignment 1 Part D).")

    pdf.h2("Fill missing values")
    pdf.code(
        "df['num_col'].fillna(df['num_col'].median())\n"
        "df['cat_col'].fillna(df['cat_col'].mode()[0])\n"
        "df['cat_col'].fillna('Missing')\n\n"
        "df.dropna()                    # drop rows with any NaN\n"
        "df.dropna(subset=['SalePrice']) # drop if target missing\n\n"
        "# LotFrontage by neighborhood\n"
        "df['LotFrontage'] = df.groupby('Neighborhood')['LotFrontage'].transform(\n"
        "    lambda x: x.fillna(x.median())\n"
        ")"
    )
    pdf.usecase("Impute missing values (median for numeric, mode for categorical).")

    pdf.h2("Filter rows with/without nulls")
    pdf.code(
        "df[df['SalePrice'].notna()]         # rows where price exists\n"
        "df[df['PoolQC'].isnull()]           # rows where PoolQC is missing\n"
        "df.drop(columns=['Id'])             # remove a column"
    )
    pdf.usecase("Clean dataset by keeping only valid rows.")

    # ========== 12. PANDAS ESSENTIALS ==========
    pdf.add_page()
    pdf.h1("12. Pandas Essentials")
    pdf.code(
        "df.head(10)          # first 10 rows\n"
        "df.tail()            # last 5 rows\n"
        "df.shape             # (rows, cols)\n"
        "df.columns           # column names\n"
        "df.dtypes            # data types\n"
        "df.info()            # summary\n"
        "df.describe()        # numeric stats\n\n"
        "df['SalePrice']      # one column\n"
        "df[['A', 'B']]       # multiple columns\n"
        "df.loc[0]            # row by label\n"
        "df.iloc[0]           # row by index\n"
        "df[df['Age'] > 18]   # filter rows"
    )
    pdf.usecase("Explore and slice tabular data (Assignment 1 Part A).")

    pdf.h2("Useful operations")
    pdf.code(
        "df['SalePrice'].mean()\n"
        "df['SalePrice'].median()\n"
        "df['SalePrice'].std()\n"
        "df['SalePrice'].min()\n"
        "df['SalePrice'].max()\n"
        "df['Neighborhood'].value_counts()\n"
        "df.select_dtypes(include=['number']).columns\n"
        "df.select_dtypes(include=['object']).columns\n"
        "df.corr()            # correlation matrix"
    )
    pdf.usecase("Statistics and EDA for ML assignments.")

    # ========== 13. NUMPY ==========
    pdf.h1("13. NumPy Essentials")
    pdf.code(
        "import numpy as np\n\n"
        "arr = np.array([1, 2, 3, 4, 5])\n"
        "arr.shape\n"
        "arr.mean()\n"
        "arr.std()\n"
        "arr.min(), arr.max()\n\n"
        "np.zeros((3, 3))     # 3x3 zeros\n"
        "np.ones((2, 4))      # 2x4 ones\n"
        "np.arange(0, 10, 2)  # [0,2,4,6,8]\n"
        "np.linspace(0, 1, 5) # 5 evenly spaced\n\n"
        "arr[arr > 3]         # filter\n"
        "np.where(arr > 3)    # indices where True\n"
        "np.isin(arr, [1, 5]) # element in list?\n"
        "np.unique(arr)       # unique values\n"
        "np.sort(arr)         # sorted copy"
    )
    pdf.usecase("Numerical arrays for ML lab NumPy questions (Assignment 1 Q7-Q19).")

    pdf.h2("Common NumPy functions (from your assignments)")
    pdf.code(
        "np.percentile(arr, 50)           # median\n"
        "np.argsort(arr)                  # sort indices\n"
        "np.partition(arr, 4)           # partition at position\n"
        "np.linalg.norm(a - b)            # euclidean distance\n"
        "np.diff(arr, prepend=[0], append=[200])\n"
        "np.abs(np.round(arr))            # round + absolute\n"
        "arr[~np.isnan(arr)]              # remove NaN"
    )
    pdf.usecase("Directly maps to Assignment 1 NumPy exercises.")

    # ========== 14. IMPORTS ==========
    pdf.h1("14. Common Imports for ML Labs")
    pdf.code(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.preprocessing import StandardScaler\n"
        "from sklearn.linear_model import LinearRegression\n"
        "from sklearn.metrics import r2_score, mean_squared_error\n"
        "from sklearn.tree import DecisionTreeClassifier\n"
        "from scipy import stats"
    )
    pdf.usecase("Standard imports used across all 3 assignments.")

    # ========== 15. CHEAT SHEET TABLE ==========
    pdf.add_page()
    pdf.h1("15. Quick Syntax Cheat Sheet")
    rows = [
        ("Check if None", "x is None", "Variable has no value"),
        ("Check if not None", "x is not None", "Variable has a value"),
        ("Check if empty list", "not my_list", "List is empty"),
        ("Check membership", "x in my_list", "x exists in list"),
        ("Safe dict get", "d.get('key', default)", "Avoid KeyError"),
        ("Ternary if", "a if cond else b", "One-line if/else"),
        ("Pandas missing?", "df.isnull()", "Find NaN cells"),
        ("Pandas has value?", "df.notna()", "Find non-missing"),
        ("Count missing", "df.isnull().sum()", "Per column count"),
        ("Fill missing", "df.fillna(value)", "Replace NaN"),
        ("Filter rows", "df[df['col'] > 5]", "Conditional rows"),
        ("Group stats", "df.groupby('col').mean()", "Stats per group"),
        ("Train/test split", "train_test_split(X, y, test_size=0.2)", "ML evaluation"),
        ("Read CSV", "pd.read_csv('file.csv')", "Load dataset"),
        ("Save CSV", "df.to_csv('out.csv', index=False)", "Export results"),
    ]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_x(pdf.l_margin)
    pdf.cell(45, 7, "Task", border=1)
    pdf.cell(55, 7, "Syntax", border=1)
    pdf.cell(80, 7, "Use case", border=1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    for task, syntax, use in rows:
        pdf.set_x(pdf.l_margin)
        pdf.cell(45, 6, task, border=1)
        pdf.cell(55, 6, syntax, border=1)
        pdf.cell(80, 6, use, border=1)
        pdf.ln()

    pdf.ln(4)
    pdf.h2("Common mistakes to avoid")
    pdf.body(
        "1. Using == None instead of is None\n"
        "2. Forgetting to call a function: len vs len()\n"
        "3. Modifying a list while looping over it\n"
        "4. Not handling missing values before sklearn models\n"
        "5. Using df['col'] = ... without copy -> SettingWithCopyWarning\n"
        "6. Comparing strings with == when you need .strip() first\n"
        "7. Dividing by zero -> check denominator first\n"
        "8. Not setting random_state in train_test_split (results change each run)"
    )

    pdf.output(str(OUT))
    print(f"Created: {OUT} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build()
