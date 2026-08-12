import discord


# =========================
# CẤU HÌNH
# =========================

OWNER_ID = 1514447473748475975

# Để None trước.
# Sau này có thể đặt ID Category chứa ticket.
TICKET_CATEGORY_ID = None


# =========================
# TICKET VIEW
# =========================

class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Đóng Ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒",
        custom_id="cloudai_close_ticket"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                "❌ Chỉ chủ bot mới có thể đóng ticket!",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "🔒 Đang đóng ticket..."
        )

        await interaction.channel.delete()


# =========================
# ORDER VIEW
# =========================

class OrderView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Đặt Bot",
        style=discord.ButtonStyle.primary,
        emoji="🤖",
        custom_id="cloudai_order"
    )
    async def order_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ Chỉ có thể đặt bot trong server Discord.",
                ephemeral=True
            )
            return

        # Kiểm tra ticket cũ
        ticket_name = f"ticket-{interaction.user.id}"

        for channel in guild.text_channels:
            if channel.name == ticket_name:
                await interaction.response.send_message(
                    f"❌ Bạn đã có ticket: {channel.mention}",
                    ephemeral=True
                )
                return

        # Quyền xem ticket
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        }

        # Cho chủ bot xem ticket
        owner = guild.get_member(OWNER_ID)

        if owner:
            overwrites[owner] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

        # Category ticket
        category = None

        if TICKET_CATEGORY_ID is not None:
            category = guild.get_channel(TICKET_CATEGORY_ID)

        # Tạo ticket
        channel = await guild.create_text_channel(
            ticket_name,
            category=category,
            overwrites=overwrites,
            reason="CloudAI Order"
        )

        # Nội dung ticket
        embed = discord.Embed(
            title="🎫 CloudAI Order",
            description=(
                "Chào bạn! 👋\n\n"
                "Hãy gửi thông tin bot bạn muốn đặt:\n\n"
                "🤖 **Tên bot:**\n"
                "🖼️ **Avatar:**\n"
                "🎯 **Chủ đề:**\n"
                "😎 **Tính cách:**\n"
                "⚙️ **Chức năng:**\n"
                "🎮 **Có Minecraft không:**\n\n"
                "Bạn có thể gửi ảnh avatar trực tiếp "
                "trong ticket."
            ),
            color=0x00BFFF
        )

        await channel.send(
            content=interaction.user.mention,
            embed=embed,
            view=TicketView()
        )

        await interaction.response.send_message(
            f"✅ Đã tạo ticket: {channel.mention}",
            ephemeral=True
        )


# =========================
# ORDER EMBED
# =========================

def create_order_embed():

    embed = discord.Embed(
        title="🛒 Đặt CloudAI",
        description=(
            "Bạn muốn sở hữu một Discord Bot riêng?\n\n"
            "Bạn có thể tự chọn:\n"
            "🤖 Tên bot\n"
            "🖼️ Avatar\n"
            "🎯 Chủ đề\n"
            "😎 Tính cách\n"
            "⚙️ Chức năng"
        ),
        color=0x00BFFF
    )

    embed.add_field(
        name="🟢 Basic — 20.000đ",
        value=(
            "• AI Chat\n"
            "• Memory\n"
            "• Discord Commands"
        ),
        inline=False
    )

    embed.add_field(
        name="🔵 VIP — 40.000đ",
        value=(
            "• AI Chat\n"
            "• Memory\n"
            "• Welcome\n"
            "• Moderation\n"
            "• Custom Personality"
        ),
        inline=False
    )

    embed.add_field(
        name="🔥 Custom — từ 50.000đ",
        value=(
            "• Chủ đề riêng\n"
            "• Chức năng riêng\n"
            "• Custom Commands"
        ),
        inline=False
    )

    embed.set_footer(
        text="📩 Nhấn nút Đặt Bot để bắt đầu"
    )

    return embed
