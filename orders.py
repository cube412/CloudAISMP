import discord
from discord.ui import Modal, TextInput

OWNER_ID = 1514447473748475975
TICKET_CATEGORY_ID = None

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
            "amount": "Chưa chọn",
            "card_type": "Chưa chọn",
            "serial": "Chưa nhập",
            "code": "Chưa nhập"
        }

    return orders[user_id]


def create_order_embed(user_id):
    order = get_order(user_id)

    embed = discord.Embed(
        title="🤖 ĐẶT BOT CLOUD AI",
        description="Hãy chọn thông tin bot của bạn bên dưới.",
        color=0x00BFFF
    )

    embed.add_field(name="🤖 Tên bot", value=order["name"], inline=False)
    embed.add_field(name="🖼️ Avatar", value=order["avatar"], inline=False)
    embed.add_field(name="🎯 Chủ đề", value=order["topic"], inline=False)
    embed.add_field(name="😎 Tính cách", value=order["personality"], inline=False)
    embed.add_field(name="⚙️ Chức năng", value=order["features"], inline=False)
    embed.add_field(name="📦 Gói", value=order["plan"], inline=True)
    embed.add_field(name="💳 Thanh toán", value=order["payment"], inline=True)
    embed.add_field(name="💰 Mệnh giá", value=order["amount"], inline=True)
    embed.add_field(name="🎫 Loại thẻ", value=order["card_type"], inline=True)

    return embed


class NameModal(Modal):
    def __init__(self, user_id):
        super().__init__(title="🤖 Đặt tên bot")
        self.user_id = user_id

        self.name = TextInput(
            label="Tên bot",
            placeholder="Ví dụ: MyAI",
            max_length=32
        )

        self.add_item(self.name)

    async def on_submit(self, interaction):
        orders[self.user_id]["name"] = self.name.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class AvatarModal(Modal):
    def __init__(self, user_id):
        super().__init__(title="🖼️ Avatar bot")
        self.user_id = user_id

        self.avatar = TextInput(
            label="Link Avatar",
            placeholder="https://..."
        )

        self.add_item(self.avatar)

    async def on_submit(self, interaction):
        orders[self.user_id]["avatar"] = self.avatar.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class TopicModal(Modal):
    def __init__(self, user_id):
        super().__init__(title="🎯 Chủ đề bot")
        self.user_id = user_id

        self.topic = TextInput(
            label="Chủ đề",
            placeholder="Minecraft, Gaming, Anime..."
        )

        self.add_item(self.topic)

    async def on_submit(self, interaction):
        orders[self.user_id]["topic"] = self.topic.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PersonalityModal(Modal):
    def __init__(self, user_id):
        super().__init__(title="😎 Tính cách bot")
        self.user_id = user_id

        self.personality = TextInput(
            label="Tính cách",
            placeholder="Vui vẻ, chill, nghiêm túc..."
        )

        self.add_item(self.personality)

    async def on_submit(self, interaction):
        orders[self.user_id]["personality"] = self.personality.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


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
        orders[self.user_id]["features"] = self.features.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PaymentModal(Modal):
    def __init__(self, user_id):
        super().__init__(title="💳 Thông tin thanh toán")
        self.user_id = user_id

        self.amount = TextInput(
            label="Mệnh giá",
            placeholder="Ví dụ: 40.000đ",
            max_length=20
        )

        self.card_type = TextInput(
            label="Loại thẻ",
            placeholder="Ví dụ: Viettel, Vinaphone...",
            max_length=30
        )

        self.serial = TextInput(
            label="Serial",
            placeholder="Nhập serial thẻ",
            max_length=50
        )

        self.code = TextInput(
            label="Mã thẻ",
            placeholder="Nhập mã thẻ",
            max_length=50
        )

        self.add_item(self.amount)
        self.add_item(self.card_type)
        self.add_item(self.serial)
        self.add_item(self.code)

    async def on_submit(self, interaction):
        order = orders[self.user_id]

        order["payment"] = "Thẻ cào"
        order["amount"] = self.amount.value
        order["card_type"] = self.card_type.value
        order["serial"] = self.serial.value
        order["code"] = self.code.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


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
        super().__init__(timeout=60)
        self.add_item(PlanSelect(user_id))


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
        await interaction.response.send_modal(
            PaymentModal(self.user_id)
        )


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

        required = {
            "name": "Tên bot",
            "avatar": "Avatar",
            "topic": "Chủ đề",
            "personality": "Tính cách",
            "features": "Chức năng",
            "plan": "Gói",
            "payment": "Thanh toán"
        }

        missing = []

        for key, label in required.items():
            if order[key] == "Chưa chọn":
                missing.append(label)

        if missing:
            await interaction.response.send_message(
                "❌ Bạn chưa chọn:\n\n" +
                "\n".join(f"• {x}" for x in missing),
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "✅ **Đã gửi đơn!**\n"
            "⏳ Chủ bot sẽ kiểm tra và xử lý.",
            ephemeral=True
        )

        embed = discord.Embed(
            title="🔔 ĐƠN BOT MỚI",
            color=0x00BFFF
        )

        embed.add_field(
            name="👤 Khách",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="🤖 Tên bot",
            value=order["name"],
            inline=True
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
            name="💰 Mệnh giá",
            value=order["amount"],
            inline=True
        )

        embed.add_field(
            name="🎫 Loại thẻ",
            value=order["card_type"],
            inline=True
        )

        # Thông tin thanh toán chỉ gửi riêng cho OWNER
        owner = interaction.guild.get_member(OWNER_ID)

        if owner:
            payment_embed = embed.copy()

            payment_embed.add_field(
                name="🔐 Serial",
                value=order["serial"],
                inline=False
            )

            payment_embed.add_field(
                name="🔐 Mã thẻ",
                value=order["code"],
                inline=False
            )

            payment_embed.add_field(
                name="📌 Trạng thái",
                value="🟡 CHỜ KIỂM TRA",
                inline=False
            )

            try:
                await owner.send(embed=payment_embed)
            except discord.Forbidden:
                print("[CloudAI] Không thể gửi DM cho OWNER.")


