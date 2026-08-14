from pathlib import Path
import shutil
import idaes_examples
import prommis

home = Path.home()
# create all of the folders
basic_examples = home / "Basic Examples"
flowsheets = home / "Flowsheets"
integrated_process_design_and_market_interactions = home / "Integrated Process Design and Market Interactions"

# ...  for the other folders

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
source_destination_dict = {
    (idaes_source / "core" / "hda_flowsheet.ipynb") :  basic_examples
    
}

# then we copy from from the source to the destination
for source, destination in source_destination_dict.items():
    shutil.copy2(source, destination)

