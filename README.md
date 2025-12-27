# OrganizeMyFiles 📼️

[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)

OrganizeMyFiles is a Python utility that automatically sorts and organizes your files. It categorizes files into folders based on type, manages recently modified files, and handles filename collisions efficiently.

---

## 🚀 Features

* Automatically sorts files into categories:

  * Images, Videos, Audio, Documents, Applications, Code, Archives, Other
* Moves recently modified files (within 7 days) to a `recent` folder
* Smart collision resolution:

  * Increments `(1)`, `(2)`, etc. only when a real collision occurs
  * Prevents stacking numbers like `(1)(1)` for repeated moves
* Dry-run mode to preview changes without moving files
* Easy configuration via `details.json`

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Abhi2009CU/OrganizeMyFiles.git
cd OrganizeMyFiles
```

### 2. Create a virtual environment

Recommended for managing dependencies:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies (optional)

```bash
pip install -r requirements.txt
```

*(No external dependencies are required; Python standard library is sufficient.)*

---

## 🏊 Usage

### Dry-run (preview changes without moving files)

```bash
python main.py --dry-run
```

### Live mode (organize files)

```bash
python main.py
```

**Example Output:**

```
MOVED: photo.jpg → Images/photo.jpg
[DRY-RUN] WOULD MOVE: report.docx → Documents/report.docx
```

---

## 📁 Folder Structure

* `recent/` → Files modified within the last 7 days
* `Images/` → jpg, png, gif, svg, etc.
* `Videos/` → mp4, mkv, avi, mov, etc.
* `Audio/` → mp3, wav, flac, etc.
* `Documents/` → pdf, docx, txt, pptx, etc.
* `Applications/` → exe, dmg, apk, etc.
* `Code/` → py, js, cpp, java, html, css, etc.
* `Archives/` → zip, rar, 7z, tar, gz
* `Other/` → Any uncategorized files

---

## 🛠️ Notes

* Organizes files **non-recursively** (does not process files within subfolders)
* Collision resolution prevents overwriting files

---

## 💪 Contributing

Contributions are welcome! Open issues, submit pull requests, or suggest features. OrganizeMyFiles is open to ideas for additional file types and functionality.
