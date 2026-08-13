import discord
from discord.ui import Modal, TextInput


# ==========================================
# CẤU HÌNH
# ==========================================

OWNER_ID = 1514447473748475975

# Chưa dùng category riêng thì để None
TICKET_CATEGORY_ID = None


# ==========================================
# DỮ LIỆU ĐƠN HÀNG
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
            "Hãy chọn thông tin cho bot của bạn.\n\n"
            "Bạn có thể thay đổi thông tin trước khi xác nhận đơn."
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
        inline=False
    )

    embed.add_field(
        name="💳 Thanh toán",
        value=order["payment"],
        inline=False
    )

    embed.set_footer(
        text="CloudAI • Custom Discord Bot"
    )

    return embed


# ==========================================
# MODAL TÊN BOT
# ==========================================

class BotNameModal(Modal):

    def __init__(self, user_id, view):
        super().__init__(title="🤖 Đặt tên bot")

        self.user_id = user_id
        self.order_view = view

        self.name_input = TextInput(
            label="Tên bot",
            placeholder="Ví dụ: MyAI",
            max_length=32,
            required=True
        )

        self.add_item(self.name_input)

    async def on_submit(self, interaction):

        order = get_order(self.user_id)

        order["name"] = self.name_input.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=self.order_view
        )


# ==========================================
# MODAL AVATAR
# ==========================================

class AvatarModal(Modal):

    def __init__(self, user_id, view):
        super().__init__(title="🖼️ Avatar bot")

        self.user_id = user_id
        self.order_view = view

        self.avatar_input = TextInput(
            label="Link ảnh Avatar",
            placeholder="https://...",
            required=True
        )

        self.add_item(self.avatar_input)

    async def on_submit(self, interaction):

        order = get_order(self.user_id)

        order["avatar"] = self.avatar_input.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=self.order_view
        )


# ==========================================
# MODAL CHỦ ĐỀ
# ==========================================

class TopicModal(Modal):

    def __init__(self, user_id, view):
        super().__init__(title="🎯 Chủ đề bot")

        self.user_id = user_id
        self.order_view = view

        self.topic_input = TextInput(
            label="Chủ đề",
            placeholder="Minecraft, Anime, AI, Gaming...",
            max_length=100,
            required=True
        )

        self.add_item(self.topic_input)

    async def on_submit(self, interaction):

        order = get_order(self.user_id)

        order["topic"] = self.topic_input.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=self.order_view
        )


# ==========================================
# MODAL TÍNH CÁCH
# ==========================================

class PersonalityModal(Modal):

    def __init__(self, user_id, view):
        super().__init__(title="😎 Tính cách bot")

        self.user_id = user_id
        self.order_view = view

        self.personality_input = TextInput(
            label="Tính cách",
            placeholder="Vui vẻ, nghiêm túc, chill...",
            max_length=200,
            required=True
        )

        self.add_item(self.personality_input)

    async def on_submit(self, interaction):

        order = get_order(self.user_id)

        order["personality"] = self.personality_input.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=self.order_view
        )


# ==========================================
# MODAL CHỨC NĂNG
# ==========================================

class FeaturesModal(Modal):

    def __init__(self, user_id, view):
        super().__init__(title="⚙️ Chức năng bot")

        self.user_id = user_id
        self.order_view = view

        self.features_input = TextInput(
            label="Chức năng",
            placeholder="AI Chat, Welcome, Moderation...",
            style=discord.TextStyle.paragraph,
            max_length=500,
            required=True
        )

        self.add_item(self.features_input)

    async def on_submit(self, interaction):

        order = get_order(self.user_id)

        order["features"] = self.features_input.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=self.order_view
        )


# ==========================================
# CHỌN GÓI
# ==========================================

class PlanSelect(discord.ui.Select):

    def __init__(self, user_id, view):

        self.user_id = user_id
        self.order_view = view

        options = [

            discord.SelectOption(
                label="Basic",
                description="AI Chat + Memory",
                emoji="🟢",
                value="Basic - 20.000đ"
            ),

            discord.SelectOption(
                label="VIP",
                description="AI + Welcome + Moderation",
                emoji="🔵",
                value="VIP - 40.000đ"
            ),

            discord.SelectOption(
                label="Custom",
                description="Bot theo yêu cầu",
                emoji="🔥",
                value="Custom - từ 50.000đ"
            )

        ]

        super().__init__(
            placeholder="📦 Chọn gói bot",
            options=options
        )

    async def callback(self, interaction):

        order = get_order(self.user_id)

        order["plan"] = self.values[0]

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=self.order_view
        )


