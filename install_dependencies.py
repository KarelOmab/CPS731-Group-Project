import subprocess
import sys

# List of dependencies to install
dependencies = [
    "flask",
    "mysql-connector-python",
    "python-dotenv",
    "docker",
    "coverage",         #for testing
    "beautifulsoup4"    #for testing
]

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except:
        pass

if __name__ == "__main__":
    for dependency in dependencies:
        print(f"Installing {dependency}...")
        install(dependency)
    print("All dependencies have been installed.")
