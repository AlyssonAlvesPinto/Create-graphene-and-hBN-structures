import tkinter as tk
from tkinter import messagebox
from pymatgen.core import Lattice, Structure
from ase import Atoms
from ase.visualize import view

def save_structure(structure, output_name):
    """
    Save the structure in CIF and VASP formats.
    """
    # Save as CIF
    structure.to(fmt='cif', filename=f'{output_name}.cif')
    print(f"Structure saved as {output_name}.cif")

    # Save as VASP
    structure.to(fmt='poscar', filename=f'{output_name}.vasp')
    print(f"Structure saved as {output_name}.vasp")


def create_graphene_structure(size=(1, 1, 1), output_name='graphene'):
    """
    Creates a graphene structure.
    """
    a = 2.46  # Lattice constant in Ångströms
    lattice = Lattice.hexagonal(a, a * 2.5)
    species = ["C", "C"]
    positions = [
        [1/3, 2/3, 0.0],
        [2/3, 1/3, 0.0]
    ]
    structure = Structure(lattice, species, positions) * size
    save_structure(structure, output_name)
    
    # Convert pymatgen structure to ASE Atoms
    ase_structure = Atoms(
        symbols=[str(s) for s in structure.species],
        positions=structure.cart_coords,
        cell=structure.lattice.matrix,
        pbc=True
    )
    return ase_structure

def create_hbn_structure(size=(1, 1, 1), output_name='hBN'):
    """
    Creates a hBN (hexagonal boron nitride) structure.
    """
    a = 2.50
    c = 6.66
    lattice = Lattice.hexagonal(a, c)
    species = ["B", "N"]
    positions = [
        [1/3, 2/3, 0.0],
        [2/3, 1/3, 0.0]
    ]
    structure = Structure(lattice, species, positions) * size
    save_structure(structure, output_name)

    ase_structure = Atoms(
        symbols=[str(s) for s in structure.species],
        positions=structure.cart_coords,
        cell=structure.lattice.matrix,
        pbc=True
    )
    return ase_structure

def generate_structure():
    material_type = material_var.get()
    size_x = int(size_x_entry.get())
    size_y = int(size_y_entry.get())
    size_z = int(size_z_entry.get())
    output_name = output_name_entry.get()

    try:
        if material_type == "Graphene":
            ase_structure = create_graphene_structure(size=(size_x, size_y, size_z), output_name=output_name)
        elif material_type == "hBN":
            ase_structure = create_hbn_structure(size=(size_x, size_y, size_z), output_name=output_name)
        else:
            raise ValueError("Invalid material type selected.")
        
        view(ase_structure)
        messagebox.showinfo("Success", f"{material_type} structure generated and saved as {output_name}.cif and {output_name}.vasp")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Interface
root = tk.Tk()
root.title("2D Material Generator")

material_label = tk.Label(root, text="Select Material:")
material_label.grid(row=0, column=0, padx=10, pady=5)

material_var = tk.StringVar(value="Graphene")
material_dropdown = tk.OptionMenu(root, material_var, "Graphene", "hBN")
material_dropdown.grid(row=0, column=1, padx=10, pady=5)

size_label = tk.Label(root, text="Supercell Size (x, y, z):")
size_label.grid(row=1, column=0, padx=10, pady=5)

size_x_entry = tk.Entry(root, width=5)
size_x_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
size_x_entry.insert(0, "1")

size_y_entry = tk.Entry(root, width=5)
size_y_entry.grid(row=1, column=2, padx=(0, 10), pady=5)
size_y_entry.insert(0, "1")

size_z_entry = tk.Entry(root, width=5)
size_z_entry.grid(row=1, column=3, padx=(0, 10), pady=5)
size_z_entry.insert(0, "1")

output_name_label = tk.Label(root, text="Output Filename Prefix:")
output_name_label.grid(row=2, column=0, padx=10, pady=5)

output_name_entry = tk.Entry(root, width=15)
output_name_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5)
output_name_entry.insert(0, "material_structure")

generate_button = tk.Button(root, text="Generate Structure", command=generate_structure)
generate_button.grid(row=3, column=0, columnspan=4, pady=10)

root.mainloop()
