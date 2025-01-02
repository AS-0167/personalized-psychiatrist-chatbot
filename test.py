import streamlit as st

# --- Set up Streamlit page ---
st.set_page_config(page_title="Chatbot", layout="centered")
st.title("**Personalized Chatbot**")

# --- Ask for user's name ---
if "user_name" not in st.session_state:
    # Capture user input
    user_name_input = st.text_input("Enter your full name to continue:", key="name_input")
    
    # Debugging output
    st.write(f"User input from the text box: {user_name_input}")

    # If the user has provided input, save it to the session state
    print(user_name_input)
    if user_name_input:
        st.session_state["user_name"] = user_name_input
        st.write(f"User name saved: {st.session_state['user_name']}")
else:
    st.write(f"User name from session state: {st.session_state['user_name']}")
