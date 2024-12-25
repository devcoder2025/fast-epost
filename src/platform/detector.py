import os
import sys
import platform
import subprocess
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

@dataclass
class PlatformInfo:
    system: str
    architecture: str
    version: str
    machine: str
    python_version: str
    cpu_count: int
    memory_gb: float
    is_64bit: bool
    container_info: Optional[str] = None

class PlatformDetector:
    def __init__(self):
        self._platform_info = None
        self._container_types = {
            '/.dockerenv': 'Docker',
            '/run/.containerenv': 'Podman',
            '/run/containerd': 'Containerd'
        }

    def detect(self) -> PlatformInfo:
        if self._platform_info is None:
            self._platform_info = PlatformInfo(
                system=self._detect_system(),
                architecture=self._detect_architecture(),
                version=self._detect_version(),
                machine=platform.machine(),
                python_version=sys.version.split()[0],
                cpu_count=self._get_cpu_count(),
                memory_gb=self._get_memory_gb(),
                is_64bit=sys.maxsize > 2**32,
                container_info=self._detect_container()
            )
        return self._platform_info

    def _detect_system(self) -> str:
        system = platform.system().lower()
        if system == 'darwin':
            return 'macos'
        if system == 'linux':
            return self._detect_linux_distro()
        return system

    def _detect_linux_distro(self) -> str:
        try:
            with open('/etc/os-release') as f:
                info = dict(line.strip().split('=', 1) for line in f if '=' in line)
                return info.get('ID', 'linux').strip('"')
        except FileNotFoundError:
            return 'linux'

    def _detect_architecture(self) -> str:
        arch = platform.machine().lower()
        arch_map = {
            'x86_64': 'amd64',
            'amd64': 'amd64',
            'i386': 'x86',
            'i686': 'x86',
            'aarch64': 'arm64',
            'armv7l': 'arm'
        }
        return arch_map.get(arch, arch)

    def _detect_version(self) -> str:
        if platform.system() == 'Darwin':
            return platform.mac_ver()[0]
        elif platform.system() == 'Windows':
            return platform.win32_ver()[0]
        return platform.release()

    def _get_cpu_count(self) -> int:
        try:
            return os.cpu_count() or 1
        except Exception:
            return 1

    def _get_memory_gb(self) -> float:
        try:
            import psutil
            return psutil.virtual_memory().total / (1024 ** 3)
        except ImportError:
            return 0.0

    def _detect_container(self) -> Optional[str]:
        for path, container_type in self._container_types.items():
            if os.path.exists(path):
                return container_type
        return None
