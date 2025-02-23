import streamlit as st
from src.database import create_database, validate_user, register_user, get_user_indexes, save_index
import os
import re
from src.pdf_load import PdfLoader
from src.split_docs import Splitter
from src.create_embeddings import CreateEmbeddings
from src.query import RunLLM
from streamlit_chat import message


def main():
    st.title("PDF Search Engine")
    create_database()  # Ensure the database and tables are created

    # Initialize session state variables
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"  # Default to the login page
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    if 'index_name' not in st.session_state:
        st.session_state.index_name = None

    # Navigation based on the current page
    if st.session_state.current_page == "login":
        show_login_page()
    elif st.session_state.current_page == "search_engine":
        show_pdf_search_engine()



def show_login_page():
    """Displays the login or registration page."""
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.subheader("Create a New Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            if register_user(username, password):
                st.success("Account created successfully! You can now log in.")
            else:
                st.error("Username already exists.")
    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_id = validate_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.logged_in = True
                st.session_state.current_page = "search_engine"  # Redirect to the search engine


def show_pdf_search_engine():
    """Displays the PDF search engine page."""
    st.sidebar.subheader(f"Welcome, User {st.session_state.user_id}")
    user_id = st.session_state.user_id

    # Retrieve and display user-specific indexes
    index_names = get_user_indexes(user_id)
    with st.sidebar:
        selected_index = st.selectbox("Select PDF", [""] + index_names)
        if selected_index:
            st.session_state.index_name = selected_index
            st.session_state.pdf_processed = True

    # PDF Upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        with st.spinner("Processing PDF.."):
            original_filename = uploaded_file.name
            index_name = re.sub(r'[^a-z0-9-]', '', original_filename.lower().replace(' ', '-').replace('_', '-')).strip('-')

            # Check if index_name already exists for the user
            if index_name in index_names:
                st.warning(f"The PDF with the index name '{index_name}' has already been processed.")
                st.session_state.pdf_processed = True
                st.session_state.index_name = index_name
            else:
                # Process the PDF
                with open(original_filename, "wb") as f:
                    f.write(uploaded_file.getvalue())
                loader = PdfLoader(original_filename)
                pages = loader.load_pages_sync()
                splitter = Splitter()
                documents = splitter.split_text(pages)
                embeddings = CreateEmbeddings()
                embeddings.create_embeddings(documents, index_name)
                os.remove(original_filename)
                save_index(user_id, index_name)
                st.success("PDF processed successfully!")

    if (
        "chat_answers_history" not in st.session_state
        and "user_prompt_history" not in st.session_state
        and "chat_history" not in st.session_state
    ):
        st.session_state["chat_answers_history"] = []
        st.session_state["user_prompt_history"] = []
        st.session_state["chat_history"] = []    

    # Query section
    if st.session_state.pdf_processed and st.session_state.index_name:
        query = st.text_input("Ask a question about the PDF")


        if st.button("Submit"):
            with st.spinner("Generating response.."):
                query_runner = RunLLM(st.session_state.index_name)
                result = query_runner.run_query(query, chat_history=st.session_state["chat_history"])

                st.session_state["user_prompt_history"].append(query)
                st.session_state["chat_answers_history"].append(result)
                st.session_state["chat_history"].append(("human", query))
                st.session_state["chat_history"].append(("ai", result))

    if st.session_state["chat_answers_history"]:
        for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        ):
            message(user_query, is_user=True)
            message(generated_response)


if __name__ == "__main__":
    main()