class PlanView(discord.ui.View):

    def __init__(self, user_id, main_view):

        super().__init__(timeout=60)

        self.add_item(
            PlanSelect(
                user_id,
                main_view
            )
        )


# ==========================================
# THANH TOÁN
# ==========================================

class PaymentView(discord.ui.View):

    def __init__(self, user_id, main_view):

        super().__init__(timeout=60)

        self.user_id = user_id
        self.main_view = main_view

    @discord.ui.button(
        label="Chuyển khoản",
        emoji="💳",
        style=discord.ButtonStyle.primary
    )
    async def bank(
        self,
        interaction,
        button
    ):

        order = get_order(self.user_id)

        order["payment"] = "Chuyển khoản"

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=self.main_view
        )

    @discord.ui.button(
        label="Chưa thanh toán",
        emoji="⏳",
        style=discord.ButtonStyle.secondary
    )
    async def not_paid(
        self,
        interaction,
        button
    ):

        order = get_order(self.user_id)

        order["payment"] = "Chưa thanh toán"

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=self.main_view
        )


# ==========================================
# XÁC NHẬN ĐƠN
# ==========================================

class ConfirmView(discord.ui.View):

    def __init__(self, user_id):
        super().__init__(timeout=60)

        self.user_id = user_id

    @discord.ui.button(
        label="Xác nhận đơn",
        emoji="✅",
        style=discord.ButtonStyle.success
    )
    async def confirm(
        self,
        interaction,
        button
    ):

        order = get_order(self.user_id)

        missing = []

        for key, label in [
            ("name", "Tên bot"),
            ("avatar", "Avatar"),
            ("topic", "Chủ đề"),
            ("personality", "Tính cách"),
            ("features", "Chức năng"),
            ("plan", "Gói")
        ]:

            if order[key] == "Chưa chọn":
                missing.append(label)

        if missing:

            await interaction.response.send_message(
                "❌ Bạn chưa chọn:\n"
                + "\n".join(
                    f"• {x}"
                    for x in missing
                ),
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "✅ Đã gửi đơn đặt bot!\n"
            "Chủ bot sẽ kiểm tra đơn của bạn.",
            ephemeral=True
        )

        channel = interaction.channel

        owner = interaction.guild.get_member(
            OWNER_ID
        )

        if owner:

            await channel.send(
                f"🔔 **Đơn hàng mới!**\n"
                f"👤 Khách: {interaction.user.mention}\n\n"
                f"```text\n"
                f"Tên: {order['name']}\n"
                f"Avatar: {order['avatar']}\n"
                f"Chủ đề: {order['topic']}\n"
                f"Tính cách: {order['personality']}\n"
                f"Chức năng: {order['features']}\n"
                f"Gói: {order['plan']}\n"
                f"Thanh toán: {order['payment']}\n"
                f"```"
            )


# ==========================================
# BẢNG ĐẶT BOT
# ==========================================

