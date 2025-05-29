# QuickAbout – AI HTML Snippet Generator

QuickAbout is a lightweight internal tool designed for Electronic First. It converts plain “About” category text into clean, structured HTML that matches the official EF content layout.

## ✨ Features

- Converts raw text to EF-formatted HTML
- Auto-generates accordion-style FAQs
- Copy/download snippet directly
- Streamlit interface for non-tech users

## 🧰 Tech Stack

- Python 3.10+
- Streamlit
- OpenAI GPT-4 Turbo API
- `python-dotenv` for secure key handling

## 🚀 Getting Started

```bash
git clone https://github.com/mejba13/quickabout-html-generator.git
cd quickabout-html-generator
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your-secret-api-key
```

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