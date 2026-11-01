import os
import sys
import streamlit as st
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

# Add the project root directory explicitly to the Python path to eliminate runtime path issues
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.document_parser import parse_course_material
from utils.rag_engine import initialize_vector_store, seed_academic_glossary, retrieve_academic_context

# 1. Initialize environment parameters and IBM watsonx client endpoints
load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_APIKEY")
)

# Lock down operational generation constraints for the target environment
model_params = {
    "max_new_tokens": 1024,
    "min_new_tokens": 1,
    "temperature": 0.2
}

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params=model_params
)

# Mount local zero-binary Python RAG vectors indexing engine
db = initialize_vector_store()
seed_academic_glossary(db)

# 2. Premium UI Page Configuration
st.set_page_config(page_title="EduTranslate AI", page_icon="🌐", layout="centered")

# Custom UI inject to establish a professional, modern chat user experience
st.markdown("""
    <style>
    .main-header { font-size: 2.3rem; font-weight: 700; color: #1E293B; text-align: center; margin-bottom: 0.1rem; }
    .sub-header { font-size: 1rem; color: #64748B; text-align: center; margin-bottom: 2rem; }
    .chat-bubble-user { background-color: #F1F5F9; padding: 1rem; border-radius: 12px; margin-bottom: 1rem; color: #1E293B; }
    .chat-bubble-agent { background-color: #EEF2FF; padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #4F46E5; color: #1E293B; }
    div[data-testid="stExpander"] { border: 1px solid #E2E8F0; border-radius: 8px; background-color: #F8FAFC; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">EduTranslate AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-language Academic Course Translation Agent</div>', unsafe_allow_html=True)

# 3. Comprehensive Indian Language Array Mapping
languages = [
    "English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", 
    "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", 
    "Marathi", "Nepali", "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi", 
    "Tamil", "Telugu", "Urdu", "Haryanvi", "Rajasthani", "Bhojpuri"
]

if "source_lang" not in st.session_state: st.session_state.source_lang = "English"
if "target_lang" not in st.session_state: st.session_state.target_lang = "Hindi"
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# Language Navigation Matrix Bar Selection Row
lang_col1, lang_col_btn, lang_col2 = st.columns([4, 1, 4])
with lang_col1:
    st.session_state.source_lang = st.selectbox("From:", languages, index=languages.index(st.session_state.source_lang), label_visibility="collapsed")
with lang_col_btn:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("⇄", help="Swap languages"):
        st.session_state.source_lang, st.session_state.target_lang = st.session_state.target_lang, st.session_state.source_lang
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
with lang_col2:
    st.session_state.target_lang = st.selectbox("To:", languages, index=languages.index(st.session_state.target_lang), label_visibility="collapsed")

st.markdown("---")

# Render active chat history workspace stream
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user"><b>You:</b><br>{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-agent"><b>EduTranslate AI Agent:</b><br>{message["text"]}</div>', unsafe_allow_html=True)

# 4. Modern Bottom Attachment and Entry Console Bar Layout
st.markdown("---")
with st.expander("➕ Upload Course Assets (PDF / DOCX / PPTX)", expanded=True):
    # Verified visible layout parameters to support older local package engines cleanly
    uploaded_doc = st.file_uploader(
        "Select or drag academic course material here:", 
        type=["pdf", "docx", "pptx"], 
        label_visibility="visible"
    )

# Unified Chat Input box at the very bottom line console
chat_query = st.chat_input("Ask EduTranslate to translate text or process uploaded document...")

# 5. Core Execution Routing Pipeline Engine Logic
if chat_query or uploaded_doc is not None:
    input_text = ""
    source_origin = "text prompt"
    
    if uploaded_doc is not None:
        source_origin = f"Document ({uploaded_doc.name})"
        temp_path = f"temp_{uploaded_doc.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_doc.getbuffer())
        with st.spinner("Extracting comprehensive document text layers page-by-page..."):
            try:
                file_ext = uploaded_doc.name.split(".")[-1]
                input_text = parse_course_material(temp_path, file_ext)
            except Exception as ex:
                st.error(f"File extraction failure: {str(ex)}")
            finally:
                if os.path.exists(temp_path): 
                    os.remove(temp_path)
    else:
        input_text = chat_query

    if input_text.strip():
        # Append User action into state logger
        display_user_msg = f"[{source_origin}] {chat_query if chat_query else 'Process uploaded course document'}"
        st.session_state.chat_history.append({"role": "user", "text": display_user_msg})
        
        with st.spinner("Analyzing material matching boundaries via local RAG matrices..."):
            glossary_context = retrieve_academic_context(input_text, db)
            
            # CHUNKING LOGIC: Break long multi-page text strings into small pieces to prevent 50% translation truncations
            text_chunks = [input_text[i:i+1200] for i in range(0, len(input_text), 1200)]
            translated_chunks = []
            
            for idx, chunk in enumerate(text_chunks):
                with st.spinner(f"Processing translation matrix block {idx+1}/{len(text_chunks)}..."):
                    translation_prompt = (
                        f"System: You are an expert precise academic translator.\n"
                        f"Task: Automatically detect the source dialect and translate the following text chunk exactly into {st.session_state.target_lang}.\n"
                        f"Glossary alignment rules:\n{glossary_context}\n\n"
                        f"Constraint: Translate the content literally and completely. Do not summarize, compress, or add chat commentary. Return ONLY the translation.\n\n"
                        f"Content chunk:\n{chunk}\n\n"
                        f"{st.session_state.target_lang} Translation:"
                    )
                    try:
                        chunk_response = model.generate_text(prompt=translation_prompt)
                        translated_chunks.append(chunk_response.strip())
                    except Exception as err:
                        st.error(f"Chunk processing dropped: {str(err)}")
            
            final_compiled_output = "\n".join(translated_chunks)
            st.session_state.chat_history.append({"role": "agent", "text": final_compiled_output})
            st.rerun()
