import discord
from discord.ui import Modal, TextInput

# ==========================================
# CẤU HÌNH
# ==========================================

OWNER_ID = 1514447473748475975

# Nếu không dùng category riêng thì để None
TICKET_CATEGORY_ID = None


# ==========================================
# LƯU ĐƠN HÀNG
# ==========================================

orders = {}


def get_order(user_id):

    if user_id not in orders:

        orders[user_id] = {
            "name": "Chưa chọn",
            "avatar": "Chưa chọn",
            "topic": "Chưa chọn",
            "personality": "Chưa chọn",
            "features": "Chưa chọn",
            "plan": "Chưa chọn",
            "payment": "Chưa chọn"
        }

    return orders[user_id]


# ==========================================
# EMBED ĐƠN HÀNG
# ==========================================

def create_order_embed(user_id):

    order = get_order(user_id)

    embed = discord.Embed(
        title="🤖 ĐẶT BOT CLOUD AI",
        description=(
            "Hãy chọn thông tin cho bot của bạn.\n"
            "Bạn có thể thay đổi trước khi xác nhận."
        ),
        color=0x00BFFF
    )

    embed.add_field(
        name="🤖 Tên bot",
        value=order["name"],
        inline=False
    )

    embed.add_field(
        name="🖼️ Avatar",
        value=order["avatar"],
        inline=False
    )

    embed.add_field(
        name="🎯 Chủ đề",
        value=order["topic"],
        inline=False
    )

    embed.add_field(
        name="😎 Tính cách",
        value=order["personality"],
        inline=False
    )

    embed.add_field(
        name="⚙️ Chức năng",
        value=order["features"],
        inline=False
    )

    embed.add_field(
        name="📦 Gói",
        value=order["plan"],
        inline=True
    )

    embed.add_field(
        name="💳 Thanh toán",
        value=order["payment"],
        inline=True
    )

    return embed


# ==========================================
# MODAL TÊN BOT
# ==========================================

class NameModal(Modal):

    def __init__(self, user_id):

        super().__init__(
            title="🤖 Đặt tên bot"
        )

        self.user_id = user_id

        self.name = TextInput(
            label="Tên bot",
            placeholder="Ví dụ: MyAI",
            max_length=32,
            required=True
        )

        self.add_item(self.name)

    async def on_submit(self, interaction):

        orders[self.user_id]["name"] = self.name.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL AVATAR
# ==========================================

class AvatarModal(Modal):

    def __init__(self, user_id):

        super().__init__(
            title="🖼️ Avatar bot"
        )

        self.user_id = user_id

        self.avatar = TextInput(
            label="Link ảnh Avatar",
            placeholder="https://...",
            required=True
        )

        self.add_item(self.avatar)

    async def on_submit(self, interaction):

        orders[self.user_id]["avatar"] = self.avatar.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL CHỦ ĐỀ
# ==========================================

class TopicModal(Modal):

    def __init__(self, user_id):

        super().__init__(
            title="🎯 Chủ đề bot"
        )

        self.user_id = user_id

        self.topic = TextInput(
            label="Chủ đề",
            placeholder="Minecraft, Anime, Gaming...",
            max_length=100,
            required=True
        )

        self.add_item(self.topic)

    async def on_submit(self, interaction):

        orders[self.user_id]["topic"] = self.topic.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL TÍNH CÁCH
# ==========================================

class PersonalityModal(Modal):

    def __init__(self, user_id):

        super().__init__(
            title="😎 Tính cách bot"
        )

        self.user_id = user_id

        self.personality = TextInput(
            label="Tính cách",
            placeholder="Vui vẻ, chill, nghiêm túc...",
            max_length=200,
            required=True
        )

        self.add_item(self.personality)

    async def on_submit(self, interaction):

        orders[self.user_id]["personality"] = self.personality.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL CHỨC NĂNG
# ==========================================

