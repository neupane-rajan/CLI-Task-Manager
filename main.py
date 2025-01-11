# main.py
import os
import sys
from colorama import Fore, Back, Style, init
from system_monitor import SystemMonitor
from system_tasks import SystemTasks
from network_tools import NetworkTools
from service_manager import ServiceManager
from process_manager import ProcessManager
from disk_tools import DiskTools
from user_manager import UserManager
from package_manager import PackageManager

# Initialize colorama
init()


def display_banner():
    print(
        f"""{Fore.CYAN}
    ████████╗ █████╗ ███████╗██╗  ██╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
    ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
       ██║   ███████║███████╗█████╔╝     ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
       ██║   ██╔══██║╚════██║██╔═██╗     ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
       ██║   ██║  ██║███████║██║  ██╗    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
       ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    {Style.RESET_ALL}"""
    )


def display_status_bar():
    monitor = SystemMonitor()
    cpu = monitor.get_cpu_usage()
    mem = monitor.get_memory_usage()

    print(
        f"""
    {Fore.YELLOW}╔═══ System Status ══════════════════════════════════════════════════════════════════╗
    ║ 🖥️  CPU: {cpu}% | 🧠 RAM: {mem['percent']}% | 🌡️  Temp: {monitor.get_cpu_temperature()}°C | ⏰ Uptime: {monitor.get_uptime()}
    ╚════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    )


def display_menu():
    print(
        f"""{Fore.GREEN}
    ┌───────────── 🎯 Main Menu ─────────────┐    ┌───────── 💻 System Tools ──────────┐
    │  1. System Monitor 📊                  │    │  8. Service Management 🔧          │
    │  2. Process Manager 🔄                 │    │  9. Package Management 📦          │
    │  3. Disk Tools 💾                      │    │  10. User Management 👥            │
    │  4. Network Tools 🌐                   │    │  11. System Backup 💾              │
    │  5. System Tasks ⚡                    │    │  12. System Restore 🔄             │
    │  6. Performance Monitor 📈             │    │  13. Security Tools 🔒             │
    │  7. Resource Usage 📊                  │    │  14. System Logs 📝                │
    └────────────────────────────────────────┘    └────────────────────────────────────┘
    {Fore.YELLOW}                                   
    ┌───────── ⚙️  System Actions ──────────┐   
    │  15. Update System 🔄                 │   
    │  16. Upgrade System ⬆️                │   
    │  17. Clean System 🧹                  │   
    └───────────────────────────────────────┘   
    
     {Fore.RED}
    ┌────── ⚠️  Power Options ─────┐
    │  18. Shutdown System 🔌      │ 
    │  19. Restart System 🔃       │
    │  0.  Exit ❌                 │
    └──────────────────────────────┘{Style.RESET_ALL}
     """
    )


def main():
    system_monitor = SystemMonitor()
    system_tasks = SystemTasks()
    network_tools = NetworkTools()
    service_manager = ServiceManager()
    process_manager = ProcessManager()
    disk_tools = DiskTools()
    user_manager = UserManager()
    package_manager = PackageManager()

    while True:
        os.system("clear")
        display_banner()
        display_status_bar()
        display_menu()

        try:
            choice = input(f"{Fore.CYAN}Enter your choice (0-19): {Style.RESET_ALL}")

            if choice == "0":
                print(
                    f"\n{Fore.YELLOW}👋 Thank you for using Task Manager! Goodbye!{Style.RESET_ALL}"
                )
                sys.exit(0)

            handlers = {
                "1": system_monitor.show_system_info,
                "2": process_manager.show_processes,
                "3": disk_tools.show_disk_menu,
                "4": network_tools.show_network_menu,
                "5": system_tasks.show_tasks_menu,
                "6": system_monitor.show_performance,
                "7": system_monitor.show_resource_usage,
                "8": service_manager.show_services_menu,
                "9": package_manager.show_package_menu,
                "10": user_manager.show_user_menu,
                "11": system_tasks.backup_system,
                "12": system_tasks.restore_system,
                "13": system_tasks.security_menu,
                "14": system_tasks.show_logs,
                "15": system_tasks.update_system,
                "16": system_tasks.upgrade_system,
                "17": system_tasks.clean_system,
                "18": system_tasks.shutdown_system,
                "19": system_tasks.restart_system,
            }

            if choice in handlers:
                handlers[choice]()
            else:
                print(
                    f"{Fore.RED}❌ Invalid choice. Please try again.{Style.RESET_ALL}"
                )

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Exiting Task Manager...{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
