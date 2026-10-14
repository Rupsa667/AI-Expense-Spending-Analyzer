import pandas as pd

# Load CSV or Excel file
def load_file(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        expense_data = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        expense_data = pd.read_excel(uploaded_file)

    elif file_name.endswith(".xls"):
        expense_data = pd.read_excel(uploaded_file)

    else:
        raise ValueError(
            "Only CSV and Excel files are supported."
        )

    return expense_data


# Change different column names into our standard names
def standardize_columns(expense_data):

    column_mapping = {}

    for column in expense_data.columns:

        column_name = column.strip().lower()

        if "date" in column_name:
            column_mapping[column] = "Date"

        elif (
            "category" in column_name
            or "expense type" in column_name
            or column_name == "type"
        ):
            column_mapping[column] = "Category"

        elif (
            "amount" in column_name
            or "cost" in column_name
            or "price" in column_name
            or "spent" in column_name
        ):
            column_mapping[column] = "Amount"

    expense_data = expense_data.rename(
        columns=column_mapping
    )

    return expense_data

def clean_data(expense_data):
    expense_data["Date"] = pd.to_datetime( expense_data["Date"] )
    expense_data["Amount"] = pd.to_numeric(expense_data["Amount"], errors="coerce")
    expense_data = expense_data.dropna(subset=["Date", "Category", "Amount"])
    expense_data = expense_data.drop_duplicates()
    return expense_data


def calculate_total_expense(cleaned_expense_data):
   return cleaned_expense_data["Amount"].sum()


def calculate_average_expense(cleaned_expense_data):
    return cleaned_expense_data["Amount"].mean()


def find_highest_expense(cleaned_expense_data):
    return  cleaned_expense_data.loc[
        cleaned_expense_data["Amount"].idxmax()
    ]

def calculate_category_expense(cleaned_expense_data):
    return(
        cleaned_expense_data
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

def calculate_monthly_expense(cleaned_expense_data):
    return(
        cleaned_expense_data.groupby(cleaned_expense_data['Date'].dt.to_period("M"))['Amount']
        .sum()
    )

if __name__ == "__main__":
    expense_data= pd.read_csv("../data/expenses.csv")
    expense_data = standardize_columns(expense_data)
    cleaned_expense_data = clean_data(expense_data)
    print("Total Expense:", calculate_total_expense(cleaned_expense_data))
    print("Average Expense:", calculate_average_expense(cleaned_expense_data)) 

    print("\nHighest Expense:")
    print(find_highest_expense(
    cleaned_expense_data
    ))

    print("\nCategory-wise Expense:")
    print(calculate_category_expense(
    cleaned_expense_data
     ))

    print("\nMonthly Expense:")
    print(calculate_monthly_expense(
        cleaned_expense_data
    ))





