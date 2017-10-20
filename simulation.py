################################################
#             FRANCESCA RAMUNNO                #
################################################

import matplotlib.pyplot as plt
import random
from scipy.stats import binom

#################################################
#                  FUNCTIONS                    #
#################################################

# function to get binomial value
def get_binomial(n,p):
    return binom.rvs(n,p)

# function to return the index of the shortest queue
def get_shortest_queue(queue_length_array):
    count = 1
    shortest_index = 0
    while count < len(queue_length_array):
        if queue_length_array[count] < queue_length_array[shortest_index]:
            shortest_index = count
        count = count+1
    return shortest_index

# function to generate d based on given mu val
def generate_d(mu_val):
    rand_num = random.uniform(0,1)
    if (rand_num >= mu_val):
        return 1
    else:
        return 0

# function to delete the last non zero index in an array (to follow FIFO order of queue)
# by setting it to 0
def delete_last_index(queue):
    i = 0
    for num in queue:
        if num == 0:
            break
        else:
            i = i + 1
    queue[i]=0

# function to return the index of the last non-zero element of an array
def get_index(queue):
    i = 0
    for num in queue:
        if num == 0:
            break
        else:
            i = i+1
    return i

###################################################
#               END OF FUNCTIONS                  #
###################################################

N = 5 # the number of servers
T = 1001 # the number of time slots = 10 ^ 6

x_axis_1 = [] # this array will store values on the first graphs x axis, to be plotted
y_axis_1 = [] # this array will store values on the first graphs y axis, to be plotted
x_axis_2 = [] # this array will store values on the second graphs x axis, to be plotted
y_axis_2 = [] # this array will store values on the second graphs y axis, to be plotted

MU = 0.5 # probability server completes a job
lambda_val = [0.2,0.3,0.4,0.45,0.49,0.495] # the lambda values

server_queue_lengths=[0,0,0,0,0]

# this will keep track of the jobs in the queues by storing their arrival rate
SIZE = T
queue_1 = [0] * SIZE
queue_2 = [0] * SIZE
queue_3 = [0] * SIZE
queue_4 = [0] * SIZE
queue_5 = [0] * SIZE

job_count = 0 # keep count of jobs for lambda = 0.45
hist_delay_array = [0] * T # keep track of job delays for lambda = 0.45

server_queues = [queue_1, queue_2, queue_3, queue_4, queue_5]
delay_array = [0] * T # this will keep track of the delays


for val in lambda_val:
    # print("LAMBDA VALUE: ", val)
    index = 0

    while index < T:
        num_arrivals = get_binomial(N, val) # generate arrivals

        # --- THIS IS FOR THE HISTOGRAM --- #
        if val == 0.45:
            job_count = job_count + num_arrivals # keep track of the number of jobs for
                                                 # lambda = 0.45, to calculate the fraction
                                                 # of jobs experience a certain delay, later
        # print("# ARRIVALS: ", num_arrivals)
        # --------------------------------- #

        i = 0

        # process each arrival
        while i < num_arrivals:

            # get the shortest queue index
            shortest_queue_index = get_shortest_queue(server_queue_lengths)
            # print("SHORTEST QUEUE INDEX = ", shortest_queue_index)

            # insert the job into the front of the queue
            server_queues[shortest_queue_index].insert(0,index) # index = arrival time

            # update the queue length
            server_queue_lengths[shortest_queue_index] = server_queue_lengths[shortest_queue_index] + 1
            # print("THE QUEUE AT INDEX 0: ", server_queues[shortest_queue_index][0], " THE SERVER LENGTH UPDATED: ",
            # server_queue_lengths[shortest_queue_index])

            i = i+1

        i = 0

        # for each server, generate a departure (as you would in Single Server queue)
        while i < N:

            queue_length = server_queue_lengths[i] # get the queue length

            if queue_length > 0: # make sure the queue length is greater than 0 before generating a departure

                num_departures = generate_d(MU) # generate departure, as would in single server queue

                if num_departures > 0:

                    # print("FOR i=", i, " # DEPARTURES = ", num_departures)
                    server_queue_lengths[i] = queue_length - 1 # update the queue length
                    queue = server_queues[i] # access the corresponding queue

                    # print("LENGTH BEFORE: ", len(queue))
                    last_index = get_index(queue) # get the index of the departure to find the arrival time
                    arrival_time = queue[last_index] # get the arrival time of the departure
                    delay = index - arrival_time # get the delay by subtracting the arrival time slot from the
                                                 # current (departure) time slot
                    delay_array[delay] = delay_array[delay] + 1 # keep track of the delays, so increase the count of this delay

                    # -- FOR HISTOGRAM -- #
                    if val == 0.45:
                        hist_delay_array[delay] = hist_delay_array[delay] + 1 # increase # jobs that experience a delay of
                                                                              # variable "delay" time slots
                    # ------------------- #

                    delete_last_index(queue) # delete the last non-zero job from queue

                    # print("LENGTH AFTER: ", len(queue))
            i = i+1
        index = index + 1

    x_axis_1.append(val) # lambda values on x-axis for the first graph

    delay_total = 0
    d = 0

    # need to get the total delays by summing the delay * how many jobs had that delay
    for delay in delay_array:
        delay_total = delay_total + (d * delay)
        d = d+1

    # calculate the mean delay
    mean_delay = delay_total / T

    # the mean delay for lambda should be on the y-axis
    y_axis_1.append(mean_delay)

# -- BUILD THE FIRST GRAPH -- #
plt.plot(x_axis_1, y_axis_1)
plt.xlabel('Lambda values')
plt.ylabel('Mean delay')
plt.title('Mean delay of a job as a function of the arrival rate')
plt.grid(True)
plt.show()
# -------------------------- #

d=0 # d will denote the time delay

# -- FOR THE HISTOGRAM -- #
for delay in hist_delay_array:
   x_axis_2.append(d) # the x axis should be the delay
   fraction = (d*delay) / job_count # get the fraction of jobs that experience this delay
   y_axis_2.append(fraction) # the y-axis should be the fraction of jobs
   d=d+1
# ----------------------- #

# -- BUILD THE HISTOGRAM FOR LAMBDA=0.45 -- #
plt.hist([x_axis_2, y_axis_2])
plt.xlabel("Job delay (# of time slots)")
plt.ylabel("Fraction of jobs")
plt.title("Fraction of jobs as a function of their delays")
plt.grid(True)
plt.show()
# ----------------------------------------- #
