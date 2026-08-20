# STEM Treasure Run - Online Hosting & Publishing Guide

This guide explains how to compile **STEM Treasure Run** to run in a web browser using WebAssembly, and host it online for free.

---

## 1. Local Browser Testing (Using Pygbag)

[Pygbag](https://pypi.org/project/pygbag/) is the official tool to compile Pygame projects into WebAssembly (WASM) so they can run directly in a browser.

### Step 1: Install Pygbag
Open your terminal (PowerShell, Command Prompt, or bash) and install pygbag via pip:
```bash
pip install pygbag
```

### Step 2: Test the Web Build Locally
Run pygbag in the root folder containing `main.py` with the sound format check disabled (since our chiptunes are generated programmatically in PCM `.wav` format):
```bash
python -m pygbag --disable-sound-format-error .
```
* Pygbag will start a local server, usually at `http://localhost:8000`.
* Open your browser and navigate to `http://localhost:8000` to play the web version of your game locally.

---

## 2. Option A: Host for Free on Itch.io (Recommended)

Itch.io is the most popular free hosting platform for indie games.

### Step 1: Package the Build
When you ran `python -m pygbag --disable-sound-format-error .`, pygbag created a `build/web/` directory containing:
* `index.html`
* JavaScript / WASM loader files
* A `.apk` or `.js` package containing your code and assets.

Run the helper packaging script to compress everything inside the `build/web/` folder into a single `.zip` file (which ensures `index.html` remains correctly at the root level of the archive):
```bash
python zip_build.py
```
This generates `web_build.zip` directly in your project root directory.

### Step 2: Upload to Itch.io
1. Go to [itch.io](https://itch.io) and log in (or create a free account).
2. Click **Create a new project** from your dashboard.
3. Fill out the details:
   * **Kind of project**: Select **HTML** (You have a ZIP file of HTML/JS/WASM).
   * **Uploads**: Click **Upload files** and select your `web_build.zip`.
   * **Play in browser**: Check the box **This file will be played in the browser**.
4. Set display dimensions:
   * **Viewport size**: Set to **Width: 1000px** and **Height: 600px** (matching the game's canvas dimensions).
5. Save and view page to test!

---

## 3. Option B: Host for Free on GitHub Pages

GitHub Pages is ideal if you have your project version-controlled on GitHub.

### Step 1: Create a GitHub Repository
1. Create a public repository named `stem-treasure-run` on GitHub.
2. Push your code (including the `build/web/` folder containing `index.html`).

### Step 2: Enable GitHub Pages
1. Go to your repository settings on GitHub.
2. Click on **Pages** in the left sidebar.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select your main branch and choose the directory `/build/web` (or move the contents of `build/web/` to the repository root and select `/root`).
5. Click **Save**.
6. Within a minute, your game will be live at `https://<your-username>.github.io/stem-treasure-run/`!
