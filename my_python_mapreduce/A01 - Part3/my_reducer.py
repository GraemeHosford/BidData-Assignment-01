#!/usr/bin/python

# --------------------------------------------------------
#           PYTHON PROGRAM
# Here is where we are going to define our set of...
# - Imports
# - Global Variables
# - Functions
# ...to achieve the functionality required.
# When executing > python 'this_file'.py in a terminal,
# the Python interpreter will load our program,
# but it will execute nothing yet.
# --------------------------------------------------------

import sys
import codecs
from datetime import timedelta, datetime


# ---------------------------------------
#  FUNCTION get_key_value
# ---------------------------------------
def get_key_value(line):
    # 1. We create the output variable
    res = ()

    # 2. We remove the end of line char
    line = line.replace('\n', '')

    # 3. We get the key and value
    words = line.split('\t')
    day = words[0]
    hour = words[1]

    # 4. We process the value
    hour = hour.rstrip(')')
    hour = hour.strip('(')

    # 4. We assign res
    res = (day, hour)

    # 5. We return res
    return res


def get_num_minutes_ago(date: str, time: str, time_interval: int):
    date_info = date.split("-")
    time_info = time.split(":")

    year = int(date_info[0])
    month = int(date_info[1])
    day = int(date_info[2])

    hour = int(time_info[0])
    minute = int(time_info[1])
    second = int(time_info[2])

    date_time_object = datetime(year, month, day, hour, minute, second)

    time_minutes_ago = date_time_object - timedelta(minutes=time_interval)

    date_string = time_minutes_ago.strftime("%Y-%m-%d")
    time_string = time_minutes_ago.strftime("%H:%M:%S")

    return (date_string, time_string)


# ------------------------------------------
# FUNCTION my_reduce
# ------------------------------------------
def my_reduce(my_input_stream, my_output_stream, my_reducer_input_parameters):
    time_interval = my_reducer_input_parameters[0]
    reduce_list = list()
    continuations = 0

    for line in my_input_stream:
        line_info = get_key_value(line)
        date = line_info[0]
        time = line_info[1]

        reduce_list += [([date, time, 1])]

        previous_time_interval = get_num_minutes_ago(date, time, time_interval)
        previous_date = previous_time_interval[0]
        previous_time = previous_time_interval[1]

        if len(reduce_list) > 1:
            previous = reduce_list[len(reduce_list) - 2]

            if previous[0] == previous_date and previous[1] == previous_time:
                continuations += 1
            else:
                reduce_list[len(reduce_list) - continuations - 2] = tuple(
                    [reduce_list[len(reduce_list) - continuations - 2][0],
                     reduce_list[len(reduce_list) - continuations - 2][1],
                     continuations + 1]
                )

                for i in range(continuations):
                    reduce_list.pop(-2)
                continuations = 0

    for item in reduce_list:
        my_output_stream.write(str(item[0]) + "\t(" + str(item[1]) + ", " + str(item[2]) + ")\n")


# ------------------------------------------
# FUNCTION my_main
# ------------------------------------------
def my_main(local_False_Cloudera_True,
            my_reducer_input_parameters,
            input_file_example,
            output_file_example
            ):
    # 1. We select the input and output streams based on our working mode
    my_input_stream = None
    my_output_stream = None

    # 1.1: Local Mode --> We use the debug files
    if (local_False_Cloudera_True == False):
        my_input_stream = codecs.open(input_file_example, "r", encoding='utf-8')
        my_output_stream = codecs.open(output_file_example, "w", encoding='utf-8')

    # 1.2: Cloudera --> We use the stdin and stdout streams
    else:
        my_input_stream = sys.stdin
        my_output_stream = sys.stdout

    # 2. We trigger my_reducer
    my_reduce(my_input_stream, my_output_stream, my_reducer_input_parameters)


# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    # 1. Local Mode or Cloudera
    local_False_Cloudera_True = False

    # 2. Debug Names
    input_file_example = "../../my_result/A01 - Part3/2. my_sort_simulation/sort_1.txt"
    output_file_example = "../my_result/A01 - Part3/3. my_reduce_simulation/reduce_sort_1.txt"

    # 3. my_reducer.py input parameters
    # We list the parameters here
    measurement_time = 5

    # We create a list with them all
    my_reducer_input_parameters = [measurement_time]

    # 4. We call to my_main
    my_main(local_False_Cloudera_True,
            my_reducer_input_parameters,
            input_file_example,
            output_file_example
            )
