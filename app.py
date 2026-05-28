import streamlit as st
import requests as rq
import pandas as pd
import matplotlib.pyplot as plt

server_loc = "https://expense-tracker-backend.onrender.com"

st.title("EXPENSE TRACKER")


# =========================================
# REQUEST FUNCTION
# =========================================

def make_request(method, endpoint, data=None):

    url = f"{server_loc}{endpoint}"

    try:

        if method == "GET":
            res = rq.get(url, timeout=60)

        elif method == "POST":
            res = rq.post(
                url,
                json=data,
                timeout=60
            )

        elif method == "PUT":
            res = rq.put(
                url,
                json=data,
                timeout=60
            )

        elif method == "DELETE":
            res = rq.delete(
                url,
                timeout=60
            )

        try:
            response = res.json()

        except:
            st.error("Backend is not returning JSON")
            st.write(res.text)
            return None

        if res.status_code != 200:

            st.error(f"Backend Error: {res.status_code}")
            st.write(response)

            return None

        return response

    except rq.exceptions.Timeout:

        st.error("Server timeout. Render may be sleeping.")
        return None

    except Exception as e:

        st.error(f"Error: {e}")
        return None


# =========================================
# SIDEBAR
# =========================================

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


# =========================================
# ADD
# =========================================

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

            response = make_request(
                "POST",
                "/add_expense",
                new_data
            )

            if response:
                st.success(response["msg"])


# =========================================
# VIEW
# =========================================

elif opt == "VIEW_EXPENSE":

    st.header("VIEW EXPENSES")

    data = make_request(
        "GET",
        "/view_expense"
    )

    if data:

        df = pd.DataFrame(data)

        st.dataframe(df)


# =========================================
# DELETE
# =========================================

elif opt == "DELETE_EXPENSE":

    st.header("DELETE EXPENSE")

    expense_id = st.number_input(
        "Enter Expense ID",
        step=1
    )

    if st.button("DELETE"):

        response = make_request(
            "DELETE",
            f"/delete_expense/{expense_id}"
        )

        if response:
            st.success(response["msg"])


# =========================================
# UPDATE
# =========================================

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

        response = make_request(
            "PUT",
            f"/update_expense/{expense_id}",
            update_data
        )

        if response:
            st.success(response["msg"])


# =========================================
# SEARCH
# =========================================

elif opt == "SEARCH_EXPENSE":

    st.header("SEARCH EXPENSE")

    title = st.text_input("Enter Expense Title")

    if st.button("SEARCH"):

        data = make_request(
            "GET",
            f"/search_expense/{title}"
        )

        if data:

            df = pd.DataFrame(data)

            st.dataframe(df)


# =========================================
# SORT
# =========================================

elif opt == "SORT_EXPENSE":

    st.header("SORT EXPENSE")

    order = st.selectbox(
        "Choose Order",
        ["asc", "desc"]
    )

    if st.button("SORT"):

        data = make_request(
            "GET",
            f"/sort_expense/{order}"
        )

        if data:

            df = pd.DataFrame(data)

            st.dataframe(df)


# =========================================
# FILTER
# =========================================

elif opt == "FILTER_EXPENSE":

    st.header("FILTER EXPENSE")

    category = st.selectbox(
        "Choose Category",
        ["Food", "Travel", "Bills", "Shopping", "Other"]
    )

    if st.button("FILTER"):

        data = make_request(
            "GET",
            f"/filter_expense/{category}"
        )

        if data:

            df = pd.DataFrame(data)

            st.dataframe(df)


# =========================================
# ANALYSIS
# =========================================

elif opt == "SPENDING_ANALYSIS":

    st.header("CATEGORY WISE SPENDING")

    data = make_request(
        "GET",
        "/spending_analysis"
    )

    if data:

        df = pd.DataFrame(data)

        st.dataframe(df)

        fig, ax = plt.subplots()

        ax.bar(df["category"], df["total"])

        ax.set_xlabel("Category")

        ax.set_ylabel("Amount")

        ax.set_title("Expense Analysis")

        st.pyplot(fig)