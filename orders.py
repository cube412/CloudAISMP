import discord


# =========================
# CẤU HÌNH
# =========================

OWNER_ID = 1514447473748475975

# Nếu chưa có Category riêng thì để None
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

        # Báo Discord rằng bot đang xử lý
        await interaction.response.defer(
            ephemeral=True
        )

        guild = interaction.guild

        if guild is None:
            await interaction.followup.send(
                "❌ Chỉ có thể đặt bot trong server Discord.",
                ephemeral=True
            )
            return

        # Tên ticket
        ticket_name = f"ticket-{interaction.user.id}"

        # Kiểm tra ticket cũ
        for channel in guild.text_channels:
            if channel.name == ticket_name:
                await interaction.followup.send(
                    f"❌ Bạn đã có ticket: {channel.mention}",
                    ephemeral=True
                )
                return

        # Quyền của ticket
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

        # Category
        category = None

        if TICKET_CATEGORY_ID is not None:
            category = guild.get_channel(
                TICKET_CATEGORY_ID
            )

        # Tạo ticket
        try:

            channel = await guild.create_text_channel(
                ticket_name,
                category=category,
                overwrites=overwrites,
                reason="CloudAI Order"
            )

        except discord.Forbidden:

            await interaction.followup.send(
                "❌ CloudAI không có quyền tạo kênh!\n"
                "Hãy cấp quyền **Manage Channels** cho bot.",
                ephemeral=True
            )
            return

        except Exception as e:

            print(
                f"[CloudAI] Lỗi tạo ticket: {e}"
            )

            await interaction.followup.send(
                "❌ Không thể tạo ticket.\n"
                "Hãy xem log Railway.",
                ephemeral=True
            )
            return

        # Embed ticket
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

        # Thông báo cho người đặt
        await interaction.followup.send(
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
