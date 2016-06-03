import numpy as np

def importNeoHookeanConfigFile(fileName):
    """
    Read the config file and return the necessary variables.

    NOTE: This function can be made more flexible/intricate.
    This function demonstrates one way of reading a file, and searching the lines for special characters.
    Other methods can be employed to import data from text files.

    This is a basic file reader. Values defined after the colon (:) will be variables.
    Lines with variables must start with * followed by the variable name.

    The variable names are hard coded in this function.

    This function also assumes that file containing stress-strain data is a two column csv file
    where the first line is a header.

    mu: float
    stress strain file name: string - The file name of the csv file which contains the measured stretches.

    example cfg file:

        Here is a very good description of this cfg file.
        There are so many descriptive statements about this file's use and such.
        Words words words.

        *mu: 0.2
        *stress strain file name: ..\someFolder\dataSet01.csv

    :param fileName: string, The path to the config file.
    :return: list [float, nx2 array], The specified mu value and the stress-strain data.
    """
    # Initialize the value to be returned
    mu = None
    stressStrain = None

    # Open the file as a list of strings. Using 'with' statement means the file is automatically closed at the end of the code block.
    with open(fileName, mode='r') as fl:
        lines = fl.readlines()

    # Iterate over the lines
    for line in lines:
        # If '*' does not start the line, then advance to the next iteration.
        if line[0] != '*':
            continue # Advance to the next iteration.

        # If the line contains '*mu'
        if '*mu' in line:
            data = line.split(':') # Make the line into a list. Entries are separated by ':'
            mu = float(data[1])

        elif '*stress strain file name' in line:
            data = line.split(':')  # Make the line into a list. Entries are separated by ':'
            stressStrainFileName = data[-1] # Define the stress strain file name as the last entry in the data list.
            stressStrainFileName = stressStrainFileName.strip() # Take off any spaces in the file name, and overwrite the stressStrainFileName variable

            stressStrain = np.genfromtxt(stressStrainFileName, delimiter=',', skip_header=1)
    return mu, stressStrain

def importMooneyConfigFile(fileName):
    """
    Read the config file and return the necessary variables.

    NOTE: This function can be made more flexible/intricate.
    This function demonstrates one way of reading a file, and searching the lines for special characters.
    Other methods can be employed to import data from text files.

    This is a basic file reader. Values defined after the colon (:) will be variables.
    Lines with variables must start with * followed by the variable name.

    The variable names are hard coded in this function.

    This function also assumes that file containing stress-strain data is a two column csv file
    where the first line is a header.

    mu: float
    stress strain file name: string - The file name of the csv file which contains the measured stretches.

    example cfg file:

        Here is a very good description of this cfg file.
        There are so many descriptive statements about this file's use and such.
        Words words words.

        *c10: 0.7
        *c11: 17.6
        *c01: 3.9
        *stress strain file name: ..\someFolder\dataSet01.csv

    :param fileName: string, The path to the config file.
    :return: list [float, float, float, nx2 array], The specified constants and the stress-strain data. [c10, c11, c01, stressStrain]
    """
    # Initialize the value to be returned
    c10 = None
    c11 = None
    c01 = None
    stressStrain = None

    # Open the file as a list of strings. Using 'with' statement means the file is automatically closed at the end of the code block.
    with open(fileName, mode='r') as fl:
        lines = fl.readlines()

    # Iterate over the lines
    for line in lines:
        # If '*' does not start the line, then advance to the next iteration.
        if line[0] != '*':
            continue # Advance to the next iteration.

        # If the line contains '*mu'
        if '*c10' in line:
            data = line.split(':') # Make the line into a list. Entries are separated by ':'
            c10 = float(data[1])

        elif '*c11' in line:
            data = line.split(':')  # Make the line into a list. Entries are separated by ':'
            c11 = float(data[1])

        elif '*c01' in line:
            data = line.split(':')  # Make the line into a list. Entries are separated by ':'
            c01 = float(data[1])

        elif '*stress strain file name' in line:
            data = line.split(':')  # Make the line into a list. Entries are separated by ':'
            stressStrainFileName = data[-1] # Define the stress strain file name as the last entry in the data list.
            stressStrainFileName = stressStrainFileName.strip() # Take off any spaces in the file name, and overwrite the stressStrainFileName variable

            stressStrain = np.genfromtxt(stressStrainFileName, delimiter=',', skip_header=1)
    return c10, c11, c01, stressStrain

def writeStressData(fileName, stress, strain):
    """
    Write a text file with strain in the first column and stress in the second column.
    The corresponding column will have a header of 'stress' or 'strain'
    This script assumes that stress and strain are arrays with the same number of indicies.
    This script also assumes that the indicies in the stress array correspond to the indicies in the strain array,
    i.e. stress[i] corresponds with strain[i]

    :param fileName: string, The file name of the desired text file to be written
    :param stress: 1xn or nx1 array, An array of floats that will be written in the 'stress' column
    :param strain: 1xn or nx1 array, An array of floats that will be written in the 'strain' column
    :return:
    """
    textBlock = '' # Initialize an empty string. This will be one long string that gets written to the desired fileName
    textBlock += '{}, {}\n'.format('strain', 'stress') # The column heading

    for i in range(len(stress)):
        line = '{}, {}\n'.format(strain[i], stress[i])
        textBlock += line # Append the line to the end of the textBlock string

    with open(fileName, mode='w') as fl:
        fl.write(textBlock)
    return

def _testImportNeoHookeanConfigFile():
    import matplotlib.pyplot as plt
    cfgFilename = 'NeoHookeanInputs.cfg'

    mu, stressStrain = importNeoHookeanConfigFile(cfgFilename)
    plt.plot(stressStrain[:,0], stressStrain[:,1])
    plt.show()
    return

def _testWriteStressData():
    fileName = 'testOutput.txt'
    stress = np.array([1,2,3,4])
    strain = np.array([5,6,7,8])
    writeStressData(fileName, stress, strain)
    return

if __name__=='__main__':
    _testImportNeoHookeanConfigFile()
    # _testWriteStressData()