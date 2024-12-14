from napalm import get_network_driver
import json

# Connect to the router
optional_args = {
    "dest_file_system": "nvram:",  # Specify the file system explicitly
    "session_log": "napalm_session.log",  # Log file for the session
}
router_ip = "192.168.10.6"  # Replace with R1's management IP address
username = "admin"
password = "cisco"

# Interface configuration
interface_configs = """
interface f0/0
 ip address 172.16.1.33 255.255.255.0
 no shutdown
!
interface s1/0
 ip address 192.168.10.10 255.255.255.252
 no shutdown
"""

# OSPF configuration
ospf_configs = """
router ospf 1
 router-id 3.3.3.3
 network 192.168.10.4 0.0.0.3 area 0
 network 192.168.10.8 0.0.0.3 area 0
 network 172.16.1.32 0.0.0.7 area 0
"""

def configure_router(ip, username, password, config):
    print(f"Connecting to {ip}...")
    driver = get_network_driver("ios")
    device = driver(hostname=ip, username=username, password=password, optional_args=optional_args)
    try:
        device.open()
        print("Applying configuration...")
        device.load_merge_candidate(config=config.strip())
        device.commit_config()
        print("Configuration applied successfully!")
        device.close()
        print(f"Session log saved to {optional_args['session_log']}")
    except Exception as e:
        print(f"Failed to configure {ip}: {e}")

# Run the configuration
if __name__ == "__main__":
    print("Applying interface configuration...")
    configure_router(router_ip, username, password, interface_configs)

    print("Applying OSPF configuration...")
    configure_router(router_ip, username, password, ospf_configs)
