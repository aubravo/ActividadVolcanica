import sys

def read(filename):
    try:
        OpenedFile = open(filename,"r")
    except OSError as err:
        print('Error opening file', err)
        raise
    """
    Do file verification
    """
    CheckedFile = OpenedFile.read()
    OpenedFile.close()
    return CheckedFile

def save(filename,file):
    try:
        WriteFile = open(filename,"w")
    except:
        print ('Error creating or opening file', err)
        raise
    try:
        WriteFile.write(file)
    except:
        print('Error writing into file', err)
        raise
    WriteFile.close()
        
if __name__ == '__main__':
    pass