
import pytest
from src.validation.validator import ValidatorBuilder
from src.validation.rules import ValidationError

@pytest.mark.asyncio
async def test_required_validation():
    validator = (ValidatorBuilder()
                .required("name")
                .build())
    
    errors = await validator.validate({"name": ""})
    assert len(errors) == 1
    assert errors[0].field == "name"
    assert errors[0].code == "required"

@pytest.mark.asyncio
async def test_length_validation():
    validator = (ValidatorBuilder()
                .length("password", min=8, max=20)
                .build())
    
    errors = await validator.validate({"password": "123"})
    assert len(errors) == 1
    assert errors[0].code == "min_length"

@pytest.mark.asyncio
async def test_pattern_validation():
    validator = (ValidatorBuilder()
                .pattern("email", r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
                .build())
    
    errors = await validator.validate({"email": "invalid-email"})
    assert len(errors) == 1
    assert errors[0].code == "pattern"

@pytest.mark.asyncio
async def test_range_validation():
    validator = (ValidatorBuilder()
                .range("age", min_value=18, max_value=100)
                .build())
    
    errors = await validator.validate({"age": 15})
    assert len(errors) == 1
    assert errors[0].code == "min_value"

@pytest.mark.asyncio
async def test_custom_validation():
    async def custom_validator(value, data):
        if value and value != data.get('password_confirm'):
            return ValidationError("password", "Passwords do not match", "password_mismatch")
    
    validator = (ValidatorBuilder()
                .custom("password", custom_validator)
                .build())
    
    errors = await validator.validate({
        "password": "123456",
        "password_confirm": "654321"
    })
    assert len(errors) == 1
    assert errors[0].code == "password_mismatch"

@pytest.mark.asyncio
async def test_multiple_rules():
    validator = (ValidatorBuilder()
                .required("username")
                .length("username", min=3, max=20)
                .pattern("username", r"^[a-zA-Z0-9_]+$")
                .build())
    
    errors = await validator.validate({"username": "@invalid!"})
    assert len(errors) == 1
    assert errors[0].code == "pattern"
