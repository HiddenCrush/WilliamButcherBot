"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from pyrogram import filters
from pyrogram.types import Message

from wbb import app, app2, arq, MESSAGE_DUMP_CHAT
from wbb.utils.dbfunctions import update_trust_db, get_trust_db


@app.on_message(
        (filters.text | filters.caption)
        & ~filters.chat(MESSAGE_DUMP_CHAT)
        & ~filters.me
        & ~filters.private
    )
async def trust_watcher_func(_, message: Message):
    if message.command:
        return
    if not message.from_user:
        return
    user_id = message.from_user.id
    text = message.text if message.text else message.caption
    text = text.strip()
    if not text:
        return
    if len(text) < 2:
        return
    data = (await arq.nlp(text)).result
    spam = data.result.spam
    ham = data.result.ham
    await update_trust_db(user_id, [spam, ham])


async def get_spam_probability(user_id) -> float:
    data = await get_trust_db(user_id)
    if not data:
        return 0
    mean = lambda x: sum(x) / len(x)
    return mean([i['spam'] for i in data])
