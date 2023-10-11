import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style

# Se crea la ventana principal
root = tk.Tk()
root.title("Notes App")
root.geometry("500x500")
style = Style(theme='journal')
style = ttk.Style()

# Configurar la fuente para que sea bold
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

# Crear el cuaderno para contener las notas
notebook = ttk.Notebook(root, style="TNotebook")

# Cargar las notas guardadas
notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass

# Crear el cuaderno para contener las notas
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Crear la funcion para agregar nuevas notas
def add_note():
    # Abrir una nueva pestaña
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text="New Note")
    
    # Crear los widgets para titulo y contenido
    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
    
    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)
    
    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
    
    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Crear la funcion para guardar las notas
    def save_note():
        # Obtener el titulo y contenido de las notas
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)
        
        # Añadir las notas al diccionario de notas
        notes[title] = content.strip()
        
        # Guardar el diccionario de notas al archivo
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        
        # Añadir la nota al cuaderno
        note_content = tk.Text(notebook, width=40, height=10)
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)
        
    # Añadir un boton de guardar a la nueva pestaña
    save_button = ttk.Button(note_frame, text="Save", 
                             command=save_note, style="secondary.TButton")
    save_button.grid(row=2, column=1, padx=10, pady=10)

def load_notes():
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)

        for title, content in notes.items():
            # Añadir la nota al cuaderno
            note_content = tk.Text(notebook, width=40, height=10)
            note_content.insert(tk.END, content)
            notebook.add(note_content, text=title)

    except FileNotFoundError:
        pass

# Llamar la funcion cargar notas cuando la app se inicie
load_notes()

# Create a function to delete a note
def delete_note():
    # Obtener el indice actual
    current_tab = notebook.index(notebook.select())
    
    # Obtener el titulo de la nota para eliminar
    note_title = notebook.tab(current_tab, "text")
    
    # Dialogo de confirmacion
    confirm = messagebox.askyesno("Delete Note", 
                                  f"Are you sure you want to delete {note_title}?")
    
    if confirm:
        # Remover la nota del cuaderno
        notebook.forget(current_tab)
        
        # Remover la nota del diccionario de notas
        notes.pop(note_title)
        
        # Guardar el diccionario de notas a los archivos
        with open("notes.json", "w") as f:
            json.dump(notes, f)

# Añadir botones a la ventana principal
new_button = ttk.Button(root, text="New Note", 
                        command=add_note, style="info.TButton")
new_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = ttk.Button(root, text="Delete", 
                           command=delete_note, style="primary.TButton")
delete_button.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()