
import pytest
from unittest.mock import Mock, patch
from src.notifications.sender import NotificationManager, NotificationConfig
from src.notifications.templates import NotificationTemplates

@pytest.fixture
def notification_config():
    return NotificationConfig(
        smtp_host="smtp.test.com",
        smtp_port=587,
        smtp_user="test",
        smtp_password="test",
        webhook_urls=["http://webhook1.test", "http://webhook2.test"],
        sms_api_key="test_key",
        default_from="test@example.com"
    )

@pytest.fixture
def notification_manager(notification_config):
    return NotificationManager(notification_config)

@pytest.mark.asyncio
async def test_email_sending(notification_manager):
    with patch('aiosmtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.__aenter__.return_value = Mock()
        await notification_manager.send_email(
            "test@example.com",
            "Test Subject",
            "Test Body"
        )
        assert notification_manager._email_queue.qsize() == 1

@pytest.mark.asyncio
async def test_sms_sending(notification_manager):
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value = Mock()
        await notification_manager.send_sms(
            "+1234567890",
            "Test Message"
        )
        assert notification_manager._sms_queue.qsize() == 1

@pytest.mark.asyncio
async def test_webhook_sending(notification_manager):
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value = Mock()
        await notification_manager.send_webhook({"test": "data"})
        assert notification_manager._webhook_queue.qsize() == 1

def test_template_rendering():
    templates = NotificationTemplates()
    context = {
        "project_name": "Test Project",
        "version": "1.0.0",
        "build_time": 10,
        "artifacts": ["file1.txt", "file2.txt"]
    }
    
    rendered = templates.render("BUILD_SUCCESS", context)
    assert "Test Project" in rendered
    assert "1.0.0" in rendered
