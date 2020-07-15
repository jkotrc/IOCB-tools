"""
    file that lets you specify the torsion angles and the directory with all output files;
    making a directory structure: ./BPW91/num/
                                  ./B3LYP/num/
    runs xtorsion, reads its results, along with energies, into a csv file located at .
    
    USAGE: python xtorsion_helper.py <root directory>
"""
from sys import argv
import os
import glob
import re



class GaussianOutput:
    def __init__(self, segments, headers):
        #headers: look for line with hash tag, if present, read it and the next line and continue searching through the file until a line with a hash tag is foundroa
        #that makes a segment
        self.segments=segments
        self.headers=headers
        self.nSegments=len(segments);
        pass;
    def parse(string):
        segments=[]
        headers=[]
        inp = string.split("\n")
        
        header=True
        for i in range(0, len(inp)):
           line = inp[i]
           segment=""
           
           if "#" in line:
                if header:
                    header=False
                    header_text = line+inp[i+1]
                    headers.append(header_text)
                else:
                    header=True
                    segments.append(segment+inp[i])
                    segment=""
           else:
                if not header:
                    segment+=line
        
        ret = GaussianOutput(segments, headers);
        #print(f"DONE \n headers: {ret.headers}\n")
        #print(f"There were {len(ret.headers)} headers")
        return ret
    
    def fromFile(path):
        f=None
        try:
            f=open(path, "r")
        except:
            print(f"Failed to open GaussianOutput as {path}!")
            return None;
        inp=f.read()
        return GaussianOutput.parse(inp)
        

#print("TESTING on an output file.")
#out = GaussianOutput.fromFile("sample.out");
#exit()

if len(argv) != 2:
    print("USAGE: python xtorsion_helper.py <root directory>")
    exit()

root_directory = argv[1]

os.chdir(root_directory)

file_paths = glob.glob("*.out")

print(f"Using root directory {root_directory} with files:")
for file in file_paths:
    print(f"{file} that has index: {re.search('[0-9]+', file).group()}")



#num_torsion_angles = int(input("How many torsion angles?"))
#torsion_angle_names=[]
#for i in range(0, num_torsion_angles):
#    torsion_angle_names.append(input(f"Name angle {i}: "))

try:
    os.mkdir("BPW91")
    os.mkdir("B3LYP")
except:
    print("Directories already exist... Overwriting")

# def strip_to_roa(infile, sav, functional):
    # if "B3LYP" in functional:
        # print(functional)
        
    # foundroa=False
    # for line in f.readlines():
        # if ("#" in line):
            # print(line)
           
        # if ("#"+functional in line) and ("freq=roa"):
        
            # print("foundroa")
            
            # foundroa=True
            # sav.write(line)
        # elif (foundroa is True) and ("#" not in line):
            # sav.write(line)
        # elif (foundroa is True) and ("#" in line):
            # sav.write(line)
            # break



for file_path in file_paths:
    f = GaussianOutput.fromFile(file_path)
    idx = int(re.search('[0-9]+', file).group())
    print(idx)
    
    
    #######################
    os.chdir("BPW91")
    try:
        os.mkdir(str(idx))
    except:pass;
    os.chdir(str(idx))
    
    sav = open("roa.out", "w")
    
    for i in range(0, f.nSegments):
        print(i)
        header = f.headers[i]
        segment = f.segments[i]
        if ('BPW91' in header) and ('freq=roa' in header):
            sav.write(header+"\n")
            sav.write(segment)
            print(f"Written {header}")
            break;
        else:
            print(f"BPW91 is not present in: {header}")
    
    sav.close()
    
    os.chdir("..")
    #######################
    os.chdir("../B3LYP")
    try:
        os.mkdir(str(idx))
    except:pass;
    os.chdir(str(idx))
    
    sav = open("roa.out", "w")
    
    for i in range(0, f.nSegments):
        header = f.headers[i]
        segment = f.segments[i]
        if ('B3LYP' in header) and ("freq=roa" in header):
            sav.write(header+"\n")
            sav.write(segment)
            break;
    
    sav.close()
    
    os.chdir("../..")
    #########################
    #sav = open(file_path+".roa", "r")
    exit()
    



