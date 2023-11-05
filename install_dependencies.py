import subprocess
import sys

# List of dependencies to install
dependencies = [
    "flask",
    "mysql-connector-python",
    "python-dotenv",
    "docker",
]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    for dependency in dependencies:
        print(f"Installing {dependency}...")
        install(dependency)
    print("All dependencies have been installed.")
