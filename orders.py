import discord
from discord.ui import Modal, TextInput
from datetime import datetime
from pathlib import Path
import json
import os
import aiohttp

# =========================================================
# CLOUDAI STORE - ORDERS SYSTEM
# Dark • Blue • Premium • Minimal
# =========================================================

OWNER_ID = 1514447473748475975
TICKET_CATEGORY_ID = None

PLANS_FILE = Path("plans.json")
ORDERS_FILE = Path("orders.json")
BOT_CONFIGS_FILE = Path("bot_configs.json")

orders = {}


# =========================================================
# PLAN SYSTEM
# =========================================================

def normalize_plan(plan):
    if not plan:
        return "Chưa đăng ký"

    text = str(plan).upper()

    if "60K" in text or "PREMIUM" in text:
        return "60K"

    if "40K" in text or "VIP" in text:
        return "40K"

    if "20K" in text or "BASIC" in text:
        return "20K"

    if "CUSTOM" in text:
        return "CUSTOM"

    return str(plan)


def get_server_plan(server_id):
    """Lấy gói CloudAI hiện tại của server."""
    try:
        if not PLANS_FILE.exists():
            return "Chưa đăng ký"

        data = json.loads(
            PLANS_FILE.read_text(encoding="utf-8")
        )

        value = data.get(str(server_id), data.get(server_id))

        if isinstance(value, dict):
            return value.get("plan", "Chưa đăng ký")

        return value or "Chưa đăng ký"

    except Exception as e:
        print(f"[CloudAI] plans.json error: {e}")
        return "Chưa đăng ký"


def set_server_plan(server_id, plan):
    """Lưu gói CloudAI của server."""
    data = {}

    try:
        if PLANS_FILE.exists():
            data = json.loads(
                PLANS_FILE.read_text(encoding="utf-8")
            )
    except Exception:
        data = {}

    data[str(server_id)] = {
        "plan": normalize_plan(plan),
        "updated_at": datetime.utcnow().isoformat()
    }

    PLANS_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def upgrade_server_plan(server_id, new_plan):
    """Nâng gói server mà không tạo lại order/bot."""
    new_plan = normalize_plan(new_plan)
    current = normalize_plan(get_server_plan(server_id))
    rank = {"20K": 1, "40K": 2, "60K": 3, "CUSTOM": 4}
    if current in rank and new_plan in rank and rank[new_plan] < rank[current]:
        return False
    set_server_plan(server_id, new_plan)
    return True


# =========================================================
# ORDER STORAGE
# =========================================================

