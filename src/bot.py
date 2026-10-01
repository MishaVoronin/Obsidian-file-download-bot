from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src import services
 

router = Router()

@router.message(Command("start"))
async def start(message: Message) -> None:
    await services.start(message)

@router.message(F.text)
async def get_file(message: Message) -> None:
    await services.get_file(message)