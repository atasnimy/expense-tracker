import streamlit as st

def add_expense(expenses, amount, category):
    expenses.append({'amount': amount, 'category': category})

def print_expenses(expenses):
    for expense in expenses:
        st.write(f'Amount: ${expense["amount"]}, Category: {expense["category"]}')

def total_expenses(expenses):
    return sum(expense['amount'] for expense in expenses)

def filter_expenses_by_category(expenses, category):
    return [expense for expense in expenses if expense['category'] == category]

# Streamlit App
st.title("Spending Log")

# Store expenses in session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Add expense form
with st.form("expense_form"):
    amount = st.number_input("Amount", min_value=0.0)  # Removed format="%.2f"
    category = st.text_input("Category")
    date = st.date_input("Date")
    budget = st.number_input("Set your Budget", min_value=0.0)
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        if category.strip():
            add_expense(st.session_state.expenses, amount, category)
            st.success("Expense added!")
        else:
            st.warning("Please enter a valid category.")

# Show expenses
st.subheader("All Expenses")
if st.session_state.expenses:
    print_expenses(st.session_state.expenses)
else:
    st.write("No expenses yet.")

# Show total
st.subheader("Total Spent")
st.write(f"${total_expenses(st.session_state.expenses)}")

# Show budget
st.subheader("Budget Overview")
if budget > 0:
    remaining = budget - total_expenses
    if remaining >= 0:
        st.success(f"You are within budget. Remaining: ${remaining}")
    else:
        st.error(f"You exceeded the budget by ${abs(remaining)}")
else:
        st.info("No budget entered yet.")

# Filter by category
st.subheader("Filter by Category")
categories = list(set([e['category'] for e in st.session_state.expenses]))
if categories:
    selected = st.selectbox("Select a category", categories)
    filtered = filter_expenses_by_category(st.session_state.expenses, selected)
    st.write(f"Expenses for {selected}:")
    print_expenses(filtered)
