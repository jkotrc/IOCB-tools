# A python script that cuts down the Gaussian output, leaving only issued commands and all the output following
# the command with freq=roa

import sys
import glob

path = sys.argv[1]

for filename in glob.glob(path): #allows wildcards (*) to work
    with open(filename, "r") as f:
        lines = iter(f.readlines())
        
    with open(filename+".condensed", "w") as f:
        roa = False
        for line in lines:
            if roa is True:
                f.write(line)
                continue;
            elif "#" in line.strip("\n"):
                f.write(line)
                f.write(lines.__next__())
                if "roa" in line.strip("\n"):
                    f.write(lines.__next__())
                    roa=True
        
            