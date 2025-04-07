import streamlit as st
import pandas as pd
import datetime
import os

# Load questions
df = pd.read_csv("questions.csv")

# Initialize session state
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

    st.header("Step 1: Your Information")

    st.session_state.username = st.text_input("Enter your username:")

    st.session_state.culture = st.selectbox(
        "Select your culture:",
        ["Chinese", "American", "Indian", "Korean", "Persian", "Arabic", "African", "Japanese"]
    )

    st.session_state.gender = st.selectbox(
        "Select your gender:",
        ["Male", "Female"]
    )

    if st.button("Start Questionnaire"):
        if st.session_state.username.strip() == "":
            st.error("❗ Please enter a username before proceeding.")
        else:
            progress_file = f"{st.session_state.username}_progress.csv"
            if os.path.exists(progress_file):
                # username exists, load and check culture/gender
                progress_df = pd.read_csv(progress_file)
                saved_culture = progress_df.iloc[0]['culture']
                saved_gender = progress_df.iloc[0]['gender']

                if (st.session_state.culture != saved_culture) or (st.session_state.gender != saved_gender):
                    st.error(f"This username is already registered with culture '{saved_culture}' and gender '{saved_gender}'. Please match exactly or choose a new username.")
                elif len(progress_df) >= len(df):
                    st.error("This username has already completed the questionnaire. Please choose a different username.")
                else:
                    st.session_state.responses = progress_df.to_dict('records')
                    st.session_state.page = len(progress_df) + 1
                    st.success(f"Welcome back {st.session_state.username}! Continuing from Question {st.session_state.page}.")
                    st.rerun()
            else:
                st.session_state.page = 1
                st.rerun()

# ---------------------- Step 2: Questionnaire -----------------------
else:
    if st.session_state.page > len(df):
        st.success("Thank you! You have completed all questions.")
        st.balloons()
        st.stop()

    st.markdown(f"**Username:** {st.session_state.username} | **Culture:** {st.session_state.culture} | **Gender:** {st.session_state.gender}")

    total_questions = len(df)
    current_question = st.session_state.page
    progress_percentage = int((current_question / total_questions) * 100)

    st.markdown(f"**Progress:** {progress_percentage}% complete")
    progress = st.progress(0)
    progress.progress(progress_percentage / 100)

    st.markdown("---")

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

                results_df = pd.DataFrame(st.session_state.responses)
                results_df.to_csv(f"{st.session_state.username}_progress.csv", index=False)

                st.session_state.page += 1
                st.rerun()

    with col2:
        if st.button("Save & Exit"):
            results_df = pd.DataFrame(st.session_state.responses)
            results_df.to_csv(f"{st.session_state.username}_progress.csv", index=False)
            st.success(" Progress saved! You can return anytime to continue.")
            st.stop()
