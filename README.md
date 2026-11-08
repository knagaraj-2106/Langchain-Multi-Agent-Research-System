# Multi-Agent Research System

A Streamlit application that researches a topic with a four-stage AI workflow: web search, page reading, report writing, and an AI-generated review. The app displays each stage's results and lets you download the final report as Markdown.

## Features

- Search the web for relevant sources with Tavily.
- Extract readable content from a selected webpage.
- Generate a structured research report with OpenAI.
- Review the report with a separate critic chain.
- View search results, scraped content, the report, and feedback in the Streamlit interface.

## Technologies

- **Python** — application language
- **Streamlit** — web interface
- **LangChain** and **LangChain OpenAI** — agent and prompt-chain orchestration
- **OpenAI GPT-4o mini** — language model used for the agents, writer, and critic
- **Tavily** — web search
- **Requests**, **Trafilatura**, **Readability-lxml**, and **Beautiful Soup** — page fetching and content extraction
- **python-dotenv** — loading API credentials from a local `.env` file

## Getting started

### Prerequisites

- Python installed and available on your `PATH`
- An OpenAI API key
- A Tavily API key

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace the placeholders with the URL and directory name for your fork or clone.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keep `.env` private; do not commit API keys or other credentials to source control.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit. Enter a research topic and select **Run Research**. When the workflow completes, browse the report, critic review, scraped content, and search results. The report can be downloaded as a Markdown file.

## Architecture

The Streamlit interface in `app.py` coordinates the workflow and stores completed results in the user's Streamlit session. The research runs through these stages in sequence:

```text
Research topic
      |
      v
Search agent (Tavily web search)
      |
      v
Reader agent (fetch and extract a relevant webpage)
      |
      v
Writer chain (synthesize search and page content into a report)
      |
      v
Critic chain (score the report and suggest improvements)
      |
      v
Streamlit results and Markdown download
```

- `src/agents/agents.py` defines the search and reader agents and the writer and critic chains.
- `src/tools/tools.py` provides the Tavily search and webpage-scraping tools.
- `src/pipelines/pipeline.py` implements the same four-stage workflow for command-line use.
- `app.py` provides the interactive Streamlit experience.
- `main.py` is a small example that runs the pipeline for a preset topic.

## Configuration

The model is currently set to `gpt-4o-mini` in `src/agents/agents.py`. The search tool uses Tavily and requires `TAVILY_API_KEY`; model calls require `OPENAI_API_KEY`.

## Contributing

Contributions are welcome. Fork the repository, create a focused branch, and open a pull request describing the change and any relevant testing. Please do not include credentials or local environment files in your changes.

## License

No license file is currently included. Add a license before redistributing this project under open-source terms.
