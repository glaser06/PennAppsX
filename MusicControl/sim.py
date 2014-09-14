sample_length = 5
crop = 3
span = 3
step = 1
threshold = 0.5

import re
import commands
import numpy
import math

def variance(listx):
    meanx = numpy.mean(listx)
    meanx_sqr = 0
    for x in listx:
        meanx_sqr += x**2
    meanx_sqr = meanx_sqr / float(len(listx))
    return meanx_sqr - meanx**2

def correlation(listx, listy):
    if len(listx) != len(listy):
        return -2
    meanx = numpy.mean(listx)
    meany = numpy.mean(listy)
    covariance = 0
    for i in range(len(listx)):
        covariance += (listx[i] - meanx) * (listy[i] - meany)
    covariance = covariance / float(len(listx))
    return covariance / (math.sqrt(variance(listx)) * math.sqrt(variance(listy)))

def cross_correlation(listx, listy, offset):
    if offset > 0:
        listx = listx[offset:]
        listy = listy[:len(listx)]
    elif offset < 0:
        offset = -offset
        listy = listy[offset:]
        listx = listx[:len(listy)]
    return correlation(listx, listy)

def compare(listx, listy, span, step):
    corr_xy = []
    for offset in numpy.arange(-span, span + 1, step):
        corr_xy.append(cross_correlation(listx, listy, offset))
    return corr_xy

def max_index(listx):
    max_index = 0
    max_value = listx[0]
    for i, value in enumerate(listx):
        if value > max_value:
            max_value = value
            max_index = i
    return max_index

file_a = "~/Desktop/ring.mp3"
fpcalc_out = commands.getoutput('fpcalc -raw -length ' \
                                     + str(sample_length) + ' ' + file_a)
fingerprint_index = fpcalc_out.find('FINGERPRINT=') + 12
fingerprint_a = map(int, fpcalc_out[fingerprint_index:].split(','))
print(fingerprint_a)
    
file_b = "~/Desktop/ring2.mp3"
fpcalc_out = commands.getoutput('fpcalc -raw -length ' \
                                         + str(sample_length) + ' ' + file_b)
fingerprint_index = fpcalc_out.find('FINGERPRINT=') + 12
fingerprint_b = map(int, fpcalc_out[fingerprint_index:].split(','))
print(fingerprint_b)
corr_ab = compare(fingerprint_a[1:], fingerprint_b[1:], span, step)
max_corr_index = max_index(corr_ab)
max_corr_offset = -span + max_corr_index * step

print(corr_ab[max_corr_index])