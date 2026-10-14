import plotly.express as plotly_express
from .analysis import  *


def create_category_pie_chart(category_wise_expense):

    return plotly_express.pie(
        values=category_wise_expense.values,
        names=category_wise_expense.index,
        title="Expense by Category Using PIE CHART"
    )
def create_category_bar_chart(category_wise_expense):

    return plotly_express.bar(
        x=category_wise_expense.index,
        y=category_wise_expense.values,
        title="Expense by Category Using BAR CHART",
        labels={
        "x": "Category",
        "y": "Total Expense (₹)"
    }
)

def create_monthly_line_chart(monthly_expense):

    month_labels = monthly_expense.index.to_timestamp().strftime("%b %Y")

    return plotly_express.line(
        x=month_labels,
        y=monthly_expense.values,
        title="Monthly Expense Trend",
        labels={
            "x": "Month",
            "y": "Total Expense (₹)"
        },
        markers=True
    )

