# TaskMaster - Linux System Management Tool 🚀

TaskMaster is a comprehensive Linux system management and monitoring tool that provides a user-friendly CLI interface for various system administration tasks. It features real-time system monitoring, process management, disk operations, network tools, and more.

![Command Line Interface](https://raw.githubusercontent.com/yourusername/taskmaster/main/screenshots/cli.png)

## 🌟 Features

### 💻 System Monitoring
- Real-time CPU, memory, and disk usage monitoring
- System temperature tracking
- Detailed system information display
- Performance metrics visualization

### 🔄 Process Management
- List and monitor running processes
- Process search functionality
- Kill/terminate processes
- Process priority management
- Real-time process monitoring
- Process tree visualization

### 💾 Disk Tools
- Disk usage analysis
- Partition management
- Disk health monitoring
- Disk speed testing
- Mount/unmount operations
- File system information

### 🌐 Network Tools
- Network interface monitoring
- Speed testing
- Ping and traceroute utilities
- Port scanning
- DNS lookup
- Network statistics
- Active connection monitoring

### 📦 Package Management
- Search packages
- Install/remove packages
- List installed packages
- Update package lists
- Clean package cache

### 👥 User Management
- User account creation/deletion
- Password management
- User group management
- User information display

### 🔧 Service Management
- Start/stop services
- Service status monitoring
- Enable/disable services
- Service listing

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/taskmaster.git
cd taskmaster
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Install system dependencies:
```bash
# For Debian/Ubuntu
sudo apt-get install speedtest-cli traceroute net-tools smartmontools

# For Fedora/RHEL
sudo dnf install speedtest-cli traceroute net-tools smartmontools
```

## 🚀 Usage

Run the main script:
```bash
sudo python main.py
```

Navigate through the menus using the number keys and follow the on-screen prompts.

## 📋 Requirements

- Python 3.8+
- Linux operating system
- Root/sudo privileges for certain operations

### Python Dependencies
- psutil==5.9.8
- colorama==0.4.6
- tabulate==0.9.0
- python-daemon==3.0.1
- speedtest-cli==2.1.3
- netifaces==0.11.0
- distro==1.8.0
- py-cpuinfo==9.0.0
- click==8.1.7
- rich==13.7.0

## 🔒 Security Notes

- Some operations require root privileges
- Be careful with system-critical operations
- Always verify before killing processes or modifying system settings

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Authors

- Rajan - Initial work - [YourGithubUsername](https://github.com/neupane-rajan)

## 🙏 Acknowledgments

- [psutil](https://github.com/giampaolo/psutil) - Process and system utilities
- [colorama](https://github.com/tartley/colorama) - Cross-platform colored terminal text
- [tabulate](https://github.com/astanin/python-tabulate) - Pretty-print tabular data
