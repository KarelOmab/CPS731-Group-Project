import subprocess
import webbrowser
import os

def run_coverage_tests():
    # Run the tests with coverage
    subprocess.run(['coverage', 'run', '-m', 'unittest', 'discover'])

    # Generate a coverage report in the terminal
    subprocess.run(['coverage', 'report'])

    # Generate an HTML coverage report
    subprocess.run(['coverage', 'html'])

    # Open the HTML report in the default web browser
    report_file_path = os.path.abspath(os.path.join('htmlcov', 'index.html'))
    webbrowser.open('file://' + report_file_path)

if __name__ == '__main__':
    run_coverage_tests()
