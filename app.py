
import os
import time
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from PIL import Image
from pypdf import PdfReader
from google import genai


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Multimodal AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ Gemini API key is missing.")
    st.info(
        "Create a .env file in the same folder as app.py "
        "and add:\n\n"
        "GEMINI_API_KEY=YOUR_API_KEY"
    )
    st.stop()


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=API_KEY
)

MODEL_NAME = "gemini-3.8-flash"


# =========================================================
# SESSION STATE
# =========================================================

if "file_content" not in st.session_state:
    st.session_state.file_content = ""

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None


# =========================================================
# GEMINI REQUEST WITH ERROR HANDLING
# =========================================================

def generate_answer(contents):

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents
            )

            return response, None

        except Exception as error:

            error_text = str(error)

            # ---------------------------------------------
            # 429 - QUOTA EXCEEDED
            # ---------------------------------------------

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                return None, (
                    "QUOTA"
                )

            # ---------------------------------------------
            # 503 - SERVER BUSY
            # ---------------------------------------------

            elif "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < max_retries - 1:

                    wait_time = 5 * (attempt + 1)

                    time.sleep(wait_time)

                    continue

                return None, (
                    "BUSY"
                )

            # ---------------------------------------------
            # OTHER ERROR
            # ---------------------------------------------

            else:

                return None, (
                    "OTHER",
                    error_text
                )

    return None, "BUSY"


# =========================================================
# TITLE
# =========================================================

st.title("🎓 Multimodal AI Study Assistant")

st.write(
    "Upload your study material and ask questions about it."
)

st.caption(
    "📄 PDF  •  🖼️ Image  •  📝 TXT  •  📊 CSV"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Study Assistant")

    st.write("### Supported Files")

    st.write("📄 PDF")
    st.write("🖼️ JPG / JPEG / PNG")
    st.write("📝 TXT")
    st.write("📊 CSV")

    st.divider()

    st.write("### 🤖 AI Model")

    st.write(MODEL_NAME)

    st.divider()

    if st.button(
        "🗑️ Clear Everything",
        use_container_width=True
    ):

        st.session_state.file_content = ""
        st.session_state.file_name = ""
        st.session_state.uploaded_image = None

        st.rerun()


# =========================================================
# FILE UPLOAD
# =========================================================

st.subheader("📂 Upload Study Material")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "txt",
        "csv"
    ]
)


# =========================================================
# PROCESS UPLOADED FILE
# =========================================================

if uploaded_file is not None:

    file_name = uploaded_file.name

    file_extension = (
        file_name.lower().split(".")[-1]
    )

    st.session_state.file_name = file_name


    # =====================================================
    # PDF
    # =====================================================

    if file_extension == "pdf":

        try:

            reader = PdfReader(
                uploaded_file
            )

            extracted_text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    extracted_text += (
                        page_text + "\n"
                    )

            if extracted_text.strip():

                st.session_state.file_content = (
                    extracted_text
                )

                st.session_state.uploaded_image = None

                st.success(
                    f"✅ PDF loaded successfully: {file_name}"
                )

                st.info(
                    f"📄 Number of pages: "
                    f"{len(reader.pages)}"
                )

            else:

                st.warning(
                    "⚠️ No selectable text was found "
                    "in this PDF."
                )

        except Exception as error:

            st.error(
                "❌ Unable to read the PDF."
            )

            st.caption(
                str(error)
            )


    # =====================================================
    # IMAGE
    # =====================================================

    elif file_extension in [
        "png",
        "jpg",
        "jpeg"
    ]:

        try:

            image = Image.open(
                uploaded_file
            )

            st.session_state.uploaded_image = image

            st.session_state.file_content = ""

            st.success(
                f"✅ Image loaded successfully: "
                f"{file_name}"
            )

            st.image(
                image,
                caption=file_name,
                width=500
            )

        except Exception as error:

            st.error(
                "❌ Unable to read the image."
            )

            st.caption(
                str(error)
            )


    # =====================================================
    # TXT
    # =====================================================

    elif file_extension == "txt":

        try:

            text = uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

            st.session_state.file_content = text

            st.session_state.uploaded_image = None

            st.success(
                f"✅ Text file loaded successfully: "
                f"{file_name}"
            )

        except Exception as error:

            st.error(
                "❌ Unable to read the TXT file."
            )

            st.caption(
                str(error)
            )


    # =====================================================
    # CSV
    # =====================================================

    elif file_extension == "csv":

        try:

            dataframe = pd.read_csv(
                uploaded_file
            )

            st.session_state.file_content = (
                dataframe.to_string(
                    index=False
                )
            )

            st.session_state.uploaded_image = None

            st.success(
                f"✅ CSV loaded successfully: "
                f"{file_name}"
            )

            st.dataframe(
                dataframe,
                use_container_width=True
            )

        except Exception as error:

            st.error(
                "❌ Unable to read the CSV file."
            )

            st.caption(
                str(error)
            )


