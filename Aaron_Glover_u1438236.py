import argparse
import subprocess

# --- Helper to run shell commands ---
def run(cmd):
    print(f"[+] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

# --- Build Docker topology ---
def build_topology():
    run(["docker", "compose", "up", "-d"])

# --- Enable ospfd daemon and restart FRR ---
def enable_ospfd():
    routers = ["r1", "r2", "r3", "r4"]
    for r in routers:
        print(f"[+] Enabling ospfd on {r}")
        run(["docker", "exec", r, "sed", "-i", "s/ospfd=no/ospfd=yes/", "/etc/frr/daemons"])
        run(["docker", "exec", r, "service", "frr", "restart"])

# --- Start OSPF on all routers ---
def start_ospf():
    enable_ospfd()
    routers = ["r1", "r2", "r3", "r4"]
    ospf_config = {
        "r1": ["10.0.0.0/24"],
        "r2": ["10.0.0.0/24"],
        "r3": ["10.0.0.0/24"],
        "r4": ["10.0.0.0/24"]
    }

    for r in routers:
        net_cmds = [f"-c network {n} area 0.0.0.0" for n in ospf_config[r]]
        run([
            "docker", "exec", r, "vtysh",
            "-c", "configure terminal",
            "-c", "router ospf",
            "-c", f"ospf router-id 1.1.1.{routers.index(r) + 1}",
            *net_cmds,
            "-c", "exit",
            "-c", "exit",
            "-c", "write memory"
        ])

# --- Add routes to HostA and HostB ---
def setup_routes():
    try:
        run(["docker", "exec", "hosta", "ip", "route", "add", "default", "via", "10.0.0.2"])
    except subprocess.CalledProcessError:
        print("[!] hosta route may already exist, skipping.")
    try:
        run(["docker", "exec", "hostb", "ip", "route", "add", "default", "via", "10.0.0.4"])
    except subprocess.CalledProcessError:
        print("[!] hostb route may already exist, skipping.")

# --- Switch to NORTH path: R1 -> R2 -> R3 ---
def switch_north():
    run(["docker", "exec", "r1", "vtysh", "-c", "conf t", "-c", "interface eth0", "-c", "ip ospf cost 1", "-c", "end", "-c", "write memory"])
    run(["docker", "exec", "r3", "vtysh", "-c", "conf t", "-c", "interface eth0", "-c", "ip ospf cost 1", "-c", "end", "-c", "write memory"])
    run(["docker", "exec", "r4", "vtysh", "-c", "conf t", "-c", "interface eth0", "-c", "ip ospf cost 100", "-c", "end", "-c", "write memory"])

# --- Switch to SOUTH path: R1 -> R4 -> R3 ---
def switch_south():
    run(["docker", "exec", "r1", "vtysh", "-c", "conf t", "-c", "interface eth0", "-c", "ip ospf cost 100", "-c", "end", "-c", "write memory"])
    run(["docker", "exec", "r3", "vtysh", "-c", "conf t", "-c", "interface eth0", "-c", "ip ospf cost 100", "-c", "end", "-c", "write memory"])
    run(["docker", "exec", "r4", "vtysh", "-c", "conf t", "-c", "interface eth0", "-c", "ip ospf cost 1", "-c", "end", "-c", "write memory"])

# --- Main entry point ---
def main():
    parser = argparse.ArgumentParser(description="OSPF Traffic Orchestrator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("build", help="Build Docker topology")
    subparsers.add_parser("start", help="Start and configure OSPF daemons")
    subparsers.add_parser("route", help="Add static routes to hosts")
    subparsers.add_parser("north", help="Switch to R1-R2-R3 (north) path")
    subparsers.add_parser("south", help="Switch to R1-R4-R3 (south) path")

    args = parser.parse_args()

    if args.command == "build":
        build_topology()
    elif args.command == "start":
        start_ospf()
    elif args.command == "route":
        setup_routes()
    elif args.command == "north":
        switch_north()
    elif args.command == "south":
        switch_south()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()