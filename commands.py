import discord
from discord import app_commands

from ai import ask_ai
from plans import get_all_plans
from orders import OrderView, create_order_embed


class CloudCommands(app_commands.Group):

    def __init__(self):
        super().__init__(
            name="cloud",
            description="CloudAI Commands"
        )

    @app_commands.command(
        name="ping",
        description="Kiểm tra bot"
    )
    async def ping(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            f"🏓 Pong!\nLatency: {round(interaction.client.latency * 1000)} ms"
        )

    @app_commands.command(
        name="help",
        description="Hiện hướng dẫn"
    )
    async def help(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🤖 CloudAI",
            color=0x00BFFF
        )

        embed.add_field(
            name="/cloud ai",
            value="Hỏi AI",
            inline=False
        )

        embed.add_field(
            name="/cloud plugin",
            value="Hỏi về Plugin Minecraft",
            inline=False
        )

        embed.add_field(
            name="/cloud tps",
            value="Giải thích TPS",
            inline=False
        )

        embed.add_field(
            name="/cloud helpmc",
            value="Hướng dẫn Minecraft",
            inline=False
        )

        embed.add_field(
            name="/cloud plans",
            value="Xem bảng giá CloudAI",
            inline=False
        )

        embed.add_field(
            name="/cloud order",
            value="Đặt một bot riêng",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="plans",
        description="Xem bảng giá CloudAI"
    )
    async def plans(self, interaction: discord.Interaction):

        plans = get_all_plans()

        embed = discord.Embed(
            title="☁️ CloudAI — Bảng giá",
            description="Nhận làm Discord Bot AI theo yêu cầu",
            color=0x00BFFF
        )

        for plan_id, plan in plans.items():

            features = "\n".join(
                f"• {feature}"
                for feature in plan["features"]
            )

            embed.add_field(
                name=f"{plan['name']} — {plan['price']:,}đ",
                value=features,
                inline=False
            )

        embed.set_footer(
            text="📩 Dùng /cloud order để đặt bot"
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="order",
        description="Đặt một bot CloudAI riêng"
    )
    async def order(self, interaction: discord.Interaction):

        embed = create_order_embed()

        await interaction.response.send_message(
            embed=embed,
            view=OrderView()
        )

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

        await interaction.followup.send(answer)

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

        await interaction.followup.send(answer)

    @app_commands.command(
        name="tps",
        description="Giải thích TPS"
    )
    async def tps(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="⚡ TPS Minecraft",
            description="""
🟢 20 TPS = Server rất mượt

🟡 18-19 TPS = Bình thường

🟠 15-17 TPS = Có dấu hiệu lag

🔴 Dưới 15 TPS = Server đang lag nặng
""",
            color=0x00BFFF
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="helpmc",
        description="Hướng dẫn Minecraft"
    )
    async def helpmc(self, interaction: discord.Interaction):

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

        await interaction.response.send_message(
            embed=embed
        )        embed.add_field(
            name="/cloud ai",
            value="Hỏi AI",
            inline=False
        )

        embed.add_field(
            name="/cloud plugin",
            value="Hỏi về plugin Minecraft",
            inline=False
        )

        embed.add_field(
            name="/cloud tps",
            value="Giải thích TPS",
            inline=False
        )

        embed.add_field(
            name="/cloud helpmc",
            value="Hướng dẫn Minecraft",
            inline=False
        )

        embed.add_field(
            name="/cloud plans",
            value="Xem các gói CloudAI",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="plans",
        description="Xem bảng giá CloudAI"
    )
    async def plans(self, interaction: discord.Interaction):

        plans = get_all_plans()

        embed = discord.Embed(
            title="☁️ CloudAI — Bảng giá",
            description="Nhận làm bot Discord AI theo yêu cầu",
            color=0x00BFFF
        )

        for plan_id, plan in plans.items():

            features = "\n".join(
                f"• {feature}"
                for feature in plan["features"]
            )

            embed.add_field(
                name=f"{plan['name']} — {plan['price']:,}đ",
                value=features,
                inline=False
            )

        embed.set_footer(
            text="📩 Liên hệ để đặt bot"
        )

        await interaction.response.send_message(
            embed=embed
        )

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

        await interaction.followup.send(answer)

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

        await interaction.followup.send(answer)

    @app_commands.command(
        name="tps",
        description="Giải thích TPS"
    )
    async def tps(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="⚡ TPS Minecraft",
            description="""
🟢 20 TPS = Server rất mượt

🟡 18-19 TPS = Bình thường

🟠 15-17 TPS = Có dấu hiệu lag

🔴 Dưới 15 TPS = Server đang lag nặng
""",
            color=0x00BFFF
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="helpmc",
        description="Hướng dẫn Minecraft"
    )
    async def helpmc(self, interaction: discord.Interaction):

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

        await interaction.response.send_message(
            embed=embed
        )
