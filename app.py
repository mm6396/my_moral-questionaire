import streamlit as st
import pandas as pd
import os
from collections import defaultdict


TOTAL_QUESTIONS = 680

# Load questions
df = pd.read_csv("questions.csv")

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 0

if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'culture' not in st.session_state:
    st.session_state.culture = None

if 'gender' not in st.session_state:
    st.session_state.gender = None

if 'username' not in st.session_state:
    st.session_state.username = None

if 'current_choice' not in st.session_state:
    st.session_state.current_choice = ""

# ---------------------- Step 1: User Profile -----------------------
if st.session_state.page == 0:
    st.title("Moral Choice Annotation")

    st.header("Current Participation Statistics")

    progress_files = [f for f in os.listdir() if f.endswith('_progress.csv')]
    total_users = 0
    completed_users = 0

    # Dictionaries for counts
    started_counter = defaultdict(int)
    completed_counter = defaultdict(int)

    for file in progress_files:
        if os.path.getsize(file) > 0:  
            try:
                df_progress = pd.read_csv(file)
                if len(df_progress) > 0:
                    key = (df_progress.iloc[0]['culture'], df_progress.iloc[0]['gender'])
                    started_counter[key] += 1
                    total_users += 1

                if len(df_progress) == TOTAL_QUESTIONS:
                    completed_counter[key] += 1
                    completed_users += 1
            except Exception as e:
                # st.warning(f"Could not read file {file}: {e}")
                continue

    # # Overall stats
    # st.info(f"**Total Users Started:** {total_users}")
    # st.success(f"**Users Completed Questionnaire:** {completed_users}")
    # st.markdown("---")

    # Detail
    st.subheader("Detailed information about Participation (Culture + Gender)")
    cultures = ["Chinese", "American", "Indian", "Korean", "Persian", "Arabic", "African", "Japanese"]
    genders = ["Male", "Female"]

    for culture in cultures:
        for gender in genders:
            started = started_counter.get((culture, gender), 0)
            completed = completed_counter.get((culture, gender), 0)
            if started > 0 or completed > 0:
                st.write(f"**{culture} - {gender}:** Started: {started} | Completed: {completed}")
                
                
# -----------------------------------
# Download Progress File if exists
# -----------------------------------
    progress_file = f"{st.session_state.username}_progress.csv"

    if st.session_state.username and os.path.exists(progress_file):
        with open(progress_file, "rb") as f:
            st.download_button(
                label="⬇️ Download My Progress File",
                data=f,
                file_name=progress_file,
                mime="text/csv"
            )

    st.markdown("---")

    # ------------------- User Login -------------------
    st.header("Step 1: Your Information")

    st.session_state.username = st.text_input("Enter your username:")

    st.session_state.culture = st.selectbox(
        "Select your culture:",
        cultures
    )

    st.session_state.gender = st.selectbox(
        "Select your gender:",
        genders
    )

    if st.button("Start Questionnaire"):
        if st.session_state.username.strip() == "":
            st.error("Please enter a username before proceeding.")
        else:
            progress_file = f"{st.session_state.username}_progress.csv"
            if os.path.exists(progress_file):
                if os.path.getsize(progress_file) > 0:
                    progress_df = pd.read_csv(progress_file)
                    st.session_state.responses = progress_df.to_dict('records')
                    st.session_state.page = len(progress_df) + 1
                    st.success(f"Welcome back {st.session_state.username}! Continuing from Question {st.session_state.page}.")
                else:
                    st.session_state.page = 1
            else:
                st.session_state.page = 1  # New user
            st.rerun()

# ---------------------- Step 2: Questionnaire -----------------------
else:
    if st.session_state.page > len(df):
        st.success("Thank you! You have completed all questions.")
        st.balloons()
        st.stop()

    # Show user info
    st.markdown(f"**Username:** {st.session_state.username} | **Culture:** {st.session_state.culture} | **Gender:** {st.session_state.gender}")

    # Progress Bar
    total_questions = len(df)
    current_question = st.session_state.page
    progress_percentage = int((current_question / total_questions) * 100)

    st.markdown(f"**Progress:** {progress_percentage}% complete")
    progress = st.progress(progress_percentage / 100)

    st.markdown("---")

    # Show current question
    st.title(f"Question {st.session_state.page}")

    current_row = df.iloc[st.session_state.page - 1]

    st.write(f"### Context:\n{current_row['context']}")
    st.write(f"**Action 1:** {current_row['action1']}")
    st.write(f"**Action 2:** {current_row['action2']}")

    choice = st.radio(
        "Which action is more moral?",
        ("", "Action 1", "Action 2"),
        index=0,
        key=f"choice_{st.session_state.page}"
    )

    col1, col2 = st.columns(2)

    with col1:
        if choice != "":
            if st.button("Next Question"):
                st.session_state.responses.append({
                    "username": st.session_state.username,
                    "culture": st.session_state.culture,
                    "gender": st.session_state.gender,
                    "context": current_row['context'],
                    "action1": current_row['action1'],
                    "action2": current_row['action2'],
                    "selected_action": choice,
                })

                # Save progress
                results_df = pd.DataFrame(st.session_state.responses)
                results_df.to_csv(f"{st.session_state.username}_progress.csv", index=False)

                st.session_state.page += 1
                st.rerun()

    with col2:
        if st.button("Save & Exit!"):
            results_df = pd.DataFrame(st.session_state.responses)
            results_df.to_csv(f"{st.session_state.username}_progress.csv", index=False)
            st.success("Progress saved! You can return anytime to continue.")
            st.stop()
