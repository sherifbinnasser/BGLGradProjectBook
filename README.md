# BGL Grad Project Book

This repository contains the LaTeX source for the BGL graduate project book, plus supporting figures and assets.

## links

- Banner PDF: https://github.com/sherifbinnasser/BGLGradProjectBook/raw/main/assets/Banner.pdf
- Book PDF: https://github.com/sherifbinnasser/BGLGradProjectBook/raw/main/assets/Book.pdf
- Our GlucoAI App: https://github.com/sherifbinnasser/GlucoAI
- Our Diabetes Samples Collecting App: https://github.com/sherifbinnasser/DiabetesCollector

## Local build output

- Generated book PDF: `build/main.pdf`

## Build instructions

From the repository root:

```bash
./run.sh
```

Or manually:

```bash
pdflatex -shell-escape -output-directory=build main.tex
bibtex build/main
pdflatex -shell-escape -output-directory=build main.tex
pdflatex -shell-escape -output-directory=build main.tex
```

## Repository structure

- `main.tex` — main LaTeX entry point
- `assets/` — pre-built `Banner.pdf` and `Book.pdf`
- `chapters/` — chapter source files
- `figures/` — image assets used by the document
- `build/` — generated build artifacts
- `run.sh` — build script
