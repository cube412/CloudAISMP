import discord
from discord import app_commands

from ai import ask_ai
from orders import OrderView, get_server_plan


class CloudCommands(app_commands.Group):

    def __init__(self):
        super().__init__(
            name="cloud",
            description="CloudAI Commands"
        )

    # =========================
    # PING
    # =========================

    @app_commands.command(
        name="ping",
        description="Kiểm tra bot"
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(
            f"🏓 Pong!\n"
            f"Latency: {round(interaction.client.latency * 1000)} ms"
        )

    # =========================
    # PLAN
    # =========================

    @app_commands.command(
        name="plan",
        description="Xem gói CloudAI của server"
    )
    async def plan(
        self,
        interaction: discord.Interaction
    ):

        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ Lệnh này chỉ dùng được trong server.",
                ephemeral=True
            )
            return

        current_plan = get_server_plan(
            interaction.guild.id
        )

        if current_plan == "40K":
            title = "🔵 GÓI VIP 40K"
            description = (
                "Server của bạn đang sử dụng **CloudAI VIP 40K**.\n\n"
                "✨ Các tính năng VIP đã được mở."
            )
            color = 0x3498DB

        elif current_plan == "20K":
            title = "🟢 GÓI BASIC 20K"
            description = (
                "Server của bạn đang sử dụng **CloudAI Basic 20K**.\n\n"
                "🤖 Các tính năng Basic đang hoạt động."
            )
            color = 0x2ECC71

        else:
            title = "📦 GÓI CLOUD AI"
            description = (
                f"Server đang sử dụng gói: **{current_plan}**"
            )
            color = 0x00BFFF

        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        embed.add_field(
            name="🏠 Server",
            value=interaction.guild.name,
            inline=False
        )

        embed.add_field(
            name="📦 Gói hiện tại",
            value=current_plan,
            inline=True
        )

        await interaction.response.send_message(
            embed=embed
        )

    # =========================
    # HELP
    # =========================

    @app_commands.command(
        name="help",
        description="Hiện hướng dẫn"
    )
    async def help(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🤖 CloudAI",
            description="Danh sách lệnh CloudAI",
            color=0x00BFFF
        )

        embed.add_field(
            name="/cloud ai",
            value="Hỏi CloudAI",
            inline=False
        )

        embed.add_field(
            name="/cloud plugin",
            value="Hỏi về Plugin Minecraft",
            inline=False
        )

        embed.add_field(
            name="/cloud tps",
            value="Xem thông tin TPS",
            inline=False
        )

        embed.add_field(
            name="/cloud helpmc",
            value="Hướng dẫn Minecraft",
            inline=False
        )

        embed.add_field(
            name="/cloud plan",
            value="Xem gói CloudAI của server",
            inline=False
        )

        embed.add_field(
            name="/cloud order",
            value="Đặt một Discord Bot riêng",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )

    # =========================
    # AI
    # =========================

    @app_commands.command(
        name="ai",
        description="Hỏi CloudAI"
    )
    @app_commands.describe(
        question="Nhập câu hỏi"
    )
    async def ai(
        self,
        interaction: discord.Interaction,
        question: str
    ):

        await interaction.response.defer()

        answer = await ask_ai(
            str(interaction.user.id),
            question
        )

        if len(answer) > 2000:
            answer = answer[:1990] + "..."

        await interaction.followup.send(
            answer
        )

    # =========================
    # PLUGIN
    # =========================

    @app_commands.command(
        name="plugin",
        description="Hỏi về Plugin Minecraft"
    )
    @app_commands.describe(
        question="Nhập câu hỏi"
    )
    async def plugin(
        self,
        interaction: discord.Interaction,
        question: str
    ):

        await interaction.response.defer()

        answer = await ask_ai(
            str(interaction.user.id),
            "Minecraft Plugin: " + question
        )

        if len(answer) > 2000:
            answer = answer[:1990] + "..."

        await interaction.followup.send(
            answer
        )

    # =========================
    # TPS
    # =========================

    @app_commands.command(
        name="tps",
        description="Giải thích TPS Minecraft"
    )
    async def tps(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="⚡ TPS Minecraft",
            description=(
                "🟢 **20 TPS** = Server rất mượt\n\n"
                "🟡 **18-19 TPS** = Bình thường\n\n"
                "🟠 **15-17 TPS** = Có dấu hiệu lag\n\n"
                "🔴 **Dưới 15 TPS** = Server lag"
            ),
            color=0x00BFFF
        )

        await interaction.response.send_message(
            embed=embed
        )

    # =========================
    # HELP MINECRAFT
    # =========================

    @app_commands.command(
        name="helpmc",
        description="Hướng dẫn Minecraft"
    )
    async def helpmc(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🎮 Minecraft Assistant",
            description="CloudAI hỗ trợ Minecraft",
            color=0x00BFFF
        )

        embed.add_field(
            name="📄 Plugin",
            value="/cloud plugin LuckPerms là gì?",
            inline=False
        )

        embed.add_field(
            name="🤖 AI",
            value="/cloud ai Paper khác Spigot như thế nào?",
            inline=False
        )

        embed.add_field(
            name="⚡ TPS",
            value="/cloud tps",
            inline=False
        )

        embed.add_field(
            name="📦 Gói",
            value="/cloud plan",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )

    # =========================
    # ĐẶT BOT
    # =========================

    @app_commands.command(
        name="order",
        description="Đặt một Discord Bot riêng"
    )
    async def order(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🛒 Đặt CloudAI",
            description=(
                "Bạn muốn sở hữu một Discord Bot riêng?\n\n"
                "🤖 **Tên bot:** Tùy chọn\n"
                "🖼️ **Avatar:** Tùy chọn\n"
                "🎯 **Chủ đề:** Tùy chọn\n"
                "😎 **Tính cách:** Tùy chọn\n"
                "⚙️ **Chức năng:** Tùy chọn\n"
                "📦 **Gói:** Chọn trong ticket\n"
                "💳 **Thanh toán:** Chọn trong ticket\n\n"
                "Nhấn **🤖 Đặt Bot** để bắt đầu."
            ),
            color=0x00BFFF
        )

        await interaction.response.send_message(
            embed=embed,
            view=OrderView()
        )
