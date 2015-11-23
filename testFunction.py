import numpy as np

def firstDeJong(basicPlane):
    result = 0
    for dim in basicPlane:
        result += dim**2
    return result

def rosenbrocksSaddle(data):
    result = None
    for i in range(len(data)-1):
        if(result is None):
            result = ((100 * (data[i]**2 - data[i+1])**2) + (1 - data[i])**2)
        else:
            result += ((100 * (data[i]**2 - data[i+1])**2) + (1 - data[i])**2)
    return result

def thirdDeJong(data):
    result = None
    for dim in data:
        if(result is None):
            result = abs(dim)
        else:
            result += abs(dim)
    return result

def forthDeJong(data):
    result = None
    for i in range(len(data)):
        if(result is None):
            result = (i+1) * data[i]**4
        else:
            result += (i+1) * data[i]**4
    return result

def rastrigin(data):
    result = None
    count_dim = len(data)
    for x in data:
        if(result is None):
            result = x**2 - (10 * np.cos((2*np.pi*x)))
        else:
            result += x**2 - (10 * np.cos((2*np.pi*x)))
    return 2*count_dim*result

def schewefel(data):
    result = None
    for x in data:
        if(result is None):
            result = (-x) * np.sin(np.sqrt(abs(x)))
        else:
            result += (-x) * np.sin(np.sqrt(abs(x)))
    return result

def griewangkova(data):
    result_sum = None
    result_mult = None
    for i in range(len(data)):
        if(result_sum is None):
            result_sum = (data[i]**2)/4000
            result_mult = np.cos(data[i]/np.sqrt((i+1)))
        else:
            result_sum += (data[i]**2)/4000
            result_mult *= np.cos(data[i]/np.sqrt((i+1)))
    return 1 + result_sum - result_mult

def sineEnvelope(data):
    result_sum = None
    for i in range(len(data)-1):
        x1 = data[i]**2
        x2 = data[i+1]**2
        if(result_sum is None):
            result_sum = 0.5 + (np.sin(x1 + x2 - 0.5)**2  /  (1+0.001*(x1 + x2))**2)
        else:
            result_sum += (0.5 + (  (np.sin(x1 + x2 - 0.5)**2)  /  (1+0.001*(x1 + x2))**2 ))
    return -1 *result_sum

def sineWave(data):
    result = None
    for i in range(len(data)-1):
        x1 = data[i]**2
        x2 = data[i+1]**2
        if(result is None):
            result = ((np.sqrt(np.sqrt(x1 + x2))) * np.sin((50 * (x1 + x2)**0.1))**2 + 1)
        else:
            result += ((np.sqrt(np.sqrt(x1 + x2))) * np.sin((50 * (x1 + x2)**0.1))**2 + 1)

    return result

