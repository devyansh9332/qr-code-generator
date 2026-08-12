import os
import sys
import subprocess
import platform
from pathlib import Path


# ============================================================
# PROJECT / VIRTUAL ENVIRONMENT
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"


def is_running_inside_venv():
    """Return True if the program is already running inside a venv."""
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def get_venv_python():
    """Return the Python executable inside the virtual environment."""

    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"

    return VENV_DIR / "bin" / "python"


def create_virtual_environment():
    """Create the project's virtual environment."""

    print("Creating virtual environment...")

    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "venv",
                str(VENV_DIR)
            ]
        )

    except subprocess.CalledProcessError:
        print("\nUnable to create the virtual environment.")

        if platform.system() == "Linux":
            print("\nFor Ubuntu/Debian:")
            print("sudo apt install python3-venv")

            print("\nFor Fedora:")
            print("sudo dnf install python3")

        sys.exit(1)


def restart_inside_venv():
    """Restart this program using the virtual environment."""

    python_path = get_venv_python()

    if not python_path.exists():
        print("\nVirtual environment Python was not found.")
        sys.exit(1)

    print("Starting application inside virtual environment...")

    os.execv(
        str(python_path),
        [
            str(python_path),
            str(Path(__file__).resolve())
        ]
    )


def install_python_dependencies():
    """Install Python dependencies inside the virtual environment."""

    print("\nInstalling required Python packages...")

    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip"
            ]
        )

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "qrcode[pil]"
            ]
        )

    except subprocess.CalledProcessError:
        print("\nFailed to install Python dependencies.")
        sys.exit(1)


def check_python_dependencies():
    """Check and install required Python packages."""

    try:
        import qrcode
        from PIL import Image

        return True

    except ImportError:
        install_python_dependencies()

        return False


def check_tkinter():
    """Check whether Tkinter is available."""

    try:
        import tkinter
        return True

    except ImportError:
        return False


def install_tkinter_linux():
    """Try to install Tkinter automatically on Linux."""

    print("\nTkinter is not installed.")
    print("Trying to install it automatically...\n")

    try:

        if Path("/usr/bin/apt").exists():

            commands = [
                ["sudo", "apt", "update"],
                ["sudo", "apt", "install", "-y", "python3-tk"]
            ]

        elif Path("/usr/bin/dnf").exists():

            commands = [
                [
                    "sudo",
                    "dnf",
                    "install",
                    "-y",
                    "python3-tkinter"
                ]
            ]

        elif Path("/usr/bin/pacman").exists():

            commands = [
                [
                    "sudo",
                    "pacman",
                    "-S",
                    "--needed",
                    "--noconfirm",
                    "tk"
                ]
            ]

        else:

            print(
                "Could not detect your Linux package manager."
            )

            return False

        for command in commands:

            print(
                "Running:",
                " ".join(command)
            )

            subprocess.check_call(command)

        return check_tkinter()

    except (subprocess.CalledProcessError, OSError):

        return False


def setup_environment():
    """Prepare the environment before starting the application."""

    # --------------------------------------------------------
    # Create virtual environment
    # --------------------------------------------------------

    if not VENV_DIR.exists():
        create_virtual_environment()

    # --------------------------------------------------------
    # Restart inside virtual environment
    # --------------------------------------------------------

    if not is_running_inside_venv():
        restart_inside_venv()

    # --------------------------------------------------------
    # Install Python packages
    # --------------------------------------------------------

    dependencies_ready = check_python_dependencies()

    if not dependencies_ready:

        os.execv(
            sys.executable,
            [
                sys.executable,
                str(Path(__file__).resolve())
            ]
        )

    # --------------------------------------------------------
    # Tkinter
    # --------------------------------------------------------

    if not check_tkinter():

        if platform.system() == "Linux":

            installed = install_tkinter_linux()

            if installed:

                os.execv(
                    sys.executable,
                    [
                        sys.executable,
                        str(Path(__file__).resolve())
                    ]
                )

            print(
                "\nTkinter could not be installed automatically."
            )

            print(
                "Please install it manually and run the program again."
            )

            sys.exit(1)

        else:

            print(
                "\nTkinter is not available in this Python installation."
            )

            print(
                "Please install a Python distribution that includes Tkinter."
            )

            sys.exit(1)


# Run environment setup first
setup_environment()


# ============================================================
# APPLICATION IMPORTS
# ============================================================

import tkinter as tk

from tkinter import (
    filedialog,
    messagebox,
    colorchooser
)

import qrcode