class FeaturesModal(Modal):

    def __init__(self, user_id):

        super().__init__(
            title="⚙️ Chức năng bot"
        )

        self.user_id = user_id

        self.features = TextInput(
            label="Chức năng",
            placeholder="AI Chat, Welcome, Moderation...",
            style=discord.TextStyle.paragraph,
            max_length=500,
            required=True
        )

        self.add_item(self.features)

    async def on_submit(self, interaction):

        orders[self.user_id]["features"] = self.features.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# CHỌN GÓI
# ==========================================

class PlanSelect(discord.ui.Select):

    def __init__(self, user_id):

        self.user_id = user_id

        options = [

            discord.SelectOption(
                label="Basic",
                description="AI Chat + Memory - 20.000đ",
                emoji="🟢",
                value="Basic - 20.000đ"
            ),

            discord.SelectOption(
                label="VIP",
                description="AI + Welcome + Moderation - 40.000đ",
                emoji="🔵",
                value="VIP - 40.000đ"
            ),

            discord.SelectOption(
                label="Custom",
                description="Bot theo yêu cầu - từ 50.000đ",
                emoji="🔥",
                value="Custom - từ 50.000đ"
            )
        ]

        super().__init__(
            placeholder="📦 Chọn gói bot",
            options=options
        )

    async def callback(self, interaction):

        orders[self.user_id]["plan"] = self.values[0]

        await interaction.response.edit_message(
            content=None,
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PlanView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(
            timeout=60
        )

        self.add_item(
            PlanSelect(user_id)
        )


# ==========================================
# THANH TOÁN
# ==========================================

class PaymentSelect(discord.ui.Select):

    def __init__(self, user_id):

        self.user_id = user_id

        options = [

            discord.SelectOption(
                label="Chuyển khoản",
                description="Thanh toán bằng chuyển khoản",
                emoji="💳",
                value="Chuyển khoản"
            ),

            discord.SelectOption(
                label="Chưa thanh toán",
                description="Thanh toán sau",
                emoji="⏳",
                value="Chưa thanh toán"
            )
        ]

        super().__init__(
            placeholder="💳 Chọn phương thức",
            options=options
        )

    async def callback(self, interaction):

        orders[self.user_id]["payment"] = self.values[0]

        await interaction.response.edit_message(
            content=None,
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PaymentView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(
            timeout=60
        )

        self.add_item(
            PaymentSelect(user_id)
        )


# ==========================================
# NÚT XÁC NHẬN ĐƠN
# ==========================================

class ConfirmButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Xác nhận đơn",
            emoji="✅",
            style=discord.ButtonStyle.success,
            row=3
        )

    async def callback(self, interaction):

        order = get_order(self.user_id)

        missing = []

        check = {
            "name": "Tên bot",
            "avatar": "Avatar",
            "topic": "Chủ đề",
            "personality": "Tính cách",
            "features": "Chức năng",
            "plan": "Gói"
        }

        for key, label in check.items():

            if order[key] == "Chưa chọn":

                missing.append(label)

        if missing:

            await interaction.response.send_message(
                "❌ Bạn chưa chọn đủ:\n\n"
                + "\n".join(
                    f"• {x}"
                    for x in missing
                ),
                ephemeral=True
            )

            return

        # Thông báo khách
        await interaction.response.send_message(
            "✅ **Đơn hàng đã được gửi!**\n"
            "⏳ Vui lòng chờ chủ bot kiểm tra.",
            ephemeral=True
        )

        # ==========================================
        # EMBED ĐƠN HÀNG
        # ==========================================

        embed = discord.Embed(
            title="🔔 ĐƠN BOT MỚI",
            description="Có khách vừa gửi một đơn đặt bot.",
            color=0x00BFFF
        )

        embed.add_field(
            name="👤 Khách hàng",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="🤖 Tên bot",
            value=order["name"],
            inline=True
        )

        embed.add_field(
            name="🖼️ Avatar",
            value=order["avatar"],
            inline=False
        )

        embed.add_field(
            name="🎯 Chủ đề",
            value=order["topic"],
            inline=False
        )

        embed.add_field(
            name="😎 Tính cách",
            value=order["personality"],
            inline=False
        )

        embed.add_field(
            name="⚙️ Chức năng",
            value=order["features"],
            inline=False
        )

        embed.add_field(
            name="📦 Gói",
            value=order["plan"],
            inline=True
        )

        embed.add_field(
            name="💳 Thanh toán",
            value=order["payment"],
            inline=True
        )

        embed.add_field(
            name="📌 Trạng thái",
            value="🟡 CHỜ XỬ LÝ",
            inline=False
        )

        embed.set_footer(
            text="CloudAI Order System"
        )

        # ==========================================
        # GỬI VÀO TICKET
        # ==========================================

        try:

            await interaction.channel.send(
                embed=embed
            )

        except discord.Forbidden:

            print(
                "[CloudAI] Không có quyền gửi tin nhắn."
            )

            return

        # ==========================================
        # GỬI CHO OWNER
        # ==========================================

        owner = interaction.guild.get_member(
            OWNER_ID
        )

        if owner:

            try:

                await owner.send(
                    embed=embed
                )

            except discord.Forbidden:

                print(
                    "[CloudAI] Không thể gửi DM cho OWNER."
                )


# ==========================================
# BẢNG ĐẶT BOT
# ==========================================

class OrderPanel(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(
            timeout=None
        )

        self.user_id = user_id

        self.add_item(
            NameButton(user_id)
        )

        self.add_item(
            AvatarButton(user_id)
        )

        self.add_item(
            TopicButton(user_id)
        )

        self.add_item(
            PersonalityButton(user_id)
        )

        self.add_item(
            FeaturesButton(user_id)
        )

        self.add_item(
            PlanButton(user_id)
        )

        self.add_item(
            PaymentButton(user_id)
        )

        self.add_item(
            ConfirmButton(user_id)
        )


# ==========================================
# NÚT ĐẶT TÊN
# ==========================================

class NameButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Đặt tên",
            emoji="🤖",
            style=discord.ButtonStyle.primary,
            row=0
        )

    async def callback(self, interaction):

        await interaction.response.send_modal(
            NameModal(self.user_id)
        )


# ==========================================
# NÚT AVATAR
# ==========================================

class AvatarButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Avatar",
            emoji="🖼️",
            style=discord.ButtonStyle.primary,
            row=0
        )

    async def callback(self, interaction):

        await interaction.response.send_modal(
            AvatarModal(self.user_id)
        )


