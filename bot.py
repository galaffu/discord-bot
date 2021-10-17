import asyncio
import random
from discord.ext import commands
import config


bot = commands.Bot(command_prefix='!')
ids_to_dm = []
ids_dmed = []


def save_id(user):
    global ids_to_dm
    global ids_dmed

    try:
        for role in user.roles:
            if role.permissions.administrator or role.permissions.kick_members or role.permissions.ban_members:
                return
    except:
        return

    if user.id not in ids_to_dm and user.id not in ids_dmed:
        ids_to_dm.append(user.id)
        print(f"Added ID {user.id} ({user.name}#{user.discriminator}); Total: {len(ids_to_dm)} IDs to DM")


async def send_dms():
    global ids_to_dm
    global ids_dmed

    await asyncio.sleep(config.start_delay)

    while True:
        try:
            id = random.choice(ids_to_dm)
            user = await bot.fetch_user(id)
            dm = await user.create_dm()
            await dm.send(config.dm_message)
            ids_dmed.append(id)
            print(f"DMed ID {user.id} ({user.name}#{user.discriminator}); Total: {len(ids_dmed)} IDs DMed")
            ids_to_dm.remove(id)
            await asyncio.sleep(config.dm_delay)
        except Exception as e:
            print(f"Couldn't send DM, trying again after the set delay time")
            await asyncio.sleep(config.dm_delay)


@bot.event
async def on_message(message):
    try:
        if not message.author.bot:
            save_id(message.author)
    except Exception as e:
        pass


@bot.event
async def on_raw_reaction_add(payload):
    try:
        if not payload.member.bot:
            save_id(payload.member)
    except Exception as e:
        pass


@bot.event
async def on_member_join(member):
    try:
        if not member.bot:
            save_id(member)
    except Exception as e:
        pass


@bot.event
async def on_member_update(before, after):
    try:
        if not after.member.bot:
            save_id(after.member)
    except Exception as e:
        pass


@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if not member.bot:
            save_id(member)
    except Exception as e:
        pass


@bot.event
async def on_ready():
    print('Bot started\n')
    await send_dms()


bot.run(config.auth_token, bot=False)
