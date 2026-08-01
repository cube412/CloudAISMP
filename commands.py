import discord
from discord import app_commands
from ai import ask_ai

class CloudCommands(app_commands.Group):
    def __init__(self):
        super().__init__(name="cloud", description="CloudAI Commands")

    @app_commands.command(name="ping", description="Kiểm tra bot")
    async def ping(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            f"🏓 Pong!\nLatency: {round(interaction.client.latency*1000)}ms"
        )

    @app_commands.command(name="help", description="Hướng dẫn")
    async def help(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🤖 CloudAI Help",
            description="Các lệnh hiện có",
            color=0x00BFFF
        )

        embed.add_field(
            name="/cloud ai",
            value="Hỏi AI",
            inline=False
        )

        embed.add_field(
            name="/cloud ping",
            value="Kiểm tra bot",
            inline=False
        )

        embed.add_field(
            name="/cloud help",
            value="Hiện hướng dẫn",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ai", description="Hỏi CloudAI")
    @app_commands.describe(question="Nhập câu hỏi")
    async def ai(self, interaction: discord.Interaction, question: str):

        await interaction.response.defer()

        answer = await ask_ai(question)

        if len(answer) > 2000:
            answer = answer[:1990] + "..."

        await interaction.followup.send(answer)
