bank_cards = {}

for i in range(1, 101):
    card_suffix = f"{i:03d}"
    card_number = "610" + card_suffix
    bank_cards[card_number] = "000000"

print("100个银行卡及密码如下：")
print(bank_cards)
