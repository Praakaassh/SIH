import os
import sys
import traci

if __name__ == '__main__':
    # Ensure the SUMO_HOME environment variable is set
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # Command to start SUMO (change "sumo" to "sumo-gui" to watch it run)
    sumo_cmd = ["sumo", "-c", "attingal.sumocfg", "--no-warnings", "true"]

    # Start the simulation and connect to it with TraCI
    traci.start(sumo_cmd)
    
    # --- STATIC (FIXED-TIME) CONTROLLER LOGIC ---
    
    traffic_light_id = "intersection_north"
    
    # Define the traffic light phases
    PHASE_NS_GREEN = 0  # North-South Green
    PHASE_NS_YELLOW = 1 # North-South Yellow
    PHASE_W_GREEN = 2   # West Green
    PHASE_W_YELLOW = 3  # West Yellow

    # Define the fixed duration for each phase in seconds
    NS_GREEN_TIME = 30
    NS_YELLOW_TIME = 4
    W_GREEN_TIME = 15
    W_YELLOW_TIME = 4
    
    # The total time for one full, repeating cycle
    TOTAL_CYCLE_TIME = NS_GREEN_TIME + NS_YELLOW_TIME + W_GREEN_TIME + W_YELLOW_TIME

    print("Running baseline simulation with static traffic lights...")
    
    # --- THIS LOOP IS CHANGED ---
    # It now runs until the simulation time reaches 3600 seconds
    while traci.simulation.getTime() < 3600:
        traci.simulationStep() # Advance the simulation by one second
        
        # Get the current simulation time
        current_time = traci.simulation.getTime()
        
        # Calculate where we are in the repeating traffic light cycle
        cycle_time = current_time % TOTAL_CYCLE_TIME
        
        # Set the correct traffic light phase based on the cycle time
        if cycle_time < NS_GREEN_TIME:
            traci.trafficlight.setPhase(traffic_light_id, PHASE_NS_GREEN)
        elif cycle_time < NS_GREEN_TIME + NS_YELLOW_TIME:
            traci.trafficlight.setPhase(traffic_light_id, PHASE_NS_YELLOW)
        elif cycle_time < NS_GREEN_TIME + NS_YELLOW_TIME + W_GREEN_TIME:
            traci.trafficlight.setPhase(traffic_light_id, PHASE_W_GREEN)
        else:
            traci.trafficlight.setPhase(traffic_light_id, PHASE_W_YELLOW)

    # Close the TraCI connection
    traci.close()
    
    print("\nBaseline simulation finished after 3600 seconds. Results saved to 'tripinfo.xml'.")