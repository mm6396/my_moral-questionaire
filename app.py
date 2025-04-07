import streamlit as st
import pandas as pd
import datetime

# Load questions
df = pd.read_csv("questions.csv")

# Initialize session states
if 'page' not in st.session_state:
    st.session_state.page = 0

if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'username' not in st.session_state:
    st.session_state.username = None

if 'culture' not in st.session_state:
    st.session_state.culture = None

if 'gender' not in st.session_state:
    st.session_state.gender = None

if 'current_choice' not in st.session_state:
    st.session_state.current_choice = ""

# Step 1: Get user information
if st.session_state.page == 0:
    st.title("Moral Choice Annotation")

    st.header("Step 1: Your Information")

    st.session_state.username = st.text_input("Enter your username:")

    st.session_state.culture = st.selectbox(
        "Select your culture:",
        ["Chinese", "American", "Indian", "Iranian", "Korean", "Persian", "Arabic", "African", "Japanese"]
    )

    st.session_state.gender = st.selectbox(
        "Please select your gender:",
        ["Male", "Female"]
    )

    if st.button("Start Questionnaire") and st.session_state.username:
        st.session_state.page = 1
        st.rerun()

# Step 2: Show questions
else:
    # --- Display User Info + Progress ---
    st.markdown(f"**Username:** {st.session_state.username} | **Culture:** {st.session_state.culture} | **Gender:** {st.session_state.gender}")
    st.progress((st.session_state.page - 1) / len(df))
    st.markdown("---")

    st.title(f"Question {st.session_state.page}")

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

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Next Question", key="next"):
            if st.session_state.current_choice != "":
                st.session_state.responses.append({
                    "username": st.session_state.username,
                    "culture": st.session_state.culture,
                    "gender": st.session_state.gender,
                    "context": current_row['context'],
                    "action1": current_row['action1'],
                    "action2": current_row['action2'],
                    "selected_action": st.session_state.current_choice,
                })

                st.session_state.page += 1

                if st.session_state.page > len(df):
                    results_df = pd.DataFrame(st.session_state.responses)
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    results_df.to_csv(f"annotation_results_{st.session_state.username}_{timestamp}.csv", index=False)
                    st.success("Thank you! Your answers have been recorded!")
                    st.stop()
                else:
                    st.rerun()

    with col2:
        if st.button("Save & Exit", key="save_exit"):
            results_df = pd.DataFrame(st.session_state.responses)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            results_df.to_csv(f"annotation_results_{st.session_state.username}_{timestamp}.csv", index=False)
            st.success("Your progress has been saved. You can return later by entering the same
