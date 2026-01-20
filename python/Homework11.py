while True:
    receiver = input("请输入收件人姓名：").strip()
    if receiver == "":
        print("❌ 收件人姓名不能为空，请重新输入！")
    else:
        break
while True:
    theme = input("请输入节日主题（如：新年快乐）：").strip()
    if theme == "":
        print("❌ 节日主题不能为空，请重新输入！")
    else:
        break
while True:
    blessing = input("请输入祝福短语（1~50个字符）：").strip()
    if blessing == "":
        print("❌ 祝福短语不能为空，请重新输入！")
    elif len(blessing) > 50:
        print("❌ 祝福短语长度不能超过50个字符，请重新输入！")
    else:
        break
width = 40
border = "🎀" + "*" * (width - 2) + "🎀"
blank = "✨" + " " * (width - 2) + "✨"

title_line = f"✨{(theme + '，' + receiver + '！').center(width - 2)}✨"
blessing_line = f"✨{blessing.center(width - 2)}✨"

card = (
    border + "\n" +
    blank + "\n" +
    title_line + "\n" +
    blank + "\n" +
    blessing_line + "\n" +
    blank + "\n" +
    border
)

print(card)
while True:
    choice = input("是否将贺卡内容转为大写？(y/n)：").strip().lower()
    if choice == "y":
        card = card.upper()
        break
    elif choice == "n":
        break
    else:
        print("❌ 只能输入 y 或 n，请重新输入！")
while True:
    again = input("是否继续制作新贺卡？(y/n)：").strip().lower()
    if again == "y":
        break
    elif again == "n":
        print("🙏 感谢使用节日贺卡生成器！")
        exit()
    else:
        print("❌ 只能输入 y 或 n，请重新输入！")
