import discord
from discord.ext import commands, tasks


# Define intents
intents = discord.Intents.default()
intents.guilds = True  # Ensure we have guild intents to manage channels
intents.messages = True
intents.message_content = True  # Ensure you enable message content intent


# Initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)


previous_total_listed = 100  # Initial placeholder value, adjust as needed
previous_holders = 50


async def fetch_nft_data():
    global previous_total_listed, previous_holders
    # Placeholder for your data fetching logic
    # Return a dictionary with 'total_listed' and 'holders'

    return {
        "total_listed": previous_total_listed+1,  # Example data
        "holders": previous_holders+1,  # Example data
    }


@tasks.loop(minutes=1)
async def update_nft_data():
    global previous_total_listed, previous_holders
    for guild in bot.guilds:
        category = discord.utils.get(guild.categories, name="Kyzzen NFT Data")
        if category:
            nft_data = await fetch_nft_data()

            # Assuming 'Total Listed' and 'Holders' channels exist
            # Update channel names with the latest data
            # Fetch the new data
            new_total_listed = nft_data['total_listed']
            new_holders = nft_data['holders']

            # Find channels by their previous names
            total_listed_channel = discord.utils.get(
                category.text_channels, name=f"total-listed-{previous_total_listed}")
            holders_channel = discord.utils.get(
                category.text_channels, name=f"holders-{previous_holders}")

            # Update channels if they exist
            if total_listed_channel:
                await total_listed_channel.edit(name=f"total-listed-{new_total_listed}")
                previous_total_listed = new_total_listed  # Update the stored previous value

            if holders_channel:
                await holders_channel.edit(name=f"holders-{new_holders}")
                previous_holders = new_holders  # Update the stored previous value

            # Make channels read-only for @everyone role
            # Note: This sets the permissions when you initially create the channels.
            # If the channels already exist, you need to adjust their permissions separately.


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    if not update_nft_data.is_running():
        update_nft_data.start()


@bot.command(name='hi')
async def hi(ctx):
    await ctx.send('Hi there!')


@bot.command(name='setup_nft_data')
@commands.has_permissions(manage_channels=True)
async def setup_nft_data(ctx):
    guild = ctx.guild

    existing_category = discord.utils.get(
        guild.categories, name="Kyzzen NFT Data")
    if existing_category:
        await ctx.send("The 'Kyzzen NFT Data' category already exists!")
        return

    category = await guild.create_category("Kyzzen NFT Data")

    # Define read-only permissions for @everyone
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False)
    }

    # Create channels with these overwrites
    await guild.create_text_channel(f"total-listed-{previous_total_listed}", category=category, overwrites=overwrites)
    await guild.create_text_channel(f"holders-{previous_holders}", category=category, overwrites=overwrites)

    await ctx.send("NFT data tracking setup complete!")


@update_nft_data.before_loop
async def before_update_nft_data():
    await bot.wait_until_ready()  # Wait until the bot logs in


# Replace 'YOUR_BOT_TOKEN' with your bot's actual token
bot.run('MTIxODQ5NjM0MDk1NTM2NTM4Ng.GOjJs9.SI9tYB5BrCXbTw-oQYLUl2iSCqwX7Q5XJS5cK4')
