from SimPy.Simulation import *
from random import expovariate,seed
from math import *
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


'''
Pacakges arrive at random into a c-server queue with exponential processing-time distribution. 
Simulate to determine the average number in the system and
the average time jobs spend in the system.
'''


class Generator(Process):
    """ generates Packages at random """

    def execute(self, maxPackages, arrivalRate, processingTime):
        for i in range(maxPackages):
            L = Package("Package{0}".format(i))

            # one queue including priority and regular packages
            package = np.random.choice([0, 1], size=1, p=[0.9,0.1])

            # priority packages
            if package == 0:
                activate(L, L.execute(processingTime), delay=0, prior=0)
                packages.append(0)

            # regular packages
            else:
                activate(L, L.execute(processingTime), delay=0, prior=1)
                packages.append(1)

            yield hold, self, expovariate(arrivalRate)



class Package(Process):
    ''' Packages request a post-office worker and hold it for an exponential time '''

    NoInSystem = 0

    def execute(self, processingTime):

        # a package arrive
        arrival_time = now()
        Package.NoInSystem += 1
        monitor_packages_number.observe(Package.NoInSystem)
        yield request, self, worker

        # process a package
        time = expovariate(1.0 / processingTime)
        monitor_processing_time.observe(time)
        working_workers.append(len(worker.activeQ) / 9)
        yield hold, self, time
        yield release, self, worker

        # finish a package
        Package.NoInSystem -= 1
        monitor_packages_number.observe(Package.NoInSystem)
        monitor_time.observe(now() - arrival_time) # how long a package stays in the system


    def trace(self, message):
        FMT = "{0:7.4f}{1:6}{2:10}({3:2d})"
        if TRACING:
            print(FMT.format(now(), self.name, message, Package.NoInSystem))


# parameters
TRACING = True
workers = 9 # number of workers in M/M/C
processing_time = 2.0 # mean processing time
arrival_rate = 4.0 # mean arrival rate
max_packages = 9000
seed(666)

packages = []
working_workers = [] # the number of working workers


# initialize
monitor_packages_number = Monitor() # monitor for the number of packages
monitor_time = Monitor() # monitor for the time in system
monitor_processing_time = Monitor() # monitor for the generated processing times
worker = Resource(capacity=workers, qType=PriorityQ, name='workers')

# activate
initialize()

generator = Generator('packages')
activate(generator, generator.execute(maxPackages=max_packages,arrivalRate=arrival_rate, processingTime=processing_time))

monitor_packages_number.observe(0) # when the system starts, the number of packages is 0
simulate(until=2000.0) # simulate the process for 2000 unit times


# simulation report
print("{0:2d} workers,{1:6.1f} arrival rate, {2:6.0f} mean processing time".format(workers, arrival_rate,
                                                                                   processing_time))
print("-"*30)

# average packages number in system
print("Average packages number in the system is {0:6.4f}".format(monitor_packages_number.timeAverage())) # time average
c1,c2 = monitor_packages_number.mean() - 1.96*sqrt(monitor_packages_number.var()/monitor_packages_number.count()),\
        monitor_packages_number.mean() + 1.96*sqrt(monitor_packages_number.var()/monitor_packages_number.count())
print("95% CI for average packages number: [{0:6.4f},{1:6.4f}]".format(c1,c2))
print("-"*30)

# average time
print("Average time in the system is {0:6.4f}".format(monitor_time.mean()))
c1,c2 = monitor_time.mean() - 1.96*sqrt(monitor_time.var()/monitor_time.count()),\
        monitor_time.mean() + 1.96*sqrt(monitor_time.var()/monitor_time.count())
print("95% CI for average time in the system: [{0:6.4f},{1:6.4f}]".format(c1,c2))
print("-"*30)

# average service time
c1,c2 = monitor_processing_time.mean() - 1.96*sqrt(monitor_processing_time.var()/monitor_processing_time.count()),\
        monitor_processing_time.mean() + 1.96*sqrt(monitor_processing_time.var()/monitor_processing_time.count())
print("Actual average processing time is {0:6.4f}".format(monitor_processing_time.mean()))
print("95% CI for average processing time: [{0:6.4f},{1:6.4f}]".format(c1,c2))
print("-"*30)

# busy workers proportion
print("The proportion of time that all workers are busy:", working_workers.count(1)/len(working_workers))

# count the number of regualr(1) and priority(0) packages respectively
print(Counter(packages))


