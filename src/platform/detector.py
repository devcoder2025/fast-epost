import os
import sys
import platform
import socket
import psutil
import docker
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class NetworkInfo:
    interfaces: Dict[str, List[str]]
    hostname: str
    open_ports: List[int]
    docker_networks: Optional[List[str]] = None

@dataclass
class ResourceLimits:
    cpu_count: int
    cpu_quota: Optional[int]
    memory_limit: int
    swap_limit: Optional[int]
    disk_quota: Optional[int]

class EnhancedPlatformDetector:
    def __init__(self):
        self.platform_info = self._detect_platform()
        self.container_info = self._detect_container()
        self.resource_limits = self._detect_resource_limits()
        self.network_info = self._detect_network()

    def _detect_platform(self) -> Dict:
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': sys.version,
            'architecture': platform.architecture(),
            'node': platform.node()
        }

    def _detect_container(self) -> Dict:
        container_info = {
            'is_container': False,
            'type': None,
            'orchestrator': None,
            'container_id': None
        }

        # Docker detection
        if os.path.exists('/.dockerenv'):
            container_info['is_container'] = True
            container_info['type'] = 'docker'
            try:
                client = docker.from_env()
                container = client.containers.get(socket.gethostname())
                container_info['container_id'] = container.id
            except Exception:
                pass

        # Kubernetes detection
        if os.path.exists('/var/run/secrets/kubernetes.io'):
            container_info['orchestrator'] = 'kubernetes'
            try:
                with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace') as f:
                    container_info['namespace'] = f.read().strip()
            except Exception:
                pass

        return container_info

    def _detect_resource_limits(self) -> ResourceLimits:
        cpu_count = os.cpu_count() or 1
        memory_limit = psutil.virtual_memory().total

        # CGroup v2 detection
        cgroup_path = '/sys/fs/cgroup'
        if os.path.exists(f"{cgroup_path}/cpu.max"):
            try:
                with open(f"{cgroup_path}/cpu.max") as f:
                    quota = f.read().strip().split()[0]
                    cpu_quota = int(quota) if quota != 'max' else None
            except Exception:
                cpu_quota = None
        else:
            cpu_quota = None

        # Memory limits from cgroups
        try:
            with open('/sys/fs/cgroup/memory.max') as f:
                mem_limit = int(f.read().strip())
                if mem_limit < memory_limit:
                    memory_limit = mem_limit
        except Exception:
            pass

        return ResourceLimits(
            cpu_count=cpu_count,
            cpu_quota=cpu_quota,
            memory_limit=memory_limit,
            swap_limit=self._get_swap_limit(),
            disk_quota=self._get_disk_quota()
        )

    def _detect_network(self) -> NetworkInfo:
        interfaces = {}
        for iface, addrs in psutil.net_if_addrs().items():
            interfaces[iface] = [addr.address for addr in addrs]

        # Scan common ports
        open_ports = []
        for port in [80, 443, 8080]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                open_ports.append(port)
            sock.close()

        # Docker network detection
        docker_networks = None
        if self.container_info['type'] == 'docker':
            try:
                client = docker.from_env()
                container = client.containers.get(socket.gethostname())
                docker_networks = list(container.attrs['NetworkSettings']['Networks'].keys())
            except Exception:
                pass

        return NetworkInfo(
            interfaces=interfaces,
            hostname=socket.gethostname(),
            open_ports=open_ports,
            docker_networks=docker_networks
        )

    def _get_swap_limit(self) -> Optional[int]:
        try:
            with open('/sys/fs/cgroup/memory.swap.max') as f:
                return int(f.read().strip())
        except Exception:
            return None

    def _get_disk_quota(self) -> Optional[int]:
        try:
            with open('/sys/fs/cgroup/io.max') as f:
                return int(f.read().strip().split()[1])
        except Exception:
            return None

    def get_full_info(self) -> Dict:
        return {
            'platform': self.platform_info,
            'container': self.container_info,
            'resources': self.resource_limits.__dict__,
            'network': self.network_info.__dict__
        }
