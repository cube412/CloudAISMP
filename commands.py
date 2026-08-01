import discord
from discord import app_commands

class CloudCommands(app_commands.Group):
    def __init__(self):
        super().__init__(name="cloud", description="Lệnh của CloudAI")

    @app_commands.command(name="ping", description="Kiểm tra độ trễ bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"🏓 Pong!\nĐộ trễ: **{round(interaction.client.latency * 1000)}ms**"
        )

    @app_commands.command(name="help", description="Xem hướng dẫn")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 CloudAI Help",
            description="Các lệnh hiện có",
            color=0x00BFFF
        )

        embed.add_field(name="/cloud ping", value="Kiểm tra bot", inline=False)
        embed.add_field(name="/cloud help", value="Hiện trợ giúp", inline=False)

        await interaction.response.send_message(embed=embed)
