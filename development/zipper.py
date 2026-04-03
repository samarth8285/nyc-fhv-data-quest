import zipfile
import os

INCLUDE_PATHS = ["lambda/ingestion_lambda/", "src/", "development/"]
EXCLUDE_FILES = ["zipper.py", "data_explore.ipynb"]


def create_zip(zip_path="build/function.zip"):

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:

        for path in INCLUDE_PATHS:

            for root, _, files in os.walk(path):

                for file in files:

                    if file.endswith(".pyc") or file in EXCLUDE_FILES:
                        continue

                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath)
                    z.write(filepath, arcname)
