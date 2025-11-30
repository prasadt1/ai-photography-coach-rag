# 📸 AI Photography Coach

A **Retrieval-Augmented Generation (RAG)** powered AI assistant for photography education. Built with Streamlit, LangChain, FAISS, and tinyllama - 100% local, no API costs.

## 🎯 Problem

Learning photography is overwhelming with technical jargon and contradictory advice. Generic AI models often hallucinate facts, making them unreliable for technical learning.

## 💡 Solution

A two-mode intelligent system combining RAG and Chain-of-Thought reasoning:

- **📚 RAG Mode:** Ask photography questions and get verified answers with source attribution
- **🎬 Creative Mode:** Generate 6-step creative shot lists using step-by-step reasoning

## ✨ Features

✅ **RAG-Powered Q&A** - Answers grounded in verified knowledge base  
✅ **Chain-of-Thought Reasoning** - Creative shot lists with detailed plans  
✅ **Hallucination Prevention** - Prompt engineering + low temperature  
✅ **Source Attribution** - See which documents support each answer  
✅ **100% Local** - No API costs, full privacy with tinyllama  
✅ **Fast Response** - Optimized for MacBook Air (M1/M2)  

## 🏗️ Architecture

```
User Query
    ↓
Streamlit UI
    ↓
Query Embedding (HuggingFace all-MiniLM-L6-v2)
    ↓
FAISS Vector Search (retrieve top-3 documents)
    ↓
Prompt Engineering (system instructions + context + question)
    ↓
tinyllama LLM (temperature: 0.1 for RAG, 0.7 for CoT)
    ↓
Verified Answer + Sources (for RAG mode)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Ollama installed
- ~3GB disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/[your-username]/ai-photography-coach-rag.git
cd ai-photography-coach-rag

# Create environment
conda create -n photo-coach python=3.11
conda activate photo-coach

# Install dependencies
pip install streamlit ollama langchain-community faiss-cpu sentence-transformers

# Pull the model
ollama pull tinyllama

# Add your photography PDFs to data/ folder
mkdir data
# Place your photography PDFs here

# Build vector store
python ingest.py

# Run the app
streamlit run app.py
```

Visit `http://localhost:8501`

## 📚 Usage

### Tab 1: Ask Photography Questions
- Ask questions about exposure, lighting, composition, focus, etc.
- Get answers retrieved from your knowledge base
- See source documents that support each answer
- Perfect for learning photography fundamentals

### Tab 2: Generate Creative Shot Lists
- Describe your photography theme or mood
- Get a detailed 6-step shot plan
- Includes composition techniques, lighting approaches, technical tips
- Great for planning shoots or learning creative thinking

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| LLM | tinyllama (637MB) |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Vector DB | FAISS |
| Framework | LangChain |
| Deployment | Local (no cloud needed) |

## 📊 Performance

- **Load time:** 3-5 seconds
- **RAG query:** 15-30 seconds
- **CoT query:** 20-60 seconds
- **Model size:** 637MB
- **Memory:** ~2GB

## 🎓 Lessons Demonstrated

- **Lesson 1:** LLM Integration (Ollama)
- **Lesson 2:** RAG Architecture (FAISS + LangChain)
- **Lesson 4:** Chain-of-Thought Reasoning
- **Guardrails:** Hallucination Prevention via prompt engineering

## 📁 Project Structure

```
ai-photography-coach-rag/
├── app.py              # Main Streamlit application
├── ingest.py          # Document ingestion & vectorization
├── data/              # Your photography PDFs
├── faiss_index/       # Vector store (auto-generated)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🔄 Workflow

1. **Document Ingestion:** PDFs are loaded, chunked, and embedded
2. **Query Processing:** User question is embedded using same model
3. **Retrieval:** FAISS finds top-3 most relevant document chunks
4. **Augmentation:** Context is combined with prompt instructions
5. **Generation:** tinyllama generates answer grounded in context
6. **Presentation:** Answer with sources shown to user

## 🎯 Key Takeaways

- RAG significantly reduces hallucinations vs pure LLMs
- Prompt engineering is critical for model behavior
- Local LLMs are practical and cost-effective
- Small models with good prompts > large models without guardrails
- Vector search enables semantic understanding

## 🚀 Future Enhancements

- Multi-modal support (image analysis)
- Fine-tuning on photography domain
- Cloud deployment (Colab/AWS)
- User feedback loop
- API endpoint

## 📝 How to Contribute

1. Add photography PDFs to `data/` folder
2. Run `python ingest.py` to rebuild vector store
3. Test the app
4. Submit improvements via GitHub

## 📄 License

MIT License - feel free to use this project for learning and experimentation.


## 🙏 Acknowledgments

- ByteByteAI for the excellent AI Engineering curriculum
- LangChain for RAG framework
- Ollama for accessible local LLMs
- FAISS for efficient vector search

---
## 🧩 Capstone: Agentic Gemini Version

This repository also contains a second implementation of the AI Photography Coach as part of the **Google AI Agents Intensive (Kaggle) capstone**.

That version lives in [`agents_capstone/`](agents_capstone/) and demonstrates:

- 🧠 **Gemini 2.5 Flash vision** for image‑aware composition and lighting analysis  
- 🎯 **EXIF‑aware coaching** (focal length, aperture, shutter speed, ISO)  
- 🤖 **Agentic architecture** (Vision agent + Chat coach + optional knowledge agent)  
- 💬 **Interactive Streamlit UI** for back‑and‑forth coaching on a single photo  

If you’re interested in the multi‑agent / Gemini version rather than the local RAG app, start here:

➡️ [`agents_capstone/README.md`](agents_capstone/README.md)

**Built for ByteByteAI AI Engineering Capstone - November 2025**  
**Demonstrates:** LLM Integration • RAG Architecture • Chain-of-Thought • Hallucination Prevention
