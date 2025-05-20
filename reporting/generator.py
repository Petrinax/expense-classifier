import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class ReportGenerator:
    """
    Generates financial reports and visualizations from processed transaction data
    """
    
    def __init__(self, data, output_path=None):
        """
        Initialize with transaction data
        
        Parameters:
        - data: pandas DataFrame with processed transaction data
        - output_path: directory to save generated reports
        """
        self.data = data
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Set default output path if none provided
        if output_path is None:
            self.output_path = "/Users/piyushupreti/Documents/Finance/FY 2024-25/reports"
        else:
            self.output_path = output_path
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_path, exist_ok=True)
    
    def generate_basic_reports(self):
        """
        Generate basic summary reports (monthly, quarterly, annual)
        """
        reports = {}
        
        # 1. Monthly summary by category
        monthly_category = self.data.pivot_table(
            values='Amount',
            index=['Fiscal_Year', 'Fiscal_Period', 'Fiscal_Month'],
            columns='Category',
            aggfunc='sum'
        ).reset_index()
        
        reports['monthly_category'] = monthly_category
        
        # 2. Quarterly summary by bank
        quarterly_bank = self.data.pivot_table(
            values='Amount',
            index=['Fiscal_Year', 'Quarter'],
            columns='Bank',
            aggfunc='sum'
        ).reset_index()
        
        reports['quarterly_bank'] = quarterly_bank
        
        # 3. Annual summary by group (Income/Expense)
        annual_group = self.data.pivot_table(
            values='Amount',
            index=['Fiscal_Year'],
            columns='Group',
            aggfunc='sum'
        ).reset_index()
        
        # Add net savings (Income - Expense) column
        if 'Income' in annual_group.columns and 'Expense' in annual_group.columns:
            annual_group['Net Savings'] = annual_group['Income'] + annual_group['Expense']
        
        reports['annual_group'] = annual_group
        
        # Save reports
        for name, df in reports.items():
            path = f"{self.output_path}/{name}_summary_{self.timestamp}.csv"
            df.to_csv(path, index=False)
            print(f"{name.title()} summary saved to: {path}")
        
        return reports
    
    def generate_detailed_reports(self):
        """
        Generate more detailed analytical reports
        """
        reports = {}
        
        # 1. Top spending categories
        top_expenses = self.data[self.data['Group'] == 'Expense'].groupby('Category')['Amount'].sum().abs()
        top_expenses = top_expenses.sort_values(ascending=False).reset_index()
        top_expenses.columns = ['Category', 'Total_Expense']
        
        reports['top_expense_categories'] = top_expenses
        
        # 2. Top income sources
        top_income = self.data[self.data['Group'] == 'Income'].groupby('Category')['Amount'].sum()
        top_income = top_income.sort_values(ascending=False).reset_index()
        top_income.columns = ['Category', 'Total_Income']
        
        reports['top_income_categories'] = top_income
        
        # 3. Monthly cash flow
        monthly_flow = self.data.pivot_table(
            values='Amount',
            index=['Fiscal_Year', 'Fiscal_Period', 'Fiscal_Month'],
            columns='Group',
            aggfunc='sum'
        ).reset_index()
        
        if 'Income' in monthly_flow.columns and 'Expense' in monthly_flow.columns:
            monthly_flow['Net'] = monthly_flow['Income'] + monthly_flow['Expense']
        
        reports['monthly_cash_flow'] = monthly_flow
        
        # Save reports
        for name, df in reports.items():
            path = f"{self.output_path}/{name}_{self.timestamp}.csv"
            df.to_csv(path, index=False)
            print(f"{name.title()} report saved to: {path}")
        
        return reports
    
    def generate_visualizations(self):
        """
        Generate financial visualizations and save them
        """
        # Set plot style
        plt.style.use('ggplot')
        
        # 1. Monthly Income vs Expense
        monthly_flow = self.data.pivot_table(
            values='Amount',
            index=['Fiscal_Month'],
            columns='Group',
            aggfunc='sum'
        ).reset_index()
        
        if 'Expense' in monthly_flow.columns:
            monthly_flow['Expense'] = monthly_flow['Expense'].abs()
        
        plt.figure(figsize=(12, 6))
        
        if 'Income' in monthly_flow.columns:
            plt.bar(monthly_flow['Fiscal_Month'], monthly_flow['Income'], color='green', label='Income')
        
        if 'Expense' in monthly_flow.columns:
            plt.bar(monthly_flow['Fiscal_Month'], -monthly_flow['Expense'], color='red', label='Expense')
        
        plt.title('Monthly Income vs Expense')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        income_expense_path = f"{self.output_path}/monthly_income_expense_{self.timestamp}.png"
        plt.savefig(income_expense_path)
        print(f"Monthly income vs expense visualization saved to: {income_expense_path}")
        
        # 2. Expense distribution by category
        expense_by_category = self.data[self.data['Group'] == 'Expense'].groupby('Category')['Amount'].sum().abs()
        expense_by_category = expense_by_category.sort_values(ascending=False)
        
        plt.figure(figsize=(12, 6))
        expense_by_category.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Expense Distribution by Category')
        plt.ylabel('')
        plt.tight_layout()
        
        expense_category_path = f"{self.output_path}/expense_distribution_{self.timestamp}.png"
        plt.savefig(expense_category_path)
        print(f"Expense distribution visualization saved to: {expense_category_path}")
        
        # 3. Bank-wise transaction volume
        bank_volume = self.data.groupby('Bank').size().sort_values(ascending=False)
        
        plt.figure(figsize=(10, 6))
        bank_volume.plot(kind='bar', color='skyblue')
        plt.title('Transaction Volume by Bank')
        plt.xlabel('Bank')
        plt.ylabel('Number of Transactions')
        plt.tight_layout()
        
        bank_volume_path = f"{self.output_path}/bank_transaction_volume_{self.timestamp}.png"
        plt.savefig(bank_volume_path)
        print(f"Bank transaction volume visualization saved to: {bank_volume_path}")
        
        # Close all plots
        plt.close('all')

def generate_comprehensive_report(data, output_path=None):
    """
    Generate a comprehensive financial report from processed transaction data
    
    Parameters:
    - data: pandas DataFrame with processed transaction data
    - output_path: directory to save generated reports
    
    Returns:
    - Dictionary containing generated reports
    """
    report_gen = ReportGenerator(data, output_path)
    
    # Generate all reports
    basic_reports = report_gen.generate_basic_reports()
    detailed_reports = report_gen.generate_detailed_reports()
    report_gen.generate_visualizations()
    
    # Return combined reports dictionary
    return {**basic_reports, **detailed_reports}