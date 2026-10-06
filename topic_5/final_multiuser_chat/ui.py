"""Streamlit interface for the multi-user chat application.

Run from this directory with:
    streamlit run ui.py
"""

from __future__ import annotations

import uuid
from typing import Any

import streamlit as st

from main import create_user, chat


st.set_page_config(page_title="Multi-User Persistent Chat", page_icon="💬", layout="wide")


def initialise_state() -> None:
    """Create the browser-session stores used to drive sidebar navigation.

    These values are UI state. The backend separately persists LangGraph
    messages using each chat's ``thread_id``.
    """
    st.session_state.setdefault("users", {})
    st.session_state.setdefault("selected_user", None)
    st.session_state.setdefault("selected_chat", None)

    users = st.session_state.users
    if users and st.session_state.selected_user not in users:
        st.session_state.selected_user = next(iter(users))


def add_user(name: str) -> None:
    """Register a user locally and initialise that user's memory collection."""
    name = name.strip()
    if not name:
        st.warning("Please enter a user name.")
        return

    if name in st.session_state.users:
        st.warning("That user already exists.")
        return

    # Creating the vector collection is optional for rendering the UI.  If the
    # backend has not been configured yet, users can still organise their chats.
    try:

        create_user(name)
    except Exception:
        raise

    st.session_state.users[name] = {"chats": {}}
    st.session_state.selected_user = name
    st.session_state.selected_chat = None
    st.rerun()


def add_chat() -> None:
    """Open the default, empty conversation for the active user."""
    st.session_state.selected_chat = None
    st.rerun()


def chat_name_from_first_message(message: str, chats: dict[str, Any]) -> str:
    """Make a short, unique saved-chat name from its first message."""
    base_name = " ".join(message.split())[:45].rstrip() or "New chat"
    if base_name not in chats:
        return base_name

    suffix = 2
    while f"{base_name} ({suffix})" in chats:
        suffix += 1
    return f"{base_name} ({suffix})"


@st.dialog("Create a new user")
def new_user_dialog() -> None:
    """Show the small form used to create a user from the sidebar."""
    name = st.text_input("User name", key="new_user_name")
    if st.button("Create user", type="primary"):
        add_user(name)


def chat_front(message: str, thread_id: str, user: str) -> str:
    """Send a message to the backend for the active user and chat thread."""
    try:

        response: Any = chat(message, thread_id, user)
        return str(response)
    except Exception as error:
        raise


initialise_state()

with st.sidebar:
    st.title("💬 Personal Chat")

    if st.button("＋ New user", use_container_width=True):
        new_user_dialog()

    user_names = list(st.session_state.users)
    if user_names:
        selected_index = (
            user_names.index(st.session_state.selected_user)
            if st.session_state.selected_user in user_names
            else 0
        )
        chosen_user = st.selectbox("Choose a user", user_names, index=selected_index)
        if chosen_user != st.session_state.selected_user:
            st.session_state.selected_user = chosen_user
            st.session_state.selected_chat = None
            st.rerun()

        st.divider()
        if st.button("＋ New chat", use_container_width=True):
            add_chat()

        chats = st.session_state.users[st.session_state.selected_user]["chats"]
        if chats:
            st.caption("CHATS")
            for chat_name in chats:
                active = chat_name == st.session_state.selected_chat
                if st.button(
                    chat_name,
                    key=f"open-{chat_name}",
                    use_container_width=True,
                    type="primary" if active else "secondary",
                ):
                    st.session_state.selected_chat = chat_name
                    st.rerun()
        else:
            st.caption("No chats yet.")

        st.divider()
        st.caption(f"Signed in as: **{st.session_state.selected_user}**")


user = st.session_state.selected_user
chat_name = st.session_state.selected_chat

if not user:
    st.title("Welcome to Personal Chat")
    st.write("Create a user from the sidebar, then create a chat to begin.")
elif not chat_name:
    st.title("Personal Chat")
    st.caption(f"Start a new conversation as {user}.")

    if prompt := st.chat_input("Message a new chat"):
        # A thread is created only for the first submitted message. The chat is
        # then saved in the sidebar after its first complete exchange.
        thread_id = str(uuid.uuid4())
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = chat_front(prompt, thread_id, user)
            st.markdown(answer)

        chats = st.session_state.users[user]["chats"]
        saved_name = chat_name_from_first_message(prompt, chats)
        chats[saved_name] = {
            "thread_id": thread_id,
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": answer},
            ],
        }
        # Rerun so the just-created chat is rendered as a normal saved chat.
        st.session_state.selected_chat = saved_name
        st.rerun()
else:
    chat_data = st.session_state.users[user]["chats"][chat_name]
    title_column, delete_column = st.columns([8, 1])
    with title_column:
        st.title(chat_name)
    with delete_column:
        if st.button("🗑️", help="Delete this chat", key="delete-chat"):
            del st.session_state.users[user]["chats"][chat_name]
            st.session_state.selected_chat = None
            st.rerun()

    for item in chat_data["messages"]:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    if prompt := st.chat_input("Message this chat"):
        # Reusing the saved thread ID lets LangGraph restore this chat's history.
        chat_data["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = chat_front(prompt, chat_data["thread_id"], user)
            st.markdown(answer)

        chat_data["messages"].append({"role": "assistant", "content": answer})
