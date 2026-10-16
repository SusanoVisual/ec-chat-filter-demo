"""
EC Chat Filter Demo — throwaway bot
====================================
Not the production bot. Exists only to demonstrate, for Discord's privileged-
intent review, that the self-promo/link filter in the real bot.py works:
same blocked-phrase list, same delete + notice behavior, reading message
content via the Message Content Intent. Runs against a brand-new,
low-user-count Discord application so the intent can be granted without
review, in a throwaway test server with no staff roles — so unlike the real
bot there's no owner/staff exemption here, nothing to carve out.
"""

import os
import discord

TOKEN = os.environ["DISCORD_TOKEN"]

# Same list as CHAT_BLOCKED_PATTERNS in the real bot.py.
BLOCKED_PATTERNS = (
    "looking for client", "looking for clients", "need a client", "need clients",
    "find a client", "find clients", "dm me if interested", "dm if interested",
    "contact me for", "hire me", "available for hire", "commission based",
    "commission-based", "come dm", "dm to order", "slide into my dm",
    "dm for commissions", "taking commissions", "open for commissions",
    "http://", "https://", "discord.gg/", "www.",
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Demo bot logged in as {client.user} ({client.user.id})", flush=True)


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content_lower = message.content.lower()
    if not any(pattern in content_lower for pattern in BLOCKED_PATTERNS):
        return

    try:
        await message.delete()
        print(f"Deleted blocked message from {message.author}: {message.content!r}", flush=True)
    except discord.HTTPException as e:
        print(f"Failed to delete message: {e}", flush=True)
        return

    try:
        await message.channel.send(
            f"{message.author.mention} that got removed — this channel is for conversation, "
            "not client-hunting/self-promo or links."
        )
    except discord.HTTPException:
        pass


client.run(TOKEN)
