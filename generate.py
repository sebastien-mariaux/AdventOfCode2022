import os
import shutil

def generate(day):
    new_folder = f"day_{day}" 
    new_file = f"{new_folder}/day_{day}.py"
    os.mkdir(new_folder)
    shutil.copyfile("template.py", new_file)
    open(f"{new_folder}/data.txt", "x")
    open(f"{new_folder}/sample_data.txt", "x")

    f = open("days.txt", "a")
    f.write(f"\n{str(day)}")



f = open("days.txt", "r")
day = int(f.readlines()[-1])
generate(day + 1)
