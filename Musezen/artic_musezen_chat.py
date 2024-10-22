import streamlit as st
import time
import numpy as np
import os
from musezen.generative_components.agent import ChatAgent
from musezen.generative_components.llm_client_openai import OpenAIClient
from musezen.generative_components.tool_artsy import (
    SearchGene,
    SearchArtist,
    FetchAPILinks,
)
from musezen.cv_components.musezen_cv_foundation import musezen_cv

# Local environment
# import dotenv

# dotenv.load_dotenv()

#############
# Constants #
#############
PROVIDERS = {
    "OpenAI": {
        "GPT-4o-mini": "gpt-4o-mini",
        "GPT-4o": "gpt-4o",
    }
}
# Keys to persist certain objects in session state
CHAT_DISPLAY_KEY = "chat_display"
MUSEZEN_AGENT_KEY = "musezen_agent"
CV_MODEL_KEY = "cv_model"
PAINTING_CLASS_KEY = "painting_class"
CONTEXT_ADDED_KEY = "context_added"

WELCOME_MESSAGE = (
    "Hi! I'm Musezen, your personal art curator. What are we looking for today?"
)


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
            with st.chat_message(role):
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
    st.sidebar.write(f"You uploaded a painting in **{painting_style}**")
    st.session_state[PAINTING_CLASS_KEY] = painting_style


st.sidebar.header("Settings")
provider = st.sidebar.selectbox(
    "Select Provider",
    list(PROVIDERS.keys()),
    on_change=clear,
    help="Changing the provider will reinitialize the agent.",
)
model = PROVIDERS[provider][
    st.sidebar.selectbox("Select Model", list(PROVIDERS[provider].keys()))
]
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
    # Initialized the LLM Client
    if provider == "OpenAI":
        llm = OpenAIClient(
            api_key=os.environ.get("OPENAI_API_KEY"),
            helicone_api_key=os.environ.get("HELICONE_API_KEY"),
        )
    # Initialize the agent
    st.session_state[MUSEZEN_AGENT_KEY] = ChatAgent(
        llm_client=llm,
        chat_history=[
            {
                "role": "system",
                "content": "You are an art curator. You are helping a user discover more about artworks, artists, or the venues. Write in well-formatted markdowns for streamlit and provide images where necessary.",
            },
            {"role": "assistant", "content": WELCOME_MESSAGE},
        ],
        tools=[SearchGene, SearchArtist, FetchAPILinks],
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
st.title("🎨 Musezen - Your Personal Art Curator")
st.write(
    """
Musezen is your personal art curator. Chat with Musezen to discover more about artworks, artists, or the venues. Right now, Musezen is in the beta phase and can help you with the following tasks:
- Search for genes, whereas a 'gene' refers to a distinctive characteristic or attribute that defines an art object (e.g. 'Pop Art', 'Impressionism', 'Bright Colors'), as defined by [the Art Genome Project at Artsy](https://www.artsy.net/categories)
- Search for specific artists, where as an artist is generally one person, but can also be two people collaborating, a collective of people, or even a mysterious entity such as "Banksy".
- Answer simple follow-up questions about your queries, like give me some art works by this artist, or show me some art with this gene.

To get started, select a provider and a model from the sidebar and start chatting with Musezen (Anthropic function calling not supported yet)!
         
**Please note that the responses are generated by AI models and may not always be accurate.**
"""
)
display_messages()

# Chat with agent
if prompt := st.chat_input("Type here"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Update chat display
    st.session_state[CHAT_DISPLAY_KEY].append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # Thought process
        with st.status("Typing...", expanded=False) as status:
            agent: ChatAgent = st.session_state[MUSEZEN_AGENT_KEY]

            # Add image context to user prompt if image is uploaded and context has not been uploaded
            # in previous user messages
            if uploaded_painting is not None and not st.session_state[CONTEXT_ADDED_KEY]:
                prompt = (
                    f"Context: the user uploaded image with the style of {st.session_state[PAINTING_CLASS_KEY]}\nAnd Here is the user prompt:\n"
                    + prompt
                )
                # Set the flag to true
                st.session_state[CONTEXT_ADDED_KEY] = True

            # Get response from the agent
            response = agent.invoke(input_message=prompt, model=model)
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

# st._bottom.write('# ')