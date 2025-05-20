
import pandas as pd
from transformers import pipeline
from expense_classifier.db_utils import get_category_keywords


keywords = get_category_keywords()
categories = list(keywords.keys())


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

extended_prompt = (
            f"\n\nRelevant categories to keywords mapping to consider: \n {keywords}"
        )
def generate_transaction_text(row):
    mode = row.get('Mode', '')
    payee = row.get('Payee', '')
    payee_account = row.get('Payee Account', '')
    txn_details = row.get('Transaction Details', '')
    remarks = row.get('Remarks', '')
    tags = row.get('Tags', '')
    comment = row.get('Comment', '')

    transaction_text = (
        f"The transaction was made via {mode} to {payee} "
        f"({payee_account}). Description: '{txn_details}'. "
        f"Remarks: '{remarks}'. Comments: {comment}. Tags include: {tags}."
    )
    return transaction_text


def categorize_with_huggingface(prompt):
    try:
        print(f"\nPrompt: \n\t{prompt}")
        prompt += extended_prompt
        result = classifier(prompt, categories)
        # Get the category with the highest score
        print(f"\nResult: \n\t{result['labels'][0]}\n---------------------")
        return result['labels'][0]
    except Exception as e:
        print(f"Error categorizing prompt: {e}")
        return "Error"


if __name__ == '__main__':
    paytm_df = pd.read_excel(
        "/Users/piyushupreti/Documents/Finance/FY 2025 26/Paytm_UPI_Statement_01_Jan'25_-_18_May'25.xlsx",
        sheet_name='Passbook Payment History')

    bank_df = pd.read_csv(
        "/Users/piyushupreti/Documents/Finance/FY 2025 26/categorized_OpTransactionHistoryUX519-05-2025.csv")

    joined = pd.merge(left=bank_df, right=paytm_df, left_on="Txn ID", right_on="UPI Ref No.", how="left")

    joined['Prompt'] = joined.apply(generate_transaction_text, axis=1)

    joined['AI_Classification'] = joined['Prompt'].apply(categorize_with_huggingface)
    joined.to_csv("/Users/piyushupreti/Documents/Finance/FY 2025 26/AI_classified.csv")

