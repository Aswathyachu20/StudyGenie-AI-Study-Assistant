import streamlit as st
import requests
import uuid
import re

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StudyGenie",
    page_icon="📚",
    layout="centered"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.answer-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #555;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">📚 StudyGenie</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Smart Study Assistant</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your study material and ask questions, "
    "generate quizzes, flashcards, summaries, "
    "and personalized study plans."
)

# ============================================================
# LANGFLOW CONFIGURATION
# ============================================================

API_KEY = "YOUR_LANGFLOW_API_KEY"

BASE_URL = "http://localhost:7860"

FLOW_ID = "f4da18eb-4203-4e76-a144-58be021a02ba"

FILE_COMPONENT_ID = "File-yMnPg"

RUN_URL = f"{BASE_URL}/api/v1/run/{FLOW_ID}"

# ============================================================
# PDF UPLOAD
# ============================================================

st.markdown("### 📄 Upload Study Material")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

# ============================================================
# QUESTION INPUT
# ============================================================

st.markdown("### 💬 Ask StudyGenie")

question = st.text_area(
    "Enter your question",
    placeholder=(
        "Examples:\n"
        "• What are the main topics covered in this material?\n"
        "• Explain process scheduling\n"
        "• Generate 5 MCQs\n"
        "• Generate 5 flashcards\n"
        "• Create a 7-day study plan\n"
        "• Summarize the material"
    ),
    height=140
)

# ============================================================
# ASK BUTTON
# ============================================================

if st.button(
    "🚀 Ask StudyGenie",
    use_container_width=True
):

    # --------------------------------------------------------
    # CHECK QUESTION
    # --------------------------------------------------------

    if not question.strip():
        st.warning("⚠️ Please enter a question.")
        st.stop()

    # --------------------------------------------------------
    # CHECK PDF
    # --------------------------------------------------------

    if uploaded_file is None:
        st.warning("📄 Please upload a PDF study material first.")
        st.stop()

    headers = {
        "x-api-key": API_KEY
    }

    # ========================================================
    # STEP 1 — UPLOAD PDF TO LANGFLOW
    # ========================================================

    with st.spinner("📤 Uploading your PDF..."):

        try:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            upload_response = requests.post(
                f"{BASE_URL}/api/v2/files",
                headers=headers,
                files=files,
                timeout=120
            )

            upload_response.raise_for_status()

            upload_result = upload_response.json()

            file_path = upload_result["path"]

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ PDF upload timed out. Please try again."
            )
            st.stop()

        except requests.exceptions.ConnectionError:

            st.error(
                "🔌 Could not connect to Langflow.\n\n"
                "Make sure Langflow is running at "
                "http://localhost:7860"
            )
            st.stop()

        except requests.exceptions.HTTPError as e:

            st.error(
                f"❌ Langflow file upload failed:\n{e}"
            )
            st.stop()

        except (KeyError, TypeError):

            st.error(
                "❌ Langflow did not return a valid file path."
            )
            st.stop()

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ PDF upload failed:\n{e}"
            )
            st.stop()

    # ========================================================
    # STEP 2 — SEND PDF PATH TO EXISTING LANGFLOW FLOW
    # ========================================================

    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": question.strip(),
        "session_id": str(uuid.uuid4()),

        "tweaks": {
            FILE_COMPONENT_ID: {
                "path": [
                    file_path
                ]
            }
        }
    }

    # ========================================================
    # STEP 3 — RUN STUDYGENIE
    # ========================================================

    with st.spinner("🤖 StudyGenie is reading your material..."):

        try:

            response = requests.post(
                RUN_URL,
                json=payload,
                headers={
                    "x-api-key": API_KEY,
                    "Content-Type": "application/json"
                },
                timeout=180
            )

            response.raise_for_status()

            result = response.json()

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The request took too long. "
                "Please try again."
            )
            st.stop()

        except requests.exceptions.ConnectionError:

            st.error(
                "🔌 Could not connect to Langflow.\n\n"
                "Make sure Langflow is running at "
                "http://localhost:7860"
            )
            st.stop()

        except requests.exceptions.HTTPError as e:

            st.error(
                f"❌ Langflow returned an HTTP error:\n{e}"
            )
            st.stop()

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Request failed:\n{e}"
            )
            st.stop()

    # ========================================================
    # STEP 4 — EXTRACT AI RESPONSE
    # ========================================================

    try:

        answer = (
            result["outputs"][0]
            ["outputs"][0]
            ["results"]["message"]
            ["data"]["text"]
        )

    except (KeyError, IndexError, TypeError):

        st.error(
            "❌ Could not extract the AI response "
            "from Langflow."
        )

        st.json(result)
        st.stop()

    # ========================================================
    # STEP 5 — CLEAN AI RESPONSE
    # ========================================================

    # Remove [svg](...) artifacts
    answer = re.sub(
        r'\[\s*s\s*v\s*g\s*\]\s*'
        r'\(\s*http://localhost:8501/[^)]*\)',
        '',
        answer,
        flags=re.IGNORECASE
    )

    # Remove remaining [svg]
    answer = re.sub(
        r'\[\s*s\s*v\s*g\s*\]',
        '',
        answer,
        flags=re.IGNORECASE
    )

    # Remove localhost Streamlit links
    answer = re.sub(
        r'\(\s*http://localhost:8501/[^)]*\)',
        '',
        answer,
        flags=re.IGNORECASE
    )

    # Remove empty markdown links
    answer = re.sub(
        r'\[\s*\]\s*\([^)]*\)',
        '',
        answer
    )

    # Remove excessive blank lines
    answer = re.sub(
        r'\n\s*\n\s*\n+',
        '\n\n',
        answer
    )

    answer = answer.strip()

    # ========================================================
    # STEP 6 — DISPLAY ANSWER
    # ========================================================

    st.markdown("---")

    st.markdown("## 📖 StudyGenie Answer")

    st.markdown(
        '<div class="answer-box">',
        unsafe_allow_html=True
    )

    st.markdown(answer)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

