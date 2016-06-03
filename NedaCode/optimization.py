import numpy as np
from scipy import optimize

import StressFunctions
import importData


def getError(experimentalStress, modelStress):
    sampleNum = float(len(experimentalStress))
    difference = (experimentalStress - modelStress)**2
    sumDiff = np.sum(difference)
    rootMeanSquareError = np.sqrt(sumDiff/sampleNum)
    return rootMeanSquareError

def stressEvaluation(constants, args):
    modelStress = StressFunctions.getMooneyStress(args['experimentalStrain'], constants[0], constants[1], constants[2])
    error = getError(args['experimentalStress'], modelStress)
    return error

def _test():
    cfgFileName = 'MooneyInputs.cfg'
    importedData = importData.importMooneyConfigFile(cfgFileName)

    # Parse the constants into a 1x3 array. [c10, c11, c01]
    strainEnergyConstants = np.array([importedData[0], importedData[1], importedData[2]])

    # Parse the experimental data into a dictionary.
    experimentalData = {}
    experimentalData['experimentalStrain'] = importedData[3][:,0]
    experimentalData['experimentalStress'] = importedData[3][:,1]

    error = stressEvaluation(strainEnergyConstants, experimentalData)

    return

if __name__=='__main__':
    _test()