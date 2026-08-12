# 🔲 QR Code Generator

A lightweight and user-friendly QR Code Generator built with Python and Tkinter.

The application provides a graphical interface for generating QR codes from text, URLs, or any other information. It includes customizable QR colors, error correction settings, a responsive QR preview, and options to save the generated QR code and open its containing folder.

The application is designed to work across Linux, Windows, and macOS.

---

## ✨ Features

- Generate QR codes from text or URLs
- Graphical user interface using Tkinter
- Automatic Python virtual environment setup
- Automatic installation of required Python packages
- Custom foreground color
- Custom background color
- Multiple QR error-correction levels
- Responsive QR preview
- Automatic QR scaling based on window size
- Dedicated QR preview screen
- Save QR codes as PNG or JPEG
- Automatically adds `.png` extension when required
- Open the folder containing the saved QR code
- Back button to return to the generator
- Clear form functionality
- Cross-platform folder opening
- No manual virtual environment activation required

---

## 🖥️ Application Workflow

```text
Start Application
       │
       ▼
┌──────────────────────┐
│   Generator Screen   │
│                      │
│   Text / URL         │
│   File Name          │
│   QR Colors          │
│   Error Correction   │
│                      │
│   [ Generate QR ]    │
│   [ Clear ]          │
└──────────┬───────────┘
           │
           ▼
     Generate QR
           │
           ▼
┌──────────────────────┐
│   QR Preview Screen  │
│                      │
│      QR CODE         │
│                      │
│   [ Save QR ]        │
│   [ Open Folder ]    │
│                      │
│      [ ← Back ]      │
└──────────────────────┘
````

The QR preview is displayed only after a QR code has been successfully generated.

---

## 🎨 QR Code Customization

### Foreground Color

Controls the color of the QR code itself.

Default:

```text
Black
```

### Background Color

Controls the background of the QR code.

Default:

```text
White
```

### Error Correction

| Level    | Approximate Recovery |
| -------- | -------------------: |
| Low      |                   7% |
| Medium   |                  15% |
| Quartile |                  25% |
| High     |                  30% |

---

## 📱 Responsive QR Preview

After generating a QR code, the application opens a dedicated preview screen.

The QR code automatically adjusts its size according to the available window space.

```text
Small Window
     ↓
Smaller QR Code

Large Window
     ↓
Larger QR Code
```

---

## 💾 Saving QR Codes

Generated QR codes can be saved using the **Save QR** button.

Supported formats:

```text
PNG
JPEG
```

Example:

```text
qr_code.png
```

If a filename is entered without an image extension, `.png` is automatically added.

---

## 📁 Open Folder

After saving a QR code, the **Open Folder** button opens the directory containing the saved file.

The application detects the operating system automatically.

### Windows

Uses Windows File Explorer.

### macOS

Uses the macOS `open` command.

### Linux

Uses the `xdg-open` command.

---

## 🛡️ Automatic Environment Setup

The application automatically manages its Python environment.

On startup it:

1. Checks for a virtual environment.
2. Creates `.venv` if required.
3. Restarts itself using the virtual environment.
4. Checks for required Python packages.
5. Installs missing packages.
6. Starts the application.

---

## 📦 Dependencies

* Python 3
* Tkinter
* qrcode
* Pillow

The QR Code library and Pillow are installed automatically when required.

Manual installation:

```bash
python -m pip install "qrcode[pil]"
```

---

## 🚀 Requirements

* Python 3
* Tkinter
* Windows, Linux, or macOS
* Internet connection during the first automatic dependency installation

---

# 🐧 Linux

## Ubuntu / Debian

Install Python, virtual-environment support, and Tkinter:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk -y
```

Clone the repository:

```bash
git clone git@github.com:devyansh9332/qr-code-generator.git
```

Enter the project directory:

```bash
cd qr-code-generator
```

Run:

```bash
python3 qr_generator.py
```

---

## Fedora

Install Python and Tkinter:

```bash
sudo dnf install python3 python3-tkinter -y
```

Clone the repository:

```bash
git clone git@github.com:devyansh9332/qr-code-generator.git
```

Enter the project directory:

