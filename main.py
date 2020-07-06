#!/usr/bin/python

import sys
import csv
import math


def display_help():
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("USAGE:")
            print("\t./109titration [-h, --help] <file>\n")
            print("DESCRIPTION:")
            print("\t-h, --help\tDisplay this help page")
            print("\tfile\t\tA csv file containing \"vol;ph\" lines")
            sys.exit(0)
    else:
        sys.exit(84)


def load_file():
    data = []
    i = 0
    try:
        with open(sys.argv[1]) as file:
            tmpdata = list(csv.reader(file, delimiter=';'))
            try:
                while (i < len(tmpdata)):
                    if len(tmpdata[i]) != 2:
                        sys.exit(84)
                    data.append(tmpdata[i])
                    data[i][0] = float(tmpdata[i][0])
                    data[i][1] = float(tmpdata[i][1])
                    if data[i][0] < 0 or data[i][1] < 0:
                        sys.exit(84)
                    i += 1
            except (ValueError):
                sys.exit(84)
    except (EnvironmentError):
        sys.exit(84)
    if len(data) < 5:
        sys.exit(84)
    return data


def equivalence_point(derivative, data):
    default = -10000000
    res = [1, 0]
    i = 1
    while i < len(data) - 1:
        if default < derivative[i]:
            default = derivative[i]
            res[0] = data[i][0]
            res[1] = i
        i += 1
    return res

def calc_deriv(x1, y1, x2, y2, x3, y3):
    slope1 = y1 - y2
    slope1 /= (x1 - x2)
    slope2 = y2 - y3
    slope2 /= (x2 - x3)
    slope1 *= (x2 - x3) / ((x1 - x2) + (x2 - x3))
    slope2 *= (x1 - x2) / ((x1 - x2) + (x2 - x3))
    tmp = slope1 + slope2
    return (tmp)

def derivative(data):
    res = []
    res.append(0)
    i = 1
    print("Derivative:")
    while i < len(data) - 1:
        tmp = calc_deriv(data[i + 1][0], data[i + 1][1], data[i][0], data[i][1], data[i - 1][0], data[i - 1][1])
        res.append(tmp)
        print("%.1f ml -> %.2f" % (data[i][0], res[i]))
        i += 1
    print("\nEquivalence point at %.1f ml\n" % (equivalence_point(res, data)[0]))
    return res


def scnd_derivative(deriv, data):
    print("Second derivative:")
    i = 1
    while i < len(deriv) - 2:
        tmp = calc_deriv(data[i + 2][0], deriv[i + 2], data[i + 1][0], deriv[i + 1], data[i][0], deriv[i])
        print("%.1f ml -> %.2f" % (data[i + 1][0], tmp))
        i += 1
    print("\nSecond derivative estimated:")


def scnd_derivative_estimated(deriv, data):
    equi_pnt = equivalence_point(deriv, data)
    recursive = equi_pnt[0]
    key = equi_pnt[1]
    it = data[key - 1][0]
    res = []
    tmp = 0
    one = 0
    res.append(it)
    if not key - 2 < 0:
        tmp = calc_deriv(data[key][0], deriv[key], data[key - 1][0], deriv[key - 1], data[key - 2][0], deriv[key - 2])
        #tmp = (deriv[key] - deriv[key - 2])
        #tmp /= (data[key][0] - data[key - 2][0])
        one = tmp
    res.append(tmp)
    res.append(one)
    two = calc_deriv(data[key + 1][0], deriv[key + 1], data[key][0], deriv[key], data[key - 1][0], deriv[key - 1])
    #two = (deriv[key + 1] - deriv[key - 1])
    #two /= (data[key + 1][0] - data[key - 1][0])
    res.append(two)
    tmp_res = (two - one)
    tmp_res /= (10 * (data[key][0] - data[key - 1][0]))
    res.append(recursive)
    while res[0] - 0.05 < data[key][0]:
        print("%.1f ml -> %.2f" % (res[0], res[2]))
        if math.fabs(res[1]) > math.fabs(res[2]) and key + 3 < len(data):
            res[1] = res[2]
            res[4] = res[0]
        res[2] += tmp_res
        res[0] += 0.1
    scnd_derivative_estimated_last(res, deriv, data)


def scnd_derivative_estimated_last(res, deriv, data):
    pns = equivalence_point(deriv, data)
    key = pns[1]
    it = res[0]
    ph = res[1]
    one = res[2]
    two = res[3]
    recursive = res[4]
    res = 0
    if key + 3 >= len(deriv):
        res = -two / 10
    else:
        one = calc_deriv(data[key + 2][0], deriv[key + 2], data[key + 1][0], deriv[key + 1], data[key][0], deriv[key])
        #one = (deriv[key + 2] - deriv[key])
        #one /= (data[key + 2][0] - data[key][0])
        res = (one - two)
        res /= (10 * (data[key + 1][0] - data[key][0]))
    two += res
    while it - 0.05 < data[key + 1][0]:
        print("%.1f ml -> %.2f" % (it, two))
        two += res
        it += 0.1
        if math.fabs(ph) > math.fabs(two) and key + 3 < len(data):
            ph = two
            recursive = it
    print("\nEquivalence point at %.1f ml" % recursive)


def main():
    display_help()
    data = load_file()
    deriv = derivative(data)
    scnd_derivative(deriv, data)
    scnd_derivative_estimated(deriv, data)