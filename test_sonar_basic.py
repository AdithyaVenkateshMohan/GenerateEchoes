from matplotlib import pyplot
import sonarGeneration
import numpy

#%%
## variable azimuths

azimuths = numpy.linspace(-90, 90, 100)
elevations = numpy.ones(azimuths.shape) * 0
distances = numpy.ones(azimuths.shape)


echo_sequence, impulse_time, info = sonarGeneration.echo_gen_direct(distances, azimuths, elevations)

pyplot.subplot(1,2,1)
pyplot.plot(azimuths, info['echoes'])
pyplot.subplot(1,2,2)
pyplot.plot(azimuths, info['loss_directionality'])
pyplot.show()

#%%
## variable elevations

elevations = numpy.linspace(-90, 90, 100)
azimuths = numpy.ones(elevations.shape) * 0
distances = numpy.ones(elevations.shape)


echo_sequence, impulse_time, info = sonarGeneration.echo_gen_direct(distances, azimuths, elevations)

pyplot.subplot(1,2,1)
pyplot.plot(elevations, info['echoes'])
pyplot.subplot(1,2,2)
pyplot.plot(elevations, info['loss_directionality'])
pyplot.show()

#%%
## variable distances

distances = numpy.linspace(0.1, 10, 100)
azimuths = numpy.ones(distances.shape) * 0
elevations = numpy.ones(distances.shape) * 0


echo_sequence, impulse_time, info = sonarGeneration.echo_gen_direct(distances, azimuths, elevations)

pyplot.subplot(1,2,1)
pyplot.plot(distances, info['echoes'])
pyplot.subplot(1,2,2)
pyplot.plot(distances, info['loss_directionality'])
pyplot.show()