def save_orders():
    """Lưu đơn vào orders.json."""
    try:
        ORDERS_FILE.write_text(
            json.dumps(
                orders,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )
    except Exception as e:
        print(f"[CloudAI] Không thể lưu orders.json: {e}")


def load_orders():
    """Đọc đơn cũ nếu có."""
    global orders

    try:
        if not ORDERS_FILE.exists():
            orders = {}
            return

        orders = json.loads(
            ORDERS_FILE.read_text(
                encoding="utf-8"
            )
        )

    except Exception as e:
        print(f"[CloudAI] Không thể đọc orders.json: {e}")
        orders = {}


load_orders()


def make_order_id(user_id):
    return f"CLD-{str(user_id)[-4:]}-{datetime.utcnow().strftime('%m%d%H%M')}"


def get_order(user_id):
    key = str(user_id)

    if key not in orders:
        orders[key] = {
            "order_id": make_order_id(user_id),

            "user_id": user_id,
            "guild_id": None,
            "ticket_id": None,
            "client_id": "Chưa nhập",
            "invite_url": "Chưa tạo",

            "name": "Chưa chọn",
            "avatar": "Chưa chọn",
            "topic": "Chưa chọn",
            "personality": "Chưa chọn",
            "features": "Chưa chọn",

            "plan": "Chưa chọn",
            "price": "Chưa chọn",

            "payment": "Chưa chọn",
            "amount": "Chưa chọn",
            "payment_reference": "Chưa nhập",
            "payment_note": "Không có",

            "status": "🟡 CHỜ XỬ LÝ",

            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        save_orders()

    return orders[key]


def update_order(user_id, **changes):
    order = get_order(user_id)

    for key, value in changes.items():
        order[key] = value

    order["updated_at"] = datetime.utcnow().isoformat()

    save_orders()

    return order


# =========================================================
# PRICE
# =========================================================

PLAN_PRICES = {
    "Basic - 20.000đ": 20000,
    "VIP - 40.000đ": 40000,
    "Premium - 60.000đ": 60000,
    "Custom": None
}


# =========================================================
# CLOUDAI BOT PRODUCT FEATURES
# =========================================================

PRODUCT_NAME = "🤖 Discord AI Bot"

PLAN_FEATURES = {
    "20K": [
        "AI Chat", "Memory cơ bản", "Tiếng Việt", "Lệnh AI",
        "Tên/avatar/tính cách cơ bản"
    ],
    "40K": [
        "AI Chat", "Memory cơ bản", "Tiếng Việt", "Lệnh AI",
        "Tên/avatar/tính cách cơ bản", "Tự trả lời", "Minecraft AI",
        "Moderation cơ bản", "Welcome", "Embed tùy chỉnh", "Memory nâng cao"
    ],
    "60K": [
        "AI Chat", "Memory cơ bản", "Tiếng Việt", "Lệnh AI",
        "Tên/avatar/tính cách cơ bản", "Tự trả lời", "Minecraft AI",
        "Moderation cơ bản", "Welcome", "Embed tùy chỉnh", "Memory nâng cao",
        "Voice AI", "Lệnh riêng", "Tính cách nâng cao", "Ưu tiên hỗ trợ"
    ],
    "CUSTOM": [
        "Tùy chỉnh theo hợp đồng"
    ],
}

PLAN_FEATURE_FLAGS = {
    "20K": {
        "ai_chat": True, "memory": True, "auto_chat": False,
        "minecraft": False, "moderation": False, "welcome": False,
        "custom_embed": False, "advanced_memory": False,
        "voice": False, "custom_commands": False, "advanced_personality": False,
    },
    "40K": {
        "ai_chat": True, "memory": True, "auto_chat": True,
        "minecraft": True, "moderation": True, "welcome": True,
        "custom_embed": True, "advanced_memory": True,
        "voice": False, "custom_commands": False, "advanced_personality": False,
    },
    "60K": {
        "ai_chat": True, "memory": True, "auto_chat": True,
        "minecraft": True, "moderation": True, "welcome": True,
        "custom_embed": True, "advanced_memory": True,
        "voice": True, "custom_commands": True, "advanced_personality": True,
    },
    "CUSTOM": {
        "ai_chat": True, "memory": True, "auto_chat": True,
        "minecraft": True, "moderation": True, "welcome": True,
        "custom_embed": True, "advanced_memory": True,
        "voice": True, "custom_commands": True, "advanced_personality": True,
    },
}

ORDER_FEATURES = [
    "🛒 Chọn sản phẩm Bot AI",
    "📦 Chọn gói Basic / VIP / Premium / Custom",
    "🤖 Nhập tên bot",
    "🖼️ Nhập avatar",
    "🎯 Chọn chủ đề",
    "😎 Chọn tính cách",
    "⚙️ Nhập chức năng",
    "💳 Ghi nhận phương thức + số tiền + mã giao dịch",
    "🧾 Tạo mã đơn riêng",
    "💾 Lưu đơn vào orders.json",
    "📩 Gửi thông báo đơn vào ticket",
    "💰 OWNER xác nhận thanh toán",
    "✅ OWNER duyệt đơn",
    "🚀 Nhập Client ID để tạo link mời bot",
    "🔗 Tạo Discord OAuth2 Invite Link",
    "🤖 Khách tự Authorize bot vào server",
    "🔵 Chờ kiểm tra bot",
    "🟢 Hoàn tất đơn",
    "❌ Từ chối đơn",
    "🔒 Đóng ticket",
]

ORDER_STATUSES = [
    "🟡 CHỜ XỬ LÝ",
    "🟡 CHỜ XÁC NHẬN THANH TOÁN",
    "🔵 ĐÃ THANH TOÁN",
    "⚙️ ĐANG TRIỂN KHAI",
    "🟠 CHỜ KHÁCH MỜI BOT",
    "🔵 CHỜ KIỂM TRA BOT",
    "🟢 HOÀN TẤT",
    "🔴 ĐÃ TỪ CHỐI",
]


def get_plan_features(plan):
    """Lấy danh sách tính năng theo gói, hỗ trợ cả tên gói đầy đủ và 20K/40K/60K."""
    return PLAN_FEATURES.get(normalize_plan(plan), ["⚙️ Cấu hình theo yêu cầu"])


def get_plan_feature_flags(plan):
    return PLAN_FEATURE_FLAGS.get(normalize_plan(plan), {})


def has_plan_feature(plan, feature):
    return bool(get_plan_feature_flags(plan).get(feature, False))


def save_bot_configs(data):
    BOT_CONFIGS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_bot_configs():
    if not BOT_CONFIGS_FILE.exists():
        return {}
    try:
        return json.loads(BOT_CONFIGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


async def provision_bot_template(order):
    """Tạo config cho Bot Template và gửi sang Railway nếu đã cấu hình webhook."""
    plan = normalize_plan(order.get("plan"))
    config = {
        "order_id": order.get("order_id"),
        "owner_id": str(order.get("user_id")),
        "guild_id": str(order.get("guild_id")),
        "client_id": str(order.get("client_id")),
        "plan": plan,
        "features": get_plan_feature_flags(plan),
        "bot_name": order.get("name", "Chưa chọn"),
        "avatar": order.get("avatar", "Chưa chọn"),
        "topic": order.get("topic", "Chưa chọn"),
        "personality": order.get("personality", "Chưa chọn"),
        "custom_features": order.get("features", "Chưa chọn"),
        "template": "CloudAI-Discord-AI-Bot-v1",
        "status": "provisioned",
        "created_at": datetime.utcnow().isoformat(),
    }

    # Backup local.
    configs = load_bot_configs()
    configs[str(order.get("order_id"))] = config
    save_bot_configs(configs)

    # Gửi sang Railway provisioning service nếu đã đặt URL.
    webhook = os.getenv("PROVISIONING_WEBHOOK_URL", "").strip()
    if not webhook:
        return config

    secret = os.getenv("PROVISIONING_SECRET", "").strip()
    headers = {"Content-Type": "application/json"}
    if secret:
        headers["Authorization"] = f"Bearer {secret}"

    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                webhook, json=config, headers=headers
            ) as response:
                if response.status >= 400:
                    body = await response.text()
                    raise RuntimeError(
                        f"HTTP {response.status}: {body[:300]}"
                    )

        config["status"] = "sent_to_railway"
        configs[str(order.get("order_id"))] = config
        save_bot_configs(configs)
        return config

    except Exception as e:
        print(f"[CloudAI] Railway provisioning error: {e}")
        config["status"] = "local_only"
        config["provision_error"] = str(e)[:500]
        configs[str(order.get("order_id"))] = config
        save_bot_configs(configs)
        return config


def format_plan_features(plan):
    return "\n".join(f"• {item}" for item in get_plan_features(plan))


def create_store_features_embed():
    """Embed giới thiệu toàn bộ tính năng sản phẩm/shop."""
    embed = discord.Embed(
        title="🤖 CloudAI Store • Discord AI Bot",
        description=(
            "Bot AI Discord được bán theo gói.\n"
            "Khách chọn gói → cấu hình → thanh toán → duyệt → nhận link mời bot."
        ),
        color=0x3498DB
    )

    display_plans = {
        "20K": "Basic - 20.000đ",
        "40K": "VIP - 40.000đ",
        "60K": "Premium - 60.000đ",
        "CUSTOM": "Custom",
    }
    for key, label in display_plans.items():
        embed.add_field(
            name=f"📦 {label}",
            value=format_plan_features(key),
            inline=False
        )

    embed.add_field(
        name="🛒 Quy trình",
        value="\n".join(f"• {x}" for x in ORDER_FEATURES),
        inline=False
    )

    embed.set_footer(text="CloudAI Store • Premium Order System")
    return embed


def get_plan_price(plan):
    return PLAN_PRICES.get(plan)


# =========================================================
# ORDER EMBED
# =========================================================

def create_order_embed(user_id):
    order = get_order(user_id)

    embed = discord.Embed(
        title="☁️ CLOUDAI STORE",
        description=(
            "### 🛍️ TẠO ĐƠN DỊCH VỤ\n"
            "Dark • Blue • Premium • Minimal\n\n"
            "Cấu hình bot của bạn rồi hoàn tất thanh toán."
        ),
        color=0x3498DB,
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="🛍️ Sản phẩm",
        value=PRODUCT_NAME,
        inline=False
    )

    embed.add_field(
        name="🧾 Mã đơn",
        value=f"`{order['order_id']}`",
        inline=True
    )

    embed.add_field(
        name="📊 Trạng thái",
        value=order["status"],
        inline=True
    )

    embed.add_field(
        name="🆔 Client ID",
        value=order.get("client_id", "Chưa nhập"),
        inline=True
    )

    embed.add_field(
        name="🔗 Invite",
        value=(
            "Đã tạo" if order.get("invite_url", "Chưa tạo") != "Chưa tạo"
            else "Chưa tạo"
        ),
        inline=True
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
        name="💰 Giá",
        value=order["price"],
        inline=True
    )

    embed.add_field(
        name="💳 Thanh toán",
        value=order["payment"],
        inline=True
    )

    selected_plan = order.get("plan", "Chưa chọn")
    embed.add_field(
        name="✨ Tính năng gói",
        value=format_plan_features(selected_plan)[:1024],
        inline=False
    )

    embed.add_field(
        name="💵 Số tiền thanh toán",
        value=order["amount"],
        inline=True
    )

    embed.add_field(
        name="🔎 Mã giao dịch",
        value=order["payment_reference"],
        inline=False
    )

    embed.add_field(
        name="📝 Ghi chú",
        value=order["payment_note"],
        inline=False
    )

    embed.set_footer(
        text="CloudAI Store • Order System"
    )

    return embed


# =========================================================
# GENERIC MODAL
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
        update_order(
            self.user_id,
            **{
                self.key: self.field.value
            }
        )

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


# =========================================================
# PAYMENT
# =========================================================

class PaymentModal(Modal):

    def __init__(self, user_id):
        super().__init__(
            title="💳 Xác nhận thanh toán"
        )

        self.user_id = user_id

        self.method = TextInput(
            label="Phương thức thanh toán",
            placeholder="Ví dụ: Chuyển khoản",
            max_length=30,
            required=True
        )

        self.amount = TextInput(
            label="Số tiền",
            placeholder="Ví dụ: 40.000",
            max_length=20,
            required=True
        )

        self.reference = TextInput(
            label="Mã giao dịch",
            placeholder="Mã giao dịch / nội dung chuyển khoản",
            max_length=100,
            required=True
        )

        self.note = TextInput(
            label="Ghi chú",
            placeholder="Ví dụ: Thanh toán đơn CLD-1234",
            max_length=200,
            required=False
        )

        self.add_item(self.method)
        self.add_item(self.amount)
        self.add_item(self.reference)
        self.add_item(self.note)

    async def on_submit(self, interaction):
        order = get_order(self.user_id)

        update_order(
            self.user_id,
            payment=self.method.value,
            amount=self.amount.value,
            payment_reference=self.reference.value,
            payment_note=self.note.value or "Không có",
            status="🟡 CHỜ XÁC NHẬN THANH TOÁN"
        )

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
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
        order = get_order(self.user_id)

        if order["plan"] == "Chưa chọn":
            await interaction.response.send_message(
                "❌ Hãy chọn gói trước khi thanh toán.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(
            PaymentModal(self.user_id)
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
                label="Premium - 60.000đ",
                description="Tùy chỉnh nâng cao",
                emoji="🟣",
                value="Premium - 60.000đ"
            ),
            discord.SelectOption(
                label="Custom",
                description="Bot làm riêng theo yêu cầu",
                emoji="👑",
                value="Custom"
            )
        ]

        super().__init__(
            placeholder="📦 Chọn gói CloudAI",
            options=options
        )

    async def callback(self, interaction):
        selected = self.values[0]
        price = get_plan_price(selected)

        if selected == "Custom":
            price_text = "Liên hệ báo giá"
        else:
            price_text = f"{price:,}đ".replace(",", ".")

        update_order(
            self.user_id,
            plan=selected,
            price=price_text,
            payment="Chưa chọn",
            amount="Chưa chọn",
            payment_reference="Chưa nhập",
            payment_note="Không có",
            status="🟡 CHỜ XỬ LÝ"
        )

        await interaction.response.edit_message(
            content=None,
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PlanView(discord.ui.View):

    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.add_item(PlanSelect(user_id))


# =========================================================
# ADMIN PAYMENT CONFIRM + ORDER DECISION
# =========================================================

class DeployClientModal(Modal):

    def __init__(self, user_id):
        super().__init__(title="🚀 Triển khai Bot AI")
        self.user_id = user_id

        self.client_id = TextInput(
            label="Discord Application / Client ID",
            placeholder="Ví dụ: 123456789012345678",
            max_length=30,
            required=True
        )
        self.add_item(self.client_id)

    async def on_submit(self, interaction):
        client_id = self.client_id.value.strip()
        if not client_id.isdigit():
            await interaction.response.send_message(
                "❌ Client ID phải là dãy số.", ephemeral=True
            )
            return

        # Tạo quyền mời bot theo gói, nhưng luôn giữ ở mức tối thiểu cần thiết.
        permissions = discord.Permissions(
            view_channel=True,
            send_messages=True,
            embed_links=True,
            read_message_history=True,
        )

        normalized = normalize_plan(get_order(self.user_id).get("plan"))
        if normalized in ("40K", "60K"):
            permissions.manage_messages = True
            permissions.moderate_members = True

        if normalized == "60K":
            permissions.connect = True
            permissions.speak = True

        invite = (
            "https://discord.com/oauth2/authorize"
            f"?client_id={client_id}"
            "&scope=bot%20applications.commands"
            f"&permissions={permissions.value}"
        )

        update_order(
            self.user_id,
            client_id=client_id,
            invite_url=invite,
            status="🟠 CHỜ KHÁCH MỜI BOT"
        )

        # Provision từ Bot Template theo đúng gói khách đã mua.
        # Không lưu Bot Token trong orders.json.
        try:
            result = await provision_bot_template(get_order(self.user_id))
            if result.get("status") == "local_only":
                print("[CloudAI] Config chỉ lưu local; chưa nối Railway webhook.")
        except Exception as e:
            print(f"[CloudAI] Provisioning error: {e}")

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id),
            view=OrderDecisionView(self.user_id)
        )

        await notify_order_ticket(
            interaction.client,
            self.user_id,
            "🚀 **Bot AI đã sẵn sàng để thêm vào server!**\n"
            "Nhấn nút **🤖 Mời Bot vào Server** bên dưới để Discord mở màn hình Authorize.\n\n"
            "🔐 Bạn không cần gửi Bot Token cho CloudAI.",
            view=BotInviteView(self.user_id, invite)
        )