class OrderPanelView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=None)

        self.user_id = user_id

    @discord.ui.button(
        label="Đặt tên",
        emoji="🤖",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def name_button(
        self,
        interaction,
        button
    ):

        await interaction.response.send_modal(
            BotNameModal(
                self.user_id,
                self
            )
        )

    @discord.ui.button(
        label="Avatar",
        emoji="🖼️",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def avatar_button(
        self,
        interaction,
        button
    ):

        await interaction.response.send_modal(
            AvatarModal(
                self.user_id,
                self
            )
        )

    @discord.ui.button(
        label="Chủ đề",
        emoji="🎯",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def topic_button(
        self,
        interaction,
        button
    ):

        await interaction.response.send_modal(
            TopicModal(
                self.user_id,
                self
            )
        )

    @discord.ui.button(
        label="Tính cách",
        emoji="😎",
        style=discord.ButtonStyle.primary,
        row=1
    )
    async def personality_button(
        self,
        interaction,
        button
    ):

        await interaction.response.send_modal(
            PersonalityModal(
                self.user_id,
                self
            )
        )

    @discord.ui.button(
        label="Chức năng",
        emoji="⚙️",
        style=discord.ButtonStyle.primary,
        row=1
    )
    async def features_button(
        self,
        interaction,
        button
    ):

        await interaction.response.send_modal(
            FeaturesModal(
                self.user_id,
                self
            )
        )

    @discord.ui.button(
        label="Chọn gói",
        emoji="📦",
        style=discord.ButtonStyle.secondary,
        row=2
    )
    async def plan_button(
        self,
        interaction,
        button
    ):

        await interaction.response.send_message(
            "📦 Hãy chọn gói:",
            view=PlanView(
                self.user_id,
                self
            ),
            ephemeral=True
        )

    @discord.ui.button(
        label="Thanh toán",
        emoji="💳",
        style=discord.ButtonStyle.secondary,
        row=2
    )
    async def payment_button(
        self,
        interaction,
        button
    ):

        await interaction.response.send_message(
            "💳 Chọn phương thức:",
            view=PaymentView(
                self.user_id,
                self
            ),
            ephemeral=True
        )

    @discord.ui.button(
        label="Xác nhận đơn",
        emoji="✅",
        style=discord.ButtonStyle.success,
        row=3
    )
    async def confirm_button(
        self,
        interaction,
        button
    ):

        await interaction.response.send_message(
            "📋 Kiểm tra đơn hàng của bạn:",
            embed=create_order_embed(
                self.user_id
            ),
            view=ConfirmView(
                self.user_id
            ),
            ephemeral=True
        )


# ==========================================
# ĐÓNG TICKET
# ==========================================

class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Đóng Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="cloudai_close_ticket"
    )
    async def close_ticket(
        self,
        interaction,
        button
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

        super().__init__(timeout=None)

    @discord.ui.button(
        label="Đặt Bot",
        emoji="🤖",
        style=discord.ButtonStyle.primary,
        custom_id="cloudai_order"
    )
    async def order_button(
        self,
        interaction,
        button
    ):

        await interaction.response.defer(
            ephemeral=True
        )

        guild = interaction.guild

        if guild is None:

            await interaction.followup.send(
                "❌ Chỉ dùng trong server Discord.",
                ephemeral=True
            )

            return

        ticket_name = (
            f"ticket-{interaction.user.id}"
        )

        for channel in guild.text_channels:

            if channel.name == ticket_name:

                await interaction.followup.send(
                    f"❌ Bạn đã có ticket: "
                    f"{channel.mention}",
                    ephemeral=True
                )

                return

        overwrites = {

            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            interaction.user:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )
        }

        owner = guild.get_member(
            OWNER_ID
        )

        if owner:

            overwrites[owner] = (
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )
            )

        category = None

        if TICKET_CATEGORY_ID is not None:

            category = guild.get_channel(
                TICKET_CATEGORY_ID
            )

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
                "Hãy cấp **Manage Channels**.",
                ephemeral=True
            )

            return

        except Exception as e:

            print(
                f"[CloudAI] Ticket Error: {e}"
            )

            await interaction.followup.send(
                "❌ Không thể tạo ticket.\n"
                "Kiểm tra Railway log.",
                ephemeral=True
            )

            return

        # Tạo dữ liệu đơn hàng
        orders[interaction.user.id] = {
            "name": "Chưa chọn",
            "avatar": "Chưa chọn",
            "topic": "Chưa chọn",
            "personality": "Chưa chọn",
            "features": "Chưa chọn",
            "plan": "Chưa chọn",
            "payment": "Chưa chọn"
        }

        embed = create_order_embed(
            interaction.user.id
        )

        await channel.send(
            content=interaction.user.mention,
            embed=embed,
            view=OrderPanelView(
                interaction.user.id
            )
        )

        await channel.send(
            "🔒 Khi hoàn tất, chủ bot sẽ kiểm tra đơn.\n"
            "Bạn có thể đóng ticket bằng nút bên dưới.",
            view=TicketView()
        )

        await interaction.followup.send(
            f"✅ Ticket đã được tạo: "
            f"{channel.mention}",
            ephemeral=True
        )
