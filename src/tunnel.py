import sshtunnel

from src.config import settings


sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


def create_tunnel() -> sshtunnel.SSHTunnelForwarder:
    ssh_config = {
        "ssh_address_or_host": (settings.ssh_hostname),
        "ssh_username": settings.ssh_username,
        "ssh_password": settings.ssh_password,
        "remote_bind_address": (settings.db_hostname, settings.db_port),
    }

    tunnel = sshtunnel.SSHTunnelForwarder(**ssh_config)

    return tunnel