async def notify_order_ticket(client, user_id, message, embed=None, view=None):
    order = get_order(user_id)
    ticket_id = order.get("ticket_id")
    if not ticket_id:
        return False

    channel = client.get_channel(int(ticket_id))
    if channel is None:
        try:
            channel = await client.fetch_channel(int(ticket_id))
        except Exception:
            return False

    try:
        await channel.send(message, embed=embed, view=view)
        return True
    except Exception as e:
        print(f"[CloudAI] Ticket notify error: {e}")
        return False


class BotInviteView(discord.ui.View):
    """Nút mời bot và xác nhận khách đã Authorize.

    Discord bắt buộc người có quyền trong server khách phải tự bấm Authorize;
    CloudAI không thể tự ý thêm một bot khác vào server.
    """

    def __init__(self, user_id, invite_url):
        super().__init__(timeout=None)
        self.user_id = user_id

        self.add_item(
            discord.ui.Button(
                label="Mời Bot vào Server",
                emoji="🤖",
                style=discord.ButtonStyle.link,
                url=invite_url,
                row=0,
            )
        )

    @discord.ui.button(
        label="Đã mời Bot",
        emoji="✅",
        style=discord.ButtonStyle.success,
        custom_id="cloudai_customer_invited",
        row=1,
    )
    async def invited(self, interaction, button):
        if interaction.user.id != int(self.user_id):
            await interaction.response.send_message(
                "❌ Chỉ người đặt đơn mới được xác nhận.", ephemeral=True
            )
            return

        order = get_order(self.user_id)
        if order.get("status") != "🟠 CHỜ KHÁCH MỜI BOT":
            await interaction.response.send_message(
                "❌ Đơn không còn ở bước mời bot.", ephemeral=True
            )
            return

        update_order(self.user_id, status="🔵 CHỜ KIỂM TRA BOT")
        button.disabled = True

        await interaction.response.edit_message(
            content=(
                "✅ **Đã nhận xác nhận!**\n"
                "CloudAI sẽ kiểm tra/hoàn tất đơn cho bạn."
            ),
            view=self,
        )

        owner = interaction.client.get_user(OWNER_ID)
        if owner is None:
            try:
                owner = await interaction.client.fetch_user(OWNER_ID)
            except Exception:
                owner = None

        if owner:
            try:
                await owner.send(
                    f"🔔 **Đơn `{order['order_id']}` đã được khách xác nhận đã mời Bot.**\n"
                    f"🤖 Client ID: `{order.get('client_id', 'Chưa nhập')}`\n"
                    "👉 Kiểm tra bot trong server rồi bấm **🟢 Hoàn tất**."
                )
            except Exception as e:
                print(f"[CloudAI] Không thể báo OWNER: {e}")


