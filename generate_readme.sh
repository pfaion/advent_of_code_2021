#!/bin/bash

rm -rf README_files
jupyter nbconvert notebook.ipynb --to markdown --output README.md