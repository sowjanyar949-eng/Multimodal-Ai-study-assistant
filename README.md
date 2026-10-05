# Multimodal-Ai-study-assistant
it is a study planner using python and streamlit
🎓 Multimodal AI Study Assistant

A Multimodal AI Study Assistant is an AI-powered application that helps students understand their study materials.

The application allows users to upload PDFs, images, TXT files, and CSV files and ask questions about the uploaded content. The application uses Google Gemini AI to analyze the content and generate simple, student-friendly answers.

🚀 Features
📄 Upload PDF files
🖼️ Upload images
📝 Upload TXT files
📊 Upload CSV files
💬 Ask questions about uploaded content
🤖 AI-generated answers using Google Gemini
📚 Simple explanations for students
🔄 Automatic retry for temporary Gemini 503 errors
⏳ Friendly handling of Gemini 429 quota errors
🗑️ Clear uploaded files
🎨 Simple Streamlit interface
🧠 What is Multimodal AI?

Multimodal AI is an artificial intelligence system that can understand and work with different types of data such as:

Text
Images
Documents
Tables

In this project, the AI can process both text-based files and images and answer questions based on the uploaded study material.

🏗️ Project Architecture
                    ┌──────────────────────┐
                    │       Student        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Streamlit Web UI   │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
              PDF File      Image File    TXT/CSV
                 │             │             │
                 ▼             ▼             ▼
              pypdf           PIL          Pandas
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Google Gemini    │
                    │         AI           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      AI Answer       │
                    └──────────────────────┘
📁 Project Structure
multimodal-ai-study-assistant/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
Files
File	Description
app.py	Main Streamlit application
.env	Stores Gemini API key
requirements.txt	Python dependencies
README.md	Project documentation
🛠️ Technologies Used
Python

Python is used as the main programming language.

Streamlit

Streamlit is used to create the web interface.

Google Gemini AI

Gemini is used to understand uploaded content and generate answers.

PyPDF

PyPDF is used to extract text from PDF documents.

Pillow

Pillow is used to process images.

Pandas

Pandas is used to read and process CSV files.

python-dotenv

python-dotenv is used to load the Gemini API key from the .env file.

📦 Requirements

The project uses the following packages:

streamlit>=1.40,<2
python-dotenv>=1.0,<2
google-genai>=1.0,<2
pillow>=10,<13
pypdf>=5,<7
pandas>=2.2,<3
numpy>=1.26,<3