class OrderDecisionView(discord.ui.View):

    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    async def owner_only(self, interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                "❌ Chỉ chủ bot mới được quản lý đơn.", ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Xác nhận thanh toán", emoji="💰",
                       style=discord.ButtonStyle.primary,
                       custom_id="cloudai_confirm_payment", row=0)
    async def confirm_payment(self, interaction, button):
        if not await self.owner_only(interaction):
            return
        order = get_order(self.user_id)
        if order["status"] != "🟡 CHỜ XÁC NHẬN THANH TOÁN":
            await interaction.response.send_message(
                "❌ Đơn chưa ở trạng thái chờ xác nhận thanh toán.", ephemeral=True
            )
            return
        update_order(self.user_id, status="🔵 ĐÃ THANH TOÁN")
        button.disabled = True
        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id), view=self
        )
        await notify_order_ticket(
            interaction.client, self.user_id,
            f"💰 **Đơn `{order['order_id']}` đã được xác nhận thanh toán.**\n"
            "Bạn có thể chờ bước duyệt đơn."
        )

    @discord.ui.button(label="Duyệt đơn", emoji="✅",
                       style=discord.ButtonStyle.success,
                       custom_id="cloudai_approve_order", row=1)
    async def approve(self, interaction, button):
        if not await self.owner_only(interaction):
            return
        order = get_order(self.user_id)
        if order["status"] != "🔵 ĐÃ THANH TOÁN":
            await interaction.response.send_message(
                "❌ Hãy xác nhận thanh toán trước khi duyệt đơn.", ephemeral=True
            )
            return

        update_order(self.user_id, status="⚙️ ĐANG TRIỂN KHAI")
        if order.get("guild_id"):
            try:
                set_server_plan(order["guild_id"], normalize_plan(order["plan"]))
            except Exception as e:
                print(f"[CloudAI] Không thể lưu gói server: {e}")

        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id), view=self
        )
        await notify_order_ticket(
            interaction.client, self.user_id,
            f"✅ **Đơn `{order['order_id']}` đã được duyệt!**\n"
            "⚙️ CloudAI đang chuẩn bị triển khai bot."
        )

    @discord.ui.button(label="Triển khai", emoji="🚀",
                       style=discord.ButtonStyle.primary,
                       custom_id="cloudai_deploy_order", row=2)
    async def deploy(self, interaction, button):
        if not await self.owner_only(interaction):
            return
        order = get_order(self.user_id)
        if order["status"] != "⚙️ ĐANG TRIỂN KHAI":
            await interaction.response.send_message(
                "❌ Hãy duyệt đơn trước khi triển khai.", ephemeral=True
            )
            return
        await interaction.response.send_modal(DeployClientModal(self.user_id))

    @discord.ui.button(label="Hoàn tất", emoji="🟢",
                       style=discord.ButtonStyle.success,
                       custom_id="cloudai_complete_order", row=2)
    async def complete(self, interaction, button):
        if not await self.owner_only(interaction):
            return
        order = get_order(self.user_id)
        if order["status"] not in (
            "⚙️ ĐANG TRIỂN KHAI",
            "🟠 CHỜ KHÁCH MỜI BOT",
            "🔵 CHỜ KIỂM TRA BOT",
        ):
            await interaction.response.send_message(
                "❌ Đơn chưa ở bước triển khai Bot AI.", ephemeral=True
            )
            return
        if order.get("client_id", "Chưa nhập") == "Chưa nhập":
            await interaction.response.send_message(
                "❌ Hãy bấm **🚀 Triển khai** và nhập Client ID trước.", ephemeral=True
            )
            return
        update_order(self.user_id, status="🟢 HOÀN TẤT")
        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id), view=self
        )
        await notify_order_ticket(
            interaction.client, self.user_id,
            f"🟢 **Đơn `{order['order_id']}` đã hoàn tất!**\n"
            "Cảm ơn bạn đã sử dụng CloudAI Store."
        )

    @discord.ui.button(label="Từ chối", emoji="❌",
                       style=discord.ButtonStyle.danger,
                       custom_id="cloudai_reject_order", row=3)
    async def reject(self, interaction, button):
        if not await self.owner_only(interaction):
            return
        update_order(self.user_id, status="🔴 ĐÃ TỪ CHỐI")
        await interaction.response.edit_message(
            embed=create_order_embed(self.user_id), view=self
        )
        await notify_order_ticket(
            interaction.client, self.user_id,
            "❌ **Đơn CloudAI đã bị từ chối.** Vui lòng xem lại thông tin trong ticket."
        )


