import streamlit as st

# Optional tkinter support
try:
    from tkinter import Tk, filedialog
    TKINTER_AVAILABLE = True
except Exception:
    TKINTER_AVAILABLE = False

from main import process

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Test Case Categorizer",
    page_icon="📊",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
}

.big-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    color: #1f2937;
    margin-bottom: 0.3rem;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 18px;
    margin-bottom: 2rem;
}

.card {
    background: white;
    padding: 2rem;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.folder-box {
    background: #f3f4f6;
    padding: 1rem;
    border-radius: 12px;
    color: #111827;
    font-size: 15px;
    margin-top: 1rem;
    margin-bottom: 1rem;
    word-break: break-all;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3.2rem;
    border: none;
    font-size: 16px;
    font-weight: 600;
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(37,99,235,0.25);
}

.success-box {
    background: #dcfce7;
    color: #166534;
    padding: 1rem;
    border-radius: 12px;
    margin-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------

if "folder_path" not in st.session_state:
    st.session_state.folder_path = ""

if "output_file" not in st.session_state:
    st.session_state.output_file = ""

# ---------------- FUNCTIONS ----------------

def select_folder():

    if not TKINTER_AVAILABLE:
        return None

    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    folder_selected = filedialog.askdirectory()

    root.destroy()

    return folder_selected

# ---------------- UI ----------------

st.markdown(
    '<div class="big-title">📊 Local LLM Based Test Case Categorizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle"><b>Categorize Your Test Cases</b> into <b>CRITICAL, High, Medium,</b> and Low categories, '
    '<br> by using a local LLM - <b>zero cost and even without an internet connection.</b></div>',
    unsafe_allow_html=True
)

# ---------------- PREREQUISITES ----------------

with st.expander("📌 Prerequisites Before Processing", expanded=False):

    st.info("""
    • Ensure Ollama is installed and it is running locally with the appropriate model(qwen2.5:7b) downloaded. 
    
    • Input folder should contain only `.xlsx` files exported from the test case folder in Azure DevOps, with columns named 'ID' and 'Steps'
    
    """)

st.markdown('<div class="card">', unsafe_allow_html=True)

# ---------------- SELECT FOLDER BUTTON ----------------

if TKINTER_AVAILABLE:

    if st.button("📁 Select Folder"):

        selected_folder = select_folder()

        if selected_folder:

            st.session_state.folder_path = selected_folder

# ---------------- TEXTBOX ----------------

folder_input = st.text_input(
    "📂 Folder Path (Paste folder path having test cases directly alternatively)",
    value=st.session_state.folder_path,
    placeholder="/data or C:/test-cases"
)

# Keep session state updated with textbox value
st.session_state.folder_path = folder_input

# ---------------- SHOW SELECTED FOLDER ----------------



# ---------------- PROCESS BUTTON ----------------

# Show button ONLY when textbox has value
if st.session_state.folder_path.strip():

    if st.button("⚡ Categorize Test Cases"):

        with st.spinner("Categorizing test cases..."):

            output_file = process(
                st.session_state.folder_path
            )

            st.session_state.output_file = output_file

# ---------------- SUCCESS MESSAGE ----------------

if st.session_state.output_file:

    st.markdown(
        f'''
        <div class="success-box">
        ✅ Categorization completed successfully.<br><br>
        Output File:<br>
        <strong>{st.session_state.output_file}</strong>
        </div>
        ''',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)