```bash
cd qr-code-generator
```

Run:

```bash
python3 qr_generator.py
```

---

# 🪟 Windows

## 1. Install Python

Install Python 3 and make sure **Add Python to PATH** is enabled during installation.

## 2. Clone the Repository

Using SSH:

```bash
git clone git@github.com:devyansh9332/qr-code-generator.git
```

Or HTTPS:

```bash
git clone https://github.com/devyansh9332/qr-code-generator.git
```

Enter the project directory:

```bash
cd qr-code-generator
```

## 3. Run

```bash
python qr_generator.py
```

The application automatically creates the virtual environment and installs the required Python packages.

---

# 🍎 macOS

## 1. Install Python

Using Homebrew:

```bash
brew install python
```

## 2. Clone the Repository

```bash
git clone git@github.com:devyansh9332/qr-code-generator.git
```

Enter the project directory:

```bash
cd qr-code-generator
```

## 3. Run

```bash
python3 qr_generator.py
```

---

# 🚀 Quick Start

### Linux / macOS

```bash
git clone git@github.com:devyansh9332/qr-code-generator.git
cd qr-code-generator
python3 qr_generator.py
```

### Windows

```bash
git clone git@github.com:devyansh9332/qr-code-generator.git
cd qr-code-generator
python qr_generator.py
```

---

# 🧑‍💻 Manual Installation

## Linux / macOS

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install "qrcode[pil]"
```

Run:

```bash
python qr_generator.py
```

## Windows

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install "qrcode[pil]"
```

Run:

```powershell
python qr_generator.py
```

---

# 📂 Project Structure

```text
qr-code-generator/
│
├── qr_generator.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .venv/
    └── Python virtual environment
```

The `.venv` directory is created automatically and should not be committed to Git.

---

# 📄 requirements.txt

```text
qrcode[pil]
```

Install dependencies manually:

```bash
python -m pip install -r requirements.txt
```

---

# 🛠️ Technologies Used

* Python 3
* Tkinter
* qrcode
* Pillow
* pathlib
* subprocess
* platform
* os
* Git

---

# 🧠 Concepts Demonstrated

* Object-oriented programming
* Classes and methods
* Functions
* Conditional statements
* Exception handling
* File handling
* Directory handling
* Path management
* Virtual environment management
* Package installation
* GUI development
* Tkinter widgets
* Event handling
* Color selection
* Image processing
* QR code generation
* Dynamic image resizing
* Operating-system detection
* Cross-platform commands
* Subprocess execution
* User input validation

---

# 🔐 Error Handling

The application handles common situations including:

* Missing Python packages
* Virtual environment creation failures
* Missing Tkinter
* Invalid QR generation
* Missing input
* Failed QR saving
* Failed folder opening
* Unsupported environment configuration

Users receive graphical error or warning messages when an operation cannot be completed.

---

# 🔄 Example Usage

Enter:

```text
https://github.com/devyansh9332
```

Choose a filename:

```text
github.png
```

Select the desired:

```text
Foreground Color
Background Color
Error Correction
```

Click:

```text
Generate QR
```

The application opens the QR preview screen.

From there:

```text
← Back
Save QR
Open Folder
```

are available.

---

# 🔮 Future Improvements

* QR code history
* Copy QR image to clipboard
* Drag-and-drop support
* Batch QR generation
* Wi-Fi QR generation
* Contact/vCard QR generation
* Email QR generation
* SMS QR generation
* Phone number QR generation
* Custom QR borders
* QR logo support
* QR templates
* Dark/light application themes
* Export settings
* Keyboard shortcuts
* Recent QR codes
* QR code sharing
* Custom output directory
* Standalone executable builds

---

# ⚠️ Notes

The application requires Tkinter for the graphical interface.

On Linux systems where Tkinter is not installed, the application attempts to install the appropriate package automatically.

An internet connection may be required during the first run to install missing Python packages.

Generated QR images are saved only when the user chooses the **Save QR** option.

---

# 👨‍💻 Author

**SudoTerminal**

---

# 📜 License

This project is open source and available for personal and educational use.

---

## ⭐ Project

If you find this project useful, consider giving the repository a star on GitHub.