# =========================================================
# SEND ORDER
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
                    f"• {item}"
                    for item in missing
                ),
                ephemeral=True
            )
            return

        if (
            order["payment"] == "Chưa chọn"
            or order["amount"] == "Chưa chọn"
            or order["payment_reference"] == "Chưa nhập"
        ):
            await interaction.response.send_message(
                "❌ Bạn chưa hoàn tất thông tin thanh toán.",
                ephemeral=True
            )
            return

        update_order(
            self.user_id,
            status="🟡 CHỜ XÁC NHẬN THANH TOÁN"
        )

        await interaction.response.send_message(
            "✅ Đã gửi đơn!\n"
            "🟡 Đơn đang chờ CloudAI xác nhận thanh toán.",
            ephemeral=True
        )

        embed = discord.Embed(
            title="🔔 CLOUDAI STORE • ĐƠN MỚI",
            description=(
                f"**Mã đơn:** `{order['order_id']}`\n"
                "Có khách vừa gửi một đơn dịch vụ."
            ),
            color=0x3498DB,
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="👤 Khách hàng",
            value=interaction.user.mention,
            inline=True
        )

        embed.add_field(
            name="🆔 User ID",
            value=str(interaction.user.id),
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
            name="💰 Giá",
            value=order["price"],
            inline=True
        )

        embed.add_field(
            name="💳 Thanh toán",
            value=order["payment"],
            inline=True
        )

        embed.add_field(
            name="💵 Số tiền",
            value=order["amount"],
            inline=True
        )

        embed.add_field(
            name="🔎 Mã giao dịch",
            value=order["payment_reference"],
            inline=False
        )

        embed.add_field(
            name="📝 Ghi chú",
            value=order["payment_note"],
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
            name="📊 Trạng thái",
            value=order["status"],
            inline=False
        )

        embed.set_footer(
            text="CloudAI Store • Admin Order Panel"
        )

        owner = interaction.client.get_user(OWNER_ID)

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
                view=OrderDecisionView(self.user_id)
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

        self.add_item(NameButton(user_id))
        self.add_item(AvatarButton(user_id))
        self.add_item(TopicButton(user_id))
        self.add_item(PersonalityButton(user_id))
        self.add_item(FeaturesButton(user_id))
        self.add_item(PlanButton(user_id))
        self.add_item(PaymentButton(user_id))
        self.add_item(ConfirmButton(user_id))


