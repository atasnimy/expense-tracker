import streamlit as st
import pandas as pd
from datetime import date
import os

# Constants
CSV_FILE = "expenses.csv"

# ------------------------
# Helper Functions
# ------------------------

def load_expenses():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["amount", "category", "date"])

def save_expense_to_csv(amount, category, date):
    new_entry = pd.DataFrame([{
        "amount": amount,
        "category": category.strip(),
        "date": date
    }])
    new_entry.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)

def add_expense(amount, category, date):
    st.session_state.expenses = st.session_state.expenses.append({
        "amount": amount,
        "category": category.strip(),
        "date": str(date)
    }, ignore_index=True)
    save_expense_to_csv(amount, category, date)

def print_expenses(df):
    for idx, row in df.iterrows():
        st.write(f"{idx+1}. 💰 Amount: ${row['amount']:.2f} | 🏷️ Category: {row['category']} | 📅 Date: {row['date']}")

def total_expenses(df):
    return df['amount'].astype(float).sum()

def filter_expenses_by_category(df, category):
    return df[df['category'].str.lower() == category.lower()]

# ------------------------
# Streamlit UI
# ------------------------

st.title("🧾 Spending Log")

# Initialize state
if 'expenses' not in st.session_state:
    st.session_state.expenses = load_expenses()

# Expense input form
with st.form("expense_form", clear_on_submit=True):
    amount = st.number_input("💵 Amount", min_value=0.01, format="%.2f")
    category = st.text_input("🏷️ Category")
    expense_date = st.date_input("📅 Date", value=date.today())
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if category.strip() == "":
            st.warning("Please enter a valid category.")
        else:
            add_expense(amount, category, expense_date)
            st.success("Expense added!")

# Display all expenses
st.subheader("📋 All Expenses")
print_expenses(st.session_state.expenses)

# Show total expenses
total = total_expenses(st.session_state.expenses)
st.write(f"**Total Spent:** 💸 ${total:.2f}")

# Filter by category
if not st.session_state.expenses.empty:
    unique_categories = sorted(st.session_state.expenses['category'].unique())
    selected_category = st.selectbox("🔍 Filter by Category", options=["-- All --"] + unique_categories)

    if selected_category != "-- All --":
        filtered = filter_expenses_by_category(st.session_state.expenses, selected_category)
        st.subheader(f"📂 Expenses in '{selected_category}'")
        print_expenses(filtered)
        st.write(f"**Total in category:** 💳 ${total_expenses(filtered):.2f}")
