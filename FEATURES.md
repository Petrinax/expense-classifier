# Features & Usage: Expense Classifier

## Feature Overview

| Category   | Feature                                      | Description                                                      |
|------------|----------------------------------------------|------------------------------------------------------------------|
| Core       | CLI Processing                               | One-command classification of bank statements                    |
| Core       | Programmatic API                             | Use pipeline in Python scripts                                   |
| Core       | Modular ETL Pipeline                         | Ingest, transform, classify, correct, and export                 |
| Core       | Database Integration                         | SQLAlchemy ORM, persistent storage, Alembic migrations           |
| Core       | Manual/File Correction                       | Export uncategorized records for user review and enrichment       |
| Core       | Multi-bank Support                           | Works with multiple banks, custom columns                        |
| Advanced   | Paytm UPI Lookup                             | Enrich uncategorized records with Paytm data                     |
| Advanced   | Progress Storage                             | Save intermediate results for auditability                       |
| Advanced   | Custom Categories/Keywords                   | User-driven enrichment and learning                              |
| Advanced   | Reporting/Export                             | Clean CSVs, DB tables for analysis                               |
| Advanced   | Error Handling                               | Validates input, handles edge cases                              |
| Planned    | AI/ML Classification                         | Plug-in for AI-based categorization                              |
| Planned    | Visualization/Dashboards                     | Hooks for BI tools and dashboards                                |
| Planned    | Automated Testing                            | pytest-based test suite                                          |

---

## CLI Usage Examples

```bash
# Basic usage
expense-classifier --path my_statement.csv --bank-code SBI --account "Savings Account"

# With Paytm lookup and manual correction
expense-classifier --path my_statement.csv --bank-code SBI --account "Savings Account" --paytm-lookup --paytm-file paytm.xlsx

# Store results in database
expense-classifier --path my_statement.csv --bank-code SBI --account "Savings Account" --store-in-db
```

---

## Programmatic Usage Example

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

## Configuration & Customization

- **Bank Codes:** Supports multiple banks via `--bank-code` or `bank_code` param.
- **Column Names:** Override with `--date-col`, `--credit-col`, `--debit-col`, `--desc-col`.
- **Categories/Keywords:** Extend via file/manual correction or DB edits.
- **Paytm Lookup:** Enable with `--paytm-lookup` and `--paytm-file`.
- **Database:** Store results with `--store-in-db`.
- **Progress Storage:** Enable/disable with `--store-progress`.

---

## Extensibility

- **Pipeline Stages:** Add/replace ETL stages by extending the pipeline.
- **Classification Logic:** Plug in AI/ML models or new rule engines.
- **Reporting:** Integrate with BI tools or custom dashboards.
- **Data Sources:** Add new banks, UPI providers, or enrichment sources.

---

## Real-World Use Cases

- **Personal Finance:** Automated expense tracking and budgeting.
- **Business Accounting:** Streamline reconciliation and reporting.
- **Tax Preparation:** Categorize and export data for tax filing.
- **Financial Analytics:** Feed clean data into BI tools for insights.

---

For more, see [README.md](README.md) or [ARCHITECTURE.md](ARCHITECTURE.md). 