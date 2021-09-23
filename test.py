
import JcampReader.fileParser as parser
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import os

path_ = "JcampReader/IR/"
files_ = os.listdir(path_)

colors = cm.rainbow(np.linspace(0,1,len(files_)))

for file_, c in zip(files_,colors) :
    try:
        print(file_)
        data=parser.parser(path_+file_)
        if "TRANSMITTANCE" in data["YUNITS"].upper():
            data_array_ = np.rot90(np.array( parser.toarray(data) ))
            names = ["X,Y"]
            plt.plot(data_array_[1],data_array_[0], color = c, label = data["TITLE"] + " (" + data["MOLFORM"] + ")" )
    except:
        print(data)
        raise
plt.legend(loc='lower right')
plt.show()
