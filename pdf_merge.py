import tkinter as tk
from tkinter import filedialog, messagebox

from pypdf import PdfWriter


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger Tool")
        self.root.geometry("400x250")

        self.selected_files = []

        # UI Components
        self.info_label = tk.Label(root, text="Step 1: Select PDFs to merge", pady=10)
        self.info_label.pack()

        self.select_button = tk.Button(
            root, text="Select PDF Files", command=self.select_files
        )
        self.select_button.pack(pady=5)

        self.file_count_label = tk.Label(root, text="Files selected: 0", fg="blue")
        self.file_count_label.pack(pady=5)

        self.merge_button = tk.Button(
            root, text="Merge & Save As...", command=self.merge_files, state=tk.DISABLED
        )
        self.merge_button.pack(pady=20)

    def select_files(self):
        # Open dialog to select multiple files
        files = filedialog.askopenfilenames(
            title="Select PDF files", filetypes=[("PDF files", "*.pdf")]
        )
        if files:
            self.selected_files = list(files)
            self.file_count_label.config(
                text=f"Files selected: {len(self.selected_files)}"
            )
            self.merge_button.config(state=tk.NORMAL)

    def merge_files(self):
        # Open dialog to name the output file and choose location
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Merged PDF As",
        )

        if not output_path:
            return

        writer = PdfWriter()
        try:
            for pdf in self.selected_files:
                writer.append(pdf)

            with open(output_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Success", "Files merged successfully.")
            # Reset app state
            self.selected_files = []
            self.file_count_label.config(text="Files selected: 0")
            self.merge_button.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
