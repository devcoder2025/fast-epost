import aio_pika

async def init_queue(settings):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    return channel
