# Imports
import os
import shutil
from html_gen import generate_pages_recursive

def main():
    generate_pages_recursive('./content', './template/template.html', './public')

def setup():
    #Check for required static directory
    if not os.path.exists('./static'):
        raise Exception("Missing static folder")

    #Check for the public directory, delete if it exists, then recreate with a copy of static
    if os.path.exists('./public'):
        shutil.rmtree('./public')
    shutil.copytree('./static', './public')


setup()
main()