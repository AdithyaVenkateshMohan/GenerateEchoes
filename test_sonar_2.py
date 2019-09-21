from matplotlib import pyplot
import sonarGeneration
import numpy

#%%
## variable azimuths

azimuths = numpy.linspace(-1, 1, 100)
elevations = numpy.ones(azimuths.shape) * 0
distances = numpy.random.rand(len(azimuths)) + 1


result = sonarGeneration.echo_gen_direct(distances, azimuths, elevations)
impulse_response = result['impulse_result']['impulse_response']
sonarGeneration.plot_echo(result)