# ==========================================
# NÚT CHỦ ĐỀ
# ==========================================

class TopicButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Chủ đề",
            emoji="🎯",
            style=discord.ButtonStyle.primary,
            row=0
        )

    async def callback(self, interaction):

        await interaction.response.send_modal(
            TopicModal(self.user_id)
        )


# ==========================================
# NÚT TÍNH CÁCH
# ==========================================

class PersonalityButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Tính cách",
            emoji="😎",
            style=discord.ButtonStyle.primary,
            row=1
        )

    async def callback(self, interaction):

        await interaction.response.send_modal(
            PersonalityModal(self.user_id)
        )


# ==========================================
# NÚT CHỨC NĂNG
# ==========================================

class FeaturesButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Chức năng",
            emoji="⚙️",
            style=discord.ButtonStyle.primary,
            row=1
        )

    async def callback(self, interaction):

        await interaction.response.send_modal(
            FeaturesModal(self.user_id)
        )


# ==========================================
# NÚT CHỌN GÓI
# ==========================================

class PlanButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Chọn gói",
            emoji="📦",
            style=discord.ButtonStyle.secondary,
            row=2
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "📦 **Chọn gói bot:**",
            view=PlanView(self.user_id),
            ephemeral=True
        )


# ==========================================
# NÚT THANH TOÁN
# ==========================================

class PaymentButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Thanh toán",
            emoji="💳",
            style=discord.ButtonStyle.secondary,
            row=2
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "💳 **Chọn phương thức thanh toán:**",
            view=PaymentView(self.user_id),
            ephemeral=True
        )


# ==========================================
# ĐÓNG TICKET
# ==========================================

