from prisma import Prisma


prisma = Prisma()


# connecting:
async def connect_prisma():
    if not prisma.is_connected():
        await prisma.connect()


# disconnecting:
async def disconnect_prisma():
    if prisma.is_connected():
        await prisma.disconnect()
