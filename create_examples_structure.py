from pathlib import Path
import shutil
import idaes_examples
import prommis

def create_directory(folder_name):
    new_folder = Path(Path().home() / folder_name)
    new_folder.mkdir(parents=True, exist_ok=True)
    return new_folder

home = Path.home()

# create the folders that the user will see
parent_folders = [
    "Basic Examples", 
    "Flowsheets", 
    "Integrated Process Design and Market Interactions"
]

parent_folder_paths = {
    parent_folder : create_directory(parent_folder) for parent_folder in parent_folders
}

# these define paths on the system where the examples live
idaes_source = (
    Path(idaes_examples.__file__).parent
    / "notebooks"
    / "docs"
    / "tut"
)

prommis_source = (
    Path(prommis.__file__).parent
    / "examples"
)

# programmatic way to do the file structure
# dictionary of source path keys and destination folder values
# you just need to augment this dictionary with a map of 
# the source of the file and its final destination
source_destination_dict = {
    (idaes_source / "core" / "hda_flowsheet.ipynb") :  parent_folder_paths["Basic Examples"]
    
}

# then we copy from from the source to the destination
for source, destination in source_destination_dict.items():
    shutil.copy2(source, destination)