# =========================================================
# FILE INFORMATION
# =========================================================

if st.session_state.file_name:

    st.divider()

    st.subheader("📌 Uploaded File")

    st.write(
        f"**File:** {st.session_state.file_name}"
    )


# =========================================================
# QUESTION
# =========================================================

st.divider()

st.subheader("💬 Ask Your Question")

question = st.text_area(
    "Enter your question",
    placeholder=(
        "Example:\n"
        "What is the main topic of this document?\n\n"
        "Explain this topic in simple words."
    ),
    height=120
)


# =========================================================
# GET ANSWER
# =========================================================

if st.button(
    "🤖 Get Answer",
    type="primary",
    use_container_width=True
):

    # -----------------------------------------------------
    # CHECK QUESTION
    # -----------------------------------------------------

    if not question.strip():

        st.warning(
            "⚠️ Please enter a question."
        )

        st.stop()


    # -----------------------------------------------------
    # CHECK FILE
    # -----------------------------------------------------

    if (
        not st.session_state.file_content
        and st.session_state.uploaded_image is None
    ):

        st.warning(
            "⚠️ Please upload a file first."
        )

        st.stop()


    # =====================================================
    # AI INSTRUCTIONS
    # =====================================================

    instructions = """
You are a helpful Multimodal AI Study Assistant.

Help the student understand their uploaded study material.

Rules:

1. Give clear and correct answers.
2. Use simple student-friendly English.
3. Use information from the uploaded material.
4. Do not invent information.
5. If the answer is not available in the uploaded material,
   clearly say that it is not available in the uploaded material.
6. Use bullet points when useful.
7. Explain difficult concepts step-by-step.
8. Keep the answer easy to understand.
"""


    # =====================================================
    # IMAGE
    # =====================================================

    if st.session_state.uploaded_image is not None:

        prompt = f"""
{instructions}

Student Question:
{question}
"""

        with st.spinner(
            "🤖 Analyzing the image..."
        ):

            response, error_type = generate_answer(
                [
                    prompt,
                    st.session_state.uploaded_image
                ]
            )


    # =====================================================
    # PDF / TXT / CSV
    # =====================================================

    else:

        prompt = f"""
{instructions}

Uploaded Study Material:
--------------------------------

{st.session_state.file_content}

--------------------------------

Student Question:
{question}
"""

        with st.spinner(
            "🤖 Generating answer..."
        ):

            response, error_type = generate_answer(
                prompt
            )


    # =====================================================
    # HANDLE RESPONSE
    # =====================================================

    if response is not None:

        if response.text:

            st.subheader("📚 Answer")

            st.write(
                response.text
            )

        else:

            st.warning(
                "⚠️ Gemini returned an empty answer. "
                "Please try again."
            )


    # =====================================================
    # HANDLE 429
    # =====================================================

    elif error_type == "QUOTA":

        st.error(
            "⏳ Gemini API quota exceeded."
        )

        st.info(
            "You have reached your current API "
            "request limit. Please wait until your "
            "quota resets or check your Gemini API "
            "usage and billing settings."
        )

        st.markdown(
            "👉 Check your Gemini API quota: "
            "https://ai.google.dev/gemini-api/docs/rate-limits"
        )


    # =====================================================
    # HANDLE 503
    # =====================================================

    elif error_type == "BUSY":

        st.warning(
            "🔄 Gemini is temporarily busy."
        )

        st.info(
            "The app automatically retried the request. "
            "Please wait a little and click "
            "'Get Answer' again."
        )


    # =====================================================
    # HANDLE OTHER ERRORS
    # =====================================================

    elif error_type is not None:

        st.error(
            "❌ Something went wrong while "
            "communicating with Gemini."
        )

        if isinstance(error_type, tuple):

            st.caption(
                error_type[1]
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎓 Multimodal AI Study Assistant | "
    "Streamlit + Gemini AI"
)