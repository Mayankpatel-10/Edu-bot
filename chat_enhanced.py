# Enhanced Q&A Chatbot with Modern UI

from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import os
import time
from datetime import datetime

load_dotenv()  # take environment variables from .env.

# Configure page
st.set_page_config(
    page_title="Student Assistant - Enhanced Chat",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
try:
    with open('styles.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    # Fallback CSS if file doesn't exist
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            border-left: 4px solid #667eea;
        }
    </style>
    """, unsafe_allow_html=True)

# Configure OpenRouter API
API_KEY = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Sidebar with settings
with st.sidebar:
    st.markdown('<div class="main-header"><h2>⚙️ Settings</h2></div>', unsafe_allow_html=True)
    
    # Model selection
    model_options = {
        "Claude 3 Haiku": "anthropic/claude-3-haiku",
        "Claude 3 Sonnet": "anthropic/claude-3-sonnet", 
        "Claude 3 Opus": "anthropic/claude-3-opus",
        "GPT-4": "openai/gpt-4",
        "GPT-4 Turbo": "openai/gpt-4-turbo",
        "Llama 3 70B": "meta-llama/llama-3-70b-instruct"
    }
    
    selected_model = st.selectbox(
        "🤖 Choose AI Model",
        list(model_options.keys()),
        index=0
    )
    
    # Temperature slider
    temperature = st.slider(
        "🌡️ Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make responses more creative, lower values more focused"
    )
    
    # Max tokens
    max_tokens = st.slider(
        "📝 Max Response Length",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100,
        help="Maximum number of tokens in the response"
    )
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", type="secondary"):
        if 'chat_history' in st.session_state:
            st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📚 Quick Tips")
    st.markdown("""
    - Be specific in your questions
    - Provide context when needed
    - Ask follow-up questions
    - Use examples for better explanations
    """)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎓 Student Assistant Chat</h1>
    <p>Get instant help with your studies</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Subject selection buttons
st.subheader("📖 Quick Subject Help")
col1, col2, col3, col4 = st.columns(4)

subject_prompts = {
    "🧮 Mathematics": "Can you help me solve this math problem step by step?",
    "🔬 Science": "Can you explain this science concept in simple terms?",
    "📚 English": "Can you help me analyze this literature text?",
    "🌍 History": "Can you explain this historical event and its significance?"
}

with col1:
    if st.button("🧮 Mathematics", use_container_width=True):
        st.session_state.quick_question = subject_prompts["🧮 Mathematics"]
        
with col2:
    if st.button("🔬 Science", use_container_width=True):
        st.session_state.quick_question = subject_prompts["🔬 Science"]
        
with col3:
    if st.button("📚 English", use_container_width=True):
        st.session_state.quick_question = subject_prompts["📚 English"]
        
with col4:
    if st.button("🌍 History", use_container_width=True):
        st.session_state.quick_question = subject_prompts["🌍 History"]

# Enhanced input section
st.markdown("### 💬 Ask Your Question")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

# Check for quick question
if 'quick_question' in st.session_state and st.session_state.quick_question:
    user_question = st.session_state.quick_question
    st.session_state.quick_question = ""
else:
    user_question = st.text_area(
        "Type your question here:",
        key="question_input",
        height=100,
        placeholder="e.g., Can you explain photosynthesis step by step?",
        help="Be as specific as possible for better answers"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Ask button with enhanced styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit = st.button("🚀 Get Answer", use_container_width=True, type="primary")

## Function to load OpenRouter model and get responses
def get_openrouter_response(question, model, temp, max_tok):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant. Provide clear, structured, and easy-to-understand answers. Use examples and break down complex concepts. Be encouraging and supportive."},
                {"role": "user", "content": question}
            ],
            max_tokens=max_tok,
            temperature=temp,
            stream=True
        )
        return response
    except Exception as e:
        return f"❌ Error: {str(e)}"

## Display chat history
if st.session_state.chat_history:
    st.markdown("### 📝 Conversation History")
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.expander(f"Q{i+1}: {question[:50]}...", expanded=False):
            st.markdown(f"**Question:** {question}")
            st.markdown(f"**Answer:** {answer}")

## If ask button is clicked
if submit and user_question:
    # Show loading spinner
    with st.spinner('🤔 Thinking...'):
        response = get_openrouter_response(user_question, model_options[selected_model], temperature, max_tokens)
        
        st.markdown("### 🎯 Answer")
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        
        if hasattr(response, '__iter__') and not isinstance(response, str):
            full_response = ""
            message_placeholder = st.empty()
            
            for chunk in response:
                if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Store in chat history
            st.session_state.chat_history.append((user_question, full_response))
        else:
            st.error(response)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons after response
        st.markdown("### 🔧 Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Copy Answer", key="copy"):
                st.success("Answer copied to clipboard!")
        
        with col2:
            if st.button("🔄 Ask Follow-up", key="followup"):
                st.session_state.quick_question = "Can you explain that in more detail?"
                st.rerun()
        
        with col3:
            if st.button("💾 Save for Later", key="save"):
                st.success("Answer saved!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🎓 Student Assistant - Your Learning Companion | Powered by OpenRouter</p>
    <p><small>Tip: The more specific your question, the better the answer!</small></p>
</div>
""", unsafe_allow_html=True)