from PIL import (
    Image,
    ImageTk
)


# ============================================================
# QR CODE GENERATOR
# ============================================================

class QRCodeGenerator:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # Window
        # ----------------------------------------------------

        self.root.title(
            "QR Code Generator"
        )

        self.root.geometry(
            "1000x700"
        )

        self.root.minsize(
            650,
            500
        )

        self.root.configure(
            bg="#F5F6FA"
        )

        # ----------------------------------------------------
        # Colors
        # ----------------------------------------------------

        self.background = "#F5F6FA"
        self.white = "#FFFFFF"

        self.primary = "#5B4CF6"
        self.primary_dark = "#4939DF"

        self.text = "#20213A"
        self.secondary = "#6F7185"

        self.border = "#E0E1E8"

        self.success = "#198754"

        # ----------------------------------------------------
        # QR settings
        # ----------------------------------------------------

        self.foreground_color = "#000000"
        self.background_color = "#FFFFFF"

        self.qr_image = None
        self.preview_photo = None

        self.last_saved_path = None

        # ----------------------------------------------------
        # Start first screen
        # ----------------------------------------------------

        self.show_generator_screen()

    # ========================================================
    # UTILITY
    # ========================================================

    def clear_window(self):

        # Make sure any mousewheel bindings from the generator
        # screen's scrollable canvas don't leak into other screens.
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.unbind(
            "<Configure>"
        )

    # ========================================================
    # GENERATOR SCREEN
    # ========================================================

    def show_generator_screen(self):

        self.clear_window()

        # ----------------------------------------------------
        # Main container
        # ----------------------------------------------------

        self.generator_screen = tk.Frame(
            self.root,
            bg=self.background
        )

        self.generator_screen.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = tk.Frame(
            self.generator_screen,
            bg=self.primary,
            height=125
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(25, 20)
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="▣  QR Code Generator",
            font=("Arial", 27, "bold"),
            fg="white",
            bg=self.primary
        ).pack(
            anchor="w",
            padx=30,
            pady=(22, 2)
        )

        tk.Label(
            header,
            text="Generate QR codes from text, URLs and more",
            font=("Arial", 11),
            fg="#E9E7FF",
            bg=self.primary
        ).pack(
            anchor="w",
            padx=33
        )

        # ----------------------------------------------------
        # Content
        # ----------------------------------------------------

        content = tk.Frame(
            self.generator_screen,
            bg=self.background
        )

        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        content.grid_columnconfigure(
            0,
            weight=1
        )

        content.grid_rowconfigure(
            0,
            weight=1
        )

        # ONLY the generator panel
        panel = self.create_input_panel(
            content
        )

        panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # ========================================================
    # INPUT PANEL (SCROLLABLE)
    # ========================================================

    def create_input_panel(self, parent):

        # Outer bordered panel, matches the original look.
        panel = tk.Frame(
            parent,
            bg=self.white,
            highlightbackground=self.border,
            highlightthickness=1
        )

        # ----------------------------------------------------
        # Scrollable area (canvas + scrollbar)
        #
        # This is the actual fix for the "Generate QR" button
        # disappearing below the visible window: all the form
        # widgets now live inside a canvas that can scroll, so
        # nothing gets clipped when the window/panel is short.
        # ----------------------------------------------------

        canvas = tk.Canvas(
            panel,
            bg=self.white,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            panel,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # This inner frame holds all the actual form widgets.
        scrollable_frame = tk.Frame(
            canvas,
            bg=self.white
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=scrollable_frame,
            anchor="nw"
        )

        def update_scrollregion(event=None):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        def match_frame_width(event):
            # Keep the inner frame the same width as the canvas
            # so widgets stretch correctly and don't get an
            # awkward strip of empty space on the right.
            canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        scrollable_frame.bind(
            "<Configure>",
            update_scrollregion
        )

        canvas.bind(
            "<Configure>",
            match_frame_width
        )

        # Mouse wheel support (Windows/Mac use <MouseWheel>,
        # Linux uses <Button-4>/<Button-5>). Only bound while
        # the pointer is over the panel so it doesn't interfere
        # with other windows/scrollables.
        def on_mousewheel(event):
            if platform.system() == "Windows":
                canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
            elif platform.system() == "Darwin":
                canvas.yview_scroll(
                    int(-1 * event.delta),
                    "units"
                )

        def on_mousewheel_up(event):
            canvas.yview_scroll(-1, "units")

        def on_mousewheel_down(event):
            canvas.yview_scroll(1, "units")

        def bind_mousewheel(event):
            canvas.bind_all(
                "<MouseWheel>",
                on_mousewheel
            )

            canvas.bind_all(
                "<Button-4>",
                on_mousewheel_up
            )

            canvas.bind_all(
                "<Button-5>",
                on_mousewheel_down
            )

        def unbind_mousewheel(event):
            canvas.unbind_all(
                "<MouseWheel>"
            )

            canvas.unbind_all(
                "<Button-4>"
            )

            canvas.unbind_all(
                "<Button-5>"
            )

        canvas.bind(
            "<Enter>",
            bind_mousewheel
        )

        canvas.bind(
            "<Leave>",
            unbind_mousewheel
        )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        tk.Label(
            scrollable_frame,
            text="Create QR Code",
            font=("Arial", 20, "bold"),
            fg=self.text,
            bg=self.white
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 3)
        )

        tk.Label(
            scrollable_frame,
            text="Enter the information you want to encode",
            font=("Arial", 10),
            fg=self.secondary,
            bg=self.white
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 25)
        )

        # ----------------------------------------------------
        # Text / URL
        # ----------------------------------------------------

        tk.Label(
            scrollable_frame,
            text="Text or URL",
            font=("Arial", 10, "bold"),
            fg=self.text,
            bg=self.white
        ).pack(
            anchor="w",
            padx=35
        )

        self.input_box = tk.Text(
            scrollable_frame,
            height=6,
            font=("Arial", 11),
            wrap="word",
            relief="solid",
            bd=1
        )

        self.input_box.pack(
            fill="x",
            padx=35,
            pady=(7, 20)
        )

        # ----------------------------------------------------
        # File name
        # ----------------------------------------------------

        tk.Label(
            scrollable_frame,
            text="File Name",
            font=("Arial", 10, "bold"),
            fg=self.text,
            bg=self.white
        ).pack(
            anchor="w",
            padx=35
        )

        self.filename_entry = tk.Entry(
            scrollable_frame,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        self.filename_entry.insert(
            0,
            "qr_code.png"
        )

        self.filename_entry.pack(
            fill="x",
            padx=35,
            pady=(7, 20)
        )

        # ----------------------------------------------------
        # Colors
        # ----------------------------------------------------

        tk.Label(
            scrollable_frame,
            text="QR Colors",
            font=("Arial", 10, "bold"),
            fg=self.text,
            bg=self.white
        ).pack(
            anchor="w",
            padx=35
        )

        colors_frame = tk.Frame(
            scrollable_frame,
            bg=self.white
        )

        colors_frame.pack(
            fill="x",
            padx=35,
            pady=(8, 20)
        )

        colors_frame.grid_columnconfigure(
            0,
            weight=1
        )

        colors_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # Foreground
        foreground_frame = tk.Frame(
            colors_frame,
            bg=self.white
        )

        foreground_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        tk.Label(
            foreground_frame,
            text="Foreground",
            font=("Arial", 9),
            fg=self.secondary,
            bg=self.white
        ).pack(
            anchor="w"
        )

        self.foreground_button = tk.Button(
            foreground_frame,
            bg=self.foreground_color,
            activebackground=self.foreground_color,
            relief="solid",
            bd=1,
            height=1,
            cursor="hand2",
            command=lambda: self.choose_color(
                "foreground"
            )
        )

        self.foreground_button.pack(
            fill="x",
            pady=(5, 0)
        )

        # Background
        background_frame = tk.Frame(
            colors_frame,
            bg=self.white
        )

        background_frame.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        tk.Label(
            background_frame,
            text="Background",
            font=("Arial", 9),
            fg=self.secondary,
            bg=self.white
        ).pack(
            anchor="w"
        )

        self.background_button = tk.Button(
            background_frame,
            bg=self.background_color,
            activebackground=self.background_color,
            relief="solid",
            bd=1,
            height=1,
            cursor="hand2",
            command=lambda: self.choose_color(
                "background"
            )
        )

        self.background_button.pack(
            fill="x",
            pady=(5, 0)
        )

        # ----------------------------------------------------
        # Error correction
        # ----------------------------------------------------

        tk.Label(
            scrollable_frame,
            text="Error Correction",
            font=("Arial", 10, "bold"),
            fg=self.text,
            bg=self.white
        ).pack(
            anchor="w",
            padx=35
        )

        self.correction_var = tk.StringVar(
            value="Medium (15%)"
        )

        self.correction_menu = tk.OptionMenu(
            scrollable_frame,
            self.correction_var,
            "Low (7%)",
            "Medium (15%)",
            "Quartile (25%)",
            "High (30%)"
        )

        self.correction_menu.config(
            font=("Arial", 9),
            bg=self.white,
            relief="solid",
            bd=1,
            highlightthickness=0
        )

        self.correction_menu.pack(
            fill="x",
            padx=35,
            pady=(7, 25)
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        button_frame = tk.Frame(
            scrollable_frame,
            bg=self.white
        )

        button_frame.pack(
            fill="x",
            padx=35,
            pady=(0, 30)
        )

        self.generate_button = tk.Button(
            button_frame,
            text="▣  Generate QR",
            font=("Arial", 11, "bold"),
            fg="white",
            bg=self.primary,
            activebackground=self.primary_dark,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.generate_qr
        )

        self.generate_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5),
            ipady=10
        )

        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 10, "bold"),
            fg=self.primary,
            bg=self.white,
            activebackground="#EEEEF8",
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self.clear_form
        )

        self.clear_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0),
            ipady=10
        )

        return panel

    # ========================================================
    # COLOR PICKER
    # ========================================================

    def choose_color(self, color_type):

        if color_type == "foreground":
            current_color = self.foreground_color
        else:
            current_color = self.background_color

        result = colorchooser.askcolor(
            color=current_color,
            title="Choose Color"
        )

        if not result[1]:
            return

        selected_color = result[1]

        if color_type == "foreground":

            self.foreground_color = selected_color

            self.foreground_button.configure(
                bg=selected_color,
                activebackground=selected_color
            )

        else:

            self.background_color = selected_color

            self.background_button.configure(
                bg=selected_color,
                activebackground=selected_color
            )

    # ========================================================
    # GENERATE QR
    # ========================================================

    def generate_qr(self):

        data = self.input_box.get(
            "1.0",
            tk.END
        ).strip()

        if not data:

            messagebox.showwarning(
                "Input Required",
                "Please enter text or a URL."
            )

            return

        correction_map = {
            "Low (7%)":
                qrcode.constants.ERROR_CORRECT_L,

            "Medium (15%)":
                qrcode.constants.ERROR_CORRECT_M,

            "Quartile (25%)":
                qrcode.constants.ERROR_CORRECT_Q,

            "High (30%)":
                qrcode.constants.ERROR_CORRECT_H
        }

        try:

            qr = qrcode.QRCode(
                version=None,
                error_correction=correction_map[
                    self.correction_var.get()
                ],
                box_size=10,
                border=4
            )

            qr.add_data(
                data
            )

            qr.make(
                fit=True
            )

            self.qr_image = qr.make_image(
                fill_color=self.foreground_color,
                back_color=self.background_color
            ).convert(
                "RGB"
            )

            self.last_saved_path = None

            # Go to QR screen only after successful generation
            self.show_qr_screen()

        except Exception as error:

            messagebox.showerror(
                "QR Generation Error",
                f"Could not generate the QR code.\n\n{error}"
            )

    # ========================================================
    # QR SCREEN
    # ========================================================

    def show_qr_screen(self):

        self.clear_window()

        self.preview_screen = tk.Frame(
            self.root,
            bg=self.background
        )

        self.preview_screen.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Top bar
        # ----------------------------------------------------

        top_bar = tk.Frame(
            self.preview_screen,
            bg=self.white,
            height=70
        )

        top_bar.pack(
            fill="x"
        )

        top_bar.pack_propagate(False)

        tk.Button(
            top_bar,
            text="←  Back",
            font=("Arial", 11, "bold"),
            fg=self.primary,
            bg=self.white,
            activebackground="#EEEEF8",
            relief="flat",
            cursor="hand2",
            command=self.show_generator_screen
        ).pack(
            side="left",
            padx=25,
            pady=18
        )

        tk.Label(
            top_bar,
            text="QR Code Preview",
            font=("Arial", 17, "bold"),
            fg=self.text,
            bg=self.white
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # QR display area
        # ----------------------------------------------------

        self.qr_area = tk.Frame(
            self.preview_screen,
            bg=self.white,
            highlightbackground=self.border,
            highlightthickness=1
        )

        self.qr_area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        self.qr_display = tk.Label(
            self.qr_area,
            bg=self.white
        )

        self.qr_display.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ----------------------------------------------------
        # Bottom controls
        # ----------------------------------------------------

        bottom_bar = tk.Frame(
            self.preview_screen,
            bg=self.white,
            height=105
        )

        bottom_bar.pack(
            fill="x"
        )

        bottom_bar.pack_propagate(False)

        self.status_label = tk.Label(
            bottom_bar,
            text="✓ QR code generated successfully",
            font=("Arial", 10, "bold"),
            fg=self.success,
            bg=self.white
        )

        self.status_label.pack(
            pady=(12, 6)
        )

        controls = tk.Frame(
            bottom_bar,
            bg=self.white
        )

        controls.pack()

        tk.Button(
            controls,
            text="↓  Save QR",
            font=("Arial", 10, "bold"),
            fg="white",
            bg=self.primary,
            activebackground=self.primary_dark,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.save_qr
        ).pack(
            side="left",
            padx=5,
            ipadx=30,
            ipady=7
        )

        tk.Button(
            controls,
            text="📁  Open Folder",
            font=("Arial", 10, "bold"),
            fg=self.primary,
            bg=self.white,
            activebackground="#EEEEF8",
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self.open_folder
        ).pack(
            side="left",
            padx=5,
            ipadx=18,
            ipady=7
        )

        # ----------------------------------------------------
        # Dynamic QR resizing
        # ----------------------------------------------------

        self.root.bind(
            "<Configure>",
            self.resize_qr
        )

        self.root.after(
            100,
            self.resize_qr
        )

    # ========================================================
    # RESPONSIVE QR
    # ========================================================

    def resize_qr(self, event=None):

        if self.qr_image is None:
            return

        if not hasattr(
            self,
            "qr_area"
        ):
            return

        area_width = self.qr_area.winfo_width()
        area_height = self.qr_area.winfo_height()

        if area_width <= 1 or area_height <= 1:
            return

        # Leave comfortable margins
        available_width = area_width - 80
        available_height = area_height - 80

        size = min(
            available_width,
            available_height
        )

        # Minimum QR size
        size = max(
            size,
            150
        )

        # Maximum QR size
        size = min(
            size,
            900
        )

        image = self.qr_image.copy()

        image.thumbnail(
            (size, size),
            Image.Resampling.LANCZOS
        )

        self.preview_photo = ImageTk.PhotoImage(
            image
        )

        self.qr_display.configure(
            image=self.preview_photo
        )

    # ========================================================
    # SAVE QR
    # ========================================================

    def save_qr(self):

        if self.qr_image is None:
            return

        filename = self.filename_entry.get().strip()

        if not filename:
            filename = "qr_code.png"

        if not filename.lower().endswith(
            (
                ".png",
                ".jpg",
                ".jpeg"
            )
        ):
            filename += ".png"

        save_path = filedialog.asksaveasfilename(
            title="Save QR Code",
            initialfile=filename,
            defaultextension=".png",
            filetypes=[
                (
                    "PNG Image",
                    "*.png"
                ),
                (
                    "JPEG Image",
                    "*.jpg"
                ),
                (
                    "JPEG Image",
                    "*.jpeg"
                )
            ]
        )

        if not save_path:
            return

        try:

            self.qr_image.save(
                save_path
            )

            self.last_saved_path = save_path

            self.status_label.configure(
                text="✓ QR code saved successfully",
                fg=self.success
            )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                f"Could not save the QR code.\n\n{error}"
            )

    # ========================================================
    # OPEN FOLDER
    # ========================================================

    def open_folder(self):

        if not self.last_saved_path:

            messagebox.showinfo(
                "Save QR First",
                "Please save the QR code first."
            )

            return

        folder = os.path.dirname(
            self.last_saved_path
        )

        try:

            system = platform.system()

            if system == "Windows":

                os.startfile(
                    folder
                )

            elif system == "Darwin":

                subprocess.Popen(
                    [
                        "open",
                        folder
                    ]
                )

            else:

                subprocess.Popen(
                    [
                        "xdg-open",
                        folder
                    ]
                )

        except Exception as error:

            messagebox.showerror(
                "Folder Error",
                f"Could not open the folder.\n\n{error}"
            )

    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.input_box.delete(
            "1.0",
            tk.END
        )

        self.filename_entry.delete(
            0,
            tk.END
        )

        self.filename_entry.insert(
            0,
            "qr_code.png"
        )

        # Reset colors
        self.foreground_color = "#000000"
        self.background_color = "#FFFFFF"

        self.foreground_button.configure(
            bg="#000000",
            activebackground="#000000"
        )

        self.background_button.configure(
            bg="#FFFFFF",
            activebackground="#FFFFFF"
        )

        # Reset correction
        self.correction_var.set(
            "Medium (15%)"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    QRCodeGenerator(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()