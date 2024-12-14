# NAPALM-Network-Automation-GNS3

## **Setup the network topology**

![image](https://github.com/user-attachments/assets/59684dc2-8b8b-4db8-b569-5661ac901e4c)

Follow below addressing tables

![image](https://github.com/user-attachments/assets/afd41d96-db19-456e-9a77-263fbecf7e8a)

### ⚙️**Connect interfaces as below :**
  R1 
  f0/0 <=> e0 Switch 3
  f0/1 <=> eth1 Cloud 1
  s1/0 <=> s1/0 R2
  s1/1 <=> s1/1 R3
  
  R2
  f0/0 <=> e0 Switch 2
  s1/0 <=> s1/0 R1
  s1/1 <=> s1/0 R3
  
  R3
  f0/0 <=> e0 Switch 1
  s1/0 <=> s1/1 R2
  s1/1 <=> s1/1 R1
  
  Switch1
  e0 <=> f0/0 R3
  e1 <=> e0 PC3
  
  Switch2
  e0 <=> f0/0 R2
  e1 <=> e0 PC2
  
  Switch3
  e0 <=> f0/0 R1
  e1 <=> ens4 PC1
  
  PC1
  ens4 <=> e1 Switch3
  
  PC2
  e0 <=> e1 Switch2
  
  Cloud1
  eth1 <=> f0/1 R1

## ⚙️**Configure interfaces connected to r1 to start pushing configuration using NAPALM from pc1**
R1
- **Basic Configuration**

  **APPLY TO ALL ROUTERS**
  ```bash
  ip domain-lookup
  ip name-server 8.8.8.8
  ip domain-name cisco.com
  crypto key generate rsa #<input 812 when prompted, as we need to enable SSH version 1.99>
  username admin privilege 15 secret cisco
  line vty 0 4
  transport input ssh
  login local
  exit
  ip scp server enable
  ```

  **R1**
  ```bash
  configure terminal
  interface f0/0
  ip address 172.16.1.17 255.255.255.240
  no shutdown
  exit
  end
  write memory
  ```

  **R2**
  ```bash
  configure terminal
  interface s1/0
  ip address 192.168.10.2 255.255.255.252
  no shutdown
  exit
  ip route 0.0.0.0 0.0.0.0 192.168.10.1
  ip route 172.16.1.16 255.255.255.240 192.168.10.5 #set static routes for pc1 to communicate
  end
  write memory
  ```
  
  **R3**
  ```bash
  configure terminal
  interface s1/1
  ip address 192.168.10.6 255.255.255.252
  no shutdown
  exit
  ip route 0.0.0.0 0.0.0.0 192.168.10.5
  ip route 172.16.1.16 255.255.255.240 192.168.10.5 #set static routes for pc1 to communicate
  end
  write memory
  ```
  #IMPORTANT!!
  write memory command is very important for it to be successfully saved after pushing the config. Otherwise it will return error pattern not detected.
  
- **Configure pc1 network**  
  In this example, pc1 uses debian image in GNS3. To edit network configuration, head over to `/etc/network/interfaces`.  
  Username : debian

  Password: debian
  
  ```bash
  sudo nano /etc/network/interfaces
  ```
  Set as below and point the gateway to r1 f0/0 interface.
  ```bash
  # Static config for ens4
  auto ens4
  iface ens4 inet static
          address 172.16.1.20
          netmask 255.255.255.240
          gateway 172.16.1.17
          dns-nameservers 172.16.1.17
          dns-nameservers 8.8.8.8
  ```

### 🔗**Pushing script from pc1**
- Edit `/home/debian/verify_device_connected.py`
  Change the targeted ip to 172.16.1.17 to verify r1 can be connected.

- If successful, start pushing `r1_conf.py`
```bash
python3 r1_conf.py
```
Repeat above steps for r2 and r3
```bash
python3 r2_conf.py
```
```bash
python3 r3_conf.py
```

## ▶️**Verify Connection**

###**Verify IP assignment and OSPF**

Execute in EXEC mode
- Use the following command to verify interface assignment:
```bash
show ip int brief
```
![image](https://github.com/user-attachments/assets/888905e3-9c9f-4892-8db9-ba859e7b3090)

- For OSPF:
```bash
show ip ospf neighbour
```
![image](https://github.com/user-attachments/assets/d0ebf2b6-a0cd-451b-83f7-51fef591913a)

### **Verify Network Connectivity in each router**
- Ping R2 from PC1 in R1
```bash
ping 192.168.10.2
```
![image](https://github.com/user-attachments/assets/8ad6e54c-d915-42bd-8c9b-6f95bf290317)

- Ping PC1 in R1 from PC2 in R2
```bash
ping 172.16.1.20
```
![image](https://github.com/user-attachments/assets/37b44400-7abb-4c1c-b294-dafd8baf1b3b)

Ensure to configure and set default gateway as 10.10.10.1 in pc2 before verifying

