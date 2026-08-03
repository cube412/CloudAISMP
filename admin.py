import time
import discord
from discord import app_commands

from config import ADMIN_ID, VERSION
from memory import get_all_memory, clear_history
from rcon import run


BOT_START = time.time()


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
        description="Xem trạng thái bot"
    )
    async def status(self, interaction: discord.Interaction):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="☁️ CloudAI Status",
            color=0x00BFFF
        )

        embed.add_field(
            name="🤖 AI",
            value="🟢 Online",
            inline=True
        )

        embed.add_field(
            name="👥 Memory",
            value=f"{len(get_all_memory())} người dùng",
            inline=True
        )

        embed.add_field(
            name="📦 Version",
            value=VERSION,
            inline=True
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="info",
        description="Thông tin bot"
    )
    async def info(self, interaction: discord.Interaction):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🤖 CloudAI",
            color=0x00BFFF
        )

        embed.add_field(
            name="Tên",
            value="CloudAI",
            inline=False
        )

        embed.add_field(
            name="AI",
            value="Gemini",
            inline=True
        )

        embed.add_field(
            name="Version",
            value=VERSION,
            inline=True
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="version",
        description="Xem phiên bản"
    )
    async def version(self, interaction: discord.Interaction):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"📦 CloudAI Version: **{VERSION}**"
        )

    @app_commands.command(
        name="uptime",
        description="Thời gian hoạt động"
    )
    async def uptime(self, interaction: discord.Interaction):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        seconds = int(time.time() - BOT_START)

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        await interaction.response.send_message(
            f"⏱️ Uptime: {hours}h {minutes}m {secs}s"
        )

    @app_commands.command(
        name="clearmemory",
        description="Xóa Memory"
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

        await interaction.response.send_message(
            "✅ Đã gửi!",
            ephemeral=True
        )

        await interaction.channel.send(message)
    @app_commands.command(
        name="version",
        description="Xem phiên bản"
    )
    async def version(self, interaction: discord.Interaction):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"📦 CloudAI Version: **{VERSION}**"
        )

    @app_commands.command(
        name="uptime",
        description="Thời gian hoạt động"
    )
    async def uptime(self, interaction: discord.Interaction):

        if not self.check_owner(interaction):
            await interaction.response.send_message(
                "❌ Bạn không có quyền!",
                ephemeral=True
            )
            return

        seconds = int(time.time() - BOT_START)

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        await interaction.response.send_message(
            f"⏱️ Uptime: {hours}h {minutes}m {secs}s"
        )

    @app_commands.command(
        name="clearmemory",
        description="Xóa Memory của bạn"
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

        await interaction.response.send_message(
            "✅ Đã gửi!",
            ephemeral=True
        )

        await interaction.channel.send(message)
