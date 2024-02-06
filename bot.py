from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from links import get_all_links, write_links
from settings import CONFIG


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 1:
        await update.message.reply_text(
            f"Please provide a link to add to the list of links.\nExample:\n/link https://www.nettruyenus.com/truyen-tranh/beat-and-motion-90092"
        )
        return
    link = context.args[0]
    write_links([link], is_append=True)
    links = get_all_links()
    await update.message.reply_text(
        f"Added {link} to the list of links. There are {len(links)} links in the list of links"
    )


app = ApplicationBuilder().token(CONFIG.TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("hello", link))

app.run_polling()
