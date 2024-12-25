from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import tomli
import tomli_w
from pathlib import Path

@dataclass
class BuildSystemConfig:
    requires: List[str]
    build_backend: str
    backend_path: Optional[List[str]] = None
    
class PyProjectManager:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.pyproject_path = self.project_root / "pyproject.toml"
        self._config: Dict[str, Any] = {}
        
    def load(self) -> Dict[str, Any]:
        if self.pyproject_path.exists():
            self._config = tomli.loads(self.pyproject_path.read_text())
        return self._config
        
    def save(self) -> None:
        self.pyproject_path.write_text(tomli_w.dumps(self._config))
        
    def get_build_system(self) -> BuildSystemConfig:
        build_system = self._config.get("build-system", {})
        return BuildSystemConfig(
            requires=build_system.get("requires", []),
            build_backend=build_system.get("build-backend", ""),
            backend_path=build_system.get("backend-path")
        )
        
    def set_build_system(self, config: BuildSystemConfig) -> None:
        self._config["build-system"] = {
            "requires": config.requires,
            "build-backend": config.build_backend
        }
        if config.backend_path:
            self._config["build-system"]["backend-path"] = config.backend_path
            
    def validate_dependencies(self) -> List[str]:
        missing = []
        for req in self.get_build_system().requires:
            try:
                __import__(req.split()[0])
            except ImportError:
                missing.append(req)
        return missing
