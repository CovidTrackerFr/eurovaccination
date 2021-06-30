import json
import os


def pretty_1_json(filename):
    filer = open(filename, "r")
    jsonfile = json.load(filer)
    filer.close()
    formated = json.dumps(jsonfile, sort_keys=True, indent=4)
    filew = open(filename, "w")
    filew.write(formated)


def listfile(path: str):
    """
    Fonction qui va mettre dans une liste tous les fichiers dans le dossier actuel
    """
    f = [os.path.join(dp, f) for dp, _, fn in os.walk(
        os.path.expanduser(path)) for f in fn]
    return f


def pretty_all_json_files(path="."):
    """
    Fonction de formattage de tous les fichiers json de tous les sous-dossier
    """
    f = listfile(path)
    jsonfiles = [filename for filename in f if filename.endswith(".json")]
    for jsonfile in jsonfiles:
        pretty_1_json(jsonfile)
    return None
