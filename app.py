# Core package
import streamlit as st
import streamlit.components.v1 as stc

# EDA package
import pandas as pd
import numpy as np
import plotly.express as px

# Database
from db_utils import (create_table, add_data, view_all_data,
                      view_unique_tasks, get_task, edit_task_data, delete_task)


HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """


def main():
    stc.html(HTML_BANNER)
    menu = ["Create", "Read", "Update", "Delete", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_table()
    if choice == "Create":
        st.subheader("Add Items")

        col1, col2 = st.columns(2)

        with col1:
            task = st.text_area("Task to do")

        with col2:
            task_status = st.selectbox("Status", ("Todo", "Doing", "Done"))
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task, task_status, task_due_date)
            st.success("Successfully Added Data: {}".format(task))

    elif choice == "Read":
        st.subheader("View Items")
        result = view_all_data()
        st.write(result)
        df = pd.DataFrame(result, columns=['Task', 'Status', 'Due_Date'])
        with st.expander("View All Data"):
            st.table(df)

        with st.expander("Task Status"):
            task_df = df["Status"].value_counts()
            task_df = task_df.reset_index()
            st.table(task_df)
            p1 = px.pie(task_df, names='index', values='Status')
            st.plotly_chart(p1)

    elif choice == "Update":
        st.subheader("Edit/Update Items")
        result = view_all_data()
        df = pd.DataFrame(result, columns=['Task', 'Status', 'Due_Date'])
        with st.expander("Current Data"):
            st.table(df)

        list_of_tasks = [i[0] for i in view_unique_tasks()]
        selected_task = st.selectbox("Task to Edit", list_of_tasks)
        selected_result = get_task(selected_task)
        st.write(selected_result)

        if selected_result:
            task = selected_result[0][0]
            task_status = selected_result[0][1]
            task_due_date = selected_result[0][2]

            col1, col2 = st.columns(2)

            with col1:
                new_task = st.text_area("Task to do", task)

            with col2:
                new_task_status = st.selectbox(task_status, ("Todo", "Doing", "Done"))
                new_task_due_date = st.date_input(task_due_date)

            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date, task)
                st.success("Successfully Updated:: {} to ::{}".format(task, new_task))

        result2 = view_all_data()
        df2 = pd.DataFrame(result2, columns=['Task', 'Status', 'Due_Date'])
        with st.expander("Updated Data"):
            st.table(df2)

    elif choice == "Delete":
        st.subheader("Delete Items")
        result = view_all_data()
        df = pd.DataFrame(result, columns=['Task', 'Status', 'Due_Date'])
        with st.expander("Current Data"):
            st.table(df)

        list_of_tasks = [i[0] for i in view_unique_tasks()]
        selected_task = st.selectbox("Task to Delete", list_of_tasks)
        st.warning('You Are About To Delete : "{}"'.format(selected_task))
        if st.button("Delete Task"):
            delete_task(selected_task)
            st.success("Task Successfully Deleted")

        result2 = view_all_data()
        df2 = pd.DataFrame(result2, columns=['Task', 'Status', 'Due_Date'])
        with st.expander("New Data"):
            st.table(df2)

    else:
        st.subheader("About")


if __name__ == '__main__':
    main()
