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


# then we copy from from the source to the destination
# hda flowsheet example 
# copy from idaes to basic examples
shutil.copy2((idaes_source / "core" / "hda_flowsheet.ipynb"), basic_examples)
