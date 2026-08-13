# ==========================================
# THANH TOÁN
# ==========================================

class PaymentSelect(discord.ui.Select):

    def __init__(self, user_id):

        self.user_id = user_id

        options = [
            discord.SelectOption(
                label="Thẻ Viettel",
                description="Thanh toán bằng thẻ Viettel",
                emoji="🟢",
                value="Viettel"
            ),
            discord.SelectOption(
                label="Thẻ VinaPhone",
                description="Thanh toán bằng thẻ VinaPhone",
                emoji="🔵",
                value="VinaPhone"
            ),
            discord.SelectOption(
                label="Thẻ MobiFone",
                description="Thanh toán bằng thẻ MobiFone",
                emoji="🟠",
                value="MobiFone"
            )
        ]

        super().__init__(
            placeholder="💳 Chọn loại thẻ",
            options=options
        )

    async def callback(self, interaction):

        orders[self.user_id]["payment_type"] = self.values[0]

        await interaction.response.send_message(
            "💵 **Chọn mệnh giá:**",
            view=AmountView(self.user_id),
            ephemeral=True
        )


class AmountSelect(discord.ui.Select):

    def __init__(self, user_id):

        self.user_id = user_id

        options = [
            discord.SelectOption(
                label="20.000đ",
                emoji="💵",
                value="20.000đ"
            ),
            discord.SelectOption(
                label="40.000đ",
                emoji="💵",
                value="40.000đ"
            ),
            discord.SelectOption(
                label="50.000đ",
                emoji="💵",
                value="50.000đ"
            ),
            discord.SelectOption(
                label="100.000đ",
                emoji="💵",
                value="100.000đ"
            )
        ]

        super().__init__(
            placeholder="💵 Chọn mệnh giá",
            options=options
        )

    async def callback(self, interaction):

        orders[self.user_id]["payment_amount"] = self.values[0]
        orders[self.user_id]["payment"] = (
            f"{orders[self.user_id].get('payment_type', 'Chưa chọn')} "
            f"- {self.values[0]}"
        )

        await interaction.response.edit_message(
            content="✅ Đã chọn phương thức thanh toán!",
            embed=create_order_embed(self.user_id),
            view=OrderPanel(self.user_id)
        )


class PaymentView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=60)

        self.add_item(
            PaymentSelect(user_id)
        )


class AmountView(discord.ui.View):

    def __init__(self, user_id):

        super().__init__(timeout=60)

        self.add_item(
            AmountSelect(user_id)
        )
