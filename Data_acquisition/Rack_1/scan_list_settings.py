import numpy as np
import motor as mt

def scan_list(n_scans, length, step_size):
    scan_list_list =[]
    for i in range(n_scans*2):
        if i % 2 == 0 or 0:
            scan_list_list.append([mt.dir.DOWN, length, step_size])
        else:
            scan_list_list.append([mt.dir.UP, length, step_size])
    return scan_list_list