#bot.py
import os
import random
import re

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} conectou no Discord! (nice cachorro)')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Olá {member.name}, Bem-vindo ao meu server de testes rs!'
    )

@client.event
async def on_member_update(bfr,aft):
    await aft.create_dm()
    try:
        if isinstance(aft.activities[1],discord.Spotify):
            ytLink='https://www.youtube.com/results?search_query='
            filter = aft.activities[1].title
            filter = re.sub(r'[^a-zA-Z0-9 ]+','',filter)
            filter = re.sub(r'[ ]+','+',filter)
            ytLink += filter
            await aft.dm_channel.send(
                'Olá {}, essa música é irada!'
                ' você já viu o vídeo dela?\n'
                '( {} )'.format(aft.name,ytLink)
            )
    except IndexError:
        pass


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_message_delete(msg):
    if msg.author == client.user:
        return

    await msg.channel.send("Tô vendo essas mudanças aí, {}\n"
                           "Ei galera:\n"
                           "{}"                           
    "Só para constar, ele(a) apagou a seguinte mensagem:\n\"{}\"".format(str(msg.channel.recipients),msg.author.name,msg.content))

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)