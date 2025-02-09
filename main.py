import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
import os
import shutil
import platform

class PDFManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Manager")
        self.master.geometry("500x350")

        self.selected_matiere = tk.StringVar(self.master)
        self.selected_matiere.set('Subject 1')

        self.matiere_paths = {
            'Subject 1': './Subject1',
            'Subject 2': './Subject2',
            'Subject 3': './Subject3',
            'Subject 4': './Subject4',
            'Subject 5': './Subject5',
            'Subject 6': './Subject6'
        }

        icon_path = "icon.ico"
        self.master.iconbitmap(default=icon_path)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Number of PDFs per subject:", font=("Arial", 12)).pack(pady=10)

        for matiere in self.matiere_paths:
            tk.Label(self.master, text=f"{matiere}: {self.count_pdfs_in_matiere(matiere)} PDF", font=("Arial", 10)).pack()

        matieres = list(self.matiere_paths.keys())
        matiere_menu = tk.OptionMenu(self.master, self.selected_matiere, *matieres)
        matiere_menu.pack(pady=10)

        add_pdf_button = tk.Button(self.master, text="Add a PDF to the subject", command=self.add_pdf, font=("Arial", 12))
        add_pdf_button.pack(pady=10)

        view_pdf_button = tk.Button(self.master, text="View subject PDFs", command=self.view_pdfs, font=("Arial", 12))
        view_pdf_button.pack(pady=10)

    def count_pdfs_in_matiere(self, matiere):
        matiere_path = self.matiere_paths[matiere]
        return sum(1 for file in os.listdir(matiere_path) if file.lower().endswith('.pdf'))

    def update_pdf_count_label(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_widgets()
    
    def delete_pdf(self, matiere, pdf_name):
        matiere_path = self.matiere_paths[matiere]
        pdf_path = os.path.join(matiere_path, pdf_name)

        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            messagebox.showinfo("PDF deleted", f"The PDF '{pdf_name}' was removed from the subject {matiere}.")
            self.count_pdfs_in_matiere(matiere)
            self.update_pdf_count_label()
        else:
            messagebox.showwarning("File not found", f"The PDF '{pdf_name}' does not exist in this subject.")


    def view_pdfs(self):
        matiere = self.selected_matiere.get()
        matiere_path = os.path.abspath(self.matiere_paths[matiere])

        pdf_files = [f for f in os.listdir(matiere_path) if f.lower().endswith('.pdf')]

        if not pdf_files:
            messagebox.showwarning("No PDF", f"No PDF was found in the subject {matiere}.")
            return
    
        pdf_window = tk.Toplevel(self.master)
        pdf_window.title(f"List of PDFs of {matiere}")
        pdf_window.geometry("500x350")

        pdf_table = tk.Label(pdf_window, text="List of PDFs", font=("Arial", 12))
        pdf_table.pack(pady=10)

        for pdf in pdf_files:
            pdf_frame = tk.Frame(pdf_window)
            pdf_frame.pack()
            pdf_label = tk.Label(pdf_frame, text=pdf, font=("Arial", 10))
            pdf_label.pack(side=tk.LEFT)
            pdf_delete_button = tk.Button(pdf_frame, text="Delete", command=lambda pdf_name=pdf: self.delete_pdf(matiere, pdf_name))
            pdf_delete_button.pack(side=tk.LEFT)

        pdf_window.mainloop()



    def add_pdf(self):
        matiere = self.selected_matiere.get()

        file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            if not os.path.exists(self.matiere_paths[matiere]):
                os.makedirs(self.matiere_paths[matiere])

            file_name = os.path.basename(file_path)
            destination_path = os.path.join(self.matiere_paths[matiere], file_name)
            shutil.copy(file_path, destination_path)

            self.update_pdf_count_label()
            messagebox.showinfo("PDF added", "The PDF has been added to the subject.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFManagerApp(root)
    root.mainloop()
