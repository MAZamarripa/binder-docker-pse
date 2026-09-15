import importlib
import json
import os
import shutil
from pathlib import Path

import yaml

REPO_MANIFEST = Path(__file__).with_name("repos.yaml")
# TUTORIAL_MANIFEST = Path(__file__).with_name("tutorials.yaml")
# PSE Workshop: use the PSE Workshop manifest instead of the default tutorials manifest
TUTORIAL_MANIFEST = Path(__file__).with_name("tutorials_pse_workshop.yaml")


def create_directory(parent: Path, folder_name: str) -> Path:
    """Create a directory with the given folder_name under the parent directory. If the directory already exists, it will not raise an error.
    Returns the path to the created directory.
    """
    directory = parent / folder_name
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def copy_source(source: Path, destination: Path) -> Path:
    """Copy the source file or directory to the destination directory. If the source is a directory, it will copy all its contents recursively. If the source is a file, it will copy the file to the destination directory.
    Returns the path to the copied file or directory.
    """
    if not source.exists():
        raise FileNotFoundError(f"Source does not exist: {source}")

    target = destination / source.name
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        shutil.copy2(source, target)
    return target


def set_notebook_kernel(path: Path) -> None:
    """Set copied notebooks to use the image's registered Python kernel."""
    if path.suffix != ".ipynb":
        return

    with path.open("r", encoding="utf-8") as notebook_file:
        notebook = json.load(notebook_file)

    # Set the kernel spec to use the prommis kernel 
    notebook.setdefault("metadata", {})["kernelspec"] = {
        "display_name": "Python 3 (prommis)",
        "language": "python",
        "name": "python3",
    }

    with path.open("w", encoding="utf-8") as notebook_file:
        json.dump(notebook, notebook_file, indent=1)
        notebook_file.write("\n")


def load_manifest(path: Path) -> list:
    """Load a YAML manifest file and return its contents as a list of entries. Raises an error if the manifest does not contain a list.
    Returns the list of entries.
    """
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    if not isinstance(data, list):
        raise TypeError(f"Manifest {path.name} must contain a list of entries.")
    return data


def get_repo_base_path(repo_entry: dict) -> Path:
    """Get the base path of a repository entry. If the entry has a "path" key, it will return that path. If it has a "package" key, it will import the package and return its directory. If it has a "relative_path" key, it will append that to the base path.
    Returns the base path as a Path object.
    """
    if "path" in repo_entry:
        return Path(os.path.expandvars(repo_entry["path"]))

    package_name = repo_entry["package"]
    module = importlib.import_module(package_name)
    base_path = Path(module.__file__).resolve().parent
    relative_path = repo_entry.get("relative_path")
    if relative_path:
        return base_path / relative_path
    return base_path


def get_destination_path(root: Path, destination_spec: str) -> Path:
    """Get the destination path based on the root directory and the destination specification. The destination specification can be a relative path with multiple parts separated by "/". If the destination specification is empty, it will return the root directory.
    Returns the destination path as a Path object."""
    if not destination_spec:
        return root

    destination = root
    for part in str(destination_spec).split("/"):
        if part:
            destination = create_directory(destination, part)
    return destination


def main():
    home = Path.home()
    # Create the "PSE Models" directory in the home directory
    pse_models = create_directory(home, "PSE Models")

    repo_entries = {repo["name"]: repo for repo in load_manifest(REPO_MANIFEST)}

    for tutorial in load_manifest(TUTORIAL_MANIFEST):
        destination = get_destination_path(pse_models, tutorial.get("destination", ""))

        if tutorial.get("create_only"):
            continue

        if "path" in tutorial:
            source_path = Path(os.path.expandvars(tutorial["path"]))
        else:
            repo_name = tutorial.get("repo")
            source_rel = tutorial.get("source")
            if not repo_name or not source_rel:
                raise KeyError(
                    f"Tutorial {tutorial.get('name', '<unnamed>')} must define repo and source unless create_only is true."
                )

            if repo_name not in repo_entries:
                raise KeyError(
                    f"Tutorial {tutorial['name']} references unknown repo {repo_name!r}."
                )

            repo_entry = repo_entries[repo_name]
            source_path = get_repo_base_path(repo_entry) / source_rel
        copied_path = copy_source(source_path, destination)
        if copied_path.is_dir():
            for notebook_path in copied_path.rglob("*.ipynb"):
                set_notebook_kernel(notebook_path)
        else:
            set_notebook_kernel(copied_path)


if __name__ == "__main__":
    main()
