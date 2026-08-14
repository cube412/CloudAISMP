```python
import discord
from discord.ui import Modal, TextInput
from datetime import datetime
import json
import os


# =========================================================
# CONFIG
# =========================================================

OWNER_ID = 1514447473748475975

# Nếu muốn ticket nằm trong một category cụ thể:
# điền ID category vào đây.
# Không dùng category thì để None.
TICKET_CATEGORY_ID = None

PLANS_FILE = "plans.json"


# =========================================================
# ORDER DATA
# =========================================================

orders = {}


def new_order():
    return {
        "guild_id": None,
        "guild_name": "Chưa xác định",

        "name": "Chưa chọn",
        "avatar": "Chưa chọn",
        "topic": "Chưa chọn",
        "personality": "Chưa chọn",
        "features": "Chưa chọn",

        "plan": "Chưa chọn",

        "payment": "Chưa chọn",
        "card_type": "Chưa chọn",
        "amount": "Chưa chọn",
        "serial": "Chưa nhập",
        "code": "Chưa nhập",

        "status": "🟡 CHỜ XỬ LÝ"
    }


def get_order(user_id):
    if user_id not in orders:
        orders[user_id] = new_order()

    return orders[user_id]


# =========================================================
# PLAN SYSTEM
# =========================================================

def load_plans():
    if not os.path.exists(PLANS_FILE):
        return {}

    try:
        with open(
            PLANS_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except Exception as e:
        print(f"[CloudAI] Không đọc được plans.json: {e}")
        return {}


def save_plans(plans):
    try:
        with open(
            PLANS_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                plans,
                f,
                ensure_ascii=False,
                indent=4
            )

    except Exception as e:
        print(f"[CloudAI] Không lưu được plans.json: {e}")


def normalize_plan(plan):
    plan = str(plan).lower()

    if "basic" in plan or "20.000" in plan or "20k" in plan:
        return "20K"

    if "vip" in plan or "40.000" in plan or "40k" in plan:
        return "40K"

    if "custom" in plan:
        return "CUSTOM"

    return "UNKNOWN"


def set_server_plan(guild_id, plan):
    if guild_id is None:
        return

    plans = load_plans()

    plans[str(guild_id)] = {
        "plan": normalize_plan(plan),
        "updated_at": datetime.now().isoformat()
    }

    save_plans(plans)

    print(
        f"[CloudAI] Server {guild_id} -> "
        f"{normalize_plan(plan)}"
    )


def get_server_plan(guild_id):
    plans = load_plans()

    data = plans.get(str(guild_id))

    if not data:
        return "20K"

    if isinstance(data, dict):
        return data.get("plan", "20K")

    return str(data)


# =========================================================
# ORDER EMBED
# =========================================================

def create_order_embed(user_id):
    order = get_order(user_id)

    embed = discord.Embed(
        title="🤖 ĐẶT BOT CLOUD AI",
        description="Hãy chọn thông tin cho bot của bạn.",
        color=0x00BFFF
    )

    fields = [
        ("🤖 Tên bot", order["name"], False),
        ("🖼️ Avatar", order["avatar"], False),
        ("🎯 Chủ đề", order["topic"], False),
        ("😎 Tính cách", order["personality"], False),
        ("⚙️ Chức năng", order["features"], False),
        ("📦 Gói", order["plan"], True),
        ("💳 Thanh toán", order["payment"], True),
        ("💰 Số tiền", order["amount"], True),
        ("🏷️ Loại thẻ", order["card_type"], True),
        ("📌 Trạng thái", order["status"], False)
    ]

    for name, value, inline in fields:
        embed.add_field(
            name=name,
            value=str(value),
            inline=inline
        )

    return embed


# =========================================================
# SIMPLE MODAL
# =========================================================

class SimpleModal(Modal):

    def __init__(
        self,
        user_id,
        title,
        field_label,
        key,
        placeholder,
        max_length=200,
        paragraph=False
    ):
        super().__init__(title=title)

        self.user_id = user_id
        self.key = key

        self.field = TextInput(
            label=field_label,
            placeholder=placeholder,
            max_length=max_length,
            required=True,
            style=(
                discord.TextStyle.paragraph
                if paragraph
                else discord.TextStyle.short
            )
        )

        self.add_item(self.field)

    async def on_submit(self, interaction):

        order = get_order(self.user_id)

        order[self.key] = self.field.value

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# =========================================================
# PAYMENT MODAL
# =========================================================

class PaymentModal(Modal):

    def __init__(self, user_id):

        super().__init__(
            title="💳 Thông tin thẻ"
        )

        self.user_id = user_id

        self.card_type = TextInput(
            label="Loại thẻ",
            placeholder="Viettel, Vinaphone, Mobifone...",
            max_length=30,
            required=True
        )

        self.amount = TextInput(
            label="Mệnh giá",
            placeholder="Ví dụ: 40.000",
            max_length=20,
            required=True
        )

        self.serial = TextInput(
            label="Số seri",
            placeholder="Nhập số seri",
            max_length=50,
            required=True
        )

        self.code = TextInput(
            label="Mã thẻ",
            placeholder="Nhập mã thẻ",
            max_length=100,
            required=True
        )

        self.add_item(self.card_type)
        self.add_item(self.amount)
        self.add_item(self.serial)
        self.add_item(self.code)

    async def on_submit(self, interaction):

        order = get_order(self.user_id)

        order["payment"] = "Thẻ cào"
        order["card_type"] = self.card_type.value
        order["amount"] = self.amount.value
        order["serial"] = self.serial.value
        order["code"] = self.code.value
        order["status"] = "🟡 CHỜ BẠN KIỂM TRA"

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# =========================================================
# PLAN SELECT
# =========================================================

class PlanSelect(discord.ui.Select):

    def __init__(self, user_id):

        self.user_id = user_id

        options = [
            discord.SelectOption(
                label="Basic - 20.000đ",
                description="AI Chat + Memory",
                emoji="🟢",
                value="Basic - 20.000đ"
            ),

            discord.SelectOption(
                label="VIP - 40.000đ",
                description="AI + Welcome + Moderation",
                emoji="🔵",
                value="VIP - 40.000đ"
            ),

            discord.SelectOption(
                label="Custom - từ 50.000đ",
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
            content=None,
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PlanView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=60)

        self.add_item(
            PlanSelect(user_id)
        )


# =========================================================
# PAYMENT BUTTON
# =========================================================

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


# =========================================================
# ORDER DECISION
# =========================================================

class OrderDecisionView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=None)

        self.user_id = user_id

    # -----------------------------------------------------
    # APPROVE
    # -----------------------------------------------------

    @discord.ui.button(
        label="Duyệt đơn",
        emoji="✅",
        style=discord.ButtonStyle.success
    )
    async def approve(self, interaction, button):

        if interaction.user.id != OWNER_ID:

            await interaction.response.send_message(
                "❌ Chỉ chủ bot mới được duyệt đơn.",
                ephemeral=True
            )

            return

        order = get_order(self.user_id)

        # Kiểm tra gói
        if order["plan"] == "Chưa chọn":

            await interaction.response.send_message(
                "❌ Đơn này chưa chọn gói.",
                ephemeral=True
            )

            return

        # Lưu gói cho server
        guild_id = order.get("guild_id")

        if guild_id is not None:

            set_server_plan(
                guild_id,
                order["plan"]
            )

        order["status"] = "🟢 ĐÃ DUYỆT"

        # Disable nút
        for child in self.children:

            if isinstance(
                child,
                discord.ui.Button
            ):
                child.disabled = True

        try:

            await interaction.response.edit_message(
                embed=create_order_embed(
                    self.user_id
                ),
                view=self
            )

        except Exception:

            await interaction.response.send_message(
                "✅ Đã duyệt đơn.",
                ephemeral=True
            )

        # Gửi DM khách
        user = interaction.client.get_user(
            self.user_id
        )

        if user:

            try:

                plan = normalize_plan(
                    order["plan"]
                )

                await user.send(
                    "✅ **Đơn đặt bot của bạn đã được duyệt!**\n\n"
                    f"📦 Gói: **{plan}**\n"
                    "🤖 CloudAI sẽ tiến hành cấu hình bot cho bạn."
                )

            except discord.Forbidden:

                print(
                    "[CloudAI] Không thể DM khách."
                )

        print(
            f"[CloudAI] Đã duyệt đơn "
            f"{self.user_id}"
        )

    # -----------------------------------------------------
    # REJECT
    # -----------------------------------------------------

    @discord.ui.button(
        label="Từ chối đơn",
        emoji="❌",
        style=discord.ButtonStyle.danger
    )
    async def reject(self, interaction, button):

        if interaction.user.id != OWNER_ID:

            await interaction.response.send_message(
                "❌ Chỉ chủ bot mới được từ chối đơn.",
                ephemeral=True
            )

            return

        order = get_order(self.user_id)

        order["status"] = "🔴 ĐÃ TỪ CHỐI"

        for child in self.children:

            if isinstance(
                child,
                discord.ui.Button
            ):
                child.disabled = True

        try:

            await interaction.response.edit_message(
                embed=create_order_embed(
                    self.user_id
                ),
                view=self
            )

        except Exception:

            await interaction.response.send_message(
                "❌ Đã từ chối đơn.",
                ephemeral=True
            )

        user = interaction.client.get_user(
            self.user_id
        )

        if user:

            try:

                await user.send(
                    "❌ **Đơn đặt bot của bạn đã bị từ chối.**"
                )

            except discord.Forbidden:

                print(
                    "[CloudAI] Không thể DM khách."
                )

        print(
            f"[CloudAI] Đã từ chối đơn "
            f"{self.user_id}"
        )


# =========================================================
# CONFIRM ORDER
# =========================================================

class ConfirmButton(discord.ui.Button):

    def __init__(self, user_id):

        self.user_id = user_id

        super().__init__(
            label="Gửi đơn",
            emoji="📨",
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
            "plan": "Gói"
        }

        missing = [
            label
            for key, label in required.items()
            if order[key] == "Chưa chọn"
        ]

        if missing:

            await interaction.response.send_message(
                "❌ Bạn chưa hoàn thành:\n"
                + "\n".join(
                    f"• {x}"
                    for x in missing
                ),
                ephemeral=True
            )

            return

        if order["payment"] == "Chưa chọn":

            await interaction.response.send_message(
                "❌ Bạn chưa chọn thông tin thanh toán.",
                ephemeral=True
            )

            return

        order["status"] = "🟡 CHỜ BẠN KIỂM TRA"

        await interaction.response.send_message(
            "✅ Đã gửi đơn! Chủ bot sẽ kiểm tra.",
            ephemeral=True
        )

        # -------------------------------------------------
        # ORDER EMBED
        # -------------------------------------------------

        embed = discord.Embed(
            title="🔔 ĐƠN BOT MỚI",
            description="Có khách vừa gửi một đơn đặt bot.",
            color=0x00BFFF,
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="👤 Khách hàng",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="🆔 User ID",
            value=str(interaction.user.id),
            inline=False
        )

        embed.add_field(
            name="🏠 Server",
            value=order.get(
                "guild_name",
                "Chưa xác định"
            ),
            inline=True
        )

        embed.add_field(
            name="🆔 Server ID",
            value=str(
                order.get(
                    "guild_id",
                    "Không có"
                )
            ),
            inline=True
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
            name="💳 Thanh toán",
            value=order["payment"],
            inline=True
        )

        embed.add_field(
            name="🏷️ Loại thẻ",
            value=order["card_type"],
            inline=True
        )

        embed.add_field(
            name="💰 Mệnh giá",
            value=order["amount"],
            inline=True
        )

        embed.add_field(
            name="🔢 SERI",
            value=order["serial"],
            inline=False
        )

        embed.add_field(
            name="🔐 MÃ THẺ",
            value=order["code"],
            inline=False
        )

        embed.add_field(
            name="📌 Trạng thái",
            value=order["status"],
            inline=False
        )

        embed.set_footer(
            text="CloudAI Order System"
        )

        # -------------------------------------------------
        # GỬI VÀO TICKET
        # -------------------------------------------------

        try:

            await interaction.channel.send(
                embed=embed
            )

        except discord.Forbidden:

            print(
                "[CloudAI] Không thể gửi embed vào ticket."
            )

        # -------------------------------------------------
        # GỬI DM OWNER
        # -------------------------------------------------

        owner = interaction.client.get_user(
            OWNER_ID
        )

        if owner is None:

            try:

                owner = await interaction.client.fetch_user(
                    OWNER_ID
                )

            except Exception as e:

                print(
                    f"[CloudAI] Không tìm thấy OWNER: {e}"
                )

                return

        try:

            await owner.send(
                embed=embed,
                view=OrderDecisionView(
                    self.user_id
                )
            )

            print(
                "[CloudAI] Đã gửi đơn riêng cho OWNER."
            )

        except discord.Forbidden:

            print(
                "[CloudAI] Không thể gửi DM cho OWNER."
            )


# =========================================================
# ORDER PANEL
# =========================================================

class OrderPanel(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=None)

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


# =========================================================
# NAME BUTTON
# =========================================================

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
            SimpleModal(
                self.user_id,
                "🤖 Đặt tên bot",
                "Tên bot",
                "name",
                "Ví dụ: CloudAI",
                32
            )
        )


# =========================================================
# AVATAR BUTTON
# =========================================================

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
            SimpleModal(
                self.user_id,
                "🖼️ Avatar bot",
                "Link ảnh Avatar",
                "avatar",
                "https://...",
                500
            )
        )


# =========================================================
# TOPIC BUTTON
# =========================================================

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
            SimpleModal(
                self.user_id,
                "🎯 Chủ đề bot",
                "Chủ đề",
                "topic",
                "Minecraft, Gaming, Anime...",
                100
            )
        )


# =========================================================
# PERSONALITY BUTTON
# =========================================================

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
            SimpleModal(
                self.user_id,
                "😎 Tính cách bot",
                "Tính cách",
                "personality",
                "Vui vẻ, chill, nghiêm túc...",
                200
            )
        )


# =========================================================
# FEATURES BUTTON
# =========================================================

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
            SimpleModal(
                self.user_id,
                "⚙️ Chức năng bot",
                "Chức năng",
                "features",
                "AI Chat, Welcome, Moderation...",
                500,
                True
            )
        )


# =========================================================
# PLAN BUTTON
# =========================================================

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
            "📦 Chọn gói bot:",
            view=PlanView(
                self.user_id
            ),
            ephemeral=True
        )


# =========================================================
# TICKET VIEW
# =========================================================

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

        try:

            await interaction.channel.delete()

        except discord.Forbidden:

            print(
                "[CloudAI] Không có quyền đóng ticket."
            )


# =========================================================
# MAIN ORDER VIEW
# =========================================================

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
        interaction,
        button
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

        ticket_name = (
            f"ticket-{interaction.user.id}"
        )

        # -------------------------------------------------
        # KIỂM TRA TICKET CŨ
        # -------------------------------------------------

        for channel in guild.text_channels:

            if channel.name == ticket_name:

                await interaction.followup.send(
                    f"❌ Bạn đã có ticket: {channel.mention}",
                    ephemeral=True
                )

                return

        # -------------------------------------------------
        # PERMISSIONS
        # -------------------------------------------------

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

            overwrites[bot_member] = (
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    embed_links=True,
                    manage_channels=True
                )
            )

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

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        category = None

        if TICKET_CATEGORY_ID is not None:

            category = guild.get_channel(
                TICKET_CATEGORY_ID
            )

        # -------------------------------------------------
        # CREATE TICKET
        # -------------------------------------------------

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

            print(
                f"[CloudAI] Ticket Error: {e}"
            )

            await interaction.followup.send(
                "❌ Không thể tạo ticket.",
                ephemeral=True
            )

            return

        # -------------------------------------------------
        # CREATE ORDER
        # -------------------------------------------------

        orders[interaction.user.id] = new_order()

        orders[interaction.user.id]["guild_id"] = (
            guild.id
        )

        orders[interaction.user.id]["guild_name"] = (
            guild.name
        )

        # -------------------------------------------------
        # SEND ORDER PANEL
        # -------------------------------------------------

        try:

            await channel.send(
                content=(
                    f"👋 Xin chào "
                    f"{interaction.user.mention}!\n\n"
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
                "❌ Ticket đã tạo nhưng bot không gửi được bảng.",
                ephemeral=True
            )

            return

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        await interaction.followup.send(
            f"✅ Ticket đã được tạo: "
            f"{channel.mention}",
            ephemeral=True
        )

        print(
            f"[CloudAI] Tạo ticket "
            f"{ticket_name} "
            f"cho {interaction.user.id}"
        )
```
