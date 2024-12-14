from napalm import get_network_driver
import json

# Connect to the router
optional_args = {
    "dest_file_system": "nvram:",  # Specify the file system explicitly
    "session_log": "napalm_session.log",  # Log file for the session
}
router_ip = "172.16.1.17"  # Replace with R1's management IP address
username = "admin"
password = "cisco"

# Interface configuration
interface_configs = """
interface s1/0
 ip address 192.168.10.1 255.255.255.252
 no shutdown
!
interface s1/1
 ip address 192.168.10.5 255.255.255.252
 no shutdown
!
interface f0/1
 ip address 192.168.159.133 255.255.255.0
 ip nat outside
 no shutdown
!
interface f0/0
 ip nat inside
!
ip route 0.0.0.0 0.0.0.0 192.168.159.2
"""

# OSPF configuration
ospf_configs = """
router ospf 1
 router-id 1.1.1.1
 network 172.16.1.16 0.0.0.15 area 0
 network 192.168.10.0 0.0.0.3 area 0
 network 192.168.10.4 0.0.0.3 area 0
 default-information originate
!
ip nat inside source list 1 interface FastEthernet 0/1 overload
access-list 1 permit 172.16.1.16 0.0.0.15
access-list 1 permit 192.168.10.0 0.0.0.255
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
