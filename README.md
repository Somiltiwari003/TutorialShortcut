# TutorialShortcut 🎥🤖

**Ask Questions About YouTube Videos Using AI**

TutorialShortcut is an AI-powered YouTube Video Question Answering application built with Streamlit, LangChain, Hugging Face, and FAISS. It allows users to enter a YouTube video link, process its transcript, and ask questions about the video's content using a language model.

Instead of watching an entire video to find a particular answer, users can ask questions and receive context-based responses.

## ✨ Features

- **YouTube Transcript Extraction:** Fetches the transcript of a supported YouTube video.
- **AI-Powered Question Answering:** Uses a Hugging Face language model to generate answers.
- **Semantic Search:** Retrieves relevant transcript passages using vector embeddings.
- **FAISS Vector Database:** Efficiently searches transcript chunks for relevant information.
- **Context-Aware Responses:** Instructs the AI to answer using the provided transcript context.
- **Modern Streamlit Interface:** Provides a simple interface for loading videos and asking questions.
- **Transcript Passage Viewer:** Displays the passages retrieved to answer a question.
- **Caching:** Reuses loaded resources and indexed videos to reduce repeated processing.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| LangChain | LLM integration and retrieval pipeline |
| Hugging Face | Language model and text embeddings |
| FAISS | Vector similarity search |
| Sentence Transformers | Generates text embeddings |
| YouTube Transcript API | Retrieves YouTube transcripts |
| python-dotenv | Loads environment variables |

## 📋 Prerequisites

Before running the application, install the following:

- Python 3.10 or later (Python 3.11 is a reasonable choice for compatibility).
- Git.
- A Hugging Face account.
- An internet connection.
- Access to a YouTube video with an available English transcript.

Check your Python and Git installations:

```bash
python --version
git --version
```

## 🚀 Installation and Setup

Follow these steps to run TutorialShortcut locally.

### Step 1: Clone the repository

Open Command Prompt, PowerShell, or the VS Code terminal and run:

```bash
git clone https://github.com/Somiltiwari003/TutorialShortcut.git
```

Navigate into the project directory:

```bash
cd TutorialShortcut
```

### Step 2: Create a virtual environment

A virtual environment keeps this project's dependencies separate from other Python projects.

```bash
python -m venv venv
```

Activate it on Windows:

**Command Prompt:**

```bash
venv\Scripts\activate.bat
```

**PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

For macOS or Linux:

```bash
source venv/bin/activate
```

If PowerShell blocks activation, you can use Command Prompt instead or follow the official Python virtual-environment documentation.

### Step 3: Install dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install all project dependencies:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes the libraries required by the application:

- `streamlit`
- `python-dotenv`
- `langchain-core`
- `langchain-community`
- `langchain-huggingface`
- `langchain-text-splitters`
- `faiss-cpu`
- `sentence-transformers`
- `youtube-transcript-api`

**Note:** The first run may take longer because the sentence-embedding model must be downloaded and initialized.

## 🔑 Hugging Face API Token Setup

TutorialShortcut uses Hugging Face's hosted language model through LangChain. You must configure a valid Hugging Face access token before asking questions.

### Step 1: Create a Hugging Face account

