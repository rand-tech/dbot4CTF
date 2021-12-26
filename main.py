import discord
from discord.ext import commands
import os

TOKEN = os.environ.get('TOKEN')
DEBUG = True

client = commands.Bot(command_prefix="$")

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.command()
async def makectf(ctx, ctf_name: str, *channels):
    guild = ctx.guild
    # create category / role
    Category = await guild.create_category(ctf_name, position=1)
    # TODO: google why `position = 1 doesn't work even if it's specified in create_category
    # changes it in line 33
    role = await guild.create_role(name = ctf_name)
    await role.edit(colour=discord.Colour.random())
    # make it private
    await Category.set_permissions(role, read_messages=True, send_messages=True, connect=True, speak=True)
    await Category.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)
    # create channels
    for channel in channels:
        await guild.create_text_channel(f"{channel}", category = Category, sync_permissions=True)
    await guild.create_voice_channel(f"{ctf_name}-vc", category = Category, sync_permissions=True)

    # moves category to top (below generals)
    await Category.edit(position=2)

    if DEBUG:
        # log
        log =f"{ctf_name=}\n{channels=}"
        print(log)
        await ctx.send(f"```python\n{log}```")


client.run(TOKEN)
