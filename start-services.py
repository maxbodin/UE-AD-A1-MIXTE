import subprocess
import os
import sys
import signal

# Global list to keep track of subprocesses
processes = []

# Define the ports your services use
service_ports = [3004, 3001, 3003, 3002]

def find_and_kill_process(port):
    """Find and kill a process running on the given port."""
    try:
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:  # Ignore the header
            pid = lines[1].split()[1]
            print(f"Found process on port {port}. PID: {pid}. Terminating...")
            subprocess.run(["kill", "-9", pid])
            print(f"Process on port {port} terminated.")
    except Exception as e:
        print(f"Failed to terminate process on port {port}: {e}")

def cleanup_ports(ports):
    """Clean up all processes running on the given ports."""
    print("Cleaning up ports...")
    for port in ports:
        find_and_kill_process(port)
    print("Port cleanup completed.")

def start_service(service_path, service_dir):
    """Start a service given its path to main.py and its working directory."""
    try:
        process = subprocess.Popen(
            [sys.executable, service_path],
            cwd=service_dir  # Define the working directory
        )
        print(f"Service {service_path} started with PID {process.pid}")
        return process
    except Exception as e:
        print(f"Failed to start {service_path} in {service_dir}: {e}")
        return None

def stop_services():
    """Terminate all subprocesses."""
    print("\nStopping all services...")
    for process in processes:
        if process is not None:
            try:
                process.terminate()  # Send SIGTERM
                process.wait()       # Wait for process to terminate
                print(f"Service with PID {process.pid} stopped.")
            except Exception as e:
                print(f"Failed to stop service with PID {process.pid}: {e}")
    print("All services stopped.")

def handle_exit(signum, frame):
    """Handle exit signals (e.g., Ctrl+C)."""
    print("\nReceived exit signal. Cleaning up...")
    stop_services()
    sys.exit(0)

def validate_paths(services):
    """Validate service paths and directories."""
    for service in services:
        full_path = os.path.join(service["dir"], service["path"])
        if not os.path.exists(full_path):
            print(f"Error: Service script not found at {full_path}")
            return False
        if not os.path.isdir(service["dir"]):
            print(f"Error: Directory not found for {service['dir']}")
            return False
    return True

def main():
    # Register signal handlers for clean exit
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # Define paths to service scripts and their directories
    services = [
        {"path": "main.py", "dir": "user"},
        {"path": "main.py", "dir": "movie"},
        {"path": "main.py", "dir": "showtime"},
        {"path": "main.py", "dir": "booking"},
    ]

    # Clean up any processes using the service ports
    cleanup_ports(service_ports)

    # Validate paths before starting services
    if not validate_paths(services):
        print("Validation failed. Exiting.")
        sys.exit(1)

    # Start each service
    try:
        for service in services:
            full_path = os.path.join(service["dir"], service["path"])
            process = start_service(service["path"], service["dir"])
            if process:
                processes.append(process)

        print("All services started. Press Ctrl+C to stop them.")
        
        # Wait indefinitely
        signal.pause()
    except KeyboardInterrupt:
        handle_exit(None, None)
    except Exception as e:
        print(f"Unexpected error: {e}")
        handle_exit(None, None)

if __name__ == "__main__":
    main()
