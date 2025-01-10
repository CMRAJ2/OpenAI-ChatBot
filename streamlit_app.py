import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("Gemini Chatbot")

gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:
    # Configure Gemini client.
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the Gemini API.
        try:
            response = model.generate_content(prompt)
            result = response.text
            print(result)

            # Display the response and store it in session state.
            with st.chat_message("assistant"):
                st.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
        except Exception as e:
            st.error(f"An error occurred: {e}")