# =========================================================
# ORDER INPUT BUTTONS
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
            "📦 **Chọn gói CloudAI:**",
            view=PlanView(self.user_id),
            ephemeral=True
        )


# =========================================================
# TICKET
# =========================================================

class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Đóng Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="cloudai_close_ticket"
    )
    async def close_ticket(self, interaction, button):

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
            pass


# =========================================================
# MAIN ORDER VIEW
# =========================================================

class OrderView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Xem tính năng",
        emoji="✨",
        style=discord.ButtonStyle.secondary,
        custom_id="cloudai_features"
    )
    async def features(self, interaction, button):
        await interaction.response.send_message(
            embed=create_store_features_embed(),
            ephemeral=True
        )

    @discord.ui.button(
        label="Đặt Bot",
        emoji="🤖",
        style=discord.ButtonStyle.primary,
        custom_id="cloudai_order"
    )
    async def order_button(self, interaction, button):

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

        try:
            channel = await guild.create_text_channel(
                ticket_name,
                category=category,
                overwrites=overwrites,
                reason="CloudAI Store Order"
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

        orders[str(interaction.user.id)] = {
            "order_id": make_order_id(
                interaction.user.id
            ),

            "user_id": interaction.user.id,
            "guild_id": guild.id,
            "ticket_id": channel.id,
            "client_id": "Chưa nhập",
            "invite_url": "Chưa tạo",

            "name": "Chưa chọn",
            "avatar": "Chưa chọn",
            "topic": "Chưa chọn",
            "personality": "Chưa chọn",
            "features": "Chưa chọn",

            "plan": "Chưa chọn",
            "price": "Chưa chọn",

            "payment": "Chưa chọn",
            "amount": "Chưa chọn",
            "payment_reference": "Chưa nhập",
            "payment_note": "Không có",

            "status": "🟡 CHỜ XỬ LÝ",

            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        save_orders()

        try:
            await channel.send(
                content=(
                    f"👋 Xin chào {interaction.user.mention}!\n\n"
                    "☁️ **Chào mừng đến CloudAI Store.**\n"
                    "Hãy cấu hình bot của bạn bên dưới."
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

        await interaction.followup.send(
            f"✅ Ticket đã được tạo: {channel.mention}",
            ephemeral=True
        )
