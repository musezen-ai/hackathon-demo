import streamlit as st
import time
import numpy as np
import os
from musezen.generative_components.agent import ChatAgent
from musezen.generative_components.llm_client import ArcticClient
from musezen.cv_components.musezen_cv_foundation import musezen_cv


#############
# Constants #
#############
# Keys to persist certain objects in session state
CHAT_DISPLAY_KEY = "chat_display"
MUSEZEN_AGENT_KEY = "musezen_agent"
CV_MODEL_KEY = "cv_model"
PAINTING_CLASS_KEY = "painting_class"
CONTEXT_ADDED_KEY = "context_added"
ICONS = {"assistant": "🎨", "user": "🖌️"}

WELCOME_MESSAGE = "Hi! I'm Musezen, your personal art curator powered by Snowflake Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything!"


#############
# Functions #
#############
def display_messages():
    """
    This function displays chat messages with a fixed opener
    """
    # Display all messages in the chat history
    for message in st.session_state[CHAT_DISPLAY_KEY]:
        role = message["role"]
        content = message["content"]
        if role in ["user", "assistant"]:
            with st.chat_message(role, avatar=ICONS[role]):
                st.write(content)


def clear():
    """
    This function is called when the provider is changed
    """
    st.session_state[CHAT_DISPLAY_KEY] = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]
    st.session_state[MUSEZEN_AGENT_KEY] = None
    st.session_state[CV_MODEL_KEY] = musezen_cv()
    st.session_state[PAINTING_CLASS_KEY] = None
    st.session_state[CONTEXT_ADDED_KEY] = False


def on_file_change():
    """
    This function changes context added flag and allow a new context to be added to user prompt

    Example:
    upload file -> False
    - Add context to prompt -> True
    delete file -> False
    """
    st.session_state[CONTEXT_ADDED_KEY] = False


##############
# Page Setup #
##############
st.set_page_config(
    page_title="Musezen",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="auto",
)

### Sidebar ###
st.sidebar.header("Photo Upload")
# Receive painting pictures
uploaded_painting = st.sidebar.file_uploader("Upload photos here", type=["png", "jpg"])
# If there is a file and the context has not been added yet.
if uploaded_painting is not None and not st.session_state[CONTEXT_ADDED_KEY]:
    cv_model: musezen_cv = st.session_state[CV_MODEL_KEY]
    painting_style = cv_model.classify(uploaded_painting)
    st.sidebar.info(f"You uploaded a painting with **{painting_style}** style.")
    st.session_state[PAINTING_CLASS_KEY] = painting_style


# Create a clear history button
st.sidebar.button("Clear", on_click=clear)


#################
# Session State #
#################
# default chat display
if CHAT_DISPLAY_KEY not in st.session_state:
    st.session_state[CHAT_DISPLAY_KEY] = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

# If the agent is not initialized, initialize it, or if it is None (after changing the provider), reinitialize it
if (MUSEZEN_AGENT_KEY not in st.session_state) or (
    st.session_state[MUSEZEN_AGENT_KEY] is None
):
    llm = ArcticClient(api_key=os.environ.get("REPLICATE_API_TOKEN"))
    # Initialize the agent
    st.session_state[MUSEZEN_AGENT_KEY] = ChatAgent(
        llm_client=llm,
        chat_history=[
            {"role": "assistant", "content": WELCOME_MESSAGE},
        ],
    )

# Initialize variables to keep track of CV processes
if CV_MODEL_KEY not in st.session_state:
    st.session_state[CV_MODEL_KEY] = musezen_cv()
if PAINTING_CLASS_KEY not in st.session_state:
    st.session_state[PAINTING_CLASS_KEY] = None
if CONTEXT_ADDED_KEY not in st.session_state:
    st.session_state[CONTEXT_ADDED_KEY] = False


##############
# Main  Page #
##############
st.title("🎨 Musezen - Ar(c)tic Curator")
st.write(
"""
This is your personal art curator. Leverage the knowledge of the Snowflake Arctic model to chat about different art styles. To get started, upload
a photo of a painting for context, or start chatting directly about all things art (or non-art)!
"""
)
st.divider()
st.write("""
**Please note that the responses are generated by AI models and may not always be accurate.**
"""
)
display_messages()

# Chat with agent
if prompt := st.chat_input("Type here"):
    # Display user message
    with st.chat_message("user", avatar=ICONS["user"]):
        st.markdown(prompt)
    # Update chat display
    st.session_state[CHAT_DISPLAY_KEY].append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar=ICONS["assistant"]):
        # Thought process
        with st.status("Writing...", expanded=False) as status:
            agent: ChatAgent = st.session_state[MUSEZEN_AGENT_KEY]

            # Add image context to user prompt if image is uploaded and context has not been uploaded
            # in previous user messages
            if (
                uploaded_painting is not None
                and not st.session_state[CONTEXT_ADDED_KEY]
            ):
                prompt = (
                    f"Context: user uploaded painting has the style of {st.session_state[PAINTING_CLASS_KEY]}\nAnd here is the user prompt:\n"
                    + prompt
                )
                # Set the flag to true
                st.session_state[CONTEXT_ADDED_KEY] = True

            # Get response from the agent
            response = agent.invoke(
                input_message=prompt, model="snowflake/snowflake-arctic-instruct"
            )
            status.update(label="Finished!", state="complete", expanded=False)

        # Display response
        message_placeholder = st.empty()
        full_response = ""
        for item in response.split(" "):
            full_response += item + " "
            message_placeholder.markdown(full_response + " ▌")
            time.sleep(
                np.random.choice([0, 0, 1, 1, 2, 2, 3], 1)[0] / 100
            )  # For streaming effect
        message_placeholder.write(full_response)

        # Update chat display
        st.session_state[CHAT_DISPLAY_KEY].append(
            {"role": "assistant", "content": response}
        )
