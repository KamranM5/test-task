# Stateless Chatbot with LangGraph

A stateless chatbot built with LangGraph that uses the `solar` model via Ollama and a `get_current_time` tool to provide the current UTC time when asked.

## Setup

1. Install Ollama
Download from [https://ollama.com/](https://ollama.com/).
2. Pull the `solar` model:
```bash
     ollama pull solar
```
3. Start the Ollama server by typing the following command in the first terminal("commant prompt"):

bash
```bash
ollama serve
```

4. Cope repo:

```bash
git clone https://github.com/KamranM5/test-task.git
```

5. Set up the Python environment:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
6. Run the chatbot:

```bash
langgraph dev
```