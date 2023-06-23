# Run after annotating all the box files generated from boxfiles.py
# https://github.com/nguyenq/jTessBoxEditor/releases/tag/Release-2.3.1 can be used for annotating.

import os
import subprocess
srcdir = 'data'
destdir = 'trainfiles'
output = 'trainoutput'

# Removing all previous trained files.
try:
    os.remove('tessdata/eng.traineddata')
except OSError:
    pass
files = os.listdir(srcdir)
for item in files:
    if not item.endswith(('.jpg', '.box')):
        os.remove(os.path.join(srcdir, item))

# Generating the tuples of filenames
files = os.listdir(srcdir)
jpgs = [x for x in files if x.endswith('.jpg')]
boxes = [x for x in files if x.endswith('.box')]
trainfiles = list(zip(jpgs, boxes))

# generating TR files and unicode charecter extraction
unicharset = f"unicharset_extractor --output_unicharset {destdir}/unicharset "
unicharset_args = f""
errorfiles = []
for image, box in trainfiles:
    unicharset_args += f"{box} "
    if os.path.isfile(f"{destdir}/{image[:-4]}.tr"):
        continue
    try:
        os.system(
            f"tesseract {srcdir}/{image} {destdir}/{image[:-4]} nobatch box.train")
    except:
        errorfiles.append((image, box))

os.system(unicharset+unicharset_args[:-1])

# Creating font properties file
with open(f"{destdir}/font_properties", 'w') as f:
    f.write("ocrb 0 0 0 1 0")

# # Getting all .tr files and training
trfiles = [f for f in os.listdir(destdir) if f.endswith('.tr')]

os.chdir(destdir)
mftraining = f"mftraining -F font_properties -U unicharset -O ../{output}/eng.unicharset -D ../{output}"
cntraining = f"cntraining -D ../{output}"
for file in trfiles:
    mftraining += f" {file}"
    cntraining += f" {file}"

os.system(mftraining)
os.system(cntraining)
os.chdir('../')

# # Renaming training files and merging them
os.chdir(output)
os.rename('inttemp', 'eng.inttemp')
os.rename('normproto', 'eng.normproto')
os.rename('pffmtable', 'eng.pffmtable')
os.rename('shapetable', 'eng.shapetable')
os.system(f"combine_tessdata eng.")
os.chdir('../')

# Writing log file
if len(errorfiles) == 0:
    errorfiles.append(('no', 'Error'))
with open('scripts/logs.txt', 'w') as f:
    f.write('\n'.join('%s %s' % x for x in errorfiles))
