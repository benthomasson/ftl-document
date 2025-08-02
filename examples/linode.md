# How to Set Up and Secure a Compute Instance

## Requirements
- A newly created Compute Instance that has finished booting
- SSH client installed on your local machine
- Administrative access to the Compute Instance
- Internet connection for downloading updates
- Basic knowledge of Linux command line operations

## Tools Needed
- bash_tool
- apt_tool
- dnf_tool
- timezone_tool
- hostname_tool
- user_tool
- authorized_key_tool
- lineinfile_tool
- systemd_service_tool
- service_tool
- firewalld_tool

## User Questions
- What is your preferred timezone? (e.g., America/New_York, Europe/London)
- What hostname would you like to set for your server?
- What username would you like to create for the limited user account?
- Do you have an existing SSH key pair, or do you need to generate a new one?
- Which firewall solution would you prefer to use? (firewalld, ufw, or iptables)
- Do you want to install fail2ban for additional SSH protection?

## Implementation Steps

- **Connect to the Compute Instance**:
- Log into Cloud Manager and navigate to your Compute Instance
- Copy the SSH command from the SSH Access field
- Connect using: `ssh root@[your-instance-ip]`

- **Perform system updates**:
- For Ubuntu/Debian systems: Run `apt update && apt upgrade`
- For CentOS/RHEL 8+/Fedora: Run `dnf upgrade`
- For CentOS 7: Run `yum update`
- Accept any configuration file prompts (typically keep local versions)

- **Set the timezone**:
- List available timezones: `timedatectl list-timezones`
- Set your preferred timezone: `timedatectl set-timezone 'Your/Timezone'`
- Verify the change: `date`

- **Configure a custom hostname**:
- Set the hostname: `hostnamectl set-hostname your-chosen-hostname`
- Edit the hosts file: `nano /etc/hosts`
- Add entries for your public IP and hostname:
```
127.0.0.1 localhost.localdomain localhost
[your-public-ip] your-hostname.example.com your-hostname
[your-ipv6-address] your-hostname.example.com your-hostname
```

- **Add a limited user account**:
- For Ubuntu/Debian:
- Create user: `adduser your-username`
- Add to sudo group: `adduser your-username sudo`
- For CentOS/RHEL/Fedora:
- Create user: `useradd your-username && passwd your-username`
- Add to wheel group: `usermod -aG wheel your-username`

- **Generate and upload SSH keys**:
- On your local machine, generate SSH key: `ssh-keygen -t ed25519 -C "your-email@domain.com"`
- Upload public key to server: `ssh-copy-id your-username@[your-instance-ip]`
- Set proper permissions on server: `chmod -R 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`

- **Harden SSH access**:
- Edit SSH config: `sudo nano /etc/ssh/sshd_config`
- Set `PermitRootLogin no`
- Set `PasswordAuthentication no`
- Set `AddressFamily inet` (for IPv4 only)
- Restart SSH service: `sudo systemctl restart sshd`

- **Configure firewall**:
- For firewalld systems: Enable and configure basic rules
- For UFW systems: Enable UFW and set default policies
- Allow SSH traffic on port 22
- Enable the firewall service

- **Install and configure fail2ban** (optional):
- Install fail2ban package
- Configure basic SSH protection rules
- Enable and start fail2ban service


## Verification Steps

- **Verify system updates**:
- Run update command again to confirm no additional updates are available
- Check that system responds normally after updates

- **Verify timezone configuration**:
- Run `date` command and confirm the timezone matches your selection
- Check that `timedatectl` shows the correct timezone setting

- **Verify hostname configuration**:
- Run `hostname` command to confirm the new hostname is set
- Check that the terminal prompt shows the new hostname after reconnecting
- Verify `/etc/hosts` file contains correct entries

- **Verify limited user account**:
- Log out as root and log in as the new user
- Test sudo access: `sudo whoami` should return "root"
- Confirm the user can perform administrative tasks

- **Verify SSH key authentication**:
- Log in using SSH keys without entering a password
- Confirm that password authentication is disabled by attempting to connect with a different user
- Test that root login is blocked

- **Verify SSH hardening**:
- Attempt to SSH as root - should be denied
- Attempt to SSH with password authentication - should be denied
- Confirm SSH service is running: `sudo systemctl status sshd`

- **Verify firewall configuration**:
- Check firewall status and rules
- Confirm SSH port 22 is allowed
- Test that unwanted ports are blocked
- Verify firewall service is enabled and running

- **Verify fail2ban** (if installed):
- Check fail2ban status: `sudo systemctl status fail2ban`
- Review fail2ban logs for proper SSH monitoring
- Test that fail2ban is monitoring SSH attempts


## Produces
- A fully updated and secured Compute Instance
- A properly configured limited user account with sudo privileges
- SSH access hardened with key-based authentication only
- A configured firewall protecting against unwanted network traffic
- A system ready for production use with security best practices implemented
- Optional fail2ban protection against brute-force SSH attacks