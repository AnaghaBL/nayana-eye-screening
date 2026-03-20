import json
import os
from datetime import datetime
import streamlit as st

MESSAGES_FILE = "messages.json"

def load_all_messages():
    if not os.path.exists(MESSAGES_FILE):
        return {}
    with open(MESSAGES_FILE, "r") as f:
        return json.load(f)

def save_all_messages(data):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_messages(case_id):
    data = load_all_messages()
    return data.get(case_id, [])

def send_message(case_id, sender_name, sender_role, text):
    data = load_all_messages()
    if case_id not in data:
        data[case_id] = []
    data[case_id].append({
        "sender_name": sender_name,
        "sender_role": sender_role,
        "text": text,
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p")
    })
    save_all_messages(data)

def render_chat(case_id, current_role, current_name):
    messages = load_messages(case_id)
    st.markdown("""
    <div style="font-family:'Space Grotesk',sans-serif;font-size:11px;
                font-weight:700;letter-spacing:2px;
                text-transform:uppercase;color:#818cf8;
                margin-bottom:12px;">
        Messages
    </div>
    """, unsafe_allow_html=True)

    if not messages:
        st.caption("No messages yet — start the conversation below.")
    else:
        for msg in messages:
            is_me = msg['sender_role'] == current_role
            align = "flex-end" if is_me else "flex-start"
            bg    = "rgba(99,102,241,0.15)" if is_me else "rgba(255,255,255,0.06)"
            border= "rgba(99,102,241,0.4)" if is_me else "rgba(255,255,255,0.12)"
            name_color = "#a5b4fc" if is_me else "#94a3b8"
            text_color = "#e2e8f0"
            st.markdown(f"""
            <div style="display:flex;justify-content:{align};margin-bottom:10px;">
                <div style="max-width:75%;background:{bg};
                            border:1px solid {border};
                            border-radius:16px;padding:12px 16px;">
                    <div style="font-size:11px;font-weight:700;
                                color:{name_color};margin-bottom:4px;">
                        {msg['sender_name']} ·
                        <span style="font-weight:400;color:#64748b;">
                            {msg['timestamp']}
                        </span>
                    </div>
                    <div style="font-size:14px;color:{text_color};line-height:1.5;">
                        {msg['text']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    key = f"chat_input_{case_id}_{current_role}"
    msg_text = st.text_input(
        "Type a message",
        placeholder="Write something...",
        key=key,
        label_visibility="collapsed"
    )
    if st.button("Send", key=f"send_{case_id}_{current_role}", type="primary"):
        if msg_text.strip():
            send_message(case_id, current_name, current_role, msg_text.strip())
            st.rerun()
        else:
            st.warning("Please type a message first")
