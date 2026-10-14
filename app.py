import streamlit as st
from src.analysis import *
from src.charts import *
from src.ai import *
import pandas as pd

st.title("AI-Powered Expense & Spending Analyzer")

uploaded_file = st.file_uploader(
    "Upload your expense file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:

    expense_data = load_file(uploaded_file)
    original_expense_data = expense_data.copy()
    expense_data = standardize_columns(expense_data)
    required_columns = ["Date", "Category", "Amount"]

    missing_columns = [
        column
        for column in required_columns
        if column not in expense_data.columns
    ]

    if missing_columns:
        st.error(
            f"Missing required columns: {', '.join(missing_columns)}"
        )
        st.stop()

    cleaned_expense_data = clean_data(expense_data)

else:
    expense_data = pd.read_csv("data/expenses.csv")
    original_expense_data = expense_data.copy()
    expense_data = standardize_columns(expense_data)
    cleaned_expense_data = clean_data(expense_data)


total_expense = calculate_total_expense(cleaned_expense_data)
average_expense = calculate_average_expense(cleaned_expense_data)
highest_expense = find_highest_expense(cleaned_expense_data)
category_wise_expense =calculate_category_expense(cleaned_expense_data)
monthly_expense = calculate_monthly_expense(cleaned_expense_data)

st.subheader("Expense Data")
st.dataframe(original_expense_data)

column1, column2, column3 = st.columns(3)

column1.metric("Total Expense", f"₹{total_expense:.2f}")
column2.metric("Average Expense", f"₹{average_expense:.2f}")
column3.metric("Highest Expense", f"₹{highest_expense['Amount']:.2f}")

st.header("Category-wise Expense")
st.dataframe(category_wise_expense)

st.subheader("Monthly Expense")
st.dataframe(monthly_expense)


category_pie_chart = create_category_pie_chart(
    category_wise_expense
)
st.plotly_chart(category_pie_chart)

category_bar_chart = create_category_bar_chart(
    category_wise_expense
)
st.plotly_chart(category_bar_chart)

monthly_line_chart = create_monthly_line_chart(
    monthly_expense
)
st.plotly_chart(monthly_line_chart)



st.header("Ask AI")

question = st.text_input("Ask a question about your expenses")

if question:
    expense_summary = f"""
Total Expense: ₹{total_expense:.2f}
Average Expense: ₹{average_expense:.2f}

Highest Expense:
{highest_expense}

Category-wise Expense:
{category_wise_expense}

Monthly Expense:
{monthly_expense}
"""

    prompt = f"""
You are an expense analysis assistant.

Use the following expense data to answer the user's question.

Expense Data:
{expense_summary}

User Question:
{question}

Answer clearly and briefly.
"""

    answer = ask_groq(prompt)

    st.write(answer)