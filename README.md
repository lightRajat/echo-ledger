# 🗣️ Echo Ledger

An AI-powered voice-based ledger engine that tracks speech at a retail store checkout counter and updates the ledger in real-time.

## 📹 Demo

> **NOTE:** Turn on the video volume

<video src="https://github.com/user-attachments/assets/855f4ec6-0216-4da1-9a50-81cce142f00d" controls title="Demo Video"></video>

## 🚀 Usage Workflow

> **Setting:** Checkout Counter at a Retail Store

1. Customer brings all their items to the checkout counter.
2. The staff triggers the application by saying something like *"Start the transaction"*.
3. The staff then recites all the items, along with the quantity in their natural language, and optionally the price to refer a certain version of the item.
4. The staff then says something like *"End the transaction"*.

The application will automatically keep track of the transaction and update the ledger in real-time in the database.


## 🛠️ Tech Stack

- **Vue 3 + Vite** for frontend
- **FastAPI** for backend
- **SQLite** for database
- **Silero VAD** for voice activity detection
- **OpenAI Whisper** for speech-to-text
- **Local Llama 3** as the inference engine

## ⚙️ Installation & Setup

### Prerequisites

- [Astral UV](https://docs.astral.sh/uv/getting-started/installation/)
- [Node & npm](https://nodejs.org/en/download)

### Clone the repository

```bash
git clone git@github.com:lightRajat/echo-ledger.git
cd echo-ledger
```

### Start Backend Server

1. `cd backend`
2. Create `.env` file with the following contents:
    ```bash
    LLAMA_REPO_ID=bartowski/Llama-3.2-3B-Instruct-GGUF
    LLAMA_FILE_NAME=Llama-3.2-3B-Instruct-Q4_K_M.gguf
    HF_TOKEN=your_huggingface_token
    ```

    > NOTE: `HF_TOKEN` just speeds up download of the model. It can be omitted.
3. Install cuda dependencies for `llama-cpp-python`:
   ```bash
   sudo apt update
   sudo apt install build-essential cmake
   sudo apt install nvidia-cuda-toolkit
   export CMAKE_ARGS="-DGGML_CUDA=on"
   ```
4. Install project dependencies: `uv sync`
5. Download sample *csv* data from this [link](https://drive.google.com/drive/folders/123LdAlYHc1jk0STYFG95NMhZknSiGNVw?usp=drive_link) and paste them inside location `data/sample-data/`.
6. Initialize the database and download AI models: `uv run init.py`
   > NOTE: This may take a while.
7. Run the server: `uv run main.py`

### Start Frontend UI

1. `cd frontend`
2. Install dependencies: `npm install`
3. Create `.env` file with the following contents:
    ```bash
    VITE_BACKEND_URL=ws://localhost:8000
    ```
4. Run the server: `npm run dev`
5. Open `http://localhost:5173` in your browser.

## 📝 License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.
