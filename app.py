import streamlit as st
import requests as rq
import pandas as pd
import matplotlib.pyplot as plt

server_loc = "https://expense-tracker-backend.onrender.com"

st.title("EXPENSE TRACKER")

opt = st.sidebar.selectbox(
    "Choose Operation",
    [
        "ADD_EXPENSE",
        "VIEW_EXPENSE",
        "DELETE_EXPENSE",
        "UPDATE_EXPENSE",
        "SEARCH_EXPENSE",
        "SORT_EXPENSE",
        "FILTER_EXPENSE",
        "SPENDING_ANALYSIS"
    ]
)

#  ADD 
if opt == "ADD_EXPENSE":

    st.header("ADD EXPENSE")

    with st.form("adding"):

        title = st.text_input("Title")
        amount = st.number_input("Amount")

        category = st.selectbox(
            "Category",
            [
                "",
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Other"
            ]
        )

        expense_date = st.date_input("Date")

        btn = st.form_submit_button("ADD EXPENSE")

        if btn:

            new_data = {
                "t": title,
                "a": amount,
                "c": category,
                "d": str(expense_date)
            }

            res = rq.post(
                f"{server_loc}/add_expense",
                json=new_data
            )

            st.success(res.json()["msg"])


# VIEW 
elif opt == "VIEW_EXPENSE":

    st.header("VIEW EXPENSES")

    res = rq.get(f"{server_loc}/view_expense")

    data = res.json()

    df = pd.DataFrame(data)

    st.dataframe(df)


# DELETE 
elif opt == "DELETE_EXPENSE":

    st.header("DELETE EXPENSE")

    expense_id = st.number_input(
        "Enter Expense ID",
        step=1
    )

    if st.button("DELETE"):

        res = rq.delete(
            f"{server_loc}/delete_expense/{expense_id}"
        )

        st.success(res.json()["msg"])


# UPDATE 
elif opt == "UPDATE_EXPENSE":

    st.header("UPDATE EXPENSE")

    expense_id = st.number_input(
        "Expense ID",
        step=1
    )

    title = st.text_input("New Title")

    amount = st.number_input("New Amount")

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    expense_date = st.date_input("New Date")

    if st.button("UPDATE"):

        update_data = {
            "t": title,
            "a": amount,
            "c": category,
            "d": str(expense_date)
        }

        res = rq.put(
            f"{server_loc}/update_expense/{expense_id}",
            json=update_data
        )

        st.success(res.json()["msg"])

#SEARCH
elif opt == "SEARCH_EXPENSE":

    st.header("SEARCH EXPENSE")

    title = st.text_input("Enter Expense Title")

    if st.button("SEARCH"):

        res = rq.get(f"{server_loc}/search_expense/{title}")

        data = res.json()

        df = pd.DataFrame(data)

        st.dataframe(df)

# SORT
elif opt == "SORT_EXPENSE":

    st.header("SORT EXPENSE")

    order = st.selectbox(
        "Choose Order",
        ["asc", "desc"]
    )

    if st.button("SORT"):

        res = rq.get(f"{server_loc}/sort_expense/{order}")

        data = res.json()

        df = pd.DataFrame(data)

        st.dataframe(df)

# FILTER
elif opt=="FILTER_EXPENSE":

    st.header("FILTER EXPENSE")

    category = st.selectbox(
        "Choose Category",
        ["Food", "Travel", "Bills", "Shopping", "Other"]
    )

    if st.button("FILTER"):

        res = rq.get(f"{server_loc}/filter_expense/{category}")

        data = res.json()

        df = pd.DataFrame(data)

        st.dataframe(df)

# ANALYSE
elif opt=="SPENDING_ANALYSIS":

    st.header("CATEGORY WISE SPENDING")

    res = rq.get(f"{server_loc}/spending_analysis")

    data = res.json()

    df = pd.DataFrame(data)

    st.dataframe(df)

    fig, ax = plt.subplots()

    ax.bar(df["category"], df["total"])

    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.set_title("Expense Analysis")

    st.pyplot(fig)