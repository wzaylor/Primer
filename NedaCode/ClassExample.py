import numpy as np
import matplotlib.pyplot as plt

class MooneyStressCalculation(object):
    def __init__(self, experimentalStretch):
        """
        Comments should be here. For clarity while teaching, comments have been removed.
        """
        self.stretches = experimentalStretch #: Stretches used to calculate stress (uniaxial stretch)
        self.c10 = None #: A constant in the strain energy function.
        self.c11 = None #: A constant in the strain energy function.
        self.c01 = None #: A constant in the strain energy function.

    def getStress(self):
        """
        Comments should be here. For clarity while teaching, comments have been removed.
        """
        stress = np.zeros(len(self.stretches))  # Initialize a zeros array for the stress, 1xn

        for i in range(len(stress)):
            # Get the first and second invariant with the ith entry in the given stretches array.
            I1 = self.getMooneyI1(self.stretches[i])
            I2 = self.getMooneyI2(self.stretches[i])

            # Calculate the partial derivative of the strain energy function with respect to the first and second invariants.
            dwdI1 = self.c10 + self.c11 * (I2 - 3.0)
            dwdI2 = self.c01 + self.c11 * (I1 - 3.0)

            # Calculate hydrostatic pressure.
            hydroPressure = (2.0 / self.stretches[i]) * (dwdI1 + dwdI2 * (I1 - (1.0 / float(self.stretches[i]))))

            # Calculate the 2nd PK stress in the axial direction
            pk2Stress = -hydroPressure / float(self.stretches[i]) + 2.0 * (dwdI1 + dwdI2 * (I1 - self.stretches[i] ** 2))

            # Calculate the Cauchy stress
            stress[i] = pk2Stress * self.stretches[i] ** 2
        return stress

    def getMooneyI1(self, stretch):
        """
        Comments should be here. For clarity while teaching, comments have been removed.
        """
        I1 = stretch ** 2 + 2.0 * (1.0 / float(stretch))
        return I1

    def getMooneyI2(self, stretch):
        """
        Comments should be here. For clarity while teaching, comments have been removed.
        """
        I2 = (1.0 / stretch ** 2) + 2.0 * stretch
        return I2

def _test():
    # Import the stressStrain data
    stressStrain = np.genfromtxt('data05.csv', delimiter=',', skip_header=1)
    experimentalStretches = stressStrain[:,0] + 1

    # Define the variable 'mooney' as an instance of the MooneyStressCalculation class
    mooney1 = MooneyStressCalculation(experimentalStretches)
    # mooney = MooneyStressCalculation(stressStrain[:,0] + 1, stressStrain[:,1]) # Demonstrate that we don't need to define experimentalStrain or experimentalStress

    # Define the constants in the mooney1 class
    mooney1.c10 = 10.5
    mooney1.c11 = 0.4
    mooney1.c01 = 36

    # Get the stress from the mooney1 class
    mooney1Stress = mooney1.getStress()

    mooney2 = MooneyStressCalculation(experimentalStretches)
    # Define the constants in the mooney2 class
    mooney2.c10 = 1.9
    mooney2.c11 = 6.8
    mooney2.c01 = 0.05

    # Get the stress from the mooney2 class
    mooney2Stress = mooney2.getStress()

    stressPlot(experimentalStretches, mooney1Stress, mooney2Stress)
    return

def _testEfficient():
    print "Let's make the _test() function more efficient.\n" \
          "Do we need two instances of the MooneyStressCalculation to make that plot?"
    return

def stressPlot(stretches, stress1, stress2):
    fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.plot(stretches, stress1, color='r', label='Stress1')
    ax.plot(stretches, stress2, color='g', label='Stress2')
    ax.legend(loc='upper left')
    plt.show()
    return

if __name__=='__main__':
    _test()
    _testEfficient()