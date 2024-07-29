import re
import argparse
import numpy as np

def pa():
    p = argparse.ArgumentParser(description='Test')
    p.add_argument('filename', type=str, help='name of the file to read')
    return p.parse_args()

def ping_times(filename, num_lines=100):
    times = []
    
    # Open the file and read line by line
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            # Stop after reading the specified number of lines
            if i >= num_lines:
                break
            
            # Use a regular expression to find the time value in the line
            match = re.search(r'time=(\d+\.\d+) ms', line)
            if match:
                # Extract the time value and convert it to a float
                time_value = float(match.group(1))
                times.append(time_value)
    
    # Compute the average if we have collected any times
    if times:
        return np.array(times)
    else:
        return None

# Define the filename and call the function
args = pa()
filename = args.filename
times = ping_times(filename)

print("Average time for the first 100 lines:", np.mean(times), "ms")
print("Standard deviation for the first 100 lines:", np.std(times), "ms")

#if average_time is not None:
#    print(f"Average time for the first 100 lines: {average_time:.3f} ms")
#else:
#    print("No valid time values found in the file.")
