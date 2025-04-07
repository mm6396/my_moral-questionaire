import streamlit as st
import pandas as pd
import datetime
import os

# Load questions
df = pd.read_csv("questions.csv")

# Initialize session states
if 'page' not in st.session_state:
    st.session_state.page = 0

if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'culture' not in st.session_state:
    st.session_state.culture = None

if 'gender' not in st.session_state:
    st.session_state.gender = None

if 'current_choice' not in st.session_state:
    st.session_state.current_choice = ""

if 'username' not in st.session_state:
    st.session_state.username = ""

# Step 0: Login / Username
if st.session_state.username == "":
    st.title("Moral Choice Annotation")

    username_input = st.text_input("Enter your username (no password needed):")

    if st.button("Login"):
        if username_input.strip() != "":
            st.session_state.username = username_input.strip()

            # Check if this user already has progress
            progress_file = f"{st.session_state.username}_progress.csv"
            if os.path.exists(progress_file):
                progress_df = pd.read_csv(progress_file)
                st.session_state.responses = progress_df.to_dict(orient='records')
                st.session_state.page = len(st.session_state.responses) + 1
                if len(progress_df) > 0:
                    st.session_state.culture = progress_df.iloc[0]['culture']
                    st.session_state.gender = progress_df.iloc[0]['gender']
            else:
                st.session_state.page = 0
            st.rerun()

# Step 1: Collect user info
elif st.session_state.page == 0:
    st.title("Moral Choice Annotation")

    st.header("Step 1: Your Information")

    st.session_state.culture = st.selectbox(
        "Select your culture:",
        ["Chinese", "American", "Indian", "Iranian", "Korean", "Persian", "Arabic", "African", "Japanese"]
    )

    st.session_state.gender = st.selectbox(
        "Please select your gender:",
        ["Male", "Female"]
    )

    if st.button("Start Questionnaire"):
        st.session_state.page = 1
        st.rerun()

# Step 2: Show questions
else:
    st.title(f"Question {st.session_state.page}")

    if st.session_state.page > len(df):
        st.success("Thank you! Your answers have been recorded 🙏")
        st.stop()

    current_row = df.iloc[st.session_state.page - 1]

    st.write(f"### Context:\n{current_row['context']}")
    st.write(f"**Action 1:** {current_row['action1']}")
    st.write(f"**Action 2:** {current_row['action2']}")

    st.session_state.current_choice = st.radio(
        "Which action is more moral?",
        ("", "Action 1", "Action 2"),
        index=0,
        key=f"choice_{st.session_state.page}"
    )

    if st.session_state.current_choice != "":
        if st.button("Next Question"):
            st.session_state.responses.append({
                "culture": st.session_state.culture,
                "gender": st.session_state.gender,
                "context": current_row['context'],
                "action1": current_row['action1'],
                "action2": current_row['action2'],
                "selected_action": st.session_state.current_choice,
            })

            # Save progress
            results_df = pd.DataFrame(st.session_state.responses)
            results_df.to_csv(f"{st.session_state.username}_progress.csv", index=False)

            st.session_state.page += 1
            st.rerun()
