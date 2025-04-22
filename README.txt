CS 4480 - PA3: OSPF Traffic Orchestrator

Author: Aaron Glover
UID: u1438236

OVERVIEW
This project creates a Docker-based network simulation with OSPF-capable routers using FRRouting. It
includes a Python orchestrator script that builds the network, configures OSPF, sets host routes, and
allows traffic path switching between two routes.

    - North path: R1 -> R2 -> R3
    - South path: R1 -> R4 -> R3
    
The orchestrator automates topology creation, OSPF daemon setup, host route installation, and OSPF cost
adjustments to switch traffic paths without packet loss.

## FOLDER STRUCTURE
- Aaron_Glover_u1438236.py # Main Python script to control the setup
- docker-compose.yaml # Defines container network topology
- router.Dockerfile # Dockerfile for router containers with FRR
- host.Dockerfile # Dockerfile for HostA and HostB

## SETUP INSTRUCTIONS
1. Similar to the directions for PA3, clone the helper files: 
    git clone https://gitlab.flux.utah.edu/teach-studentview/cs4480-2025-s.git
2. Run the following command to install docker:
    cd cs4480-2025-s/pa3/part1/
    ./dockersetup
    sudo systemctl start docker
3. Next clone the orchestrator repo:
    git clone https://github.com/aaron-glover/PA3.git


## ORCHESTRATOR USAGE
Run the orchestrator script with the appropriate option:
    python3 Aaron_Glover_u1438236.py -h # brings up the help menu with commands listed below

Available Commands:
- "build": Brings up the full Docker topology using docker-compose
- "start": Enables ospfd and starts OSPF configuration on all routers
- "route": Adds default routes to HostA and HostB
- "north": Switches traffic to the North path (R1 -> R2 -> R3)
- "south": Switches traffic to the South path (R1 -> R4 -> R3)

Example Workflow:
Step 1. python3 Aaron_Glover_u1438236.py build
Step 2. python3 Aaron_Glover_u1438236.py start
Step 3. python3 Aaron_Glover_u1438236.py route
Step 4. python3 Aaron_Glover_u1438236.py north # or python3 Aaron_Glover_u1438236.py south

NOTES
- the install for tcpdump is in the router.Dockerfile but if for some reason tcpdump isn't installed:
    sudo docker exec -it r$ apt update
    sudo docker exec -it r$ apt install -y tcpdump 
    Where $ is 1, 2, 3, and 4

- To reset the environment:
    sudo docker compose down
    sudo python3 Aaron_Glover_u1438236.py build

- If Docker fails to run:
    sudo systemctl start docker

