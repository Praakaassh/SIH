import os
import sys
import traci
import numpy as np
import collections
import pickle

# Ensure SUMO_HOME is set
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# We need the QLearningAgent class definition to understand the saved file
class QLearningAgent:
    def __init__(self, action_space):
        self.action_space = action_space
        self.q_table = collections.defaultdict(lambda: np.zeros(len(action_space)))
        # In testing mode, epsilon is 0 to always choose the best action
        self.epsilon = 0

    def choose_action(self, state):
        # Always choose the best known action from the Q-table
        return np.argmax(self.q_table[state])

# We also need the get_state function
def get_state(traffic_light_id):
    lanes_to_monitor = {
        "north": ["MainN_to_I1_0", "MainN_to_I1_1"],
        "south": ["I2_to_I1_0", "I2_to_I1_1"],
        "west": ["SideW_to_I1_0"]
    }
    state = []
    for direction in ["north", "south", "west"]:
        total_queue = sum(traci.lane.getLastStepHaltingNumber(lane) for lane in lanes_to_monitor[direction])
        if total_queue < 5: state.append(0)
        elif total_queue < 10: state.append(1)
        else: state.append(2)
    return tuple(state)

if __name__ == '__main__':
    Q_TABLE_FILE = "q_table.pkl"
    TRAFFIC_LIGHT_ID = "intersection_north"
    
    action_space = [0, 1]
    action_map = {0: 0, 1: 2}

    # --- Load the Trained Agent's Brain ---
    agent = QLearningAgent(action_space)
    with open(Q_TABLE_FILE, 'rb') as f:
        loaded_dict = pickle.load(f)
        agent.q_table.update(loaded_dict)
    print("Trained Q-table loaded successfully.")

    # --- Run the Test Simulation ---
    sumo_cmd = ["sumo-gui", "--start", "-c", "attingal.sumocfg", "--seed", "42", "--no-warnings", "true"]
    traci.start(sumo_cmd)
    
    # --- THIS LOOP IS CHANGED ---
    # It now runs until the simulation time reaches 3600 seconds
    while traci.simulation.getTime() < 3600:
        traci.simulationStep()
        
        # The agent controls the light for every step of the simulation
        state = get_state(TRAFFIC_LIGHT_ID)
        action_index = agent.choose_action(state)
        phase_to_set = action_map[action_index]
        
        if traci.trafficlight.getPhase(TRAFFIC_LIGHT_ID) != phase_to_set:
            traci.trafficlight.setPhase(TRAFFIC_LIGHT_ID, phase_to_set)

    traci.close()
    print("Test simulation finished after 3600 seconds.")