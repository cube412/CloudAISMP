import discord
from discord import app_commands
from config import ADMIN_ID
from memory import get_all_memory, clear_history


class AdminCommands(app_commands.Group):

    def __init__(self):
        super().__init__(
            name="admin",
            description="CloudAI Admin Panel"
        )

    def check_owner(self, interaction: discord.Interaction):
        return interaction.user.id == ADMIN_ID

    @app_commands.command(
        name="status",
        description="Xem trạng thái CloudAI"
    )
    async def status(self, interaction: discord.Interaction):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="☁️ CloudAI V6",
            color=0x00BFFF
        )

        embed.add_field(
            name="🤖 AI",
            value="Online",
            inline=True
        )

        embed.add_field(
            name="👑 Owner",
            value=str(interaction.user),
            inline=True
        )

        embed.add_field(
            name="📦 Memory",
            value=f"{len(get_all_memory())} người dùng",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="clearmemory",
        description="Xóa memory của bạn"
    )
    async def clearmemory(self, interaction: discord.Interaction):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        clear_history(str(interaction.user.id))

        await interaction.response.send_message(
            "✅ Đã xóa Memory!"
        )

    @app_commands.command(
        name="say",
        description="Bot nói thay bạn"
    )
    async def say(
        self,
        interaction: discord.Interaction,
        message: str
    ):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        await interaction.response.send_message("✅ Đã gửi!")

        await interaction.channel.send(message)
