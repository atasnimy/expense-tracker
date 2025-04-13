import streamlit as st
from datetime import date

# ------------------------
# Expense Management Logic
# ------------------------

def add_expense(amount, category, date):
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    st.session_state.expenses.append({
        "amount": amount,
        "category": category.strip(),
        "date": date
    })

def print_expenses(expenses):
    for idx, expense in enumerate(expenses, start=1):
        st.write(f"{idx}. 💰 Amount: ${expense['amount']:.2f} | 🏷️ Category: {expense['category']} | 📅 Date: {expense['date']}")

def total_expenses(expenses):
    return sum(expense['amount'] for expense in expenses)

def filter_expenses_by_category(expenses, category):
    return [expense for expense in expenses if expense['category'].lower() == category.lower()]

# ------------------------
# Streamlit UI
# ------------------------

st.title("🧾 Spending Log")

# Ensure session state is initialized
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

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
if st.session_state.expenses:
    unique_categories = sorted(set(exp["category"] for exp in st.session_state.expenses))
    selected_category = st.selectbox("🔍 Filter by Category", options=["-- All --"] + unique_categories)

    if selected_category != "-- All --":
        filtered = filter_expenses_by_category(st.session_state.expenses, selected_category)
        st.subheader(f"📂 Expenses in '{selected_category}'")
        print_expenses(filtered)
        st.write(f"**Total in category:** 💳 ${total_expenses(filtered):.2f}")
