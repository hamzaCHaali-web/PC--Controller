import socket

def get_local_ip():
    # Get the hostname of the device
    hostname = socket.gethostname()
    # Get the local IP address using the hostname
    local_ip = socket.gethostbyname(hostname)
    return local_ip

