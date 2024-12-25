
import smtplib
import aiohttp
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class NotificationConfig:
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    webhook_urls: List[str]
    sms_api_key: str
    default_from: str

class NotificationManager:
    def __init__(self, config: NotificationConfig):
        self.config = config
        self._email_queue = asyncio.Queue()
        self._sms_queue = asyncio.Queue()
        self._webhook_queue = asyncio.Queue()
        self._running = False

    async def start(self):
        self._running = True
        await asyncio.gather(
            self._process_email_queue(),
            self._process_sms_queue(),
            self._process_webhook_queue()
        )

    async def stop(self):
        self._running = False

    async def send_email(self, to: str, subject: str, body: str):
        await self._email_queue.put({
            'to': to,
            'subject': subject,
            'body': body
        })

    async def send_sms(self, phone: str, message: str):
        await self._sms_queue.put({
            'phone': phone,
            'message': message
        })

    async def send_webhook(self, data: Dict):
        await self._webhook_queue.put(data)

    async def _process_email_queue(self):
        while self._running:
            try:
                email = await self._email_queue.get()
                await self._send_email_smtp(
                    email['to'],
                    email['subject'],
                    email['body']
                )
            except Exception as e:
                print(f"Email error: {e}")
            finally:
                self._email_queue.task_done()

    async def _process_sms_queue(self):
        while self._running:
            try:
                sms = await self._sms_queue.get()
                await self._send_sms_api(
                    sms['phone'],
                    sms['message']
                )
            except Exception as e:
                print(f"SMS error: {e}")
            finally:
                self._sms_queue.task_done()

    async def _process_webhook_queue(self):
        while self._running:
            try:
                data = await self._webhook_queue.get()
                await self._send_webhook_request(data)
            except Exception as e:
                print(f"Webhook error: {e}")
            finally:
                self._webhook_queue.task_done()

    async def _send_email_smtp(self, to: str, subject: str, body: str):
        msg = MIMEMultipart()
        msg['From'] = self.config.default_from
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        async with aiosmtplib.SMTP(
            hostname=self.config.smtp_host,
            port=self.config.smtp_port
        ) as server:
            await server.login(
                self.config.smtp_user,
                self.config.smtp_password
            )
            await server.send_message(msg)

    async def _send_sms_api(self, phone: str, message: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.sms-provider.com/send',
                headers={'Authorization': f'Bearer {self.config.sms_api_key}'},
                json={'phone': phone, 'message': message}
            ) as response:
                return await response.json()

    async def _send_webhook_request(self, data: Dict):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in self.config.webhook_urls:
                task = asyncio.create_task(
                    session.post(url, json=data)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)
