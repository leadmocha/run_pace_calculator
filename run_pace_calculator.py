#!/usr/bin/env python3
import argparse

def print_lap_pace(average_pace_min,average_pace_sec,distance, d_unit='km', step = None):
    # First, determine an appropriate step size
    if step is None:
        if distance > 1000:
            step = 100
        elif distance > 100:
            step = 10
        elif distance > 15:
            step = 5
        else:
            step = 1
    
    elapsed_distance = 0.
    elapsed_seconds = 0.
    lap = 0
    print('lap |  Distance  |   Time ')
    print('--- | ---------- | --------')
    while elapsed_distance < distance:
        lap += 1
        # Determine if we can take another whole step in this period
        elapsed_distance += step
        if elapsed_distance <= distance: # can take whole step
            elapsed_seconds += (average_pace_min*60 + average_pace_sec)*step
        else: # Cannot take whole step
            distance_in_step = distance - (elapsed_distance - step)
            elapsed_distance = distance
            elapsed_seconds += (average_pace_min*60+average_pace_sec)*distance_in_step
            round(elapsed_seconds)
        hours = int(elapsed_seconds/3600)
        minutes = int((elapsed_seconds-3600*hours)/60)
        seconds = int((elapsed_seconds-minutes*60-hours*3600))
        time_str = f'{hours:2}:' if hours > 0 else '   '
        time_str += f'{minutes:02}:{seconds:02}'

        print(f'{lap:3} | {elapsed_distance:7.2f} {d_unit} | {time_str}')

def by_target_time(target_time : str,distance : float, d_unit : str = 'km'):
    items = target_time.split(':')
    total_seconds : int = 0
    if len(items) == 3: # We have hours included
        hours,minutes,seconds = [ round(float(v)) for v in items ]
        total_seconds = seconds+60*minutes+3600*hours
    elif len(items) == 1: # Assume only seconds are given
        total_seconds = float(items[0])
    else:
        minutes,seconds = [ round(float(v)) for v in items ]
        total_seconds = seconds+60*minutes

    average_speed = distance/(total_seconds/3600)
    average_pace_total = (total_seconds/60)/distance
    average_pace_min  = int(average_pace_total)
    average_pace_sec   = round((average_pace_total - average_pace_min)*60)
    average_pace = f'{average_pace_min:2}:{average_pace_sec:02}'

    print(f'Average speed: {average_speed:.2f} {d_unit}/hr')
    print(f'Average pace: {average_pace} min/{d_unit}')

    print_lap_pace(average_pace_min,average_pace_sec,distance,d_unit=d_unit)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run calculator')

    parser.add_argument('--target-time',dest='target_time',default=None,
                        help='Calculate pace based on target time')
    parser.add_argument('--distance',dest='distance',default=None,required=True,
                        help='Distance to estimate',type=float)
    parser.add_argument('--unit',dest='unit',default='km',
                        help='Distance to estimate',type=str)

    args = parser.parse_args()

    # Select out what to do
    if args.target_time is not None:
        by_target_time(args.target_time,args.distance,d_unit=args.unit)

