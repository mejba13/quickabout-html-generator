import streamlit as st
st.set_page_config(page_title="QuickAbout - HTML Generator", page_icon="🧹", layout="wide")

from auth import login_form, is_authenticated, logout_button
from dotenv import load_dotenv
import os
import openai

#🔐 Require authentication
# if not is_authenticated():
#     login_form()
#     st.stop()
#
# # ✅ Show logout after login
# logout_button()

# 🔑 Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Load the Hugging Face API
from huggingface_hub import InferenceClient
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "tiiuae/falcon-7b-instruct")
USE_HF = os.getenv("USE_HF", "False").lower() == "true"


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

# -------------------------------
# Format Category Text into Clean HTML
# -------------------------------

def generate_formatted_html(about_text):
    prompt = f"""
You are a professional HTML formatter. Take the following raw text intended for a product category "About" section and convert it to HTML wrapped in <div class="cdkeys-paragraph"> blocks.

Format rules:
- Use <h6> for clear headings
- Use <p> for regular paragraph text
- If bullet points are present, wrap them in <ul class="what-cdkeys"> and <li>
- Never rewrite or add new text
- Do not wrap with <html>, <body>, <head>, or <style> tags

Input:
{about_text}

---
Output only the HTML body content (no <html> or <body> tag):
"""

    if USE_HF:
        client = InferenceClient(token=HF_API_KEY)
        raw_html = client.text_generation(
            prompt,
            model=HF_MODEL,
            temperature=0.3,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.03,
            stop_sequences=["---"]
        )
    else:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You convert plain marketing text into clean, component-level HTML for category pages."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        raw_html = response.choices[0].message.content.strip()

    # ✂️ Post-cleanup
    cleaned_html = raw_html.replace("<html>", "").replace("</html>", "")
    cleaned_html = cleaned_html.replace("<body>", "").replace("</body>", "")
    cleaned_html = cleaned_html.replace("<head>", "").replace("</head>", "")
    return cleaned_html.strip()

# -------------------------------
# Extract FAQs from Content
# -------------------------------
def extract_faqs(text):
    prompt = f"""
From the following content, extract up to 5 real FAQs and format them like this:

Q: Question?
A: Answer.

Only extract questions that are clearly present in the content. Do not invent or assume any.

Input:
{text}
"""

    if USE_HF:
        client = InferenceClient(token=HF_API_KEY)
        faqs = client.text_generation(
            prompt,
            model=HF_MODEL,
            temperature=0.2,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.02,
            stop_sequences=["---"]
        )
        return faqs.strip()
    else:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()


import re

import re

def build_html(full_text):
    # Extract raw FAQs from the input text first
    faqs_raw = extract_faqs(full_text)

    # If FAQs found, strip them from the original body input
    if "Q:" in faqs_raw and "A:" in faqs_raw:
        # Remove Q/A blocks and any 'FAQs' headings
        faq_block_pattern = r"(FAQs[\n:]*)?(Q:.*?\nA:.*?)(?=(\nQ:|\Z))"
        cleaned_text = re.sub(faq_block_pattern, "", full_text, flags=re.DOTALL | re.IGNORECASE).strip()
    else:
        cleaned_text = full_text  # No FAQ present, keep original

    # Generate main HTML body without duplicated FAQs
    body_html = generate_formatted_html(cleaned_text)

    # Build accordion FAQ items
    faq_html_blocks = []
    for i, qa in enumerate(faqs_raw.split("Q: ")[1:], start=1):
        parts = qa.strip().split("A: ")
        if len(parts) == 2:
            question = parts[0].strip()
            answer = parts[1].strip()
            faq_html_blocks.append(FAQ_TEMPLATE.format(index=i, question=question, answer=answer))

    # Only insert FAQ section if at least one FAQ was extracted
    spacer = SPACER if faq_html_blocks else ""
    faq_block_html = "\n".join(faq_html_blocks) if faq_html_blocks else ""

    return BASE_TEMPLATE.format(
        content_blocks=body_html,
        faq_blocks=faq_block_html,
        spacer_block=spacer
    )




# -------------------------------
# Streamlit UI
# -------------------------------

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
                "📋 Hover HTML Snippet to Copy",
                help="Move your mouse over the HTML snippet to reveal and click the copy icon.",
                key="copy_btn"
            )

        # Show the HTML output with scroll
        st.code(st.session_state["html_output"], language="html")
