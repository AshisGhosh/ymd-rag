import os
import subprocess
from subprocess import Popen, PIPE
import time



def convert_doc_to_pdf(doc_filename, pdf_filename):
    pdf_dir = os.path.dirname(pdf_filename)
    p = Popen(['soffice', '--headless', '--convert-to', 'pdf', doc_filename, '--outdir', pdf_dir], stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        print("Couldn't convert to following file: %d %s %s" % (doc_filename, output, error))


def convert_docx_to_pdf(source_path, target_path):
    """Converts a DOCX file to PDF using pandoc."""
    try:
        command = ['pandoc', source_path, '-o', target_path]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {source_path} to PDF: {e}")

def walk_and_convert(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        print(f"Processing directory: {root}")
        print("Number of files: ", len(files))
        for i,file in enumerate(files):
            print(f"Processing file: {i+1}/{len(files)} {file}")

            if file.endswith(tuple([".doc", ".docx", ".txt"])):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, source_dir)
                target_path = os.path.join(target_dir, relative_path)
                target_path = os.path.splitext(target_path)[0] + '.pdf'

                # Ensure target directory exists
                os.makedirs(os.path.dirname(target_path), exist_ok=True)

                print(f"Converting: {source_path} to PDF")
                convert_doc_to_pdf(source_path, target_path)

            if file.endswith(".pdf"):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, source_dir)
                target_path = os.path.join(target_dir, relative_path)
                print(f"Copying: {source_path} to {target_path}")
                
                # Ensure target directory exists
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                print(f"Copying: {source_path} to {target_path}")
                os.system(f"cp '{source_path}' '{target_path}'")


PROCESSED_DATA_DIR = "data/processed_data"  # directory containing the documents
RAW_DATA_DIR = "data/raw_data"  # directory containing the documents  

if __name__ == "__main__":
    start_time = time.time()
    print("Starting conversion")
    walk_and_convert(RAW_DATA_DIR, PROCESSED_DATA_DIR)
    print(f"Conversion finished in {time.time() - start_time} seconds")