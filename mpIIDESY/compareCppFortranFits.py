#
# Script to read parameter values from trees generated using C++, Fortran 
# versions of MpTest1, carrying out various comparisons of them.
#
# John Smeaton 07/02/2017
#

import ROOT
import sys
import getopt
import os
import numpy as np
import matplotlib.pyplot as plt
import millepede_utils


# Get system arguments, define string showing help message
argv = sys.argv[1:]
helpstring = "compareLabelsRoot.py -c <input_c_file> -f <input_fortran_file>"

# Define filename strings
input_c_filename = ""
input_fortran_filename = "" 

# Get options, arguments
try:
    opts, args = getopt.getopt(argv, "h:c:f:", ["help", "input_c_file", "input_fortran_file"])
except getopt.GetoptError:
    print helpstring
    sys.exit(2)

# Set input filename, if given in console argument
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print helpstring
        sys.exit(2)
    elif opt in ("-c", "--input_c_file"):
        input_c_filename = os.path.abspath(arg)
    elif opt in ("-f", "--input_fortran_file"):
        input_fortran_filename = os.path.abspath(arg)


# Dictionaries of parameter values and errors, in C++ and Fortran
c_true_vals = dict()
c_fit_vals = dict()
c_fit_errors = dict()
fortran_true_vals = dict()
fortran_fit_vals = dict()
fortran_fit_errors = dict()


# Open tree of C++ parameter values
file_c = ROOT.TFile.Open(input_c_filename, "read")
tree_c = file_c.Get("paramTree")

# Copy trees with fitted values (from inversion), and true values
fit_tree_c = tree_c.CopyTree('fitType==' + str(1.0))
true_tree_c = tree_c.CopyTree('fitType==' + str(0.0))

# Loop over C++ parameter tree entries
for i in xrange(fit_tree_c.GetEntries()):

    # Get true parameter value
    true_tree_c.GetEntry(i)
    c_true_vals[true_tree_c.label] = true_tree_c.paramValue

    # Get fitted parameter value, error.
    fit_tree_c.GetEntry(i)
    c_fit_vals[fit_tree_c.label] = fit_tree_c.paramValue
    c_fit_errors[fit_tree_c.label] = fit_tree_c.paramError

file_c.Close() # Close file

# Open tree of Fortran parameter values
file_fortran = ROOT.TFile.Open(input_fortran_filename, "read")
tree_fortran = file_fortran.Get("paramTree")

# Copy trees with fitted values (from inversion), and true values
fit_tree_fortran = tree_fortran.CopyTree('fitType==' + str(1.0))
true_tree_fortran = tree_fortran.CopyTree('fitType==' + str(0.0))

# Loop over Fortran parameter tree entries
for i in xrange(fit_tree_fortran.GetEntries()):

    # Get true parameter value
    true_tree_fortran.GetEntry(i)
    fortran_true_vals[true_tree_fortran.label] = true_tree_fortran.paramValue

    # Get fitted parameter value, error
    fit_tree_fortran.GetEntry(i)
    fortran_fit_vals[fit_tree_fortran.label] = fit_tree_fortran.paramValue
    fortran_fit_errors[fit_tree_fortran.label] = fit_tree_fortran.paramError


# Lists of parameter labels
label_plane_disp = []
label_vel_dev = []

# Lists of differences between C++, Fortran values of true parameters
true_difference_plane_disp = []
true_difference_vel_dev = []

# Lists of differences between C++, Fortran values of fitted parameters
fit_difference_plane_disp = []
fit_difference_vel_dev = []

# Normalised fit errors for Fortran and C++ parameter values
fit_error_fortran_plane_disp = []
fit_error_fortran_vel_dev = []
fit_error_c_plane_disp = []
fit_error_c_vel_dev = []


# Print table header
print ""
print ""
print "{:<10} {:<22} {:<22} {:<22} {:<22} {:<22} {:<22}".format("Label", "True Param C++", "True Param Fortran", "True Param Diff.", "Fit Param C++", "Fit Param Fortran", "Fit Param Diff.")
print ""

# Loop across all parameter labels
for label in sorted(c_true_vals.iterkeys()):

    if label == 501: print "" # For readability

    # Output parameter values, differences
    print "{:<10} {:<22} {:<22} {:<22} {:<22} {:<22} {:<22}".format(label, c_true_vals[label], fortran_true_vals[label], c_true_vals[label] - fortran_true_vals[label], c_fit_vals[label], fortran_fit_vals[label], c_fit_vals[label] - fortran_fit_vals[label])

    # Populate relevent lists for velocity deviations
    if label > 500:
        label_vel_dev.append(label)
        true_difference_vel_dev.append(c_true_vals[label] - fortran_true_vals[label])        
        fit_difference_vel_dev.append(c_fit_vals[label] - fortran_fit_vals[label])
        fit_error_c_vel_dev.append((c_fit_vals[label] - c_true_vals[label]) / c_fit_errors[label])
        fit_error_fortran_vel_dev.append((fortran_fit_vals[label] - fortran_true_vals[label]) / fortran_fit_errors[label])

    # Populate relevent lists for plane displacements
    else:
        label_plane_disp.append(label)
        true_difference_plane_disp.append(c_true_vals[label] - fortran_true_vals[label])        
        fit_difference_plane_disp.append(c_fit_vals[label] - fortran_fit_vals[label])
        fit_error_c_plane_disp.append((c_fit_vals[label] - c_true_vals[label]) / c_fit_errors[label])
        fit_error_fortran_plane_disp.append((fortran_fit_vals[label] - fortran_true_vals[label]) / fortran_fit_errors[label])
        


# Fitted Parameter Difference Histograms

