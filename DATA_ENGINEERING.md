# Data Engineering Deep Dive: Expense Classifier

## ETL Pipeline Overview

The pipeline is designed as a modular, extensible sequence of stages:

1. **Ingestion**: Load and standardize raw bank/Paytm files (CSV/XLSX)
2. **Transformation**: Extract and normalize transaction details
3. **Enrichment**: Paytm lookup and manual/file correction
4. **Classification**: Assign categories using rule-based logic
5. **Publishing**: Export to CSV and/or database

---

## 1. Ingestion

- **File Support:** CSV, XLSX (bank statements, Paytm UPI)
- **Standardization:** Renames columns, parses dates, cleans numeric fields
- **Validation:** Drops empty rows, handles invalid/missing data

```python
from expense_classifier.ingestor import Ingestor

df = Ingestor('my_statement.csv').get_data()
```

---

## 2. Transformation

- **Feature Extraction:** Payment mode, payee, UPI ID, etc.
- **Derived Columns:** Group (Income/Expense), Account, Fiscal Period
- **Normalization:** Lowercases descriptions, standardizes formats

```python
from expense_classifier.transformer import Transformer

df = Transformer(df, bank, account_name).transform()
```

---

## 3. Enrichment

### Paytm Lookup
- Matches uncategorized transactions with Paytm UPI data
- Supports both file and DB sources

```python
from expense_classifier.paytm_lookup import PaytmLookup

lookup = PaytmLookup(df, 'paytm.xlsx')
df = lookup.perform_lookup()
```

### Manual/File Correction
- Exports uncategorized records for user review
- Allows user to add new keywords/categories
- Updates mappings for future automation

---

## 4. Classification

- **Rule-Based Engine:** Keyword-driven, extensible
- **Handles:** Both expense and income categories
- **Extensible:** Plug in AI/ML models for advanced classification

```python
from expense_classifier.classifier import Classifier

df = Classifier().classify(df)
```

---

## 5. Publishing

- **Export:** Clean, categorized data to CSV and/or database
- **Persistence:** All stages can be stored for auditability

---

## Error Handling & Validation

- **Input Validation:** Checks file formats, required columns, and data types
- **Error Logging:** Handles and logs invalid/missing data
- **User Prompts:** Interactive correction for ambiguous cases

---

## Performance Optimizations

- **Vectorized Operations:** Uses pandas for fast, efficient ETL
- **Batch DB Writes:** Efficient storage of large datasets
- **Progress Storage:** Optionally saves intermediate results

---

## Extensibility

- **Add New Banks:** Extend bank_utils and mappings
- **Custom Logic:** Plug in new transformation or classification modules
- **Enrichment:** Add new data sources (e.g., other UPI providers)

---

For more, see [ARCHITECTURE.md](ARCHITECTURE.md) or [README.md](README.md). 