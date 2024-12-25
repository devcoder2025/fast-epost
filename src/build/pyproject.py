from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Any
import tomli
import tomli_w
from pathlib import Path
import os
import hashlib
import asyncio
import subprocess

@dataclass
class BuildConfig:
    requires: List[str]
    build_backend: str
    backend_path: Optional[List[str]]
    parallel_jobs: int = 4
    cache_dir: str = ".build_cache"
    rebuild_deps: bool = False

class EnhancedPyProjectManager:
    def __init__(self, project_root: str, config: Optional[BuildConfig] = None):
        self.project_root = Path(project_root)
        self.pyproject_path = self.project_root / "pyproject.toml"
        self.config = config or BuildConfig([], "", None)
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.build_cache = BuildCache(self.config.cache_dir)
        self._config: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        if self.pyproject_path.exists():
            self._config = tomli.loads(self.pyproject_path.read_text())
        return self._config

    def save(self) -> None:
        self.pyproject_path.write_text(tomli_w.dumps(self._config))

    def get_build_system(self) -> BuildConfig:
        build_system = self._config.get("build-system", {})
        return BuildConfig(
            requires=build_system.get("requires", []),
            build_backend=build_system.get("build-backend", ""),
            backend_path=build_system.get("backend-path")
        )

    def set_build_system(self, config: BuildConfig) -> None:
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

    async def build_project(self) -> None:
        await self._resolve_dependencies()
        build_tasks = self._create_build_tasks()
        await self._execute_parallel_builds(build_tasks)

    async def _resolve_dependencies(self) -> None:
        config = self.load_config()
        for requirement in config.get("build-system", {}).get("requires", []):
            await self._process_dependency(requirement)

    def load_config(self) -> Dict:
        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"No pyproject.toml found in {self.project_root}")
        return tomli.loads(self.pyproject_path.read_text())

    async def _process_dependency(self, requirement: str) -> None:
        if requirement not in self.dependency_graph:
            self.dependency_graph[requirement] = set()
            deps = await self._get_package_dependencies(requirement)
            self.dependency_graph[requirement].update(deps)
            for dep in deps:
                await self._process_dependency(dep)

    async def _get_package_dependencies(self, package: str) -> Set[str]:
        try:
            result = subprocess.run(
                ["pip", "show", package],
                capture_output=True,
                text=True
            )
            requires = []
            for line in result.stdout.split('\n'):
                if line.startswith('Requires:'):
                    requires = line.split(':')[1].strip().split(', ')
                    requires = [r for r in requires if r]
            return set(requires)
        except subprocess.SubprocessError:
            return set()

    def _create_build_tasks(self) -> List[asyncio.Task]:
        tasks = []
        for package in self._get_build_order():
            if not self.build_cache.is_cached(package) or self.config.rebuild_deps:
                task = asyncio.create_task(self._build_package(package))
                tasks.append(task)
        return tasks

    async def _execute_parallel_builds(self, tasks: List[asyncio.Task]) -> None:
        semaphore = asyncio.Semaphore(self.config.parallel_jobs)
        async with semaphore:
            await asyncio.gather(*tasks)

    def _get_build_order(self) -> List[str]:
        visited = set()
        order = []

        def visit(package: str):
            if package in visited:
                return
            visited.add(package)
            for dep in self.dependency_graph[package]:
                visit(dep)
            order.append(package)

        for package in self.dependency_graph:
            visit(package)
        return order

    async def _build_package(self, package: str) -> None:
        if self.build_cache.is_cached(package) and not self.config.rebuild_deps:
            return

        process = await asyncio.create_subprocess_exec(
            "pip", "install", "--no-deps", package,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

        if process.returncode == 0:
            self.build_cache.cache_package(package)

class BuildCache:
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def is_cached(self, package: str) -> bool:
        cache_file = self.cache_dir / self._get_cache_key(package)
        return cache_file.exists()

    def cache_package(self, package: str) -> None:
        cache_file = self.cache_dir / self._get_cache_key(package)
        cache_file.touch()

    def _get_cache_key(self, package: str) -> str:
        return hashlib.sha256(package.encode()).hexdigest()
