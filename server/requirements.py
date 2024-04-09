import subprocess

# Define the package(s) you want to install
packages = ["flask","PyPDF2","transformers"]

# Run pip install command
for package in packages:
    subprocess.run(["pip", "install", package], check=True)