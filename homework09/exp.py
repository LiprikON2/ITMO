import pathlib

def index_subfolders(folder, child):
    """ Returns subfolders - list of (name, sha) - of specified folder, that are in mygit index """
    subfolders = []
    if pathlib.Path(folder) in pathlib.Path(child).parents:
        subfolders.append((child))
    return subfolders

print(index_subfolders('folder', 'folder/example.txt'))
print(index_subfolders('folder', 'folder/example.txt'))