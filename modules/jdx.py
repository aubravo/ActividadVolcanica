#!/usr/bin/env python3

"""
JDX

Contains methods for handling JCamp-DX files and groups of files \
(.jdx files are used to store spectral data).

jcampdx.Reader class creates a file handler that contains a toolset \
for .jdx files: opening single files, open directories containing .jdx \
files, parsing, normalizing data, and unit conversion.

This is a work in progress and currently only handles the XYUNITS method.
"""

__version__ = '0.1.1'
__authors__ = 'Alvaro U. Bravo'
__license__ = 'MIT/X11 License'
__contact__ = 'Alvaro U. Bravo <alvaroubravo@gmail.com>'

import os
import re
import constant
import logging
import numpy as np

logging.basicConfig(level='INFO', format='%(asctime)s - %(pathname)s:\
%(lineno)d | %(funcName)s | %(message)s')


class Reader:
    """Allows handling of .jdx files"""

    def open(self, path):
        """Allows to open a file or directory containing .jdx files"""
        dircontent = self.checkpath(path)
        parsedblocks = []
        try:
            for filepath in dircontent:
                if (not self.checkfilename(filepath)):
                    logging.warning('{} could not be opened.'.format(filepath))
                else:
                    checked = self.checkfilecontent(filepath)
                    if checked != [None]:
                        print(checked[0]['TITLE'], len(checked[0]['XYDATA']))
                        parsedblocks.extend(checked)
                        logging.info('{} was opened and parsed correctly.'
                                     .format(filepath))
                    else:
                        logging.info('{} was not parsed correctly and will be ignored')
        except Exception as err:
            logging.error(err)
            raise
        return parsedblocks

    def parse(self, text):
        """Analyzes the contect of the text and if it matches Jcamp \
standards and returns a dictionary of extracted values."""
        commentFinder = re.compile(constant.re_findComments)
        dataFinder = re.compile(constant.re_findDataLabels)
        try:
            text = commentFinder.sub('', text)
            data = dict(dataFinder.findall(text))
            tags = ['TITLE']
            if not data['TITLE']:
                logging.error('Header data does not comply with \
jcamp standards.')
                raise
            if 'XYDATA' in data:
                normalized = self.normalize(self.xydata2array(data))
                if normalized != [None]:
                    return normalized
                else:
                    logging.error('Data could not be parsed or normalized')
                    return None
            else:
                logging.error('jdx.py only handles XYDATA types')
                raise

        except Exception as err:
            logging.error(err)
            raise

    def checkfilecontent(self, path):
        """Reviews if content is accessible and returns it parsed."""
        blockFinder = re.compile(constant.re_findBlocks)
        try:
            with open(path, 'r') as file:
                blocks = blockFinder.findall(file.read())
                if len(blocks) != 0:
                    return [self.parse(block) for block in blocks]
                else:
                    logging.warning('No JCamp Blocks found in file: {}'
                                    .format(path))
                    return None
        except Exception as err:
            logging.error(err)
            raise

    def checkpath(self, path):
        """Checks if the path exists, and if it references a directory \
or file"""
        if os.path.exists(path):
            if os.path.isfile(path):
                return [path]
            elif os.path.isdir(path):
                return [(path + filepath) for filepath in os.listdir(path)]
        else:
            logging.error('Referenced file or directory does not exist.')
            raise

    def checkfilename(self, path):
        """Checks if provided Filename mathches JCamp naming standards"""
        if path[-4:] != '.jdx':
            logging.warning('{} does not match JCamp naming standards.'
                            .format(path))
            return False
        else:
            return True

    def normalize(self, data, xunits='1/CM', yunits='TRANSMITTANCE'):
        """Checks and transforms given data to the specified x and y units"""
        if yunits in data['YUNITS'].upper():
            if xunits in data['XUNITS'].upper():
                return data
            else:
                logging.warning('jdx.py currently does not handle XUNITS \
conversion')
                return None
        else:
            logging.warning('jdx.py currently does not handle YUNITS \
conversion')
            return None

    def xydata2array(self, data):
        """Transforms Jcamp compressed XYData values into x,y tuples"""
        try:
            dataarray = []
            increment = (float(data['LASTX']) - float(data['FIRSTX'])) \
                / (float(data['NPOINTS'])-1)
            try:
                xfactor = float(data['XFACTOR'])
                yfactor = float(data['YFACTOR'])
            except:
                xfactor = 1
                yfactor = 1
            for x in data['XYDATA'].split('\n')[1:]:
                y = re.split(r'\s', x)
                for i in range(len(y) - 1):
                    dataarray.append([float(y[0])+i*increment*xfactor, float(y[i+1])*yfactor])
            data['XYDATA'] = np.rot90(np.array(dataarray))
            return data
        except Exception as err:
            logging.error(err)
            raise


if __name__ == '__main__':
    testdir = r'../data/'
    JP = Reader().open(testdir)
    from matplotlib import pyplot as plt
    for m in JP:
        plt.plot(m['XYDATA'][1], m['XYDATA'][0],
                 label=m["TITLE"] + " (" + m["MOLFORM"]+")")
    plt.xlabel("Ancho de banda (nm)")
    plt.ylabel("Transmitancia")
    plt.legend(loc='lower right')
    plt.show()
