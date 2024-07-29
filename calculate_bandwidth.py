import argparse
import re
from pathlib import Path
import numpy as np

def pa():
    p = argparse.ArgumentParser(description='Test')
    p.add_argument('logdir', type=str, help='directory with logfiles')
    return p.parse_args()

def parse_time(time_str):
    """
    Parse a time string in the format 'XmYs' and convert it to seconds.
    """
    match = re.match(r"(\d+)m(\d+)\.(\d+)s", time_str)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        milliseconds = int(match.group(3)) / 1000
        return minutes * 60 + seconds + milliseconds
    return None

def read_timing_file(filename):
    """
    Read a timing file and extract the real, user, and sys times in seconds.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    timing = {}
    for line in lines:
        if line.startswith('real'):
            timing['real'] = parse_time(line.split()[1])
        elif line.startswith('user'):
            timing['user'] = parse_time(line.split()[1])
        elif line.startswith('sys'):
            timing['sys'] = parse_time(line.split()[1])
    
    return timing

args = pa()
logdir = args.logdir

speeds = []
for file in Path(logdir).glob('*'):
    timing = read_timing_file(file)
    speeds.append(timing['real'])

#divide by 8 to get the speed in Gb/s
#speeds = [8*speed for speed in speeds]
rates = [8/speed for speed in speeds]

print("Avg rate:", sum(rates)/len(rates), "Gb/s")
print("Stdev rate:", np.std(rates), "Gb/s")

#print("Avg time:", sum(speeds)/len(speeds), "s")
#print("Stdev time:", np.std(speeds), "s")



# def extract_speeds(file_path):
#     # Regular expression to match the bandwidth line
#     speed_pattern = re.compile(r'(\d+(\.\d+)?) MB/s')
    
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
    
#     speeds = []
    
#     for line in lines:
#         match = speed_pattern.search(line)
#         if match:
#             speeds.append(float(match.group(1)))
    
#     return speeds

# def convert_mb_s_to_gb_s(speed_mb_s):
#     """ Convert speed from MB/s to Gb/s. """
#     return speed_mb_s * 8 / 1000

# args = pa()
# logdir = args.logdir

# speeds = []
# for file in Path(logdir).glob('*'):
#     speed = extract_speeds(file)
#     #print(speeds)
#     #take the min value
#     speeds.append(min(speed))

# print("Avg speed:", sum(speeds)/len(speeds), "MB/s")
# print("Avg speed:", convert_mb_s_to_gb_s(sum(speeds)/len(speeds)), "Gb/s")
# print("Stdev speed:", np.std(speeds), "MB/s")
# print("Stdev speed:", convert_mb_s_to_gb_s(np.std(speeds)), "Gb/s")