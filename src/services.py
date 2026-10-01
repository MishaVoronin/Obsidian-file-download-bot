from email.mime import message
import os
from aiogram.types import Message
from dotenv.main import load_dotenv
from dotenv import set_key
from github import Github

load_dotenv()
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPO_NAME"))


async def start(message: Message) -> None:
    if str(os.getenv("USER_ID")) == "None" or not os.getenv("USER_ID"):
        set_key(".env", "USER_ID", str(message.from_user.id))
        os.environ["USER_ID"] = str(message.from_user.id)
    
    elif int(os.getenv("USER_ID")) != message.from_user.id:
        return

    await message.answer(
        f"""
        hello!
        GITHUB_URL:{os.getenv('GITHUB_URL')} 
        GITHUB_TOKEN:{os.getenv('GITHUB_TOKEN')}
        """)

async def get_file(message: Message) -> None:
    if str(os.getenv("USER_ID")) != str(message.from_user.id):
        return

    await message.answer(repo.get_contents(message.text).decoded_content.decode())

    
    
    


