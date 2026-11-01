# EduTranslate AI: Multi-language Course Content Agent

Fulfilling **Problem Statement No.17 – Multi-language Course Content Translator Agent** for the **IBM Build for Bharat (BOB) Playground**.

EduTranslate AI is a production-grade, context-aware academic translator powered by **IBM watsonx.ai** and **IBM Granite**. It automatically parses and translates academic course materials (including text inputs, full PDFs, Word documents, and PowerPoint slides) into regional Indian languages while preserving rigorous pedagogical context, complex technical syntax, and formatting structural layouts.

## Tech Stack & Architecture
- **Core LLM Engine:** `ibm/granite-4-h-small` model instance called programmatically via the official `ibm-watsonx-ai` Python SDK framework.
- **RAG Framework:** Zero-binary, pure-Python mathematical vector inference storage engine computing text cosine-similarities locally for stable deployment without OS-level `hnswlib` or `chromadb` compiler compilation errors.
- **Document Extractors:** Multi-format structured file parsing layout pipelines using `PyMuPDF` (`fitz`), `python-docx`, and `python-pptx`.
- **User Interface:** Modern, clean, unified chat application portal built using `Streamlit`.
- **Linguistic Processing:** Sequential 1,200-character string boundary window chunking logic to completely prevent text truncations and ensure 100% processing text coverage across multi-page articles.

## Supported Regional Languages
Instantly translate course frameworks across **25 Indian regional dialects**:
- Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu, Haryanvi, Rajasthani, and Bhojpuri.

## Local Installation & Execution

1. **Clone the repository workspace layout:**
   ```bash
   git clone https://github.com
   cd EduTranslate_AI
   ```

2. **Configure Environment Variables (`.env`):**
   Create a secure `.env` file in the root workspace folder containing your active IBM Cloud parameters:
   ```env
   WATSONX_APIKEY=your_private_ibm_cloud_iam_api_key
   WATSONX_PROJECT_ID=3daee2f5-bf9e-47f8-b66b-0031e9e58504
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   ```
   *(Note: The `.env` file is excluded from git tracking to preserve access control boundaries).*

3. **Activate the local environment and install core packages:**
   ```powershell
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Launch the interface web server portal:**
   ```bash
   streamlit run app.py
   ```

## Key Production Features Implemented
- **Unified Chat-Style Dashboard Layout:** Modern attachment tray wrapper system for intuitive, clean document loading flows.
- **Bi-Directional Contextual Language Swapping:** Dynamic navigation header interface logic allowing users to flip translation vectors instantly.
- **Autonomous RAG Terminology Seeding:** Automatically injects verified technical definitions into text prompts to uphold educational integrity and prevent translation drift.
