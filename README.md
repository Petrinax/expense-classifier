# expense-classifier
# Expense Classifier

A Python package for classifying expenses from bank statements.

## Installation

**Requirements:**
- Python 3.8 or higher
- Recommended: Use a virtual environment (e.g., `python -m venv venv`)

### Install from PyPI (if available)
...TBD

### Install directly from GitHub
```bash
pip install git+https://github.com/petrinax/expense-classifier.git
```

### Development install (editable mode)
Clone the repository and install in editable mode:
```bash
git clone https://github.com/petrinax/expense-classifier.git
cd expense-classifier
pip install -e .
```

---

## Usage

### Command Line Interface

You can run the expense classifier directly from the command line after installation:

```bash
expense-classifier --path <BANK_STATEMENT_FILE> --bank-code <BANK_CODE> --account <ACCOUNT_NAME> [options]
```

#### Required Arguments

- `--path`, `-p`: Path to the bank statement file (CSV or XLSX).
- `--bank-code`, `-b`: Bank code (e.g., `SBI`, `PNB`, `BOB`).
- `--account`, `-a`: Account name (for labeling and output).

#### Optional Arguments

- `--date-col`: Date column name in your file (default: `Date`)
- `--credit-col`: Credit column name (default: `Credit`)
- `--debit-col`: Debit column name (default: `Debit`)
- `--desc-col`: Description column name (default: `Description`)
- `--paytm-lookup`: Perform Paytm lookup for uncategorized records (requires `--paytm-file`)
- `--paytm-file`: Path to Paytm data file (CSV or XLSX)
- `--store-in-db`: Store processed data in the database
- `--store-progress`: Store intermediate results (default: True)

#### Example

```bash
expense-classifier --path my_statement.csv --bank-code SBI --account "Savings Account" --paytm-lookup --paytm-file paytm.xlsx
```

If you omit required arguments, the app will prompt you interactively.

---

### Programmatic Usage

You can also use the pipeline in your own Python scripts:

```python
from expense_classifier.pipeline import Pipeline

pipeline = Pipeline(
    bank_code="SBI",
    file_path="my_statement.csv",
    account_name="Savings Account",
    paytm_lookup=True,
    paytm_file_path="paytm.xlsx"
)
pipeline.ingest()
pipeline.transform()
pipeline.join_paytm()
pipeline.categorize()
pipeline.file_correction()
final_df, final_table, final_path = pipeline.publish_data()
```

---

## Pipeline Steps

The classification pipeline consists of the following steps:

1. **Ingestion**: Loads your bank statement (CSV/XLSX) and standardizes columns.
2. **Transformation**: Extracts transaction details (mode, payee, UPI ID, etc.) and adds derived columns.
3. **Paytm Lookup (Optional)**: Matches uncategorized transactions with Paytm data for better classification.
4. **Classification**: Assigns categories to each transaction using rule-based keyword matching.
5. **File Correction**: Exports uncategorized transactions for manual review and allows you to add new keywords/categories.
6. **Publishing**: Saves the final, categorized data to CSV and/or database.

---

## Categories & Customization

- Categories and their associated keywords are stored in the database and can be extended.
- During file correction, you can add new keywords for future automatic classification.
- The system supports both expense and income categories.

**Default Categories Example:**

- Housing & Utilities: `rent`, `swaroop`
- Shopping: `amazon`, `myntra`, `reliance`, ...
- Groceries: `swiggy.sto`, `zepto`, `blinkit`, ...
- Food & Drinks: `swiggy`, `swiggyupi`, ...
- ...and many more.

You can update or extend these via the file correction step or by editing the database directly.

---

## Advanced Features

- **Paytm Lookup**: Merge Paytm UPI data for richer transaction context.
- **Manual Correction**: Export uncategorized transactions for manual labeling and keyword enrichment.
- **Database Integration**: Store and retrieve categorized data and category mappings using SQLAlchemy.
- **Extensible Pipeline**: Add your own transformation or classification logic by extending the pipeline.

---

## Example Workflow

1. Run the CLI or your script with your bank statement.
2. Review the exported file for uncategorized transactions and add categories/keywords as needed.
3. Rerun the pipeline to benefit from improved classification.
4. Analyze the final categorized CSV or database table.

---

## Supported File Formats

- Bank statements: CSV or Excel (XLSX)
- Paytm data: CSV or Excel (XLSX, sheet: `Passbook Payment History`)

---

## App Structure

```
expense-classifier/
│
├── expense_classifier/           # Main package: all core logic
│   ├── __init__.py
│   ├── ai_classifier.py          # AI-based classification (optional/advanced)
│   ├── bank_utils.py             # Bank-specific regex and helpers
│   ├── classifier.py             # Rule-based classification logic
│   ├── cli.py                    # CLI utilities
│   ├── combine.py                # Data combination utilities
│   ├── common_utils.py           # Common helper functions
│   ├── database.py               # Database handler (SQLAlchemy)
│   ├── db_utils.py               # Category/keyword DB utilities
│   ├── file_correction.py        # File-based manual correction logic
│   ├── ingestor.py               # Data ingestion and cleaning
│   ├── main.py                   # CLI entry point
│   ├── manual_correction.py      # Interactive manual correction
│   ├── models.py                 # SQLAlchemy models
│   ├── paytm_lookup.py           # Paytm data lookup/merge
│   ├── pipeline.py               # Main pipeline orchestration
│   ├── random.csv                # Example/sample data
│   ├── transformer.py            # Data transformation logic
│   ├── visualizer.py             # (Stub) for future visualizations
│
├── reporting/                    # Reporting and report generation
│   ├── __init__.py
│   └── generator.py              # Report generation logic
│
├── datasets/                     # Example, sample, and processed data
│   ├── sample_data.csv
│   ├── ... (other CSV/XLSX files)
│   └── statements/               # Example bank statement files
│       ├── statement_pnb.csv
│       ├── ...
│
├── migrations/                   # Database migration scripts (Alembic)
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       ├── <revision>.py         # Individual migration scripts
│       └── ...
│
├── local_files/                  # Local config (DB URLs, etc.)
│   ├── sql_alchemy_url.txt
│   └── jdbc_url.txt
│
├── main.py                       # (Legacy/utility) script
├── generate_report.py            # Example: run pipeline and generate report
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
├── pyproject.toml                # Build system config
├── MANIFEST.in                   # Packaging manifest
├── README.md                     # Project documentation
├── Categorization_Plan.md        # Category planning notes
├── Visualizer_Options.md         # Visualization planning notes
├── ... (other CSV/data files)
```

- **expense_classifier/**: All main logic, pipeline, and classification code.
- **reporting/**: Report generation utilities.
- **datasets/**: Example and processed data, including sample statements.
- **migrations/**: Database schema migrations (Alembic).
- **local_files/**: Local configuration (not for version control).
- **Other files**: Project-level scripts, documentation, and configuration.

*Virtual environments, cache, and build directories are omitted for clarity.*


