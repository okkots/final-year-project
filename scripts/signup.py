import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine

# Initialize connection.
def init_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sasori",
            database="honeypot"
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Perform query.
def perform_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return None

# Main function
def main():
    conn = init_connection()

    if conn is not None:
        # Sign-up form
        st.title("Sign Up")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            hashed_password = st.secrets["mysql"].password.encode("utf-8")
            query = f"""
                INSERT INTO users (name, email, password)
                VALUES ('{name}', '{email}', '{hashed_password}');
            """
            perform_query(conn, query)
            st.success("Sign Up successful!")
    else:
        st.error("Error: Could not connect to the database.")

if __name__ == "__main__":
    main()