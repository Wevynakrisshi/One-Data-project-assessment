import os
import requests
import gradio as gr
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

# 🔑 API KEYS
os.environ["GOOGLE_API_KEY"] = "Enter-Your-API-key"
SERP_API_KEY = "Enter-Your-API-key"

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0.3)

# Session context to store summary + overview for chatbot
session_context = {"context": ""}

# 1️⃣ Semantic Scholar
@tool
def search_semantic(query: str) -> str:
    """Searches Semantic Scholar for academic papers."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=3&fields=title,abstract,url,authors,year"
    response = requests.get(url)
    data = response.json().get("data", [])
    result = ""
    for paper in data:
        title = paper.get("title", "")
        authors = ', '.join([a['name'] for a in paper.get("authors", [])])
        abstract = paper.get("abstract", "")
        url = paper.get("url", "")
        year = paper.get("year", "")
        result += f"TITLE: {title}\nAUTHORS: {authors}\nYEAR: {year}\nABSTRACT: {abstract}\nURL: {url}\n\n"
    return result #or "No results from Semantic Scholar."

# 2️⃣ arXiv
@tool
def search_arxiv(query: str) -> str:
    """Searches arXiv for preprints."""
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3"
    response = requests.get(url)
    entries = response.text.split("<entry>")[1:]
    result = ""
    for entry in entries:
        title = entry.split("<title>")[1].split("</title>")[0].strip()
        summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
        link = entry.split("<id>")[1].split("</id>")[0].strip()
        result += f"TITLE: {title}\nABSTRACT: {summary}\nURL: {link}\n\n"
    return result or "No results from arXiv."

# 3️⃣ CrossRef
@tool
def search_crossref(query: str) -> str:
    """Searches CrossRef for research metadata."""
    url = f"https://api.crossref.org/works?query={query}&rows=3"
    response = requests.get(url)
    data = response.json().get("message", {}).get("items", [])
    result = ""
    for item in data:
        title = item.get("title", [""])[0]
        year = item.get("issued", {}).get("date-parts", [[None]])[0][0]
        authors = ', '.join([a.get("given", "") + " " + a.get("family", "") for a in item.get("author", [])]) if item.get("author") else "N/A"
        url = item.get("URL", "")
        result += f"TITLE: {title}\nAUTHORS: {authors}\nYEAR: {year}\nURL: {url}\n\n"
    return result or "No results from CrossRef."

# 4️⃣ SERP API
@tool
def search_serp(query: str) -> str:
    """Uses SERP API to search the web (Google Search)."""
    serp_url = f"https://serpapi.com/search.json?q={query}&api_key={SERP_API_KEY}"
    response = requests.get(serp_url)
    results = response.json().get("organic_results", [])
    result = ""
    for item in results[:3]:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        result += f"TITLE: {title}\nSNIPPET: {snippet}\nURL: {link}\n\n"
    return result or "No web results."

# 5️⃣ Summarization Tool
@tool
def summarize_papers(text: str) -> str:
    """Summarizes mixed academic content."""
    prompt = f"""
     You are a highly intelligent and precise research summarizer.
     Your task is to go through the given 'text' which contains multiple research papers (each with a title, abstract, URL, etc.). For each individual paper found in the 'text', provide a clean and concise summary as follows:
     For every paper, extract:
     TITLE: Clearly mention the title of the paper.
     KEY TECHNIQUES USED: Briefly list or describe the main methods, algorithms, or frameworks used in that specific paper.
     SUMMARY: In 5 to 10 lines, describe what the paper does, the problem it solves, and its core contribution.

     You can retrieve insights from the paper’s URL or metadata content, but avoid inventing facts or make use of your internal knowledge as a language model in worst cases whn you are not able to retrive data . Ensure that a summary is generated for each and every paper present in the input text.
     Do not use bullet symbols, markdown formatting, or asterisks. Use only plain subheadings like Title, Key Techniques Used, and Summary for each paper block. Maintain structure and consistency.


    {text}
    """
    return llm.predict(prompt)

# 6️⃣ Overview Generator
@tool
def generate_overview(summary: str) -> str:
    """Creates a research overview from summary."""
    prompt = f"""
     You are an expert research overview generator. Based on a collection of summarized research papers, generate a well-structured overview that can be used in academic reports or documentation.
     Instructions:
     - Use the provided summaries as your only source of information.
     - Do not fabricate new facts or papers.
     - Organize the overview into clear, bold subheadings.
     - Keep the content formal, readable, and informative.

     Structure your output as follows:

     1.Introduction
     Briefly introduce the research topic, explain its significance, and highlight the scope of the overview based on the summaries.

     2.Key Themes and Techniques
     Group related findings under clear theme titles (e.g., Machine Learning Models, Cloud Optimization, etc.). List the key techniques, frameworks, or methodologies frequently used across the papers. Present these in plain bullet points. Each point should be clear and informative (1–3 lines per point).

     3.Trends and Observations
     List general patterns, challenges, emerging ideas, or popular directions found across the papers. Use plain bullet points. Each point should be concise and insightful (1 - 3 lines).
     Conclusion
     Conclude with a short paragraph summarizing what this collection of research contributes to the field and what directions it suggests for future work.

      Formatting Guidelines:
      - Do not use markdown, asterisks in the front and back of subheading, or any special formatting
      - Subheadings should be written as plain bold text labels
      - Bullet points are allowed only in Key Themes and Techniques and Trends and Observations
      - Maintain a clean academic tone
      - The entire overview should reflect insights from all papers, not just a few
      - Limit the output to around 300–500 words

      Make sure the overview reads like a mini-review of the research space based on the summaries.
    {summary}
    """
    return llm.predict(prompt)

# Register tools
tools = [
    search_semantic,
    search_arxiv,
    search_crossref,
    search_serp,
    summarize_papers,
    generate_overview
]

# Initialize Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Main pipeline function
def run_research_agent(query):
    semantic = search_semantic.run(query)
    arxiv = search_arxiv.run(query)
    crossref = search_crossref.run(query)
    combined = semantic + arxiv + crossref

    summary = summarize_papers.run(combined)
    overview = generate_overview.run(summary)

    # Save context for chatbot
    session_context["context"] = summary + "\n" + overview

    return combined.strip(), summary.strip(), overview.strip()

# Chatbot function
def research_chatbot(user_input, history):
    context = session_context.get("context", "")
    prompt = f"""
    You are a research-aware AI assistant.
    Use the following research topic and the summary/overview provided to you by the system to answer the user’s question.
    Respond in a way that aligns with academic insights, keeping the language clear, informative, and moderately technical.
    #Based on the following research topic, summary or overview, answer the user's question:

    Context:
    {context}

    Question: {user_input}
    """
    answer = llm.predict(prompt)
    return answer

# Gradio Interface
with gr.Blocks(title="📚 AI-Powered Research Assistant") as demo:
    gr.Markdown("### 🔍 Enter your research topic")
    query_input = gr.Textbox(label="Research Topic")
    run_button = gr.Button("Run Research")
    with gr.Row():
        papers_output = gr.Textbox(label="🔍 Papers Found", lines=20)
        summary_output = gr.Textbox(label="📝 Summary", lines=10)
        overview_output = gr.Textbox(label="📄 Research Overview", lines=10)



    gr.Markdown("## 💬 Ask questions about the topic, summary or overview")
    chatbot = gr.ChatInterface(fn=research_chatbot, title="🧠 Research Q&A Bot")

    run_button.click(
        fn=run_research_agent,
        inputs=query_input,
        outputs=[papers_output, summary_output, overview_output],
    )

demo.launch(share=True)
