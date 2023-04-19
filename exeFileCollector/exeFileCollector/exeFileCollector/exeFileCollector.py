import psutil
#import psutil.Process
import os
import shutil
import subprocess
import sys
import re


slah="/"


def memDumpLinux(pathToSave,pid):    
    try:
        # maps contains the mapping of memory of a specific project
        map_file = f"/proc/{pid}/maps"
        mem_file = f"/proc/{pid}/mem"

        # output file
        out_file = pathToSave+f'{pid}.dump'

        # iterate over regions
        with open(map_file, 'r') as map_f, open(mem_file, 'rb', 0) as mem_f, open(out_file, 'wb') as out_f:
            for line in map_f.readlines():  # for each mapped region
                m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r])', line)
                if m.group(3) == 'r':  # readable region
                    start = int(m.group(1), 16)
                    end = int(m.group(2), 16)
                    mem_f.seek(start)  # seek to region start
                    print(hex(start), '-', hex(end))
                    try:
                        chunk = mem_f.read(end - start)  # read region contents
                        out_f.write(chunk)  # dump contents to standard output
                    except OSError:
                        print(hex(start), '-', hex(end), '[error,skipped]', file=sys.stderr)
                        continue
        #print(f'Memory dump saved to {out_file}')
    except:
        pass
    


def saveFileinPath(pathToSave,filePath):
    dest=pathToSave+os.path.basename(filePath)
    try:
        shutil.copy(filePath,dest)
    except:
        pass
def moveFileinPath(pathToSave,filePath):
    dest=pathToSave+os.path.basename(filePath)
    try:
        shutil.move(filePath,dest)
    except:
        pass

def saveProcessModule(pathToSave,process =psutil.Process()):
    dllList=process.memory_maps(grouped=True)
    for dll in dllList:
        saveFileinPath(pathToSave,dll.path)



def saveProcessFiles(pathToSave):
    ProcdumpWin=os.path.join(os.path.dirname(__file__),"Procdump","procdump.exe")
    print(ProcdumpWin)
    allpid=psutil.pids()
    for pid in allpid:
        try:
            process= psutil.Process(pid)
            print("processing {",process.exe(),"}")
            pathToSaveEXE=pathToSave+os.path.basename(process.exe())+"/"
            try:
                os.mkdir(pathToSaveEXE)
            except OSError as error:
                pass
            saveFileinPath(pathToSaveEXE,process.exe())
            saveProcessModule(pathToSaveEXE,process)

            if "lin" in sys.platform:
                memDumpLinux(pathToSaveEXE,pid)
            else:
                stdoutDump=subprocess.run(ProcdumpWin+" -ma " + str(pid),stdout=subprocess.PIPE)
                
                stdoutDump2=str(stdoutDump.stdout)
                stdoutDump2=stdoutDump2.replace("\\\\","\\")
                
                match=re.search(".?:\\\\.*dmp" , stdoutDump2)
                if match:
                    moveFileinPath(pathToSaveEXE,match.group())


        except Exception as err:
            print(err)

def main():
    if "win" in sys.platform:
        import  ctypes 

    dumpFileLocation=os.path.dirname(__file__)+"\\tmp\\"
    print("Dump File Location: "+dumpFileLocation)
    saveProcessFiles(dumpFileLocation)

if __name__ == '__main__':
    main()
    psutil.Process


