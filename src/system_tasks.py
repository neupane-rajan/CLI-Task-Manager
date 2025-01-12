import subprocess
import platform
import os
import glob
import shutil
from datetime import datetime
from typing import Optional, List, Dict
from colorama import Fore, Style


class SystemTasks:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.package_manager = self._detect_package_manager()
        self.required_tools = {
            "tar": False,
            "ufw": False,
            "netstat": False,
            "journalctl": False,
        }
        self._check_required_tools()

    def _detect_package_manager(self) -> Dict[str, List[str]]:
        """Detect the system's package manager and return appropriate commands."""
        if self.os_type == "linux":
            if shutil.which("apt"):
                return {
                    "update": ["apt", "update"],
                    "upgrade": ["apt", "upgrade", "-y"],
                    "clean": ["apt", "autoremove", "-y"],
                    "check_updates": ["apt", "list", "--upgradable"],
                }
            elif shutil.which("dnf"):
                return {
                    "update": ["dnf", "check-update"],
                    "upgrade": ["dnf", "upgrade", "-y"],
                    "clean": ["dnf", "autoremove", "-y"],
                    "check_updates": ["dnf", "list", "updates"],
                }
        return {}

    def _check_required_tools(self):
        """Check if required tools are installed."""
        for tool in self.required_tools:
            self.required_tools[tool] = shutil.which(tool) is not None

    def _run_command(self, command: List[str], sudo: bool = True) -> bool:
        """Run a system command with proper error handling."""
        try:
            if sudo and os.geteuid() != 0:
                command.insert(0, "sudo")
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(
                f"{Fore.RED}❌ Command failed: {' '.join(command)}\nError: {str(e)}{Style.RESET_ALL}"
            )
            return False
        except FileNotFoundError:
            print(f"{Fore.RED}❌ Command not found: {command[0]}{Style.RESET_ALL}")
            return False

    def show_tasks_menu(self):
        while True:
            print(
                f"""{Fore.CYAN}
            ╔═══ System Tasks ══════════════════════════╗
            ║ 1. Clean System Cache                     ║
            ║ 2. Check System Health                    ║
            ║ 3. Optimize System                        ║
            ║ 4. Repair System                          ║
            ║ 5. Backup System                          ║
            ║ 6. Restore System                         ║
            ║ 7. Security Tools                         ║
            ║ 8. System Logs                            ║
            ║ 9. Update System                          ║
            ║ 10. System Information                    ║
            ║ 0. Exit                                   ║
            ╚═══════════════════════════════════════════╝
            {Style.RESET_ALL}"""
            )

            choice = input(f"{Fore.CYAN}Enter your choice (0-10): {Style.RESET_ALL}")

            if choice == "0":
                break
            elif choice == "1":
                self.clean_system()
            elif choice == "2":
                self.check_system_health()
            elif choice == "3":
                self.optimize_system()
            elif choice == "4":
                self.repair_system()
            elif choice == "5":
                self.backup_system()
            elif choice == "6":
                self.restore_system()
            elif choice == "7":
                self.security_menu()
            elif choice == "8":
                self.show_logs()
            elif choice == "9":
                self.update_system()
            elif choice == "10":
                self.show_system_info()
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")

            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def check_system_health(self):
        """Check various system health metrics."""
        print(f"{Fore.YELLOW}🔍 Checking system health...{Style.RESET_ALL}")

        # Check disk space
        self._run_command(["df", "-h"], sudo=False)

        # Check memory usage
        self._run_command(["free", "-h"], sudo=False)

        # Check system load
        self._run_command(["uptime"], sudo=False)

        # Check system services
        if self.required_tools["journalctl"]:
            self._run_command(["journalctl", "-xn", "50", "--no-pager"])

    def optimize_system(self):
        """Perform system optimization tasks."""
        print(f"{Fore.YELLOW}⚡ Optimizing system...{Style.RESET_ALL}")

        # Clean package cache
        if self.package_manager:
            self._run_command(self.package_manager["clean"])

        # Clear system journal
        if self.required_tools["journalctl"]:
            self._run_command(["journalctl", "--vacuum-time=7d"])

        # Clear temporary files
        self._run_command(["rm", "-rf", "/tmp/*"])

        print(f"{Fore.GREEN}✅ System optimization completed!{Style.RESET_ALL}")

    def repair_system(self):
        """Perform system repair tasks."""
        print(f"{Fore.YELLOW}🔧 Repairing system...{Style.RESET_ALL}")

        if self.package_manager:
            if "apt" in self.package_manager["update"][0]:
                self._run_command(["dpkg", "--configure", "-a"])
                self._run_command(["apt", "--fix-broken", "install"])
            elif "dnf" in self.package_manager["update"][0]:
                self._run_command(["dnf", "check"])
                self._run_command(["dnf", "repair", "system"])

        print(f"{Fore.GREEN}✅ System repair completed!{Style.RESET_ALL}")

    def backup_system(self):
        """Create system backup with progress indication."""
        if not self.required_tools["tar"]:
            print(f"{Fore.RED}❌ tar command not found{Style.RESET_ALL}")
            return

        try:
            backup_dir = "system_backups"
            os.makedirs(backup_dir, exist_ok=True)

            backup_name = os.path.join(
                backup_dir,
                f"system_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz",
            )

            print(f"{Fore.YELLOW}💾 Creating system backup...{Style.RESET_ALL}")

            # Create backup with progress using pv if available
            if shutil.which("pv"):
                cmd = f"sudo tar czf - /etc /home | pv > {backup_name}"
                os.system(cmd)  # Using os.system for pipe support
            else:
                self._run_command(["tar", "czf", backup_name, "/etc", "/home"])

            print(f"{Fore.GREEN}✅ Backup saved to: {backup_name}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Backup failed: {str(e)}{Style.RESET_ALL}")

    def restore_system(self):
        """Restore system from backup."""
        if not self.required_tools["tar"]:
            print(f"{Fore.RED}❌ tar command not found{Style.RESET_ALL}")
            return

        backup_dir = "system_backups"
        if not os.path.exists(backup_dir):
            print(f"{Fore.RED}❌ No backups found in {backup_dir}{Style.RESET_ALL}")
            return

        # List available backups
        backups = sorted(glob.glob(os.path.join(backup_dir, "system_backup_*.tar.gz")))
        if not backups:
            print(f"{Fore.RED}❌ No backup files found{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}📋 Available backups:{Style.RESET_ALL}")
        for i, backup in enumerate(backups, 1):
            backup_size = os.path.getsize(backup) / (1024 * 1024)  # Convert to MB
            backup_time = datetime.fromtimestamp(os.path.getctime(backup))
            print(
                f"{i}. {os.path.basename(backup)} ({backup_size:.1f}MB) - Created: {backup_time}"
            )

        try:
            choice = int(
                input(
                    f"\n{Fore.CYAN}Enter backup number to restore (0 to cancel): {Style.RESET_ALL}"
                )
            )
            if choice == 0:
                return
            if 1 <= choice <= len(backups):
                selected_backup = backups[choice - 1]

                print(
                    f"{Fore.RED}⚠️  Warning: This will overwrite existing system files!{Style.RESET_ALL}"
                )
                confirm = input(
                    f"{Fore.YELLOW}Are you sure you want to continue? (yes/no): {Style.RESET_ALL}"
                )

                if confirm.lower() == "yes":
                    print(f"{Fore.YELLOW}🔄 Restoring from backup...{Style.RESET_ALL}")

                    # Restore with progress using pv if available
                    if shutil.which("pv"):
                        cmd = f"sudo pv {selected_backup} | tar xz -C /"
                        os.system(cmd)
                    else:
                        self._run_command(["tar", "xzf", selected_backup, "-C", "/"])

                    print(
                        f"{Fore.GREEN}✅ System restored successfully!{Style.RESET_ALL}"
                    )
                else:
                    print(f"{Fore.YELLOW}⚪ Restore cancelled{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Invalid backup number{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Invalid input{Style.RESET_ALL}")

    def show_system_info(self):
        """Display detailed system information."""
        print(f"{Fore.YELLOW}💻 System Information:{Style.RESET_ALL}")

        info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Architecture": platform.machine(),
            "Processor": platform.processor(),
            "Hostname": platform.node(),
        }

        for key, value in info.items():
            print(f"{Fore.CYAN}{key}: {Style.RESET_ALL}{value}")

        # Show memory information
        self._run_command(["free", "-h"], sudo=False)

        # Show disk information
        self._run_command(["df", "-h"], sudo=False)

    def update_system(self):
        """Update system with proper error handling and progress indication."""
        if not self.package_manager:
            print(f"{Fore.RED}❌ No supported package manager found{Style.RESET_ALL}")
            return

        try:
            # Update package lists
            print(f"{Fore.YELLOW}🔄 Checking for updates...{Style.RESET_ALL}")
            if not self._run_command(self.package_manager["update"]):
                print(f"{Fore.RED}❌ Failed to update package lists{Style.RESET_ALL}")
                return

            # Check for upgradable packages
            print(f"{Fore.CYAN}🔍 Checking for available upgrades...{Style.RESET_ALL}")
            self._run_command(self.package_manager["check_updates"], sudo=False)

            # Confirm upgrade
            confirm = input(
                f"\n{Fore.YELLOW}Do you want to proceed with the upgrade? (yes/no): {Style.RESET_ALL}"
            )
            if confirm.lower() != "yes":
                print(f"{Fore.YELLOW}⚪ Upgrade cancelled{Style.RESET_ALL}")
                return

            # Perform upgrade
            print(f"{Fore.CYAN}📦 Installing upgrades...{Style.RESET_ALL}")
            if not self._run_command(self.package_manager["upgrade"]):
                print(f"{Fore.RED}❌ Upgrade failed{Style.RESET_ALL}")
                return

            # Clean up
            print(f"{Fore.CYAN}🧹 Cleaning up...{Style.RESET_ALL}")
            self._run_command(self.package_manager["clean"])

            print(
                f"{Fore.GREEN}✅ System update completed successfully!{Style.RESET_ALL}"
            )

        except Exception as e:
            print(f"{Fore.RED}❌ Update failed: {str(e)}{Style.RESET_ALL}")

    def upgrade_system(self):
        """Perform a full system upgrade with proper error handling."""
        print(f"{Fore.YELLOW}⬆️  Starting system upgrade...{Style.RESET_ALL}")

        if not self.package_manager:
            print(f"{Fore.RED}❌ No supported package manager found{Style.RESET_ALL}")
            return

        try:
            # Update package lists
            print(f"{Fore.CYAN}📋 Updating package lists...{Style.RESET_ALL}")
            if not self._run_command(self.package_manager["update"]):
                print(f"{Fore.RED}❌ Failed to update package lists{Style.RESET_ALL}")
                return

            # Check for upgradable packages
            print(f"{Fore.CYAN}🔍 Checking for available upgrades...{Style.RESET_ALL}")
            self._run_command(self.package_manager["check_updates"], sudo=False)

            # Confirm upgrade
            confirm = input(
                f"\n{Fore.YELLOW}Do you want to proceed with the upgrade? (yes/no): {Style.RESET_ALL}"
            )
            if confirm.lower() != "yes":
                print(f"{Fore.YELLOW}⚪ Upgrade cancelled{Style.RESET_ALL}")
                return

            # Perform upgrade
            print(f"{Fore.CYAN}📦 Installing upgrades...{Style.RESET_ALL}")
            if not self._run_command(self.package_manager["upgrade"]):
                print(f"{Fore.RED}❌ Upgrade failed{Style.RESET_ALL}")
                return

            # Clean up
            print(f"{Fore.CYAN}🧹 Cleaning up...{Style.RESET_ALL}")
            self._run_command(self.package_manager["clean"])

            print(
                f"{Fore.GREEN}✅ System upgrade completed successfully!{Style.RESET_ALL}"
            )

        except Exception as e:
            print(f"{Fore.RED}❌ Upgrade failed: {str(e)}{Style.RESET_ALL}")



    #RESTART SYSTEM
    def restart_system(self):
        """Safely restart the system with confirmation."""
        print(f"{Fore.YELLOW}🔄 System Restart{Style.RESET_ALL}")
        
        # Ask for confirmation
        confirm = input(f"{Fore.RED}Are you sure you want to restart the system? (yes/no): {Style.RESET_ALL}")
        if confirm.lower() != "yes":
            print(f"{Fore.YELLOW}⚪ Restart cancelled{Style.RESET_ALL}")
            return
        
        print(f"{Fore.YELLOW}🔄 Initiating system restart...{Style.RESET_ALL}")
        
        try:
            if self.os_type == "linux":
                self._run_command(["shutdown", "-r", "now"])
            elif self.os_type == "windows":
                self._run_command(["shutdown", "/r", "/t", "0"])
            elif self.os_type == "darwin":  # macOS
                self._run_command(["shutdown", "-r", "now"])
            else:
                print(f"{Fore.RED}❌ Unsupported operating system{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Restart failed: {str(e)}{Style.RESET_ALL}")


    # SHUTDOWN SYSTEM
    def shutdown_system(self):

        print(f"{Fore.YELLOW}⚡ System Shutdown{Style.RESET_ALL}")

        # Ask for confirmation
        confirm = input(
            f"{Fore.RED}Are you sure you want to shutdown the system? (yes/no): {Style.RESET_ALL}"
        )
        if confirm.lower() != "yes":
            print(f"{Fore.YELLOW}⚪ Shutdown cancelled{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}🔄 Initiating system shutdown...{Style.RESET_ALL}")

        try:
            if self.os_type == "linux":
                self._run_command(["shutdown", "-h", "now"])
            elif self.os_type == "windows":
                self._run_command(["shutdown", "/s", "/t", "0"])
            elif self.os_type == "darwin":  # macOS
                self._run_command(["shutdown", "-h", "now"])
            else:
                print(f"{Fore.RED}❌ Unsupported operating system{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ Shutdown failed: {str(e)}{Style.RESET_ALL}")

    # CLEAN SYSTEM
    def clean_system(self):
        """Clean system cache and temporary files."""
        print(f"{Fore.YELLOW}🧹 Cleaning system...{Style.RESET_ALL}")

        # Clean package manager cache
        if self.package_manager:
            self._run_command(self.package_manager["clean"])

        # Clean temporary files
        self._run_command(["rm", "-rf", "/tmp/*"])

        # Clean journal logs if available
        if self.required_tools["journalctl"]:
            self._run_command(["journalctl", "--vacuum-time=3d"])

        # Clean thumbnail cache
        user_home = os.path.expanduser("~")
        thumbnail_cache = os.path.join(user_home, ".cache", "thumbnails")
        if os.path.exists(thumbnail_cache):
            self._run_command(["rm", "-rf", thumbnail_cache])

        # Clean browser caches
        browser_caches = [
            ".cache/google-chrome",
            ".cache/mozilla/firefox",
            ".cache/chromium",
        ]
        for cache in browser_caches:
            cache_path = os.path.join(user_home, cache)
            if os.path.exists(cache_path):
                self._run_command(["rm", "-rf", cache_path])

        print(f"{Fore.GREEN}✅ System clean completed!{Style.RESET_ALL}")

    def security_menu(self):
        if not any([self.required_tools["ufw"], self.required_tools["netstat"]]):
            print(f"{Fore.RED}❌ Required security tools not found{Style.RESET_ALL}")
            return

        while True:
            print(
                f"""{Fore.CYAN}
            ╔═══ Security Tools ══════════════════════════╗
            ║ 1. Check Firewall Status                    ║
            ║ 2. List Open Ports                          ║
            ║ 3. Show Failed Login Attempts               ║
            ║ 4. Check System Updates                     ║
            ║ 5. Security Audit                           ║
            ║ 0. Back to Main Menu                        ║
            ╚═════════════════════════════════════════════╝
            {Style.RESET_ALL}"""
            )

            choice = input(f"{Fore.CYAN}Enter your choice (0-5): {Style.RESET_ALL}")

            if choice == "0":
                break
            elif choice == "1" and self.required_tools["ufw"]:
                self._run_command(["ufw", "status", "verbose"])
            elif choice == "2" and self.required_tools["netstat"]:
                self._run_command(["netstat", "-tuln"])
            elif choice == "3" and self.required_tools["journalctl"]:
                self._run_command(
                    ["journalctl", "_SYSTEMD_UNIT=sshd.service", "--no-pager"]
                )
            elif choice == "4" and self.package_manager:
                self._run_command(self.package_manager["check_updates"])
            elif choice == "5":
                self.security_audit()
            else:
                print(
                    f"{Fore.RED}Invalid choice or required tool not available!{Style.RESET_ALL}"
                )

    def show_logs(self):
        """Display system logs."""
        if self.required_tools["journalctl"]:
            self._run_command(["journalctl", "-xn", "50", "--no-pager"])
        else:
            print(f"{Fore.RED}❌ journalctl not found{Style.RESET_ALL}")

    def security_audit(self):
        """Perform basic security audit."""
        print(f"{Fore.YELLOW}🔒 Running security audit...{Style.RESET_ALL}")

        # Check for available security updates
        if self.package_manager:
            self._run_command(self.package_manager["check_updates"])

        # Check SSH configuration
        if os.path.exists("/etc/ssh/sshd_config"):
            self._run_command(
                ["grep", "-i", "PermitRootLogin", "/etc/ssh/sshd_config"], sudo=False
            )

        # Check listening ports
        if self.required_tools["netstat"]:
            self._run_command(["netstat", "-tuln"])

        # Check system users
        self._run_command(["cat", "/etc/passwd"], sudo=False)
