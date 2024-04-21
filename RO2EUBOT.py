import os
import discord
from discord.ext import commands, tasks
import subprocess
import json

# Создаем объект намерений (Intents)
intents = discord.Intents.default()

# Включаем намерения, которые вам нужны (в данном случае мы включаем все)
intents = discord.Intents.all()

# Токен вашего бота

# Префикс для команд бота
PREFIX = '!'

# Создаем объект бота
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Функция для запроса информации о сервере игры через gamedig
def query_game_server(game, address, port):
    gamedig_path = r'C:\Users\Udano\AppData\Roaming\npm\gamedig.cmd'
    result = subprocess.run([gamedig_path, '--type', game, '--host', address, '--port', port], capture_output=True, text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        return None

# Функция для удаления ненужных символов из названия карты
def clean_map_name(map_name):
    # Удаляем префикс "TE-"
    if map_name.startswith('TE-'):
        map_name = map_name[3:]
    # Удаляем MCP, RC и цифры
    map_name = ''.join(filter(lambda x: not x.isnumeric() and x not in ['MCP', 'RC'], map_name))
    return map_name.strip()

# Функция для обновления статуса бота
@tasks.loop(minutes=1)  # Обновляем статус каждые 1 минуту
async def update_status():
    game = 'redorchestra2'  # Игра
    address = '31.186.250.228'  # IP-адрес сервера
    port = '7777'  # Порт сервера

    game_info = query_game_server(game, address, port)
    if game_info:
        map_name = game_info['map']
        map_name = clean_map_name(map_name)
        num_players = game_info['numplayers']
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{num_players} players on {map_name}'))
    else:
        await bot.change_presence(activity=discord.Game(name='Не удалось получить информацию'))

# Событие при запуске бота
@bot.event
async def on_ready():
    print(f'{bot.user.name} подключился к Discord!')
    update_status.start()

# Команда для получения информации о сервере игры
@bot.command(name='serverinfo')
async def server_info(ctx):
    game = 'redorchestra2'  # Игра
    address = '31.186.250.228'  # IP-адрес сервера
    port = '7777'  # Порт сервера

    game_info = query_game_server(game, address, port)
    if game_info:
        map_name = game_info['map']
        map_name = clean_map_name(map_name)
        num_players = game_info['numplayers']
        await ctx.send(f'На карте {map_name} сейчас играет {num_players} игроков.')
    else:
        await ctx.send('Не удалось получить информацию о сервере игры.')

# Запускаем бота
bot.run(os.environ.get("BOT_TOKEN"))
