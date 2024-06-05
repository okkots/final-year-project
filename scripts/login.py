import hashlib
import os
import streamlit as st
import mysql.connector
import random
from mysql.connector import Error
import string
from sqlalchemy import create_engine

#st.set_option("enable_experimental_features", True)

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
def perform_query(conn, query, params):
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        #conn.commit()
        result = cursor.fetchall()
        for row in result:
            pass
        return result
# Generate salt
def generate_salt():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Get salt from database
def get_salt(conn, email):
    query = "SELECT salt FROM auth WHERE email = %s"
    params = (email,)
    result = perform_query(conn, query, params)
    if result is not None and len(result) == 1:
        for row in result:
            salt = row[0]
        return salt
    else:
        return None
# Hash password
def hash_password(password, salt):
    if salt is None:
        return None
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest()
def authenticate(email, password):
    # Check if the username and password are correct
    # ...

    if authenticate:
        st.session_state["logged_in"] = True
        st.session_state["email"] = email
        st.session_state["password"] = password
        return True
    else:
        return False
# Main function
def main():
    conn = init_connection()

    if conn is not None:
        # Login form
        st.title("Login")
        email_key = "email_input"
        email = st.text_input("Email", key=email_key)
        password_key = "password_input"
        password = st.text_input("Password", type="password", key=password_key)

        if st.button("Login"):
            hashed_password = hash_password(password, get_salt(conn, email))
            if hashed_password is not None:
                query = "SELECT id, password FROM auth WHERE email = %s AND password = %s"
                params = (email, hashed_password)
                result = perform_query(conn, query, params)

                if result is not None and len(result) == 1:
                    st.success("Login successful!")
                    # Redirect to main page
                    os.system("start streamlit run stream.py")
                else:
                    st.error("Invalid email or password")
            
            else:
                st.error("Email not found in database")
    else:
        st.error("Error: Could not connect to the database.")

    if "sign_up_clicked" not in st.session_state:
        st.session_state["sign_up_clicked"] = False

    if st.button("Sign up"):
        st.session_state["sign_up_clicked"] = True

    if st.session_state["sign_up_clicked"]:
        # Sign up page
        st.title("Sign Up")
        username_key = "signup_username_input"
        username = st.text_input("Username", key=username_key)
        email_key = "signup_email_input"
        email = st.text_input("Email", key=email_key)
        password_key = "signup_password_input"
        password = st.text_input("Password", type="password", key=password_key)
        confirm_password_key = "signup_confirm_password_input"
        confirm_password = st.text_input("Confirm Password", type="password", key=confirm_password_key)

        if password != confirm_password:
            st.error("Passwords do not match")
        elif st.button("Sign Up"):
            salt = generate_salt()
            hashed_password = hash_password(password, salt)
            query = "INSERT INTO auth (username, email, password,salt) VALUES (%s, %s, %s,%s)"
            params = (username, email, hashed_password,salt)
            perform_query(conn, query, params)
            st.success("Sign up successful!")
            st.session_state["sign_up_clicked"] = False
            st.rerun()

if __name__ == "__main__":
    main()