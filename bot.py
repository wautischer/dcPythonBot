import discord
import responses
from apscheduler.schedulers.asyncio \
    import AsyncIOScheduler


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await (message.author.send(response) if is_private else message.channel.send(response))

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = '' #enter your token here
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_daily_message, "cron", hour=21, minute=17)
        scheduler.start()

    @client.event
    async def on_message(message):
        if message.author == client.user and str(message.content) != '!dailymessage':
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, '!'+user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    async def send_daily_message():
        channel_id = #enter your channel id here
        channel = client.get_channel(channel_id)

        if channel:
            try:
                await channel.send("!dailymessage")
            except Exception as e:
                print(f"An error occurred while sending the daily message: {str(e)}")

    client.run(TOKEN)