```python
import discord
from discord.ui import Modal, TextInput
from discord import app_commands

# ==========================================
# CẤU HÌNH
# ==========================================

OWNER_ID = 1514447473748475975
TICKET_CATEGORY_ID = None

# ==========================================
# LƯU ĐƠN
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
            "payment": "Chưa chọn",
            "card_type": "Chưa chọn",
            "card_amount": "Chưa chọn",
            "card_code": "Chưa nhập",
            "card_serial": "Chưa nhập"
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

    embed.add_field(
        name="🎫 Loại thẻ",
        value=order["card_type"],
        inline=True
    )

    embed.add_field(
        name="💰 Mệnh giá",
        value=order["card_amount"],
        inline=True
    )

    embed.add_field(
        name="🔢 Mã thẻ",
        value=order["card_code"],
        inline=False
    )

    embed.add_field(
        name="🔢 Seri",
        value=order["card_serial"],
        inline=False
    )

    return embed


# ==========================================
# MODAL TÊN
# ==========================================

class NameModal(Modal):

    def __init__(self, user_id):

        super().__init__(title="🤖 Đặt tên bot")

        self.user_id = user_id

        self.name = TextInput(
            label="Tên bot",
            placeholder="Ví dụ: CloudAI",
            max_length=32
        )

        self.add_item(self.name)

    async def on_submit(self, interaction):

        get_order(self.user_id)["name"] = self.name.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL AVATAR
# ==========================================

class AvatarModal(Modal):

    def __init__(self, user_id):

        super().__init__(title="🖼️ Avatar bot")

        self.user_id = user_id

        self.avatar = TextInput(
            label="Link ảnh Avatar",
            placeholder="https://...",
            max_length=500
        )

        self.add_item(self.avatar)

    async def on_submit(self, interaction):

        get_order(self.user_id)["avatar"] = self.avatar.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL CHỦ ĐỀ
# ==========================================

class TopicModal(Modal):

    def __init__(self, user_id):

        super().__init__(title="🎯 Chủ đề bot")

        self.user_id = user_id

        self.topic = TextInput(
            label="Chủ đề",
            placeholder="Minecraft, Anime, Gaming...",
            max_length=100
        )

        self.add_item(self.topic)

    async def on_submit(self, interaction):

        get_order(self.user_id)["topic"] = self.topic.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL TÍNH CÁCH
# ==========================================

class PersonalityModal(Modal):

    def __init__(self, user_id):

        super().__init__(title="😎 Tính cách bot")

        self.user_id = user_id

        self.personality = TextInput(
            label="Tính cách",
            placeholder="Vui vẻ, chill, nghiêm túc...",
            max_length=200
        )

        self.add_item(self.personality)

    async def on_submit(self, interaction):

        get_order(self.user_id)["personality"] = self.personality.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL CHỨC NĂNG
# ==========================================

class FeaturesModal(Modal):

    def __init__(self, user_id):

        super().__init__(title="⚙️ Chức năng bot")

        self.user_id = user_id

        self.features = TextInput(
            label="Chức năng",
            placeholder="AI Chat, Welcome, Moderation...",
            style=discord.TextStyle.paragraph,
            max_length=500
        )

        self.add_item(self.features)

    async def on_submit(self, interaction):

        get_order(self.user_id)["features"] = self.features.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# ==========================================
# MODAL THẺ
# ==========================================

class CardInfoModal(Modal):

    def __init__(self, user_id):

        super().__init__(title="🎫 Thông tin thẻ")

        self.user_id = user_id

        self.code = TextInput(
            label="Mã thẻ",
            placeholder="Nhập mã thẻ",
            max_length=50
        )

        self.serial = TextInput(
            label="Seri",
            placeholder="Nhập seri thẻ",
            max_length=50
        )

        self.add_item(self.code)
        self.add_item(self.serial)

    async def on_submit(self, interaction):

        order = get_order(self.user_id)

        order["card_code"] = self.code.value
        order["card_serial"] = self.serial.value

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

        get_order(self.user_id)["plan"] = self.values[0]

        await interaction.response.edit_message(
            content=None,
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PlanView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=60)

        self.add_item(PlanSelect(user_id))


# ==========================================
# THANH TOÁN
# ==========================================

class PaymentSelect(discord.ui.Select):

    def __init__(self, user_id):

        self.user_id = user_id

        options = [
            discord.SelectOption(
                label="Thẻ điện thoại",
                description="Thanh toán bằng thẻ điện thoại",
                emoji="🎫",
                value="Thẻ điện thoại"
            ),
            discord.SelectOption(
                label="Chuyển khoản",
                description="Thanh toán bằng chuyển khoản",
                emoji="🏦",
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
            placeholder="💳 Chọn phương thức thanh toán",
            options=options
        )

    async def callback(self, interaction):

        order = get_order(self.user_id)

        order["payment"] = self.values[0]

        await interaction.response.edit_message(
            content=None,
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PaymentView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=60)

        self.add_item(PaymentSelect(user_id))


# ==========================================
# LOẠI THẺ
# ==========================================

class CardTypeSelect(discord.ui.Select):

    def __init__(self, user_id):

        self.user_id = user_id

        options = [
            discord.SelectOption(
                label="Viettel",
                emoji="🟢",
                value="Viettel"
            ),
            discord.SelectOption(
                label="Vinaphone",
                emoji="🔵",
                value="Vinaphone"
            ),
            discord.SelectOption(
                label="Mobifone",
                emoji="🟠",
                value="Mobifone"
            ),
            discord.SelectOption(
                label="Vietnamobile",
                emoji="🟡",
                value="Vietnamobile"
            )
        ]

        super().__init__(
            placeholder="🎫 Chọn loại thẻ",
            options=options
        )

    async def callback(self, interaction):

        get_order(self.user_id)["card_type"] = self.values[0]

        await interaction.response.edit_message(
            content="🎫 Đã chọn loại thẻ!",
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class CardTypeView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=60)

        self.add_item(CardTypeSelect(user_id))


# ==========================================
# MỆNH GIÁ
# ==========================================

class AmountSelect(discord.ui.Select):

    def __init__(self, user_id):

        self.user_id = user_id

        options = [
            discord.SelectOption(
                label="10.000đ",
                value="10.000đ"
            ),
            discord.SelectOption(
                label="20.000đ",
                value="20.000đ"
            ),
            discord.SelectOption(
                label="30.000đ",
                value="30.000đ"
            ),
            discord.SelectOption(
                label="50.000đ",
                value="50.000đ"
            ),
            discord.SelectOption(
                label="100.000đ",
                value="100.000đ"
            )
        ]

        super().__init__(
            placeholder="💰 Chọn mệnh giá thẻ",
            options=options
        )

    async def callback(self, interaction):

        get_order(self.user_id)["card_amount"] = self.values[0]

        await interaction.response.edit_message(
            content="💰 Đã chọn mệnh giá!",
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class AmountView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=60)

        self.add_item(AmountSelect(user_id))


# ==========================================
# NÚT XÁC NHẬN
# ==========================================

class ConfirmButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Xác nhận đơn",
            emoji="✅",
            style=discord.ButtonStyle.success,
            row=4
        )

    async def callback(self, interaction):

        order = get_order(self.user_id)

        required = {
            "name": "Tên bot",
            "avatar": "Avatar",
            "topic": "Chủ đề",
            "personality": "Tính cách",
            "features": "Chức năng",
            "plan": "Gói"
        }

        missing = []

        for key, label in required.items():

            if order[key] == "Chưa chọn":
                missing.append(label)

        if order["payment"] == "Thẻ điện thoại":

            if order["card_type"] == "Chưa chọn":
                missing.append("Loại thẻ")

            if order["card_amount"] == "Chưa chọn":
                missing.append("Mệnh giá thẻ")

            if order["card_code"] == "Chưa nhập":
                missing.append("Mã thẻ")

            if order["card_serial"] == "Chưa nhập":
                missing.append("Seri")

        if missing:

            await interaction.response.send_message(
                "❌ **Bạn chưa nhập đủ:**\n\n"
                + "\n".join(
                    f"• {item}"
                    for item in missing
                ),
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "✅ **Đã gửi đơn!**\n"
            "⏳ Vui lòng chờ chủ bot duyệt đơn.",
            ephemeral=True
        )

        embed = discord.Embed(
            title="🔔 ĐƠN BOT MỚI",
            description="Có khách vừa gửi đơn đặt bot.",
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
            name="🎯 Chủ đề",
            value=order["topic"],
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

        if order["payment"] == "Thẻ điện thoại":

            embed.add_field(
                name="🎫 Loại thẻ",
                value=order["card_type"],
                inline=True
            )

            embed.add_field(
                name="💰 Mệnh giá",
                value=order["card_amount"],
                inline=True
            )

            embed.add_field(
                name="🔢 Mã thẻ",
                value=order["card_code"],
                inline=False
            )

            embed.add_field(
                name="🔢 Seri",
                value=order["card_serial"],
                inline=False
            )

        embed.add_field(
            name="📌 Trạng thái",
            value="🟡 CHỜ DUYỆT",
            inline=False
        )

        embed.set_footer(
            text="CloudAI Order System"
        )

        # Gửi vào ticket
        try:

            await interaction.channel.send(
                embed=embed,
                view=AdminOrderView(self.user_id)
            )

        except discord.Forbidden:

            print(
                "[CloudAI] Không có quyền gửi đơn vào ticket."
            )

        # Gửi riêng cho OWNER
        owner = interaction.guild.get_member(OWNER_ID)

        if owner:

            try:

                await owner.send(
                    content="🔔 **CÓ ĐƠN BOT MỚI CẦN DUYỆT**",
                    embed=embed,
                    view=AdminOrderView(self.user_id)
                )

            except discord.Forbidden:

                print(
                    "[CloudAI] Không thể gửi DM cho OWNER."
                )


# ==========================================
# DUYỆT / TỪ CHỐI
# ==========================================

class AdminOrderView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=None)

        self.user_id = user_id

    @discord.ui.button(
        label="Duyệt đơn",
        emoji="✅",
        style=discord.ButtonStyle.success
    )
    async def approve(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != OWNER_ID:

            await interaction.response.send_message(
                "❌ Bạn không có quyền duyệt đơn.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "✅ Đã duyệt đơn.",
            ephemeral=True
        )

        user = interaction.guild.get_member(
            self.user_id
        ) if interaction.guild else None

        if user:

            try:

                await user.send(
                    "🎉 **Đơn hàng của bạn đã được duyệt!**\n"
                    "Chủ bot sẽ tiến hành tạo bot cho bạn."
                )

            except discord.Forbidden:
                pass

        button.disabled = True

        await interaction.message.edit(
            view=self
        )

    @discord.ui.button(
        label="Từ chối",
        emoji="❌",
        style=discord.ButtonStyle.danger
    )
    async def reject(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != OWNER_ID:

            await interaction.response.send_message(
                "❌ Bạn không có quyền từ chối đơn.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "❌ Đã từ chối đơn.",
            ephemeral=True
        )

        user = interaction.guild.get_member(
            self.user_id
        ) if interaction.guild else None

        if user:

            try:

                await user.send(
                    "❌ **Đơn hàng của bạn đã bị từ chối.**\n"
                    "Nếu cần, hãy liên hệ chủ bot."
                )

            except discord.Forbidden:
                pass

        button.disabled = True

        await interaction.message.edit(
            view=self
        )


# ==========================================
# BẢNG ĐẶT BOT
# ==========================================

class OrderPanel(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=None)

        self.user_id = user_id

        self.add_item(NameButton(user_id))
        self.add_item(AvatarButton(user_id))
        self.add_item(TopicButton(user_id))
        self.add_item(PersonalityButton(user_id))
        self.add_item(FeaturesButton(user_id))
        self.add_item(PlanButton(user_id))
        self.add_item(PaymentButton(user_id))
        self.add_item(CardTypeButton(user_id))
        self.add_item(AmountButton(user_id))
        self.add_item(CardInfoButton(user_id))
        self.add_item(ConfirmButton(user_id))


# ==========================================
# CÁC NÚT
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
            "💳 **Chọn phương thức:**",
            view=PaymentView(self.user_id),
            ephemeral=True
        )


class CardTypeButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Loại thẻ",
            emoji="🎫",
            style=discord.ButtonStyle.secondary,
            row=3
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "🎫 **Chọn loại thẻ:**",
            view=CardTypeView(self.user_id),
            ephemeral=True
        )


class AmountButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Mệnh giá",
            emoji="💰",
            style=discord.ButtonStyle.secondary,
            row=3
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "💰 **Chọn mệnh giá:**",
            view=AmountView(self.user_id),
            ephemeral=True
        )


class CardInfoButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Mã + Seri",
            emoji="🔢",
            style=discord.ButtonStyle.secondary,
            row=3
        )

    async def callback(self, interaction):

        await interaction.response.send_modal(
            CardInfoModal(self.user_id)
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

        super().__init__(timeout=None)

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

        ticket_name = f"ticket-{interaction.user.id}"

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
        # QUYỀN
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
                    read_message_history=True
                )
        }

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

        owner = guild.get_member(OWNER_ID)

        if owner:

            overwrites[owner] = (
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    embed_links=True
                )
            )

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
                "❌ CloudAI không có quyền tạo ticket!\n\n"
                "Cần quyền:\n"
                "• Xem kênh\n"
                "• Gửi tin nhắn\n"
                "• Quản lý kênh\n"
                "• Đọc lịch sử tin nhắn\n"
                "• Nhúng liên kết",
                ephemeral=True
            )

            return

        except Exception as e:

            print(f"[CloudAI] Ticket Error: {e}")

            await interaction.followup.send(
                "❌ Không thể tạo ticket.",
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
            "payment": "Chưa chọn",
            "card_type": "Chưa chọn",
            "card_amount": "Chưa chọn",
            "card_code": "Chưa nhập",
            "card_serial": "Chưa nhập"
        }

        embed = create_order_embed(
            interaction.user.id
        )

        # ==========================================
        # GỬI BẢNG
        # ==========================================

        try:

            await channel.send(
                content=(
                    f"👋 Xin chào {interaction.user.mention}!\n\n"
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

        except discord.Forbidden:

            print(
                "[CloudAI] Không có quyền gửi tin nhắn."
            )

            await interaction.followup.send(
                "❌ Ticket đã tạo nhưng bot không thể gửi tin nhắn.",
                ephemeral=True
            )

            return

        except Exception as e:

            print(
                f"[CloudAI] Send Panel Error: {e}"
            )

            await interaction.followup.send(
                "❌ Không thể gửi bảng đặt bot.",
                ephemeral=True
            )

            return

        await interaction.followup.send(
            f"✅ Ticket đã được tạo: {channel.mention}",
            ephemeral=True
        )
```
