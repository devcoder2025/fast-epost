import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, Mock
from src.build.pyproject import EnhancedPyProjectManager, BuildConfig, BuildCache

@pytest.fixture
def build_manager(tmp_path):
    config = BuildConfig(
        requires=["pytest", "requests"],
        build_backend="setuptools.build_meta",
        parallel_jobs=2,
        cache_dir=str(tmp_path / "build_cache")
    )
    return EnhancedPyProjectManager(str(tmp_path), config)

@pytest.mark.asyncio
async def test_dependency_resolution(build_manager):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(
            stdout="Requires: urllib3, certifi\n",
            returncode=0
        )
        await build_manager._process_dependency("requests")
        assert "requests" in build_manager.dependency_graph
        assert "urllib3" in build_manager.dependency_graph["requests"]

def test_build_cache():
    cache = BuildCache(".build_cache")
    package = "test-package"
    
    assert not cache.is_cached(package)
    cache.cache_package(package)
    assert cache.is_cached(package)

@pytest.mark.asyncio
async def test_parallel_builds(build_manager):
    tasks = []
    for i in range(3):
        task = asyncio.create_task(build_manager._build_package(f"package-{i}"))
        tasks.append(task)
    
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_exec.return_value = Mock(
            communicate=asyncio.coroutine(lambda: (b"", b"")),
            returncode=0
        )
        await build_manager._execute_parallel_builds(tasks)
        assert mock_exec.call_count == 3

def test_build_order(build_manager):
    build_manager.dependency_graph = {
        "A": {"B", "C"},
        "B": {"D"},
        "C": {"D"},
        "D": set()
    }
    
    order = build_manager._get_build_order()
    assert order.index("D") < order.index("B")
    assert order.index("D") < order.index("C")
    assert order.index("B") < order.index("A")
    assert order.index("C") < order.index("A")
