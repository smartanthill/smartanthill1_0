import os

from fabric.api import local, task


@task(default=True)
def docs():
    docsuml2png()
    local('make -C docs/ html')


@task
def docsuml2png():
    modified_umls = []
    for f in os.listdir("docs/_diagrams"):
        uml_path = os.path.join("docs/_diagrams", f)
        png_path = os.path.join("docs/_static/diagrams", f[0:-4] + ".png")
        if not os.path.isfile(uml_path) or not uml_path.endswith(".uml"):
            continue
        if (
            not os.path.exists(png_path)
            or os.path.getmtime(uml_path) > os.path.getmtime(png_path)
        ):
            modified_umls.append(uml_path)

    if modified_umls:
        local(" ".join(['plantuml', '-o ../_static/diagrams'] + modified_umls))
