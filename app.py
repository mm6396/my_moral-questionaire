import streamlit as st
import pandas as pd
import os

# Load questions
questions = pd.read_csv("questions.csv")

st.title("Moral Choice Annotation")

# Step 1: User Information
st.header("Step 1: Your Information")
culture = st.selectbox("Select your culture:", ["Chinese", "Iranian", "American", "Other"])
gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])

if st.button("Start Questionnaire"):
    st.session_state['current_question'] = 0
    st.session_state['responses'] = []
    st.session_state['culture'] = culture
    st.session_state['gender'] = gender

if 'current_question' in st.session_state:
    current_idx = st.session_state['current_question']

    if current_idx < len(questions):
        st.header(f"Question {current_idx + 1} of {len(questions)}")

        context = questions.loc[current_idx, 'context']
        action1 = questions.loc[current_idx, 'action1']
        action2 = questions.loc[current_idx, 'action2']

        st.markdown(f"**Context:** {context}")
        st.markdown(f"**Action 1:** {action1}")
        st.markdown(f"**Action 2:** {action2}")

        # Radio button for answer
        choice = st.radio(
            "Which action is more moral?",
            (f"Action 1: {action1}", f"Action 2: {action2}", "Both equally moral", "Neither moral"),
            key=f"choice_{current_idx}"
        )

        if choice:
            if st.session_state.get(f"answered_{current_idx}") is None:
                st.session_state['responses'].append({
                    'culture': st.session_state['culture'],
                    'gender': st.session_state['gender'],
                    'context': context,
                    'action1': action1,
                    'action2': action2,
                    'selected_action': choice
                })
                st.session_state['current_question'] += 1
                st.session_state[f"answered_{current_idx}"] = True

    else:
        st.success("Thank you for completing the questionnaire!")

        df_responses = pd.DataFrame(st.session_state['responses'])

        # Save file based on culture and gender
        file_name = f"{st.session_state['culture'].lower()}_{st.session_state['gender'].lower()}_annot.csv"

        if os.path.exists(file_name):
            existing_df = pd.read_csv(file_name)
            df_responses = pd.concat([existing_df, df_responses], ignore_index=True)

        df_responses.to_csv(file_name, index=False)

        st.write(f"Responses saved to `{file_name}`.")

        # Reset session
        del st.session_state['current_question']
        del st.session_state['responses']
        del st.session_state['culture']
        del st.session_state['gender']
