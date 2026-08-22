# 🎬 StoryForge Agent

> AI-powered YouTube Shorts & Instagram Reels script generator with real-time research

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45-red)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-GPT--OSS--20B-orange)](https://groq.com)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.3-purple)](https://fastmcp.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🌐 Live Demo
👉 **[Try it here](https://storyforge-agent-myproject.streamlit.app/)**

---

## 📌 What is StoryForge?

StoryForge is an AI agent that researches any topic in real-time and generates optimized viral short-form video scripts for YouTube Shorts and Instagram Reels.

Built as a college project to demonstrate:
- Real-time AI research pipelines
- LLM prompt engineering for viral content
- MCP (Model Context Protocol) server building
- Full-stack AI application development

---

## 🏗️ Architecture
```
End User (Browser)              AI Agents (MCP Clients)
│                                │
▼                                ▼
Streamlit App               MCP Server (mcp_server.py)
(streamlit_app.py)               FastMCP + 3 Tools
│                                │
└──────────────┬─────────────────┘
               ▼
        Core Logic (app.py)
┌─────────────────────────┐
│   get_realtime_info()   │
│  generate_video_script()│
│      run_pipeline()     │
└────────────┬────────────┘
             │
┌────────────┴────────────┐
▼                         ▼
Tavily API               Groq API
(Real-time search)     (GPT-OSS 20B)
```

---

## ✨ Features

- 🔍 **Real-time research** — fetches latest web info on any topic instantly
- 🤖 **Viral script generation** — GPT-OSS 20B via Groq with proven hook formula
- 📱 **Multi-platform** — YouTube Shorts (60s) and Instagram Reels (60s)
- 🎭 **4 tone modes** — Educational, Funny, Dramatic, Casual
- 🎬 **Title suggestions** — 3 catchy viral titles per script
- 🔢 **Hashtag generator** — 15 optimized hashtags per script
- ⬇️ **Script download** — export as .txt file instantly
- 📚 **Script history** — all generated scripts saved in session
- 🔗 **Source links** — full transparency on research sources
- 🛡️ **Error handling** — retry logic, input validation, friendly errors
- 🤖 **MCP server** — 3 tools usable by any AI agent

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13 | Core language |
| Streamlit | 1.45 | Web UI |
| Groq API | 0.13 | LLM (GPT-OSS 20B - openai/gpt-oss-20b) |
| Tavily API | 0.5 | Real-time web search |
| FastMCP | 2.3 | MCP server framework |
| Continue.dev | Latest | MCP client (VS Code) |

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/kbharathparmaar369/storyforge-agent.git
cd storyforge-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file in the root:
```bash
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

Get your free API keys:
- **Groq** → [console.groq.com](https://console.groq.com)
- **Tavily** → [tavily.com](https://tavily.com)

### 5. Run the app
```bash
python app_main.py
```
*Note: app_main.py is the entry point that handles path configuration.*

Open browser at `http://localhost:8501`

---

## 🤖 MCP Server

### Run the server
```bash
python src/mcp_server.py
```

### Available Tools

| Tool | Description |
|------|-------------|
| `get_latest_info_mcp` | Search web for real-time info on any topic |
| `get_video_script_mcp` | Generate complete script (research + write) |
| `get_topic_summary_mcp` | Get a quick summary of any topic |

### Connect to Continue.dev (VS Code)

Add this to your `config.json` in Continue:

```json
{
  "mcpServers": [
    {
      "name": "storyforge",
      "command": "python",
      "args": [
        "C:\\PATH\\TO\\storyforge-agent\\src\\mcp_server.py"
      ],
      "env": {
        "TAVILY_API_KEY": "your_tavily_key",
        "GROQ_API_KEY": "your_groq_key",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1"
      }
    }
  ]
}
```

---

## 📁 Project Structure
```
storyforge-agent/
├── src/
│   ├── app.py                # Core pipeline (search + generate)
│   ├── mcp_server.py         # FastMCP server with 3 tools
│   ├── streamlit_app.py      # Streamlit web UI
│   ├── utils.py              # Validators and error handlers
│   └── test_mcp.py           # MCP tool tests
├── streamlit/
│   └── config.toml           # Streamlit theme config
├── .env.example              # API key template
├── .gitignore                # Git ignore rules
├── app_main.py               # Streamlit Cloud entry point
├── mcp_config.example.json   # MCP configuration template
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🚀 How It Works

1. **User enters topic**
2. **Tavily searches web** in real-time to fetch latest facts.
3. **Groq GPT-OSS 20B** processes the research and generates a viral script using a proven 5-point structure (Hook, Context, Value, CTA).
4. **Catchy Titles & Hashtags** are generated to match the content.
5. **Script is displayed** with options to download or view research sources.

---

## 🔮 Future Improvements

- [ ] Voice-over audio generation with ElevenLabs
- [ ] Auto-post to YouTube via YouTube Data API
- [ ] Script history saved to database (PostgreSQL)
- [ ] Multi-language script support
- [ ] Thumbnail idea generator

---

## 👨‍💻 Author

**Bharath**
- GitHub: [@kbharathparmaar369](https://github.com/kbharathparmaar369)

---

## 📄 License

MIT License — feel free to use, modify and build on this project!

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — High-speed LLM inference
- [Tavily](https://tavily.com) — Real-time web search API
- [Streamlit](https://streamlit.io) — Interactive web UI
- [FastMCP](https://fastmcp.com) — MCP server framework
- [Anthropic](https://anthropic.com) — Model Context Protocol creators
