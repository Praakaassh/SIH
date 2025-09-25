import os
import sys
import traci
import time # Import the time library

# This is the main entry point of the script
if __name__ == '__main__':
    # We need to import python modules from the $SUMO_HOME/tools directory
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # Defines the command to start SUMO with your configuration
    sumo_cmd = ["sumo-gui", "-c", "attingal.sumocfg", "--seed", "42"]

    # 1. Start SUMO as a subprocess and connect with TraCI
    traci.start(sumo_cmd)
    
    # 2. The main loop of the simulation
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep() # Advance the simulation by one step
        
        # --- START OF DEBUGGING CODE ---

        # Get the list of vehicle IDs that entered the simulation in this step
        departed_vehicles = traci.simulation.getDepartedIDList()
        if departed_vehicles:
            print(f"Step {traci.simulation.getTime()}: Departed vehicles: {departed_vehicles}")

        # Get the list of all vehicle IDs currently in the simulation
        all_vehicles = traci.vehicle.getIDList()
        if not all_vehicles:
             print(f"Step {traci.simulation.getTime()}: No vehicles in simulation.")
        
        # Add a small delay to make the GUI easier to watch
        time.sleep(0.1)

        # --- END OF DEBUGGING CODE ---

    # 3. Close the TraCI connection
    traci.close()