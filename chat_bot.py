# import streamlit as st
# import google.generativeai as genai


# with open("api.key", "r") as file:
#     API_KEY = file.read().strip()
# genai.configure(api_key=API_KEY)


# with open("model.name", "r") as file:
#     fine_tuned_model_name = file.read().strip()
# model = genai.GenerativeModel(model_name=fine_tuned_model_name)

# st.set_page_config(page_title="Fine-Tuned Chatbot", layout="centered")
# st.title("**PERSONALIZED PSYCHIATRIC CHATBOT**")

# # ---  Initialize session state for messages ---
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []

# # ---  Callback function to handle sending messages ---
# def send_message():
#     user_message = st.session_state.user_input.strip()
#     if user_message:
#         # ---  Append user message to chat history ---
#         st.session_state["messages"].append({"role": "user", "content": user_message})
        
#         # ---  Prepare the prompt with the last 10 messages ---
#         chat_history = st.session_state["messages"][-10:]
#         prompt = "\n".join(
#             f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history
#         )
        
#         # ---  Generate bot response ---
#         response = model.generate_content(prompt).text
#         st.session_state["messages"].append({"role": "bot", "content": response})
        
#         # ---  Clear the input field ---
#         st.session_state.user_input = ""

# # ---  Chat history container ---
# st.markdown(
#     """
#     <div style='max-height: 500px; overflow-y: auto; padding: 10px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px;'>
#     """,
#     unsafe_allow_html=True,
# )

# # ---  Display chat messages ---
# for message in st.session_state["messages"]:
#     if message["role"] == "user":
#         st.markdown(
#             f"""
#             <div style='align-self: flex-end; background-color: #dcf8c6; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%; text-align: right; float: right; clear: both;'>
#                 <b>You:</b> {message['content']}
#             </div>
#             <div style='clear: both;'></div>
#             """,
#             unsafe_allow_html=True,
#         )
#     else:
#         st.markdown(
#             f"""
#             <div style='align-self: flex-start; background-color: #f1f0f0; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%; text-align: left; float: left; clear: both;'>
#                 <b>Bot:</b> {message['content']}
#             </div>
#             <div style='clear: both;'></div>
#             """,
#             unsafe_allow_html=True,
#         )

# st.markdown("</div>", unsafe_allow_html=True)

# # ---  Input box at the bottom ---
# st.text_input(
#     "You:",
#     key="user_input",
#     placeholder="Type your message here...",
#     on_change=send_message,
# )

# # ---  Auto-focus script for the input box ---
# st.markdown(
#     """
#     <script>
#         var inputBox = window.parent.document.querySelector('input[type="text"]');
#         inputBox.focus();
#     </script>
#     """,
#     unsafe_allow_html=True,
# )






import streamlit as st
import google.generativeai as genai
import os
import json

# --- Load API key ---
with open("api.key", "r") as file:
    API_KEY = file.read().strip()
genai.configure(api_key=API_KEY)

# --- Load model name ---
with open("model.name", "r") as file:
    fine_tuned_model_name = file.read().strip()
model = genai.GenerativeModel(model_name=fine_tuned_model_name)

# --- Set up Streamlit page ---
st.set_page_config(page_title="Fine-Tuned Chatbot", layout="centered")
st.title("**PERSONALIZED PSYCHIATRIC CHATBOT**")

# --- Create chat directory if it doesn't exist ---
chat_directory = "chats"
if not os.path.exists(chat_directory):
    os.makedirs(chat_directory)

# --- Initialize session state for messages if not already initialized ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# --- Callback function to handle sending messages ---
def send_message():
    user_message = st.session_state.user_input.strip()
    if user_message:
        # --- Append user message to chat history ---
        st.session_state["messages"].append({"role": "user", "content": user_message})
        
        # --- Prepare the prompt with the last 10 messages ---
        chat_history = st.session_state["messages"][-10:]
        prompt = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history
        )
        
        # --- Generate bot response ---
        response = model.generate_content(prompt).text
        st.session_state["messages"].append({"role": "bot", "content": response})
        
        # --- Save updated chat history ---
        user_file = os.path.join(chat_directory, f"{st.session_state['user_name']}.json")
        with open(user_file, "w") as file:
            json.dump(st.session_state["messages"], file, indent=4)
        
        # --- Clear the input field ---
        st.session_state.user_input = ""


def main() :
    # --- Chat history container ---
    st.markdown(
        """
        <div style='max-height: 500px; overflow-y: auto; padding: 10px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px;'>
        """,
        unsafe_allow_html=True,
    )

    # --- Display chat messages ---
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.markdown(
                f"""
                <div style='align-self: flex-end; background-color: #dcf8c6; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%; text-align: right; float: right; clear: both;'>
                    <b>You:</b> {message['content']}
                </div>
                <div style='clear: both;'></div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='align-self: flex-start; background-color: #f1f0f0; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%; text-align: left; float: left; clear: both;'>
                    <b>Bot:</b> {message['content']}
                </div>
                <div style='clear: both;'></div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # --- Input box at the bottom ---
    st.text_input(
        "You:",
        key="user_input",
        placeholder="Type your message here...",
        on_change=send_message,
    )

    # --- Auto-focus script for the input box ---
    st.markdown(
        """
        <script>
            var inputBox = window.parent.document.querySelector('input[type="text"]');
            inputBox.focus();
        </script>
        """,
        unsafe_allow_html=True,
    )

# --- Ask for user's name ---
if "user_name" not in st.session_state:
    # Capture user input
    user_name_input = st.text_input("Enter your full name to continue:", key="name_input")
    # st.session_state["user_name"] = st.text_input("Enter your full name to continue:", key="name_input")
    # st.session_state["user_name"] = user_name_input
    
    print(user_name_input)
    if user_name_input:  
        print("here1")
        print(user_name_input)
        st.session_state["user_name"] = user_name_input
        print(st.session_state['user_name'])
        if st.session_state["user_name"]:
            print("here")
            print(st.session_state['user_name'])
            user_file = os.path.join(chat_directory, f"{st.session_state['user_name']}.json")
            
            # --- Load previous chat if it exists ---
            if os.path.exists(user_file):
                with open(user_file, "r") as file:
                    st.session_state["messages"] = json.load(file)
                    main()
            else : 
                main()

else:
    main()