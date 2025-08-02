# How to Set Up a Minecraft Java Edition Server

## Requirements
- A computer with at least 2GB RAM (4-8GB recommended for 4-8 players)
- At least 5GB of available disk space
- Stable internet connection (wired connection preferred over Wi-Fi)
- Administrative access to your computer and router
- Basic knowledge of command-line operations and networking concepts
- 

## Tools Needed
- bash_tool
- get_url_tool
- mkdir_tool
- copy_tool
- chmod_tool
- service_tool
- firewalld_tool
- lineinfile_tool
- 

## User Questions
- What version of Minecraft server do you want to run? (Latest recommended: 1.21)
- How much RAM do you want to allocate to the server? (2GB minimum, 4-8GB recommended)
- What port do you want the server to run on? (Default: 25565)
- Do you want to enable whitelist for security? (Recommended: Yes)
- Will this be a local LAN server or do you need internet access via port forwarding?
- What operating system are you running? (Windows, macOS, Linux)
- 

## Implementation Steps

**Phase 1: Java Installation**
- Check if Java is already installed:
- Open command prompt/terminal
- Run `java -version` to check current Java version
- Verify you have Java 21 for Minecraft 1.21+ or Java 17 for Minecraft 1.18+
- Install Java if needed:
- **Windows**: Download Adoptium's OpenJDK Temurin from https://adoptium.net/ or use `winget install EclipseAdoptium.Temurin.21.JRE`
- **macOS**: Install via Homebrew with `brew install --cask temurin@21`
- **Linux (Ubuntu/Debian)**: Run `sudo apt update && sudo apt install openjdk-21-jdk-headless`
- **Linux (Fedora/RHEL)**: Run `sudo dnf install java-21-openjdk-headless`

**Phase 2: Server Setup**
- Create server directory:
- Create a new folder for your Minecraft server (e.g., "minecraft-server")
- Navigate to this folder in command prompt/terminal
- Download server software:
- Visit https://www.minecraft.net/en-us/download/server
- Download the server.jar file for your desired version
- Rename the downloaded file to "server.jar"
- Move server.jar to your server directory

**Phase 3: Initial Server Configuration**
- Run server for first time:
- Open command prompt/terminal in server directory
- Run `java -jar server.jar --nogui`
- Server will create files and stop with EULA message
- Accept EULA:
- Open the generated "eula.txt" file in a text editor
- Change `eula=false` to `eula=true`
- Save the file
- Configure server properties:
- Open "server.properties" file in text editor
- Set `server-port=25565` (or your preferred port)
- Set `white-list=true` for security (recommended)
- Set `max-players` to desired number
- Configure other settings as needed

**Phase 4: Create Startup Script**
- **Windows**: Create "start.bat" file with content:
```
@ECHO OFF
java -Xms1024M -Xmx2048M -jar server.jar --nogui
pause
```
- **macOS/Linux**: Create "start.sh" file with content:
```
#!/bin/sh
cd "$(dirname "$0")"
exec java -Xms1024M -Xmx2048M -jar server.jar --nogui
```
- Make script executable (macOS/Linux): Run `chmod +x start.sh`

**Phase 5: Firewall Configuration**
- **Windows**:
- Allow Java through Windows Firewall when prompted
- Or manually add firewall rule for port 25565 (TCP/UDP)
- **Linux**: Configure firewall to allow Minecraft port:
- `sudo ufw allow 25565` (Ubuntu) or `sudo firewall-cmd --add-port=25565/tcp --permanent` (Fedora)

**Phase 6: Network Setup (Choose One)**
- **For LAN only**:
- Find your internal IP address using `ipconfig` (Windows) or `ip addr` (Linux)
- Players connect using your internal IP:25565
- **For Internet access**:
- Configure port forwarding on your router:
- Access router admin panel (usually 192.168.1.1 or 192.168.0.1)
- Find port forwarding settings
- Forward external port 25565 to your internal IP port 25565
- Set protocol to TCP/UDP or Both
- Find your external IP address (Google "what is my IP")
- Players connect using your external IP:25565

**Phase 7: Server Management Setup**
- Configure operators:
- Start the server
- In server console, run `op <username>` to make players operators
- Configure whitelist (if enabled):
- In server console, run `whitelist add <username>` for each allowed player
- Or edit whitelist.json file directly


## Verification Steps

- Run `java -version` in command prompt/terminal
- Verify output shows Java 17+ (Java 21 recommended for latest Minecraft)
- Confirm no error messages about Java not being found

- Run the startup script (start.bat or start.sh)
- Verify server console shows "Done" message without errors
- Check that server.properties file exists and contains your settings
- Confirm eula.txt shows `eula=true`

- Start Minecraft client on same machine
- Go to Multiplayer → Direct Connect
- Enter `localhost:25565` (or your custom port)
- Verify successful connection to server

- **For LAN**: Have another device on same network connect using internal IP
- **For Internet**: Use online port checker tool (e.g., yougetsignal.com) to verify port 25565 is open
- Test connection from external network using your external IP address

- Confirm no "connection timed out" errors when connecting
- Verify firewall rules allow Java/Minecraft traffic
- Test both TCP and UDP protocols if possible

- Monitor server console for lag warnings
- Check server TPS (ticks per second) - should be close to 20
- Verify RAM usage stays within allocated limits
- Confirm CPU usage is reasonable for your hardware

- Test that whitelist blocks unauthorized players (if enabled)
- Verify operator commands work for designated ops
- Confirm server responds appropriately to player connections


## Produces
- A fully functional Minecraft Java Edition server
- Proper network configuration for player access (LAN or Internet)
- Security measures including whitelist and operator controls
- Startup scripts for easy server management
- Firewall configuration allowing server traffic
- Documentation of server settings and connection details