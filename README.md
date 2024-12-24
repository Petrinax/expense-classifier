# expense-classifier

## App Structure
```
expense_classifier/
│
├── data_loader/
│   ├── __init__.py
│   ├── file_parser.py  # For parsing CSV/XLSX files
│   ├── cleanup.py      # For cleaning and normalizing data
│   └── database.py     # For database interaction
│
├── classifier/
│   ├── __init__.py
│   ├── rule_based_classifier.py  # Rule-based classification logic
│   ├── manual_correction.py      # Handle manual corrections
│   └── category_rules.py         # Predefined category rules
│
├── report_generator/
│   ├── __init__.py
│   ├── report.py       # For generating reports
│   ├── dashboard.py    # Dashboard-related logic (data aggregation)
│   └── visualizations.py # For generating visualizations like charts
│
├── requirements.txt    # Dependencies
└── main.py             # Entry point for the package

```
