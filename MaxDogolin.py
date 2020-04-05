#MaxDogolin.py
import os
import random
import re

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

cumprimento_quotes = [
                    [
                    'Fala ',
                    'Opa ',
                    'Manda ',
                    'Nice ',
                    ],
                    [
                    'meu querubim!',
                    'meu elevado!',
                    'meu bacano!',
                    'meu sobrevivente!',
                    'meu consagrado!',
                     ]
                ]

coolMusic_quotes = [
                    'Essa música é insana!',
                    'Eu particularmente adoro essa música!',
                    'Também gosto muito dessa música!',
                    'Essa música me deixa todo arrepiado!',
                ]

async def dm_about_music(memb, ytQuery):
    await memb.create_dm()
    await memb.dm_channel.send(
        '{}{}\n'
        '{} Você já viu o vídeo dela?\n'
        '{}'.format(random.choice(cumprimento_quotes[0]), random.choice(cumprimento_quotes[1]), random.choice(coolMusic_quotes), ytQuery)
    )

@client.event
async def on_ready():
    print(f'{client.user.name} conectou no Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{client.user} is connected to the following guild:\n')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Olá {member.name}, Bem-vindo ao meu server de testes rs!'
    )

@client.event
async def on_member_update(bfr,aft):
    try:
        print(client.guilds)
        for guild in client.guilds:
            if aft.voice.channel in guild.voice_channels and client:
                break
        print(guild)
        listActiveMembers = []
        for voipC in guild.voice_channels:
            listActiveMembers.extend([memb.name for memb in voipC.members])
        print(f'Active list: {listActiveMembers}, guild: {guild.name}')
        for act in aft.activities:
            if (aft.name in listActiveMembers) and isinstance(act,discord.Spotify):
                ytLink='https://www.youtube.com/results?search_query='
                filter = act.title + '+' + act.artist
                filter = re.sub(r'[^a-zA-Z0-9 +]+','',filter)
                filter = re.sub(r'[ ]+','+',filter)
                ytLink += filter

                await dm_about_music(aft, ytLink)

    except IndexError:
        pass

@client.event
async def on_voice_state_update(memb,beforeVS,afterVS):
    if afterVS.channel is not None and beforeVS.channel.id == afterVS.channel.id:
        print(f'before {beforeVS} and after {afterVS}')

        for guild in client.guilds:
            if guild.name == GUILD:
                break
        if beforeVS.channel is None and afterVS.channel in guild.voice_channels:
            try:
                for act in memb.activities:
                    if isinstance(act,discord.Spotify):
                        ytLink = 'https://www.youtube.com/results?search_query='
                        filter = act.title + '+' + act.artist
                        filter = re.sub(r'[^a-zA-Z0-9 +]+', '', filter)
                        filter = re.sub(r'[ ]+', '+', filter)
                        ytLink += filter

                        await dm_about_music(memb, ytLink)
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