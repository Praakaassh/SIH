import xml.etree.ElementTree as ET
import sys

def analyze_tripinfo(filename):
    """
    Parses a SUMO tripinfo XML file and prints key performance statistics.
    """
    
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        
        total_vehicles = 0
        total_travel_time = 0
        total_waiting_time = 0
        
        # Iterate through every 'tripinfo' element in the XML file
        for tripinfo in root.findall('tripinfo'):
            total_vehicles += 1
            # 'duration' is the total travel time for a vehicle
            total_travel_time += float(tripinfo.get('duration'))
            # 'timeLoss' is the time a vehicle spent waiting or in jams
            total_waiting_time += float(tripinfo.get('timeLoss'))
            
        if total_vehicles > 0:
            # Calculate the averages
            avg_travel_time = total_travel_time / total_vehicles
            avg_waiting_time = total_waiting_time / total_vehicles
            
            print(f"\n--- PERFORMANCE ANALYSIS for '{filename}' ---")
            print(f"Total vehicles completed: {total_vehicles}")
            print(f"Average Travel Time per vehicle: {avg_travel_time:.2f} seconds")
            print(f"Average Waiting Time per vehicle: {avg_waiting_time:.2f} seconds")
        else:
            print(f"No vehicles completed their trips in the simulation for file '{filename}'.")

    except FileNotFoundError:
        print(f"\n--- ERROR ---")
        print(f"The file '{filename}' was not found in your folder.")
        print("Please make sure the simulation that creates this file has finished running.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Get the filename from the command line argument
        filename_to_analyze = sys.argv[1]
        analyze_tripinfo(filename_to_analyze)
    else:
        print("Please provide a filename to analyze.")
        print("Example: python analyze_output.py tripinfo.xml")