plt.hist(fit_difference_vel_dev, 20)
plt.title("Histogram of Differences in C++, Fortran \n Fitted Values of Velocity Deviation")
plt.xlabel("C++, Fortran Fitted Parameter Difference")
plt.ylabel("Number of Planes")
plt.show()

plt.hist(fit_difference_plane_disp, 20)
plt.title("Histogram of Differences in C++, Fortran \n Fitted Values of Plane Displacement")
plt.xlabel("C++, Fortran Fitted Parameter Difference")
plt.ylabel("Number of Planes")
plt.show()



# Normalised fit errors in C++, Fortran, scatter plots

plt.plot(label_vel_dev, fit_error_c_vel_dev, 'b.', label="C++")
plt.plot(label_vel_dev, fit_error_fortran_vel_dev, 'r.', label="Fortran")
plt.legend(loc='best')
plt.grid()
plt.title("Misalignments of Velocity Deviation Parameters, \n Normalised by Fitted Parameter Errors")
plt.xlabel("Parameter Label")
plt.ylabel("Normalised Misalignment")
plt.show()

plt.plot(label_plane_disp, fit_error_c_plane_disp, 'b.', label="C++")
plt.plot(label_plane_disp, fit_error_fortran_plane_disp, 'r.', label="Fortran")
plt.legend(loc='best')
plt.grid()
plt.title("Misalignments of Plane Displacement Parameters, \n Normalised by Fitted Parameter Errors")
plt.xlabel("Parameter Label")
plt.ylabel("Normalised Misalignment")
plt.show()



# Ratios of normalised fit errors, scatter plots

normed_misalignment_ratio_vel_dev = np.absolute(np.array(fit_error_c_vel_dev) / np.array(fit_error_fortran_vel_dev))
normed_misalignment_ratio_plane_disp = np.absolute(np.array(fit_error_c_plane_disp) / np.array(fit_error_fortran_plane_disp))

plt.plot(label_vel_dev, normed_misalignment_ratio_vel_dev, 'b.')
plt.title("Ratios of Velocity Deviation Misalignments \n(Normalised by Fitted Parameter Error) in C++ to Misalignments in Fortran\n" + "Mean: " + str(np.mean(normed_misalignment_ratio_vel_dev)) + " Std-Dev: " + str(np.std(normed_misalignment_ratio_vel_dev)))
plt.xlabel("Parameter Label")
plt.ylabel("Misalignment Ratios")
plt.grid()
plt.show()

plt.plot(label_plane_disp, normed_misalignment_ratio_plane_disp, 'b.')
plt.title("Ratios of Plane Displacement Misalignments \n(Normalised by Fitted Parameter Error) in C++ to Misalignments in Fortran\n" + "Mean: " + str(np.mean(normed_misalignment_ratio_plane_disp)) + " Std-Dev: " + str(np.std(normed_misalignment_ratio_plane_disp)))
plt.xlabel("Parameter Label")
plt.ylabel("Misalignment Ratios")
plt.grid()
plt.show()



# Unnormalised differences between C++, Fortran parameters

plt.plot(label_vel_dev, true_difference_vel_dev, 'b.', label="True")
plt.plot(label_vel_dev, fit_difference_vel_dev, 'r.', label="Fitted")
plt.legend(loc='best')
plt.title("Differences Between Drift Velocity Parameters in \n C++, Fortran Versions of MpTest1")
plt.xlabel("Parameter Label")
plt.ylabel("C++, Fortran Parameter Value Difference")
plt.yscale('symlog', linthreshy=1.0e-10)
plt.grid()
plt.show()

plt.plot(label_plane_disp, true_difference_plane_disp, 'b.', label="True")
plt.plot(label_plane_disp, fit_difference_plane_disp, 'r.', label="Fitted")
plt.legend(loc='best')
plt.title("Differences Between Plane Displacement Parameters in \n C++, Fortran Versions of MpTest1")
plt.xlabel("Parameter Label")
plt.ylabel("C++, Fortran Parameter Value Difference")
plt.yscale('symlog', linthreshy=1.0e-10)
plt.grid()
plt.show()



# Unnormalised moduli of differences between C++, Fortran parameters

abs_true_difference_vel_dev = [abs(i) for i in true_difference_vel_dev]
abs_fit_difference_vel_dev = [abs(i) for i in fit_difference_vel_dev]

abs_true_difference_plane_disp = [abs(i) for i in true_difference_plane_disp]
abs_fit_difference_plane_disp = [abs(i) for i in fit_difference_plane_disp]

plt.plot(label_vel_dev, abs_true_difference_vel_dev, 'b.', label="True")
plt.plot(label_vel_dev, abs_fit_difference_vel_dev, 'r.', label="Fitted")
plt.legend(loc='best')
plt.title("Absolute Differences Between Drift Velocity Parameters in \n C++, Fortran Versions of MpTest1")
plt.xlabel("Parameter Label")
plt.ylabel("Modulus of C++, Fortran Parameter Value Difference")
plt.yscale('log')
plt.grid()
plt.show()

plt.plot(label_plane_disp, true_difference_plane_disp, 'b.', label="True")
plt.plot(label_plane_disp, fit_difference_plane_disp, 'r.', label="Fitted")
plt.legend(loc='best')
plt.title("Absolute Differences Between Plane Displacement Parameters in \n C++, Fortran Versions of MpTest1")
plt.xlabel("Parameter Label")
plt.ylabel("Modulus of C++, Fortran Parameter Value Difference")
plt.yscale('log')
plt.grid()
plt.show()



# Quick look for any correlation
# plt.plot(abs_true_difference_vel_dev, abs_fit_difference_vel_dev, 'b.')
# plt.show()

# plt.plot(abs_true_difference_plane_disp, abs_fit_difference_plane_disp, 'b.')
# plt.show()