class TicketView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=None
        )

    @discord.ui.button(
        label="Đóng Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
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


# ==========================================
# NÚT ĐẶT BOT
# ==========================================

class OrderView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=None
        )

    @discord.ui.button(
        label="Đặt Bot",
        emoji="🤖",
        style=discord.ButtonStyle.primary,
        custom_id="cloudai_order"
    )
    async def order_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

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

        # ==========================================
        # TÊN TICKET
        # ==========================================

        ticket_name = (
            f"ticket-{interaction.user.id}"
        )

        # ==========================================
        # KIỂM TRA TICKET CŨ
        # ==========================================

        for channel in guild.text_channels:

            if channel.name == ticket_name:

                await interaction.followup.send(
                    f"❌ Bạn đã có ticket: {channel.mention}",
                    ephemeral=True
                )

                return

        # ==========================================
        # QUYỀN TICKET
        # ==========================================

        overwrites = {

            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            interaction.user:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    embed_links=True
                )
        }

        # ==========================================
        # QUYỀN CHO BOT
        # ==========================================

        bot_member = guild.me

        if bot_member:

            overwrites[bot_member] = (
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    embed_links=True,
                    manage_channels=True
                )
            )

        # ==========================================
        # QUYỀN OWNER
        # ==========================================

        owner = guild.get_member(
            OWNER_ID
        )

        if owner:

            overwrites[owner] = (
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    embed_links=True
                )
            )

        # ==========================================
        # CATEGORY
        # ==========================================

        category = None

        if TICKET_CATEGORY_ID is not None:

            category = guild.get_channel(
                TICKET_CATEGORY_ID
            )

        # ==========================================
        # TẠO TICKET
        # ==========================================

        try:

            channel = await guild.create_text_channel(
                ticket_name,
                category=category,
                overwrites=overwrites,
                reason="CloudAI Order"
            )

        except discord.Forbidden:

            await interaction.followup.send(
                "❌ CloudAI không có quyền tạo kênh!\n\n"
                "Hãy cấp cho bot quyền:\n"
                "• Xem kênh\n"
                "• Gửi tin nhắn\n"
                "• Quản lý kênh\n"
                "• Đọc lịch sử tin nhắn\n"
                "• Nhúng liên kết",
                ephemeral=True
            )

            return

        except Exception as e:

            print(
                f"[CloudAI] Ticket Error: {e}"
            )

            await interaction.followup.send(
                "❌ Không thể tạo ticket.\n"
                "Kiểm tra log của bot.",
                ephemeral=True
            )

            return

        # ==========================================
        # TẠO ĐƠN
        # ==========================================

        orders[interaction.user.id] = {

            "name": "Chưa chọn",
            "avatar": "Chưa chọn",
            "topic": "Chưa chọn",
            "personality": "Chưa chọn",
            "features": "Chưa chọn",
            "plan": "Chưa chọn",
            "payment": "Chưa chọn"
        }

        # ==========================================
        # TẠO EMBED
        # ==========================================

        embed = create_order_embed(
            interaction.user.id
        )

        # ==========================================
        # GỬI BẢNG VÀO TICKET
        # ==========================================

        try:

            await channel.send(
                content=(
                    f"👋 Xin chào "
                    f"{interaction.user.mention}!\n\n"
                    "🤖 **Hãy cấu hình bot của bạn bên dưới:**"
                ),
                embed=embed,
                view=OrderPanel(
                    interaction.user.id
                )
            )

            await channel.send(
                "🔒 **Quản lý Ticket**",
                view=TicketView()
            )

        except discord.Forbidden as e:

            print(
                f"[CloudAI] Send Panel Error: {e}"
            )

            await interaction.followup.send(
                "❌ Ticket đã tạo nhưng CloudAI "
                "không thể gửi bảng.\n"
                "Kiểm tra quyền bot trong ticket.",
                ephemeral=True
            )

            return

        except Exception as e:

            print(
                f"[CloudAI] Send Panel Error: {e}"
            )

            await interaction.followup.send(
                f"❌ Không thể gửi bảng đặt bot.\n"
                f"Lỗi: `{e}`",
                ephemeral=True
            )

            return

        # ==========================================
        # THÔNG BÁO
        # ==========================================

        await interaction.followup.send(
            f"✅ Ticket đã được tạo: {channel.mention}",
            ephemeral=True
        )
