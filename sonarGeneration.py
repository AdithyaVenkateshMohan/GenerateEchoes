# import rospy
# import pcl
# from sensor_msgs.msg import PointCloud
# from geometry_msgs.msg import Point
# from datetime import datetime

# import sensor_msgs.point_cloud2 as pc2


import numpy
from matplotlib import pyplot
from scipy.interpolate import interp1d
import library
# import math

def echo_gen_direct(distances, azimuths, elevations, sample_frequency=125000):
    emission_level = 100
    emission_duration = 0.0025
    emission_frequency = 40000
    emitter_radius = 0.005
    absorption_coefficient = 1.318  # http://www.sengpielaudio.com/calculator-air.htm
    reflection_strength = -20
    speed_of_sound = 340

    emission_samples = int(sample_frequency * emission_duration)
    emission_time = numpy.linspace(0, emission_duration, emission_samples)
    emission = numpy.sin(2 * numpy.pi * emission_frequency * emission_time)
    emission_window = library.signal_ramp(emission_samples, 10)
    emission = emission * emission_window

    # %%
    # Calculate directivity
    piston, degrees = library.pistonmodel(emission_frequency, radius=emitter_radius)
    piston = 10 * numpy.log10(piston)
    piston_function = interp1d(degrees, piston)
    excentricity = library.gca(azimuths, elevations, 0, 0)
    delays = 2 * distances / speed_of_sound
    loss_directionality = piston_function(excentricity)

    # %%
    # Calculate path losses
    loss_attenuation = - 2 * distances * absorption_coefficient
    loss_spreading = -40 * numpy.log10(distances)

    echoes = emission_level + reflection_strength + loss_directionality + loss_attenuation + loss_spreading
    echoes_pa = library.db2pa(echoes)
    echoes_pa[echoes < 0] = 0

    # %%
    # Make impulse response and echo sequence
    impulse_result = library.make_impulse_response(delays, echoes_pa, emission_duration, sample_frequency)
    impulse_response = impulse_result['impulse_response']
    impulse_time = impulse_result['impulse_time']
    impulse_indices = impulse_result['indices']
    echo_sequence = numpy.convolve(emission, impulse_response, mode='same')

    # Get energy
    # Make impulse response and echo sequence
    first_echo_index = numpy.min(impulse_indices[echoes > 20])
    echo_window = numpy.zeros(len(impulse_time))
    echo_window[first_echo_index] = 1
    echo_window = numpy.convolve(emission_window, echo_window, mode='same')
    windowed_echo_sequence = echo_sequence * echo_window


    # %% prepare return value
    return_value = {}
    return_value['echoes'] = echoes
    return_value['echoes_pa'] = echoes_pa
    return_value['loss_directionality'] = loss_directionality
    return_value['loss_attenuation'] = loss_attenuation
    return_value['loss_spreading'] = loss_spreading
    return_value['echo_sequence'] = echo_sequence
    return_value['impulse_result'] = impulse_result
    return_value['echo_window'] = echo_window
    return_value['windowed_echo_sequence'] = windowed_echo_sequence
    return return_value




def plot_echo(return_value):
    echo_sequence = return_value['echo_sequence']
    impulse_time = return_value['impulse_result']['impulse_time']
    impulse_response = return_value['impulse_result']['impulse_response']
    echo_window = return_value['echo_window']

    pyplot.figure()
    pyplot.subplot(3,1,1)
    pyplot.plot(impulse_time, impulse_response > 0)
    pyplot.title('Echo Sequence')
    pyplot.xlabel('Time')

    pyplot.subplot(3,1,2)
    pyplot.plot(impulse_time, echo_sequence)
    pyplot.title('Echo Sequence')
    pyplot.xlabel('Time')

    pyplot.subplot(3,1,3)
    pyplot.plot(impulse_time, echo_window)
    pyplot.title('Echo Sequence')
    pyplot.xlabel('Time')

    pyplot.show()