# Figures.
# Average package amount in queues when changing packages number from 3000 to 10000
Average_package_number = [10.6615, 11.3471, 10.9885, 10.8897,11.1160,11.2457, 11.2457, 11.2457]
Average_package_number_lower = [11.0091, 11.6930, 11.3521, 11.2528, 11.4443, 11.5887, 11.5887, 11.5887]
Average_package_number_upper = [11.2638, 11.9560, 11.5736, 11.4536, 11.6337, 11.7718, 11.7718, 11.7718]
max_packages = [i*1000 for i in range(3, 11)]
plt.title("Max Packages number changes with Average packages number in the system")
plt.plot(max_packages, Average_package_number, label="Average packages number in the system")
plt.plot(max_packages, Average_package_number_lower, 'b--', label="95% CI lower limit")
plt.plot(max_packages, Average_package_number_upper, 'b--', label="95% CI upper limit")
plt.legend(loc="best")
plt.xlabel("Max Packages number")
plt.ylabel("Average packages number in the system")
plt.show()

# Average package amount in queues when changing packages number from 3000 to 10000
Average_time = [2.7688, 2.9185, 2.8197,2.7910,2.8252,2.8551, 2.8551, 2.8551]
Average_time_lower = [2.6893, 2.8454, 2.7556, 2.7325, 2.7710, 2.8036, 2.8036, 2.8036]
Average_time_upper = [2.8484, 2.9916, 2.8838, 2.8495, 2.8795, 2.9065, 2.9065, 2.9065]
max_packages = [i * 1000 for i in range(3, 11)]
plt.title("Max Packages number changes with Average time in the system")
plt.plot(max_packages, Average_time, label="Average time in the system")
plt.plot(max_packages, Average_time_lower, 'c--', color="red", label="95% CI lower limit")
plt.plot(max_packages, Average_time_upper, 'c--', color="red", label="95% CI upper limit")
plt.legend(loc="best")
plt.xlabel("Max Packages number")
plt.ylabel("Average time in the system")
plt.show()

# Average workers processing time when changing packages number from 3000 to 10000
Actual_average_processing_time = [2.0223, 2.0063, 2.0036,1.9954,1.9925,1.9959, 1.9959, 1.9959]
Actual_average_processing_time_lower = [1.0223, 1.9442, 1.9479, 1.9443, 1.9456, 1.9516, 1.9516, 1.9516]
Actual_average_processing_time_upper = [2.0946, 2.0684, 2.0594, 2.0464, 2.0395, 2.0402, 2.0402, 2.0402]
max_packages = [i * 1000 for i in range(3, 11)]
plt.title("Max Packages number changes with Actual average processing time")
plt.plot(max_packages, Actual_average_processing_time, label="Actual average processing time")
plt.plot(max_packages, Actual_average_processing_time_lower, 'c--', color="green", label="95% CI lower limit")
plt.plot(max_packages, Actual_average_processing_time_upper, 'c--', color="green", label="95% CI upper limit")
plt.legend(loc="best")
plt.xlabel("Max Packages number")
plt.ylabel("Actual average processing time")
plt.show()

# The proportion of time that all workers are busy with different package number
# when changing packages number from 3000 to 10000
All_workers_busy_proportion = [0.69, 0.69625, 0.692, 0.687, 0.6954285714285714, 0.6981467377506981, 0.6981467377506981,
                               0.6981467377506981]
max_packages = [i * 1000 for i in range(3, 11)]
plt.title("Max Packages number changes with The proportion of time that all workers are busy")
plt.plot(max_packages, All_workers_busy_proportion, label="The proportion of time that all workers are busy")
plt.xlabel("Max Packages number")
plt.ylabel("The proportion of time that all workers are busy")
plt.show()

# When max packages number is 10000,
# Packages average waiting time changes with Post-office workers number from 5 to 10
Average_time = [376.0001, 244.2345, 142.0434, 14.8906, 2.8551, 2.4387]
Actual_average_processing_time = [2.0102, 2.0080, 2.0313, 1.9976,1.9959, 2.0155]
Average_waiting_time = list(map(lambda x: x[0]-x[1], zip(Average_time, Actual_average_processing_time)))
print(Average_waiting_time)
workers_number = [i for i in range(5, 11)]
plt.title("Packages average waiting time changes with Post-office workers number")
plt.plot(workers_number, Average_waiting_time, label="The proportion of time that all workers are busy")
plt.xlabel("Post-office workers number")
plt.ylabel("Packages average waiting time")
plt.show()

# When max packages number is 10000,
# The proportion of time that all workers are busy changes with Post-office workers number from 5 to 10
All_workers_busy_proportion = [0.9967832730197025, 0.9953043769914472,0.9930131004366812, 0.9665144596651446,
                               0.6981467377506981,0.5026421741318571]
workers_number = [i for i in range(5, 11)]
plt.title("The proportion of time that all workers are busy changes with Post-office workers number")
plt.plot(workers_number, All_workers_busy_proportion, label="The proportion of time that all workers are busy")
plt.xlabel("Post-office workers number")
plt.ylabel("The proportion of time that all workers are busy")
plt.show()

