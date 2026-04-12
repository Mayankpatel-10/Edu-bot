import os
import textwrap
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import time
from datetime import datetime

# Load custom CSS
with open('styles.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Configure page
st.set_page_config(
    page_title="EduBot - Your Educational Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Configure OpenRouter API
API_KEY = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Sidebar with minimal controls
with st.sidebar:
    st.markdown('<div class="main-header"><h2>🌱 EduBot</h2></div>', unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = [
            {"role": "assistant", "content": "🌱 Hi there! I'm EduBot, your friendly educational assistant. How can I help you today?"}
        ]
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📚 About EduBot")
    st.markdown("""
    EduBot is your personal educational assistant powered by advanced AI. 
    I can help you with:
    - 📖 Homework questions
    - 🧮 Math problems
    - 🔬 Science concepts
    - 📚 Study tips
    - 🎯 Exam preparation
    """)

# Helper function to format Markdown (optional)
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>� EduBot</h1>
    <p>Your Personal Educational Assistant</p>
</div>
""", unsafe_allow_html=True)

# Quick action buttons with new styling
st.markdown("### 🚀 Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="math-btn">', unsafe_allow_html=True)
    if st.button("📚 Math Help", key="math", use_container_width=True):
        st.session_state.quick_prompt = "Can you help me with a math problem?"
    st.markdown('</div>', unsafe_allow_html=True)
        
with col2:
    st.markdown('<div class="science-btn">', unsafe_allow_html=True)
    if st.button("🔬 Science", key="science", use_container_width=True):
        st.session_state.quick_prompt = "Can you explain a science concept to me?"
    st.markdown('</div>', unsafe_allow_html=True)
        
with col3:
    st.markdown('<div class="literature-btn">', unsafe_allow_html=True)
    if st.button("📖 Literature", key="literature", use_container_width=True):
        st.session_state.quick_prompt = "Can you help me understand this literature text?"
    st.markdown('</div>', unsafe_allow_html=True)
        
with col4:
    st.markdown('<div class="study-btn">', unsafe_allow_html=True)
    if st.button("🎯 Study Tips", key="study", use_container_width=True):
        st.session_state.quick_prompt = "What are some effective study techniques?"
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "🌱 Hi there! I'm EduBot, your friendly educational assistant. I can help you with homework, explain concepts, and provide study tips. What would you like to learn about today?"}
    ]

if "quick_prompt" not in st.session_state:
    st.session_state["quick_prompt"] = ""

# Handle quick prompts
if st.session_state.quick_prompt:
    user_input = st.session_state.quick_prompt
    st.session_state.quick_prompt = ""
else:
    user_input = None

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages with enhanced styling
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🎓"):
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Function to get response from OpenRouter API
def get_openrouter_response(question):
    try:
        response = client.chat.completions.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "You are EduBot, a helpful educational assistant. Provide clear, educational responses that are easy to understand. Be encouraging and supportive. Use examples when helpful."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Sorry, I encountered an error: {str(e)}"

# Enhanced chat input with placeholder
if not user_input:
    user_input = st.chat_input(
        "💬 Ask me anything about your studies...",
        key="input"
    )

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="chat-message user-message">{user_input}</div>', unsafe_allow_html=True)
    
    # Show loading indicator
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("🤔 Thinking..."):
            # Get AI response
            response_text = get_openrouter_response(
                user_input
            )
            
        # Display response
        st.markdown(f'<div class="chat-message assistant-message">{response_text}</div>', unsafe_allow_html=True)
    
    # Add assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # Auto-scroll to bottom
    st.rerun()
