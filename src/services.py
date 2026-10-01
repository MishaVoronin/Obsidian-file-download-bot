import io
import os
import re

import markdown
from aiogram.types import BufferedInputFile, Message
from dotenv import set_key
from dotenv.main import load_dotenv
from github import Github
from github.GithubException import UnknownObjectException
from weasyprint import HTML

load_dotenv()

g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPO_NAME"))


def _md_to_pdf(md_text: str) -> bytes:
    """Конвертирует Markdown в PDF байты"""
    md_text = re.sub(r"\[\[(.*?)\]\]", r"[\1](\1)", md_text)

    html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    html_full = f"""
    <html><head><style>
        body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; color: #333; }}
        code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; }}
    </style></head><body>{html_body}</body></html>"""

    return HTML(string=html_full).write_pdf()


async def start(message: Message) -> None:
    if str(os.getenv("USER_ID")) == "None" or not os.getenv("USER_ID"):
        set_key(".env", "USER_ID", str(message.from_user.id))
        os.environ["USER_ID"] = str(message.from_user.id)

    elif int(os.getenv("USER_ID")) != message.from_user.id:
        return

    await message.answer(
        f"""
        hello!
        GITHUB_URL:{os.getenv("GITHUB_URL")} 
        GITHUB_TOKEN:{os.getenv("GITHUB_TOKEN")}
        """
    )


async def get_file(message: Message) -> None:
    if str(os.getenv("USER_ID")) != str(message.from_user.id):
        return

    try:
        filename = os.getenv("GITHUB_BASE_DIR") + message.text
        content = repo.get_contents(filename)

        raw_content = content.decoded_content
        text = (
            raw_content.decode("utf-8")
            if isinstance(raw_content, bytes)
            else str(raw_content)
        )

        if not text.strip():
            await message.answer(f"Файл `{filename}` пустой.")
            return

        if filename.lower().endswith(".md"):
            await message.answer("Генерирую PDF...")
            pdf_bytes = _md_to_pdf(text)
            pdf_buffer = io.BytesIO(pdf_bytes)

            doc = BufferedInputFile(pdf_buffer.read(), filename=f"{filename}.pdf")
            await message.answer_document(document=doc, caption=f" {filename}")

        else:
            await message.answer(text[0:4096] + ("..." if len(text) > 4096 else ""))

    except UnknownObjectException:
        await message.answer(f"фаил {filename} не найден в репозитории")

