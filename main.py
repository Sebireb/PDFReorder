import sys
import os
from pypdf import PdfWriter, PdfReader
from pypdf.errors import PdfReadError
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


file_dialog_title = "PDF-Datei auswählen"
file_save_dialog_title = "PDF-Datei speichern"
file_dialog_types = [("PDF-Datei", "*.pdf")]
messagebox_title = "PDFReorder"
messagebox_success = "Die PDF-Datei wurde umsortiert."
error_no_file = "Es wurde keine Datei ausgewählt!"
error_file_does_not_exists = "Die angegebene Datei existiert nicht!"
error_no_access = "Auf die angegebene Datei kann nicht zugegriffen werden (Anderer Prozess? )!"
error_no_pdf = "Die angegebene Datei ist keine PDF-Datei!"


def get_file_path():
    if len(sys.argv) > 1:
        return sys.argv[1]

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title=file_dialog_title,
        filetypes=file_dialog_types
    )

    if file_path is None or file_path == "":
        messagebox.showerror(messagebox_title, error_no_file)
        sys.exit(-100)

    return file_path


def check_access_to_file(file_path):
    if not os.path.exists(file_path):
        messagebox.showerror(messagebox_title, error_file_does_not_exists)
        sys.exit(-101)
    if not os.access(file_path, os.R_OK):
        messagebox.showerror(messagebox_title, error_no_access)
        sys.exit(-102)


def get_output_path(file_path):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title=file_save_dialog_title,
        filetypes=file_dialog_types,
        defaultextension='pdf',
        initialfile=os.path.basename(file_path),
        confirmoverwrite=True
    )

    if file_path is None or file_path == "":
        messagebox.showerror(messagebox_title, error_no_file)
        sys.exit(-100)

    return file_path


def create_reordered_pdf(file_path):
    with open(file_path, "rb") as file:
        try:
            old_pdf = PdfReader(file)
        except PdfReadError:
            messagebox.showerror(messagebox_title, error_no_pdf)
            sys.exit(-103)

        new_pdf = PdfWriter()
        amount_pages = len(old_pdf.pages)

        half_pages = int(amount_pages / 2 + 0.5)

        page_index = 0
        while page_index < half_pages:
            # Front:
            new_pdf.add_page(old_pdf.pages[page_index])
            # Back:
            if half_pages + page_index < amount_pages:
                new_pdf.add_page(old_pdf.pages[amount_pages - 1 - page_index])

            page_index += 1

    output_path = get_output_path(file_path)
    try:
        with open(output_path, "wb") as file:
            new_pdf.write(file)
    except OSError:
        messagebox.showerror(messagebox_title, error_no_access)
        sys.exit(-102)


def show_success_popup():
    tk.messagebox.showinfo(title=messagebox_title, message=messagebox_success)


def reorder_pdf():
    file_path = get_file_path()
    check_access_to_file(file_path)
    create_reordered_pdf(file_path)
    show_success_popup()


if __name__ == '__main__':
    reorder_pdf()
