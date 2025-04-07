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

if 'username' not in st.session_state:
    st.session_state.username = ""

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Step 0: Login / Sign-up
if not st.session_state.logged_in:
    st.title("Moral Choice Annotation - Login")

    st.header("Please Enter Your Information")

    username_input = st.text_input("Username:")
    culture_input = st.selectbox(
        "Culture:",
        ["Chinese", "American", "Indian", "Iranian", "Korean", "Persian", "Arabic", "African", "Japanese"]
    )
    gender_input = st.selectbox(
        "Gender:",
        ["Male", "Female"]
    )

    if st.button("Start"):
        if username_input.strip() == "":
            st.error("Username cannot be empty.")
        else:
            progress_file = f"{username_input.strip()}_progress.csv"
            if os.path.exists(progress_file):
                # Existing user - validate culture and gender
                progress_df = pd.read_csv(progress_file)
                saved_culture = progress_df.iloc[0]['culture']
                saved_gender = progress_df.iloc[0]['gender']

                if saved_culture != culture_input or saved_gender != gender_input:
                    st.error("Culture or Gender does not match your previous records. Please check.")
                else:
                    st.success("Welcome back! Resuming your questionnaire...")
                    st.session_state.username = username_input.strip()
                    st.session_state.culture = saved_culture
                    st.session_state.gender = saved_gender
                    st.session_state.responses = progress_df.to_dict(orient='records')
                    st.session_state.page = len(progress_df) + 1
                    st.session_state.logged_in = True
                    st.rerun()
            else:
                # New user
                st.success("Welcome! Starting new questionnaire.")
                st.session_state.username = username_input.strip()
                st.session_state.culture = culture_input
                st.session_state.gender = gender_input
                st.session_state.page = 1
                st.session_state.logged_in = True
                st.rerun()


else:
    if st.session_state.page > len(df):
        st.success("Thank you! You have completed all questions.")
        st.stop()

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
            st.success("Progress saved! You can come back later to continue.")
            st.stop()
