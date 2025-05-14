# agent
agent
Before Installation
Make sure you install the latest package versions by updating system packages if you are running this script on a fresh Ubuntu machine.

sudo apt update && sudo apt -y upgrade
and then reboot your machine

Important!
Do not run this script as root as it will fail when setting up the site. If your VPS default user is root, create a non-root user by following these steps:

Create a new user (you can change agentuser to your preferred user name):
sudo adduser agentuser
Full Name []: agentuser
Room Number []:
Work Phone []:
Home Phone []:
Other []:
Is the information correct? [Y]
Add the user to sudoers:
usermod -aG sudo agentuser
Switch to created user:
su frappeuser
Ensure you're on created user's home directory:
cd /home/frappuser
Continue with the next steps below.
Installation:
Clone the Repo:
git clone https://github.com/fozak/agent.git
navigate to the folder:
cd erpnext_quick_install
Make the script executable
chmod +x erpnext_install.sh
Run the script:
source erpnext_install.sh
Compatibility
Ubuntu 24.04 LTS, Ubuntu 23.04 LTS, Ubuntu 22.04 LTS, Ubuntu 20.04 LTS

Debian 10 (Buster), Debian 11 (Bulls Eye) Debian 12 (Bookworm)

NOTE:
