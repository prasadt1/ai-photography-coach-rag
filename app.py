import streamlit as st
import ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="AI Photography Coach",
    layout="wide",
    initial_sidebar_state="expanded"
)


# IMPROVED CSS - Dark theme, proper formatting
st.markdown("""
    <style>
    body, p, span, label, div {
        font-size: 18px !important;
    }
    h1 { font-size: 2.5em !important; }
    h2 { font-size: 1.8em !important; }
    h3 { font-size: 1.4em !important; }
    .stButton > button { font-size: 18px !important; }
    .stTextInput > div > div > input { font-size: 18px !important; }
    .stTextArea > div > div > textarea { font-size: 18px !important; }
    
    .response-card {
        background-color: #0f0f0f;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #88ab75;
        font-size: 17px;
        line-height: 1.8;
        color: #ffffff;
        margin: 16px 0;
    }
    
    .shotlist-card {
        background-color: #0f0f0f;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #6b5b95;
        font-size: 17px;
        line-height: 1.8;
        color: #ffffff;
        margin: 16px 0;
    }
    
    .source-box {
        background-color: #1a1a1a;
        padding: 12px;
        border-radius: 6px;
        border-left: 3px solid #88ab75;
        margin: 10px 0;
        font-size: 16px;
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# SESSION STATE
# ============================================================================

if 'question' not in st.session_state:
    st.session_state.question = ""
if 'theme' not in st.session_state:
    st.session_state.theme = ""


def set_question(q):
    st.session_state.question = q


def set_theme(t):
    st.session_state.theme = t


def clear_question():
    st.session_state.question = ""


def clear_theme():
    st.session_state.theme = ""


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

DB_PATH = "faiss_index"


def load_system():
    """Load the FAISS index and embeddings model."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local(
        DB_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever(search_kwargs={"k": 3})
    return retriever


if 'retriever' not in st.session_state:
    with st.spinner("🔄 Loading AI system..."):
        st.session_state.retriever = load_system()


retriever = st.session_state.retriever


# ============================================================================
# VALIDATION FUNCTION
# ============================================================================

def is_context_valid(context):
    """Check if retrieved context is valid (not corrupted, not empty)."""
    if not context or len(context) < 50:
        return False, "No relevant information found"
    
    corruption_score = context.count('/lf') + context.count('BD/') 
    if corruption_score > 5:
        return False, "Retrieved content appears corrupted (PDF quality issue)"
    
    return True, context


# ============================================================================
# RAG FUNCTION (LESSON 2)
# ============================================================================

def get_coach_response(question, retriever):
    """RAG pipeline with hallucination prevention via prompt engineering."""
    
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    is_valid, validation_msg = is_context_valid(context)
    if not is_valid:
        return f"❌ {validation_msg}. Try asking about exposure, lighting, composition, or focus.", retrieved_docs
    
    prompt_template = f"""Based on the context below, answer this question: {question}

Context:
{context}

Answer concisely:"""
    
    try:
        response = ollama.generate(
            model="tinyllama",
            prompt=prompt_template
        )
        
        if not response or 'response' not in response:
            return "⚠️ Error: No response from model. Make sure Ollama is running: `ollama serve`", retrieved_docs
        
        answer = response['response'].strip()
        
        if not answer or len(answer) < 10:
            return "⚠️ Error: Model returned empty response. Restart Ollama and try again.", retrieved_docs
        
        return answer, retrieved_docs
        
    except Exception as e:
        return f"⚠️ Error: {str(e)}. Make sure Ollama is running with: `ollama serve`", retrieved_docs


# ============================================================================
# CHAIN-OF-THOUGHT FUNCTION (LESSON 4)
# ============================================================================

def get_shot_list(theme):
    """Chain-of-Thought reasoning for creative shot lists (Lesson 4)."""
    
    prompt_template = f"""You are a creative photography director.
Generate a detailed 6-step creative shot list for a photographer.

Let's think through this step-by-step:

1. **Mood & Tone:** What is the emotional atmosphere?
2. **Shot 1 (Wide/Establishing):** What establishes the scene?
3. **Shot 2 (Medium/Action):** What shows the main subject?
4. **Shot 3 (Close-up/Detail):** What intimate detail matters?
5. **Shot 4 (Creative/Angle):** What unconventional perspective?
6. **Shot 5 (Hero/Final):** What's the ultimate winning shot?

For EACH shot include: Composition technique, Lighting approach, One technical tip.

Theme: "{theme}"

CREATIVE SHOT LIST:"""
    
    try:
        response = ollama.generate(
            model="tinyllama",
            prompt=prompt_template,
            options={"temperature": 0.7}
        )
        return response['response']
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 📸 AI Photography Coach")
    st.markdown("""
    Your AI-powered photography assistant that combines:
    
    **Two Powerful Tools:**
    - 💬 **Tab 1:** Ask photography questions and get expert answers powered by RAG
    - 🎬 **Tab 2:** Generate creative shot lists using Chain-of-Thought reasoning
    
    **Built With:**
    - Lesson 1: LLM Integration (Ollama + tinyllama)
    - Lesson 2: RAG Architecture (FAISS + LangChain)
    - Lesson 4: Chain-of-Thought Reasoning
    - Guardrails: Hallucination Prevention
    
    100% local. Fast. Efficient.
    """)


# ============================================================================
# MAIN TITLE
# ============================================================================

st.title("📸 AI Photography Coach")
st.caption("🎓 Built with RAG (Lesson 2) + Chain-of-Thought Reasoning (Lesson 4)")


tab1, tab2 = st.tabs(["💬 Ask Photography Questions (RAG)", "🎬 Creative Shot List (CoT)"])


# ============================================================================
# TAB 1: RAG Q&A
# ============================================================================

with tab1:
    st.markdown("## Ask Your Photography Questions")
    st.markdown("Get expert answers from a knowledge base using **Retrieval-Augmented Generation**")
    
    st.markdown("---")
    
    st.markdown("### Your Question")
    question = st.text_input(
        "Ask anything about photography:",
        value=st.session_state.question,
        placeholder="e.g., How do I shoot portraits with natural light?",
        help="Ask about exposure, composition, lighting, focus, white balance, etc.",
    )
    
    st.session_state.question = question
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        submit_button = st.button("🔍 Get Answer", type="primary", use_container_width=True, key="tab1_get_answer")
    
    with col2:
        st.button("🗑️ Clear", use_container_width=True, on_click=clear_question, key="tab1_clear")
    
    # Display answer
    if submit_button and question:
        with st.spinner("🤖 Searching knowledge base and generating answer..."):
            answer, sources = get_coach_response(question, retriever)
            
            if answer:
                st.markdown("---")
                st.markdown("### 📊 Answer")
                st.markdown(f'<div class="response-card">{answer}</div>', unsafe_allow_html=True)
                
                with st.expander("📚 Show Sources (RAG Retrieval)", expanded=False):
                    st.markdown("*These are the documents the AI used to generate the answer:*")
                    for i, doc in enumerate(sources, 1):
                        st.markdown(f"**Source {i}** — {doc.metadata.get('source', 'Unknown')}")
                        st.markdown(f'<div class="source-box">{doc.page_content[:300]}...</div>', unsafe_allow_html=True)
    
    elif submit_button:
        st.warning("⚠️ Please type a question first.")
    
    st.markdown("---")
    
    st.markdown("### 💡 Example Questions")
    st.markdown("*Click any question to populate the field above:*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("📐 Exposure Triangle", use_container_width=True, on_click=set_question, args=("What is the exposure triangle?",), key="q1")
        st.button("💡 Hard vs Soft Light", use_container_width=True, on_click=set_question, args=("What's the difference between hard and soft light?",), key="q2")
    
    with col2:
        st.button("🎞️ Rule of Thirds", use_container_width=True, on_click=set_question, args=("How do I use the rule of thirds?",), key="q3")
        st.button("🎯 Focus Techniques", use_container_width=True, on_click=set_question, args=("How do I improve my focus techniques?",), key="q4")


# ============================================================================
# TAB 2: CREATIVE SHOT LIST GENERATOR
# ============================================================================

with tab2:
    st.markdown("## Creative Shot List Generator")
    st.markdown("Get a detailed photography plan using **Chain-of-Thought Reasoning**")
    
    st.info("""
    💡 **How it works:** The AI breaks down your photography theme into a 6-step creative plan
    with composition, lighting, and technical tips for each shot.
    """)
    
    st.markdown("---")
    
    st.markdown("### Your Photography Theme")
    theme = st.text_area(
        "Describe your photography concept or mood:",
        value=st.session_state.theme,
        placeholder="""Examples:
- Moody portrait in autumn forest
- Golden hour beach lifestyle photoshoot
- Urban street photography at night
- Product photography for artisan coffee brand
- Fashion editorial in abandoned warehouse""",
        height=120,
        help="Be specific about mood, location, and style",
    )
    
    st.session_state.theme = theme
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        generate_button = st.button("🎬 Generate Shot List", type="primary", use_container_width=True, key="tab2_generate")
    
    with col2:
        st.button("🗑️ Clear", use_container_width=True, on_click=clear_theme, key="tab2_clear")
    
    # Generate shot list
    if generate_button and theme and len(theme) > 15:
        with st.spinner("🎨 Creating your creative shot list... (10-30 seconds with tinyllama)"):
            shot_list = get_shot_list(theme)
            
            if shot_list:
                st.markdown("---")
                st.markdown("### 🎬 Your Creative Shot List")
                st.markdown(f'<div class="shotlist-card">{shot_list}</div>', unsafe_allow_html=True)
                
                st.download_button(
                    label="📄 Download Shot List",
                    data=shot_list,
                    file_name="shot_list.txt",
                    mime="text/plain",
                    key="download_shotlist"
                )
    
    elif generate_button and theme and len(theme) <= 15:
        st.warning("⚠️ Please enter a detailed theme (at least 15 characters).")
    
    elif generate_button:
        st.warning("⚠️ Please enter a theme first.")
    
    st.markdown("---")
    
    st.markdown("### 🎨 Example Themes")
    st.markdown("*Click any theme to populate the field above:*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🌲 Autumn Forest", use_container_width=True, on_click=set_theme, args=("Moody portrait in autumn forest with golden hour light",), key="t1")
        st.button("🌃 Urban Night", use_container_width=True, on_click=set_theme, args=("Urban street photography in Tokyo at night",), key="t2")
        st.button("🏚️ Fashion Editorial", use_container_width=True, on_click=set_theme, args=("Fashion editorial in abandoned warehouse",), key="t3")
    
    with col2:
        st.button("🏖️ Beach Photoshoot", use_container_width=True, on_click=set_theme, args=("Golden hour beach lifestyle shoot with family",), key="t4")
        st.button("☕ Product Photography", use_container_width=True, on_click=set_theme, args=("Product photography for artisan coffee brand",), key="t5")


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 16px; margin-top: 20px;">
📸 AI Photography Coach | Built for AI Engineering Capstone<br>
Demonstrates: LLM Integration • RAG Architecture • Chain-of-Thought • Hallucination Prevention<br>
<strong>Powered by tinyllama (637MB - lightning fast)</strong>
</div>
""", unsafe_allow_html=True)