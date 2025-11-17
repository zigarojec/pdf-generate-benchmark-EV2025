Repository includes code to create PDF files of various sizes, pages and layers for PDF to JPG conversion benchmarking. Results under "timing.log" are results of the PDFtoPPM conversions under seccomp sandboxed conversion. 

## Step 0:
For reproduction please refer also to https://github.com/zigarojec/staticpdftoppm-EV2025 to statically build the needed pdftoppm and lockdown binaries. 

## Step 1:
### Generate benchmark files
Go to one of the subfolders (e.g. createbenchmarkfiles_IMAGERENDERING) and run

`python createfiles_rendering.py`
This step will create a set of PDF files of varius sizes. 

## Step 2:
### Run and evaluate
Run 

`python runoverall.py`

This step will run lockdown sandbox, run the pdftoppm binary under the sandbox, take PDF files as the input and store the outputs (JPG files for each page) under the subfolder fith the same name as the input file. At the end of the conversion, a file timing.log will appear with the basic runtime timing info. 

