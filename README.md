
# QuickAbout – AI HTML Snippet Generator

QuickAbout is a lightweight internal tool designed for Electronic First. It converts plain “About” category text into clean, structured HTML that matches the official EF content layout.

## ✨ Features

- Converts raw text to EF-formatted HTML
- Auto-generates accordion-style FAQs
- Copy/download snippet directly
- Streamlit interface for non-tech users
- Supports both OpenAI gpt-4o-mini Turbo and Hugging Face inference APIs

## 🧰 Tech Stack

- Python 3.10+
- Streamlit
- OpenAI gpt-4o-mini API
- Hugging Face Inference API
- `python-dotenv` for secure key handling

## 🚀 Getting Started

```bash
git clone https://github.com/mejba13/quickabout-html-generator.git
cd quickabout-html-generator
pip install -r requirements.txt
```

Create a `.env` file with either OpenAI or Hugging Face credentials:

```env
# OpenAI Option
OPENAI_API_KEY=your-openai-key

# Hugging Face Option (optional)
HF_API_KEY=your-huggingface-key
HF_MODEL=tiiuae/falcon-7b-instruct
USE_HF=True
```

Set `USE_HF=True` to switch to Hugging Face model, or leave it as `False` (default) to use GPT-4 Turbo.

Run the app:

```bash
streamlit run main.py
```

## 📌 Usage

1. Paste raw category “About” content.
2. Click `✨ Generate HTML Snippet`.
3. Copy or download the result.
4. Use it in Admin Panel > Products > Categories > Edit > About tab.

## 📄 License

MIT – Free for internal and commercial use under MIT terms.
