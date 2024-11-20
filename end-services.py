import os
import signal
import subprocess

# Define the ports your services are using
# User service: 3004, Movie service: 3001, Showtime service: 3003, Booking service: 3002
service_ports = [3004, 3001, 3003, 3002]  # Replace with your actual ports

def find_pid_by_port(port):
    """Find the PID of a process using the given port with lsof."""
    try:
        # Use lsof to find the process ID
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:  # Ignore the header
            pid = lines[1].split()[1]  # PID is the second column in lsof output
            return int(pid)
        print(f"No process found on port {port}.")
        return None
    except Exception as e:
        print(f"Error finding PID for port {port}: {e}")
        return None

def kill_process(pid, port):
    """Kill a process by its PID."""
    try:
        os.kill(pid, signal.SIGTERM)  # Send termination signal
        print(f" {port} : Process with PID {pid} terminated.")
    except Exception as e:
        print(f"Error terminating process with PID {pid}: {e}")

def main():
    print("Cleaning up ports...")
    for port in service_ports:
        pid = find_pid_by_port(port)
        if pid:
            kill_process(pid, port)
    print("All specified servers have been terminated.")

if __name__ == "__main__":
    main()