class OrderPanel(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)

        self.add_item(NameButton(user_id))
        self.add_item(AvatarButton(user_id))
        self.add_item(TopicButton(user_id))
        self.add_item(PersonalityButton(user_id))
        self.add_item(FeaturesButton(user_id))
        self.add_item(PlanButton(user_id))
        self.add_item(PaymentButton(user_id))
        self.add_item(ConfirmButton(user_id))


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
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild

        if guild is None:
            await interaction.followup.send(
                "❌ Chỉ dùng trong server Discord.",
                ephemeral=True
            )
            return

        ticket_name = f"ticket-{interaction.user.id}"

        for channel in guild.text_channels:
            if channel.name == ticket_name:
                await interaction.followup.send(
                    f"❌ Bạn đã có ticket: {channel.mention}",
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
                    read_message_history=True,
                    embed_links=True
                )
        }

        bot_member = guild.me

        if bot_member:
            overwrites[bot_member] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                embed_links=True,
                manage_channels=True
            )

        owner = guild.get_member(OWNER_ID)

        if owner:
            overwrites[owner] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                embed_links=True
            )

        category = None

        if TICKET_CATEGORY_ID is not None:
            category = guild.get_channel(TICKET_CATEGORY_ID)

        try:
            channel = await guild.create_text_channel(
                ticket_name,
                category=category,
                overwrites=overwrites,
                reason="CloudAI Order"
            )

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ CloudAI không có quyền tạo ticket!",
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

        orders[interaction.user.id] = {
            "name": "Chưa chọn",
            "avatar": "Chưa chọn",
            "topic": "Chưa chọn",
            "personality": "Chưa chọn",
            "features": "Chưa chọn",
            "plan": "Chưa chọn",
            "payment": "Chưa chọn",
            "amount": "Chưa chọn",
            "card_type": "Chưa chọn",
            "serial": "Chưa nhập",
            "code": "Chưa nhập"
        }

        try:
            await channel.send(
                content=(
                    f"👋 Xin chào {interaction.user.mention}!\n\n"
                    "🤖 **Hãy cấu hình bot của bạn bên dưới:**"
                ),
                embed=create_order_embed(
                    interaction.user.id
                ),
                view=OrderPanel(
                    interaction.user.id
                )
            )

            await channel.send(
                "🔒 **Quản lý Ticket**",
                view=TicketView()
            )

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Ticket tạo được nhưng bot không gửi được tin nhắn.",
                ephemeral=True
            )
            return

        await interaction.followup.send(
            f"✅ Ticket đã được tạo: {channel.mention}",
            ephemeral=True
        )
