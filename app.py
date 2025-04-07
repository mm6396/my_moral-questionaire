import streamlit as st
import pandas as pd
import datetime


df = pd.read_csv("questions.csv")  


if 'page' not in st.session_state:
    st.session_state.page = 0

if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'culture' not in st.session_state:
    st.session_state.culture = None

if 'gender' not in st.session_state:
    st.session_state.gender = None

if st.session_state.page == 0:
    st.title("Moral Choice Annotation")

    st.header("Step 1: Your Information")

    st.session_state.culture = st.selectbox(
        "Select your culture:", 
        ["Chinese", "American", "Indian", "Iranian", "Korean", "Persian" , "Arabic" , "African", "Japanese"]
    )
    st.session_state.gender = st.selectbox(
        "Please Select your gender:", 
        ["Male", "Female"]
    )

    if st.button("Start Questionnaire"):
        st.session_state.page += 1
        st.rerun()


else:
    st.title(f"Question {st.session_state.page}")

    current_row = df.iloc[st.session_state.page - 1]

    st.write(f"### Context:\n{current_row['context']}")
    st.write(f"**Action 1:** {current_row['action1']}")
    st.write(f"**Action 2:** {current_row['action2']}")

    choice = st.radio(
        "Which action is more moral?",
        ("", "Action 1", "Action 2"),
        index=0
    )

    if choice != "":  
        st.session_state.responses.append({
            "culture": st.session_state.culture,
            "gender": st.session_state.gender,
            "context": current_row['context'],
            "action1": current_row['action1'],
            "action2": current_row['action2'],
            "selected_action": choice,
        })
        
        st.session_state.page += 1

        if st.session_state.page > len(df):
            # All questions done, save results
            results_df = pd.DataFrame(st.session_state.responses)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            results_df.to_csv(f"annotation_results_{timestamp}.csv", index=False)
            st.success("Thank you! Your answers have been recorded. ")
            st.stop()
        else:
            st.experimental_rerun()