Visit [Hugging Face](https://huggingface.co/) and create an account or sign in.

### Step 2: Generate an access token

1. Open [Hugging Face Access Tokens](https://huggingface.co/settings/tokens).
2. Select the option to create a new token.
3. Give it a recognizable name, such as `TutorialShortcut`.
4. Choose the permissions needed to call the inference service. A fine-grained token with the required inference permissions is preferable; otherwise, follow the permissions offered by the current Hugging Face interface.
5. Create the token and copy it.

The token typically begins with `hf_`.

**Important:** Never publish your actual token in GitHub, screenshots, public notebooks, or source code.

### Step 3: Create a `.env` file

In the root directory of the cloned repository, create a file named `.env`.

Your directory should look like this:

```text
TutorialShortcut/
├── app.py
├── requirements.txt
├── .env.example
├── .env
└── venv/
```

Add the following line to `.env`:

```env
HF_TOKEN=hf_your_actual_token_here
```

Replace `hf_your_actual_token_here` with your real access token. Do not include quotation marks unless your configuration specifically requires them.

The application uses `python-dotenv` to load environment variables, and the Hugging Face integration can use `HF_TOKEN` for authentication.

### Step 4: Verify the token configuration

Your application's `app.py` already calls:

```python
from dotenv import load_dotenv

load_dotenv()
```

You can optionally verify that the variable is available without printing the secret itself:

```python
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("HF_TOKEN"):
    print("Hugging Face token is configured.")
else:
    print("HF_TOKEN is missing.")
```

Save this as a temporary test script in the project directory and run it inside your activated virtual environment.

### Step 5: Protect your token

Make sure `.env` is excluded from Git. Add the following entries to a `.gitignore` file in the repository root:

```gitignore
.env
venv/
__pycache__/
*.py[cod]
```

The repository currently contains `.env.example`, so you can use it as a template. Keep placeholders in that example file and store the real token only in `.env`.

If you accidentally publish a token, revoke it immediately in Hugging Face settings and generate a replacement.

**Official resource:** [Hugging Face authentication documentation](https://huggingface.co/docs/huggingface_hub/en/quick-start#authentication)

## ▶️ Running the Application

Once the dependencies and token are configured, make sure your terminal is in the `TutorialShortcut` project directory and your virtual environment is activated.

Run:

```bash
streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that address in your browser.

### How to use TutorialShortcut

1. Open the application in your browser.
2. Paste a YouTube video URL into the **YouTube link** field.
3. Click **Load video**.
4. Wait while the application fetches the transcript, splits it into chunks, creates embeddings, and builds the FAISS index.
5. Enter a question about the video's content.
6. Click **Ask**.
7. Read the AI-generated answer.
8. Expand **Transcript passages used** to inspect the retrieved text that supports the answer.

Example questions:

- What are the main topics discussed in this video?
- Explain the key concepts in simple language.
- What steps does the presenter recommend?
- Summarize the most important points.
- What conclusion does the speaker reach?

The quality of the answers depends on the transcript, the retrieved passages, and the language model.

## 🧠 How It Works

TutorialShortcut uses a retrieval-augmented generation (RAG) workflow.

```text
YouTube Video URL
        |
        v
Extract Video ID
        |
        v
Fetch YouTube Transcript
        |
        v
Split Transcript into Chunks
        |
        v
Generate Text Embeddings
        |
        v
Build FAISS Vector Index
        |
        v
User Enters a Question
        |
        v
Retrieve Relevant Passages
        |
        v
Hugging Face Language Model
        |
        v
Context-Based Answer
```

### Workflow explanation

1. **Video identification:** The application extracts the YouTube video ID from supported URL formats.
2. **Transcript extraction:** The YouTube Transcript API retrieves available transcript text.
3. **Text chunking:** LangChain's `RecursiveCharacterTextSplitter` splits the transcript into chunks of 1,000 characters, with a 200-character overlap.
4. **Embedding generation:** `sentence-transformers/all-MiniLM-L6-v2` converts transcript chunks into numerical vectors.
5. **Vector indexing:** FAISS stores the vectors and supports efficient similarity retrieval.
6. **Question retrieval:** Maximum Marginal Relevance (MMR) retrieves up to four relevant passages while encouraging diversity among results.
7. **Answer generation:** The retrieved passages and question are passed to the Hugging Face language model, which generates the answer.

The language model is configured as `meta-llama/Llama-3.1-8B-Instruct` with a temperature of `0.2` and a maximum of 512 new tokens.

## 📁 Project Structure

```text
TutorialShortcut/
│
├── app.py              # Streamlit application and RAG pipeline
├── requirements.txt    # Python dependencies
├── .env.example        # Environment-variable template
├── .env                # Local Hugging Face token (create locally)
├── .gitignore          # Files excluded from Git
└── README.md           # Project documentation
```

The `.env` and `.gitignore` entries above describe the recommended local setup; create `.gitignore` if it is not already present.

## ⚙️ Important Configuration Parameters

| Parameter | Current value | Purpose |
|---|---|---|
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` | Converts transcript chunks into vectors |
| Language model | `meta-llama/Llama-3.1-8B-Instruct` | Generates answers |
| LLM task | `text-generation` | Specifies the inference task |
| Temperature | `0.2` | Controls response randomness |
| Maximum new tokens | `512` | Limits generated response length |
| Chunk size | `1000` | Sets transcript chunk length in characters |
| Chunk overlap | `200` | Preserves context between adjacent chunks |
| Retrieved documents (`k`) | `4` | Number of passages provided to the answer chain |
| MMR fetch count (`fetch_k`) | `20` | Number of candidate passages considered during retrieval |

These values are configured in `app.py`. Changing them may affect response quality, latency, and resource usage.

## 🛠️ Troubleshooting

### 1. `HF_TOKEN` is missing

**Cause:** The `.env` file is missing, incorrectly named, or stored in the wrong directory.

**Solution:**

- Confirm that `.env` is in the same project directory as `app.py`.
- Check that the variable is named `HF_TOKEN`.
- Restart Streamlit after changing environment variables.

### 2. Hugging Face authentication or inference errors

**Possible causes:**

- The token is invalid, expired, or missing required permissions.
- The selected inference service is unavailable.
- The model requires additional access approval.
- The account has reached an inference usage limit or the provider requires payment.

**Solution:**

- Generate a new token if necessary.
- Review the model page and any access conditions for [Llama 3.1 8B Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct).
- Check Hugging Face's [Inference Providers documentation](https://huggingface.co/docs/inference-providers/index) for current availability and usage requirements.

A valid token alone does not guarantee that every model or inference provider will be available for free.

### 3. No transcript found

**Cause:** The video has no available English transcript or captions are disabled.

**Solution:** Try another YouTube video with an available English transcript.

### 4. Video unavailable

**Cause:** The video may be private, deleted, restricted, or otherwise inaccessible.

**Solution:** Verify the URL and try a publicly accessible video.

### 5. Dependency installation errors

**Solution:**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If installation still fails, confirm that the virtual environment is active and that your Python version is compatible with the installed packages.

### 6. Slow first run

**Cause:** The embedding model may need to download, and the transcript index must be built.

**Solution:** Wait for the initial processing to finish. Cached resources and indexed videos can reduce repeated processing during the same application session.

### 7. Answers are incomplete or incorrect

**Cause:** The answer depends on the transcript quality, retrieval results, and the language model's behavior.

**Solution:** Ask a more specific question, verify the retrieved passages, or try a video with a more complete transcript.

## 🔒 Security and Privacy

- Keep your Hugging Face token in `.env`, not in `app.py`.
- Never commit `.env` to a public repository.
- Do not share tokens in screenshots or logs.
- Use the minimum token permissions necessary.
- Avoid pasting sensitive or confidential video content into external AI services.
- Review the terms and usage policies of the services you use.

## 🚧 Limitations

- The application relies on an accessible YouTube transcript; it does not independently transcribe audio when captions are unavailable.
- The current implementation searches transcript text rather than the video's visual content.
- The default language-model configuration is designed for English transcripts.
- Model inference can be affected by provider availability, usage limits, network connectivity, and model-access requirements.
- Answers are based on retrieved transcript passages and may omit information outside those passages.
- The FAISS index is cached by video ID during application execution; this is not a persistent database for long-term storage.

## 🔮 Future Improvements

Possible enhancements include:

- Support for additional transcript languages.
- Downloadable video summaries and notes.
- Timestamped answers linking back to relevant moments.
- Persistent storage for transcript indexes.
- Conversation history for follow-up questions.
- Configurable embedding models and language models.
- More detailed source citations in generated answers.

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Commit your changes with a descriptive message.
5. Open a pull request.

## 📄 License

No license is specified in the current repository. Check with the repository owner before redistributing or using the project under particular licensing terms.

## 👨‍💻 Author

**Somil Tiwari**

- GitHub: [Somiltiwari003](https://github.com/Somiltiwari003)
- Project Repository: [TutorialShortcut](https://github.com/Somiltiwari003/TutorialShortcut)

---

⭐ If you find TutorialShortcut useful, consider starring the repository and sharing feedback.

