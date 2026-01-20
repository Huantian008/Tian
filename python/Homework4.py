id_card=input("请输入身份证号码：")
if len(id_card)!=18:
    print("身份证号码长度不正确，请重新输入")
else:
    province_code=id_card[0:2]
    birth =id_card[6:14]
    gander_code=int(id_card[16])
    if gander_code%2==1:
        gander="男"
    else:
        gander="女"
    if province_code=="36":
        province="江西省"
        secret_id=id_card[:10]+"****"+id_card[-4:]
    print("\n该人的身份信息如下：")
    print("所在省份：", province)
    print("出生日期：", birth)
    print("性别：", gander)
    print("\n身份证保密显示如下：", secret_id)

