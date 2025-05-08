# AI-Powered Research Assistant

This project is an advanced, AI-powered research assistant that automates the process of retrieving, summarizing, and interpreting academic literature from multiple sources. It helps users get paper summaries, extract key techniques, and generate structured research overviews—all through an interactive chatbot interface.

---

## Features

* **Multi-Source Paper Search:**
  Searches Semantic Scholar, arXiv, CrossRef, and Google (via SERP API) for the latest papers and research material on any topic.

* **Smart Summarizer:**
  Uses a powerful LLM (Gemini) to summarize multiple research papers into concise insights with title, techniques used, and core contributions.

* **Overview Generator:**
  Creates a structured academic-style research overview from paper summaries, including key themes, trends, and a conclusion.

* **Interactive Chatbot:**
  Users can ask natural language questions based on the research, and the chatbot responds with relevant insights.

* **Gradio Interface:**
  A user-friendly web interface to input topics, review research, and interact with the AI.

---

## Tech Stack

| Component | Technology                                  |
| --------- | ------------------------------------------- |
| LLM       | Gemini via `langchain_google_genai`         |
| APIs      | Semantic Scholar, arXiv, CrossRef, SERP API |
| Interface | Gradio Blocks & ChatInterface               |
| Agent     | LangChain Tools + Zero-Shot Agent           |
| Language  | Python 3                                    |

---

## Code Overview

**main.py**: Contains the primary logic for the research assistant, including search, summarization, and chatbot functions.

**tools.py**: Implements the functions to interact with different academic search APIs like Semantic Scholar, arXiv, and CrossRef.

**agent.py**: Manages the AI agent and uses LangChain to initialize and interact with the tools and the language model.

**chatbot.py**: Implements the chatbot that answers questions based on the research summary and overview.

---

## How It Works

1. **User enters a research topic**
2. **The system fetches papers** using APIs (Semantic Scholar, arXiv, CrossRef, SERP API)
3. **Papers are summarized** using Gemini LLM
4. **An academic-style overview** is generated
5. **Users can chat** with the AI about the research topic and insights

---

## Setup Instructions

> Note: You must provide valid API keys for Google Generative AI and SERP API.

1. **Install dependencies**

```bash
pip install gradio langchain requests langchain_google_genai
```

2. **Set API keys**

```bash
export GOOGLE_API_KEY="your_google_api_key"
export SERP_API_KEY="your_serp_api_key"
```

3. **Run the app**

```bash
python app.py
```

---

## UI Preview

* Search for any research topic
* View fetched papers from multiple databases
* Get clean summaries and structured overviews
* Chat with the assistant using academic context

---

## Use Cases

* Literature review for academic papers
* Quick understanding of trending research areas
* AI-assisted writing for research documentation
* Research topic exploration for students & professionals

---

## Contributions

Contributions, suggestions, and improvements are welcome. Please fork the repo and raise a pull request.

---

## License

This project is for educational and demonstrative purposes only. Not intended for commercial use.
