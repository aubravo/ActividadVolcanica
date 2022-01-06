import JcampReader.fileHandler as handler
import numpy as np

def parser (filename):
    ToParse = handler.read(filename)
    ArgList = ToParse.split("##")
    ArgList.remove("")
    Parameters =dict()
    for x in ArgList:
        try:
            y = x.split("=")
            if y[0] != "XYDATA":
                Parameters[y[0].replace("\n","")] = y[1].replace("\n","")
            else:
                Parameters[y[0].replace("\n","")] = y[1]
        except:
            pass
    return Parameters

def normalize (data):
    if "TRANSMITTANCE" in data["YUNITS"].upper():
        data_array_ = np.rot90(np.array(toarray(data) ))
        if data["XUNITS"].upper() == "MICROMETERS":
            data_array_[1] = data_array_[1]*1000
        elif data["XUNITS"].upper() == "NANOMETERS":
            pass
        elif data["XUNITS"].upper() == "1/CM":
            data_array_[1] = 10000000/data_array_[1]
        return data_array_
    else:
        print ("No data to normalize")

def toarray (data):
    data_array=[]
    increment = (float(data["LASTX"])-float(data["FIRSTX"]))/(float(data["NPOINTS"])-1)
    data_set = data["XYDATA"].split("\n")
    if "X++(Y..Y)" in data_set[0]:
        for x in data_set[1:]:
            y = x.split(" ")
            for i in range (len(y)-1):
                data_array.append([float(y[0])+i*increment, float(y[i+1])])
    return data_array

if __name__ == '__main__':
    pass
