import discord
import os
import json
import requests
from discord.ext import commands
import random
import pyttsx3
from googletrans import Translator
import time 
translator = Translator()


description = "dyster bot version ambiental "

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

#Saludo del bot
@bot.command()
async def hi(ctx):
    await ctx.send('Hola, soy Dyster Memebot version Ambiental.')

#Memes
@bot.command()
async def mem(ctx):
    meme = random.choice(os.listdir("ambienmemes"))
    with open(f'ambienmemes/{meme}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

#Clima
def get_weather(city):
    link = f"https://wttr.in/{city}?format=%t+%C"
    ans = requests.get(link)
    if ans.status_code == 200:
        return ans.text.strip()
    else:
        return "not found"

#Clima TTS
def speak(city, name):
    engine = pyttsx3.init()
    engine.say(city)
    engine.runAndWait()
    engine.stop()
    engine.save_to_file(city, f"./audios/clima_{name}.mp3")


@bot.command()
async def weather(ctx, city=""):
    info = get_weather(city)
    info_voice = (f"El clima en {city} actualmente es {info}")
    await ctx.send(info_voice)
    speak(info_voice, city)
    with open("./audios/clima.mp3", "rb")as f:
        audio = discord.File(f)
    await ctx.send(file=audio)


async def useless_fact(lang):
    url = "https://uselessfacts.jsp h.pl/random.json?language=en"
    fact = requests.get(url)
    if fact.status_code == 200:
        answer = fact.json()
        answer_2 = answer.get("text", "No fact found")
        translated = await translator.translate(answer_2, src="en", dest=lang)
        return translated.text
    else:
        return "Failed to get useless fact"


@bot.command()
async def fact(ctx, lang="es"):
    await ctx.send(" Cargando dato aleatorio...")
    try:
        fact_text = await useless_fact(lang)
        await ctx.send(f"{fact_text}")
    except Exception as e:
        await ctx.send(f" Error al traducir o idioma no válido: {e}")


with open("environmental_facts.json", "r", encoding="utf-8") as f:
    facts_data = json.load(f)
    efacts = [item["fact"] for item in facts_data]

@bot.command()
async def ecofact(ctx):
    fact = random.choice(efacts)
    await ctx.send(f" **Dato ambiental:** {fact}")

with open("ecotips.json", "r", encoding="utf-8") as f:
    tips_data = json.load(f)
    etips = tips_data["eco_tips"]

@bot.command()
async def ecotip(ctx):
    tip = random.choice(etips)
    await ctx.send(f" **Tip para el cambio climatico:** {tip}")


@bot.command()
async def temp_ideal(ctx):
    ideal_temp = "La temperatura ideal del planeta sin el problema del calentamiento global rondan los 13.5°C, mientras que actualmente la temperatura promedio es de aproximadamente 15°C."
    await ctx.send(ideal_temp)

@bot.command()
async def sea_level(ctx):
    sea_level_info = "El nivel del mar ha aumentado aproximadamente 20 centímetros desde 1880, y se espera que continúe aumentando debido al derretimiento de los glaciares y la expansión térmica del agua."
    await ctx.send(sea_level_info)

@bot.command()
async def encuesta(ctx):
    question = "¿Crees que las acciones individuales pueden marcar una diferencia significativa en la lucha contra el cambio climático?"
    options = ["Sí", "No", "No estoy seguro"]
    poll_message = await ctx.send(f"**Encuesta:** {question}\n" + "\n".join(f"{i+1}. {option}" for i, option in enumerate(options)))
    for i in range(len(options)):
        await poll_message.add_reaction(f"{i+1}\N{COMBINING ENCLOSING KEYCAP}")
    time.sleep(10)
    for i in range (len(options)):
        reaction = f"{i+1}\N{COMBINING ENCLOSING KEYCAP}"
        users = await poll_message.reactions[i].users().flatten()
        count = len(users) - 1
        await ctx.send(f"Opción {options[i]}: {count} votos")
        

    await ctx.send("La encuesta ha finalizado. ¡Gracias por participar!")








bot.run("")














