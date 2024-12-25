import pytest
from pathlib import Path
from src.build.pyproject import PyProjectManager, BuildSystemConfig

@pytest.fixture
def temp_project(tmp_path):
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir

def test_pyproject_creation(temp_project):
    manager = PyProjectManager(str(temp_project))
    config = BuildSystemConfig(
        requires=["setuptools>=42", "wheel"],
        build_backend="setuptools.build_meta"
    )
    manager.set_build_system(config)
    manager.save()
    
    assert manager.pyproject_path.exists()

def test_load_existing_config(temp_project):
    original_config = {
        "build-system": {
            "requires": ["setuptools>=42", "wheel"],
            "build-backend": "setuptools.build_meta"
        }
    }
    
    pyproject_path = temp_project / "pyproject.toml"
    pyproject_path.write_text(tomli_w.dumps(original_config))
    
    manager = PyProjectManager(str(temp_project))
    loaded_config = manager.load()
    
    assert loaded_config == original_config

def test_build_system_config():
    config = BuildSystemConfig(
        requires=["setuptools>=42"],
        build_backend="setuptools.build_meta",
        backend_path=["custom_backend"]
    )
    
    assert config.requires == ["setuptools>=42"]
    assert config.build_backend == "setuptools.build_meta"
    assert config.backend_path == ["custom_backend"]

def test_validate_dependencies():
    manager = PyProjectManager(".")
    config = BuildSystemConfig(
        requires=["definitely_not_a_real_package"],
        build_backend="setuptools.build_meta"
    )
    manager.set_build_system(config)
    
    missing = manager.validate_dependencies()
    assert "definitely_not_a_real_package" in missing
