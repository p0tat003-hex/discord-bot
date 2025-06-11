import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Load token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Create an instance of Intents
intents = discord.Intents.default()
intents.reactions = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Emoji to role mappings
emoji_role_mapping_major = {
    '💻': 'CS',
    '⚡': 'CE',
    '📚': 'Other',
}
emoji_role_mapping_interests = {
    '1️⃣': 'Artificial Intelligence and Machine Learning',
    '2️⃣': 'Cybersecurity',
    '3️⃣': 'Data science',
    '4️⃣': 'Mobile App Development',
    '5️⃣': 'Web Development',
}
emoji_role_mapping_year = {
    '1️⃣': '1st year',
    '2️⃣': '2nd year',
    '3️⃣': '3rd year',
    '4️⃣': '4th year',
    '5️⃣': '5th year',
}

user_major_reactions = {}
user_interest_reactions = {}
user_year_reactions = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    channel = bot.get_channel(payload.channel_id)
    user_message = await channel.fetch_message(payload.message_id)

    if payload.message_id == 1174405095224520795:
        if payload.emoji.name in emoji_role_mapping_major:
            new_role_name = emoji_role_mapping_major[payload.emoji.name]
            new_role = discord.utils.get(guild.roles, name=new_role_name)
            non_major_roles = [r for r in member.roles if r.name not in emoji_role_mapping_major.values()]

            if payload.user_id in user_major_reactions:
                old = user_major_reactions[payload.user_id]
                if old != new_role_name:
                    old_emoji = next(k for k, v in emoji_role_mapping_major.items() if v == old)
                    await user_message.remove_reaction(old_emoji, member)

            await member.edit(roles=non_major_roles + [new_role])
            user_major_reactions[payload.user_id] = new_role_name

    elif payload.message_id == 1175061291849760799:
        if payload.emoji.name in emoji_role_mapping_year:
            new_role_name = emoji_role_mapping_year[payload.emoji.name]
            new_role = discord.utils.get(guild.roles, name=new_role_name)
            non_year_roles = [r for r in member.roles if r.name not in emoji_role_mapping_year.values()]

            if payload.user_id in user_year_reactions:
                old = user_year_reactions[payload.user_id]
                if old != new_role_name:
                    old_emoji = next(k for k, v in emoji_role_mapping_year.items() if v == old)
                    await user_message.remove_reaction(old_emoji, member)

            await member.edit(roles=non_year_roles + [new_role])
            user_year_reactions[payload.user_id] = new_role_name

    elif payload.message_id == 1174764041428811836:
        if payload.emoji.name in emoji_role_mapping_interests:
            role_name = emoji_role_mapping_interests[payload.emoji.name]
            role = discord.utils.get(guild.roles, name=role_name)
            await member.add_roles(role)

            if payload.user_id not in user_interest_reactions:
                user_interest_reactions[payload.user_id] = set()
            user_interest_reactions[payload.user_id].add(role_name)

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if payload.message_id == 1174405095224520795:
        if payload.emoji.name in emoji_role_mapping_major:
            role = discord.utils.get(guild.roles, name=emoji_role_mapping_major[payload.emoji.name])
            await member.remove_roles(role)
            user_major_reactions.pop(payload.user_id, None)

    elif payload.message_id == 1174764041428811836:
        if payload.emoji.name in emoji_role_mapping_interests:
            role = discord.utils.get(guild.roles, name=emoji_role_mapping_interests[payload.emoji.name])
            await member.remove_roles(role)
            if payload.user_id in user_interest_reactions:
                user_interest_reactions[payload.user_id].discard(role.name)
                if not user_interest_reactions[payload.user_id]:
                    user_interest_reactions.pop(payload.user_id)

    elif payload.message_id == 1175061291849760799:
        if payload.emoji.name in emoji_role_mapping_year:
            role = discord.utils.get(guild.roles, name=emoji_role_mapping_year[payload.emoji.name])
            await member.remove_roles(role)
            user_year_reactions.pop(payload.user_id, None)

bot.run(TOKEN)
