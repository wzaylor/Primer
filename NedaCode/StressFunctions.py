import numpy as np

def getNeoHookeanStress(stretches, mu):
    """
    Calculate axial stress from the stretch in the axial direction. This assumes uniaxial loading.

    stress11 = mu*(stretch**2 - 1/stretch)

    :param stretches: array nx1, The stretch of the material in the uniaxial direction.
    :param mu: float, Constant in the Neo-Hookean model
    :return: array nx1, The calculated stress at each stretch.
    """
    stress = np.zeros(len(stretches)) # Initialize a zeros array for the stress, 1xn

    # Iterate over the streches and calculate the stress
    for i in range(len(stress)):
        term1 = stretches[i]**2 # Define term1 with the ith entry in stretches.
        term2 = 1.0/float(stretches[i]) # Define term 2. Also make sure stretches[i] is a float before dividing.

        stress[i] = mu*(term1 - term2) # Calculate the ith term in stress. This overwrites the initial zero value.
        # stress[i] = mu*(stretches[i]**2 - (1.0/float(stretches[i]))) # The same stress value calculated in one line.

    return stress

def getMooneyStress(stretches, c10, c11, c01):
    """
    Calculate axial stress from the stretch in the axial direction. This assumes uniaxial loading and incompressibility.
    I don't know the strain energy function that is being used...

    Pk2Stress11 = p/stretch**2 + 2*[(dw/dI1) + (dw/dI2)(I1 - 1/stretch)]

    CauchyStress = Pk2Stress11*stretch**2

    :param stretches: 1xn array, The axial stretches.
    :param c10: float, Constants in the strain energy function. I don't know what this function is.
    :param c11: float, Constants in the strain energy function. I don't know what this function is.
    :param c01: float, Constants in the strain energy function. I don't know what this function is.
    :return: 1xn array, The Cauchy stress calculated from the given stretches and constants.
    """
    stress = np.zeros(len(stretches)) # Initialize a zeros array for the stress, 1xn

    for i in range(len(stress)):
        # Get the first and second invariant with the ith entry in the given stretches array.
        I1 = getMooneyI1(stretches[i])
        I2 = getMooneyI2(stretches[i])

        # Calculate the partial derivative of the strain energy function with respect to the first and second invariants.
        dwdI1 = c10 + c11*(I2 - 3.0)
        dwdI2 = c01 + c11*(I1 - 3.0)

        # Calculate hydrostatic pressure.
        hydroPressure = (2.0/stretches[i])*(dwdI1 + dwdI2*(I1 - (1.0/float(stretches[i]))))

        # Calculate the 2nd PK stress in the axial direction
        pk2Stress = -hydroPressure/float(stretches[i]) + 2.0*(dwdI1 + dwdI2*(I1 - stretches[i]**2))

        # Calculate the Cauchy stress
        stress[i] = pk2Stress*stretches[i]**2
    return stress

def getMooneyI1(stretch):
    """
    Calculate I1 from a given stretch for the getMooneyStress function.
    This assumes incompressibility, and uniaxial stretches in the axial direction.

    :param stretch: float, The stretch in the axial direction.
    :return: float, The calculated first invariant.
    """
    I1 = stretch**2 + 2.0*(1.0/float(stretch))
    return I1

def getMooneyI2(stretch):
    """
    Calculate I2 from a given stretch for the getMooneyStress function.
    This assumes incompressibility, and uniaxial stretches in the axial direction.

    :param stretch: float, The stretch in the axial direction.
    :return: float, The calculated second invariant
    """
    I2 = (1.0/stretch**2) + 2.0*stretch
    return I2

def _testNeoHookean():
    mu = 0.34
    strch = np.array([1, 1.1, 1.2, 1.25, 1.40])
    stress = getNeoHookeanStress(strch, mu)
    return

def _testMooney():
    constant1 = 20.0
    constant2 = 5.3
    constant3 = 40
    strch = np.array([1, 1.1, 1.2, 1.25, 1.40])
    stress = getMooneyStress(strch, constant1, constant2, constant3)
    return

if __name__=='__main__':
    _testNeoHookean()
    _testMooney()