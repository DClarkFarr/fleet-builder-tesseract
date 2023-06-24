# reads all the image files present in data dir and creates corresponding box files.
# Files need to have the correct naming convention.
import os
os.chdir('data')
number_of_files = len(os.listdir('./'))
for i in range(0, number_of_files):
    os.system(
        f"tesseract eng.fleet.exp{i}.jpg eng.fleet.exp{i} batch.nochop makebox")
