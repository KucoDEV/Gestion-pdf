
# KucoDEV (c) 2023
# https://github.com/KucoDEV

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
import os
import shutil
import platform

class PDFManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestionnaire de PDF")
        self.master.geometry("500x350")  # Taille de la fenêtre

        # Initialisation de la variable selected_matiere
        self.selected_matiere = tk.StringVar(self.master)
        self.selected_matiere.set('Matière 1')  # Sélection par défaut

        # Chemin vers les dossiers de chaque matière
        self.matiere_paths = {
            'Matière 1': './Matiere1',
            'Matière 2': './Matiere2',
            'Matière 3': './Matiere3',
            'Matière 4': './Matiere4',
            'Matière 5': './Matiere5',
            'Matière 6': './Matiere6'
        }

        # Définir l'icône de l'application (à modifier avec votre propre icône)
        icon_path = "icon.ico"
        self.master.iconbitmap(default=icon_path)

        # Interface graphique
        self.create_widgets()

    def create_widgets(self):
        # Labels pour l'affichage du nombre de PDF par matière
        tk.Label(self.master, text="Nombre de PDF par matière", font=("Arial", 12)).pack(pady=10)

        for matiere in self.matiere_paths:
            tk.Label(self.master, text=f"{matiere}: {self.count_pdfs_in_matiere(matiere)} PDF", font=("Arial", 10)).pack()

        # Liste déroulante pour sélectionner la matière
        matieres = list(self.matiere_paths.keys())
        matiere_menu = tk.OptionMenu(self.master, self.selected_matiere, *matieres)
        matiere_menu.pack(pady=10)

        # Bouton pour voir les PDF de la matière sélectionnée
        view_pdf_button = tk.Button(self.master, text="Voir les PDF de la matière", command=self.view_pdfs, font=("Arial", 12))
        view_pdf_button.pack(pady=10)

        # Bouton pour ajouter un PDF à la matière sélectionnée
        add_pdf_button = tk.Button(self.master, text="Ajouter un PDF à la matière", command=self.add_pdf, font=("Arial", 12))
        add_pdf_button.pack(pady=10)

    def count_pdfs_in_matiere(self, matiere):
        matiere_path = self.matiere_paths[matiere]
        return sum(1 for file in os.listdir(matiere_path) if file.lower().endswith('.pdf'))

    def update_pdf_count_label(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_widgets()

    def view_pdfs(self):
        matiere = self.selected_matiere.get()
        matiere_path = os.path.abspath(self.matiere_paths[matiere])

        # Ouvrir le dossier dans l'explorateur de fichiers
        if platform.system() == "Windows":
            os.startfile(matiere_path)
        elif platform.system() == "Darwin":
            os.system("open " + matiere_path)
        else:
            os.system("xdg-open " + matiere_path)

    def add_pdf(self):
        matiere = self.selected_matiere.get()

        # Sélectionner un fichier PDF depuis l'ordinateur
        file_path = filedialog.askopenfilename(title="Sélectionner un fichier PDF", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            # Vérifier si le dossier de la matière existe, sinon le créer
            if not os.path.exists(self.matiere_paths[matiere]):
                os.makedirs(self.matiere_paths[matiere])

            # Extraire le nom du fichier et copier dans le dossier de la matière
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(self.matiere_paths[matiere], file_name)
            shutil.copy(file_path, destination_path)

            # Mettre à jour le nombre de PDF et l'affichage
            self.update_pdf_count_label()
            messagebox.showinfo("PDF ajouté", "Le PDF a été ajouté à la matière.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFManagerApp(root)
    root.mainloop()
