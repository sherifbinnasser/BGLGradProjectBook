#!/bin/bash

# 1. Force-create the build directory if it doesn't exist
mkdir -p build

# 1. إنشاء المجلد الفرعي المطلوب داخل مجلد الـ build
mkdir -p build/chapters

# 2. Run Pass 1
pdflatex -shell-escape -output-directory=build main.tex

# 3. Run BibTeX on the build folder
bibtex build/main

# 4. Run Pass 2 & 3 to lock in citations and page numbers
pdflatex -shell-escape -output-directory=build main.tex
pdflatex -shell-escape -output-directory=build main.tex