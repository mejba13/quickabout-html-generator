# QuickAbout - AI-Powered HTML Snippet Generator for Category "About" Sections
from dotenv import load_dotenv
import os
import openai
import streamlit as st

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------
# Base HTML Template
# -------------------------------
BASE_TEMPLATE = """
<div class="cdkeys-content-wrap">

  {content_blocks}

  <div class="cdkeys-paragraph">
    <h4 class="text-center font-weight-bold mt-4 mb-3">FAQs</h4>
  </div>

  <div class="accordion" id="accordions">
    {faq_blocks}
  </div>

  {spacer_block}

</div>
"""

FAQ_TEMPLATE = """
    <div class="accordion-item">
      <h5 class="collapsed heading" data-toggle="collapse" data-target="#faq-{index}" aria-expanded="false">
        {question}
      </h5>
      <div id="faq-{index}" class="collapse" data-parent="#accordions">
        <div class="acr-body">
          <p>{answer}</p>
        </div>
      </div>
    </div>
"""

SPACER = """
  <div class="cdkeys-paragraph">
    <h4 class="text-center font-weight-bold mt-4 mb-3"></h4>
  </div>
"""

def generate_formatted_html(about_text):
    prompt = f"""
You are a professional HTML formatter. Take the following raw text intended for a product category "About" section and convert it to HTML wrapped in <div class=\"cdkeys-paragraph\"> blocks.

- Use <h6> for headings, <p> for paragraphs.
- Use <ul>/<li> only if lists are clearly intended.
- Do not change the text.
- Do not add any extra text.

Input:
{about_text}

---
Output only the body sections (no outer wrapper):
"""
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You format plain marketing text into HTML for product descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def extract_faqs(text):
    prompt = f"""
From the following content, extract up to 5 FAQs and format them in this structure:

Q: Question 1
A: Answer 1
Q: Question 2
A: Answer 2

Only include FAQs present in the content. Do not make them up.

Input:
{text}
"""
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def build_html(full_text):
    body_html = generate_formatted_html(full_text)
    faqs_raw = extract_faqs(full_text)

    faq_html_blocks = []
    for i, qa in enumerate(faqs_raw.split("Q: ")[1:], start=1):
        parts = qa.strip().split("A: ")
        if len(parts) == 2:
            question = parts[0].strip()
            answer = parts[1].strip()
            faq_html_blocks.append(FAQ_TEMPLATE.format(index=i, question=question, answer=answer))

    spacer = SPACER if faq_html_blocks else ""
    return BASE_TEMPLATE.format(content_blocks=body_html, faq_blocks="\n".join(faq_html_blocks), spacer_block=spacer)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="QuickAbout - HTML Generator", page_icon="🧹", layout="wide")

st.markdown("""
<style>
    .title-wrap {
        text-align: center;
        padding-bottom: 20px;
    }
    .big-sub {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin: 0 auto;
        margin-bottom: 40px;
        max-width: 800px;
    }
    .button-row {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-bottom: 10px;
    }
    .admin-help {
        background: #fffbe6;
        border-left: 6px solid #ffe58f;
        padding: 15px 20px;
        border-radius: 6px;
        font-size: 15px;
        line-height: 1.6;
        margin-top: 30px;
    }
    textarea {
        font-family: 'Courier New', monospace;
        font-size: 15px;
    }
</style>

<div class="title-wrap">
    <h1>🧹 QuickAbout – AI HTML Snippet Builder</h1>
</div>
<div class="big-sub">
    Paste your raw category “About” text below. This tool will convert it into clean, formatted HTML for use in the EF category About tab.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📄 Paste your plain About Text")
    about_input = st.text_area("", height=400, placeholder="Enter product category about text here...")

    # Buttons in same row
    btn1, btn2 = st.columns([1, 1])

    with btn1:
        generate_clicked = st.button("✨ Generate HTML Snippet")

    with btn2:
        clear_clicked = st.button("🔄 Clear & Start New")

    # Handle Generate
    if generate_clicked and about_input.strip():
        with st.spinner("QuickAbout is on it..."):
            st.session_state["html_output"] = build_html(about_input)

    # Handle Clear
    if clear_clicked:
        st.session_state["html_output"] = ""
        st.rerun()  # ✅ Use this instead of st.experimental_rerun()

    st.markdown("""
    <div class="admin-help" style="font-size:16px;">
  <strong>📘 How to Paste This in Admin Panel:</strong>
  <ul>
    <li>Go to <strong>Admin Panel → Products → Categories → Edit</strong></li>
    <li>Click the <strong>&lt;/&gt;</strong> (code view) icon in the 'About' section</li>
    <li>Paste the HTML snippet generated above</li>
    <li>To add a product link (e.g., “Steam Wallet Card - £10”), use this anchor tag format: <br>
      <code>&lt;a class="ef-default-link" href="https://www.electronicfirst.com/gift-cards/steam-gift-card-10-gbp-uk/"&gt;Steam Wallet Card - £10&lt;/a&gt;</code>, 
    </li>
    <li>Toggle <strong>Show ‘About’ tab</strong> to YES</li>
    <li>Click Save</li>
  </ul>
</div>

    """, unsafe_allow_html=True)

with col2:
    if "html_output" in st.session_state:
        st.markdown("#### 📄 Generated HTML Snippet")

        # Align buttons in a row using Streamlit columns
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            st.download_button(
                "⬇️ Download HTML",
                st.session_state["html_output"],
                file_name="about_snippet.html",
                key="download_btn"
            )
        with btn_col2:
            st.button(
                "📋 Copy to Clipboard",
                help="Use right-click > Copy if browser copy fails",
                key="copy_btn"
            )

        # Show the HTML output with scroll
        st.code(st.session_state["html_output"], language="html")
