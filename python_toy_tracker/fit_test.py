import toytraceback as ttb
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import math
import scipy.stats as stats
from scipy.optimize import curve_fit 

track_count = 30 # Number of tracks to fit
module_alignment = 0.3 # Set up detector, and change alignment of first module
fit_count = 150 # Number of times to run fit

alignment_residuals = []

print "Carrying out", fit_count, "fits, with", track_count, "tracks:"  

for k in xrange(fit_count):
    true_detector = ttb.Detector()
    true_detector.set_module_x_align(1, module_alignment)

    # Get wire coordinates
    x_true_wires = true_detector.get_wires_x()
    y_true_wires = true_detector.get_wires_y()

    # Coordinates at beginning, end of track
    x_bottom = [random.uniform(ttb.track_boundary_x_lower, ttb.track_boundary_x_upper) for i in xrange(track_count)]
    x_top = [random.uniform(ttb.track_boundary_x_lower, ttb.track_boundary_x_upper) for i in xrange(track_count)]
    y_bottom = [ttb.track_boundary_y_lower for i in xrange(track_count)]
    y_top = [ttb.track_boundary_y_upper for i in xrange(track_count)]

    # # Get boundaries on intercepts and gradients for fit, with large boundary on module alignment distance
    # lower_fit_bounds = [0]*((2 * track_count) + 1)
    # upper_fit_bounds = [0]*((2 * track_count) + 1)
    # for i in xrange(len(lower_fit_bounds)):
    #     if (i % 2 == 0):
    #         lower_fit_bounds[i] = (ttb.track_boundary_x_lower - ttb.track_boundary_x_upper) / (ttb.track_boundary_y_upper - ttb.track_boundary_y_lower)
    #         upper_fit_bounds[i] = (ttb.track_boundary_x_upper - ttb.track_boundary_x_lower) / (ttb.track_boundary_y_upper - ttb.track_boundary_y_lower)
    #     else:
    #         lower_fit_bounds[i] = ttb.track_boundary_x_lower
    #         upper_fit_bounds[i] = ttb.track_boundary_x_upper
    
    # lower_fit_bounds[-1] = -np.inf
    # upper_fit_bounds[-1] = np.inf
    
    # fit_bounds = (lower_fit_bounds, upper_fit_bounds)
    # print fit_bounds
    
    
    
    # Calculate track gradient and x-intercept from track coordinates
    gradient = [((x_top[i] - x_bottom[i]) / (y_top[i] - y_bottom[i])) for i in xrange(track_count)]
    intercept = [x_bottom[i] - (gradient[i] * y_bottom[i]) for i in xrange(track_count)]

    # Set up track, and get pos of beginning, end points
    true_track = [ttb.Track(gradient[i], intercept[i]) for i in xrange(track_count)]
    x_true_track = [true_track[i].get_x_points() for i in xrange(track_count)]
    y_true_track = [true_track[i].get_y_points() for i in xrange(track_count)]

    # Get wire hits in each layer, then assign these to detector
    wire_hits = []
    for i in xrange(track_count): 
        wire_hits = wire_hits + (ttb.closest_hit_wires(true_detector, true_track[i], True))
        
    true_detector.set_wire_hits(wire_hits)

    # New detector object for fitting
    fitting_detector = ttb.Detector()
    fitting_detector.set_wire_hits(wire_hits)

    # Get x-displacement of all closest approached wires
    hit_rads = [wire_hit.get_hit_dist() for wire_hit in wire_hits]
        
    wire_keys = [str((i - (i % 8)) / 8) + "-" + str(i % 8) for i in xrange(8 * track_count)] # Numbers to index all layers


    guess = [0.0 for i in xrange((2 * track_count) + 1)] # Initial guess for fitted track gradient and intercept, and module alignment (spurious convergence without this)

    print k

    fit_sigmas = [ttb.hit_resolution]*len(hit_rads)

    # Finds values for track gradient and intercept, by fitting to wire hit x-displacements
    popt, pcov = curve_fit(fitting_detector.get_hit_radius, wire_keys, hit_rads, p0=guess, sigma=fit_sigmas)
    
    alignment_residuals.append(popt[-1] - module_alignment)


print ""
print "Mean Residual:", np.mean(np.array(alignment_residuals)), "mm"
print "Standard Deviation:", np.std(np.array(alignment_residuals)), "mm"

# Plot histogram of residuals
plt.hist(alignment_residuals, bins=10)
plt.xlabel("Residual Value / mm")
plt.ylabel("Frequency")

plt.show()
