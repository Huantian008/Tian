
import requests
from bs4 import BeautifulSoup
import csv
import pymysql
import pymongo

# ======================== 爬虫部分 ========================

def crawl_maoyan():
    """爬取猫眼电影TOP榜单数据"""
    url = "https://www.maoyan.com/board/4"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    movies = []
    try:
        response = requests.get(url=url, headers=headers)
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # 查找所有电影条目
        items = soup.find_all("dd")
        for dd in items:
            try:
                name_tag = dd.find("p", class_="name")
                star_tag = dd.find("p", class_="star")
                time_tag = dd.find("p", class_="releasetime")
                score_tags = dd.find("p", class_="score")

                if name_tag and star_tag and time_tag and score_tags:
                    name = name_tag.find("a").get("title", "").strip()
                    star = star_tag.text.strip()
                    releasetime = time_tag.text.strip()
                    score = "".join([i.text for i in score_tags.find_all("i")])

                    movie = {
                        "name": name,
                        "star": star,
                        "releasetime": releasetime,
                        "score": score
                    }
                    movies.append(movie)
                    print(f"爬取成功: {name} | {star} | {releasetime} | {score}")
            except Exception:
                continue

    except Exception as e:
        print(f"爬取失败: {e}")

    # 如果爬取失败或无数据，使用备用示例数据
    if not movies:
        print("\n爬取未获取到数据，使用备用示例数据...")
        movies = [
            {"name": "肖申克的救赎", "star": "主演：蒂姆·罗宾斯,摩根·弗里曼", "releasetime": "上映时间：1994-09-10", "score": "9.5"},
            {"name": "霸王别姬", "star": "主演：张国荣,张丰毅,巩俐", "releasetime": "上映时间：1993-01-01", "score": "9.4"},
            {"name": "罗马假日", "star": "主演：格利高里·派克,奥黛丽·赫本", "releasetime": "上映时间：1953-08-20", "score": "9.1"},
            {"name": "这个杀手不太冷", "star": "主演：让·雷诺,加里·奥德曼,娜塔莉·波特曼", "releasetime": "上映时间：1994-09-14", "score": "9.5"},
            {"name": "泰坦尼克号", "star": "主演：莱昂纳多·迪卡普里奥,凯特·温丝莱特", "releasetime": "上映时间：1998-04-03", "score": "9.3"},
            {"name": "千与千寻", "star": "主演：柊瑠美,入野自由,夏木真理", "releasetime": "上映时间：2019-06-21", "score": "9.2"},
            {"name": "星际穿越", "star": "主演：马修·麦康纳,安妮·海瑟薇", "releasetime": "上映时间：2014-11-12", "score": "9.4"},
            {"name": "忠犬八公的故事", "star": "主演：理查·基尔,萨拉·罗默尔", "releasetime": "上映时间：2010-03-12", "score": "9.2"},
            {"name": "海上钢琴师", "star": "主演：蒂姆·罗斯,比尔·努恩", "releasetime": "上映时间：2019-11-15", "score": "9.2"},
            {"name": "三傻大闹宝莱坞", "star": "主演：阿米尔·汗,卡琳娜·卡普尔", "releasetime": "上映时间：2011-12-08", "score": "9.1"},
        ]
        for m in movies:
            print(f"备用数据: {m['name']} | {m['star']} | {m['releasetime']} | {m['score']}")

    return movies


# ======================== CSV 存储 ========================

def save_to_csv(movies):
    """将电影数据存储到CSV文件"""
    print("\n" + "=" * 50)
    print("【CSV存储】开始...")
    filepath = "maoyan_movies.csv"

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(["电影名称", "主演", "上映时间", "评分"])
        # 写入数据
        for movie in movies:
            writer.writerow([movie["name"], movie["star"], movie["releasetime"], movie["score"]])

    print(f"【CSV存储】成功！共写入 {len(movies)} 条数据到 {filepath}")


# ======================== PyMySQL 存储 ========================

def save_to_mysql(movies):
    """将电影数据存储到MySQL数据库"""
    print("\n" + "=" * 50)
    print("【MySQL存储】开始...")

    # MySQL 连接配置（请根据实际情况修改）
    config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "ywt123YWT",  # 修改为你的MySQL密码
        "charset": "utf8mb4",
        "connect_timeout": 5
    }

    db = None
    cursor = None
    try:
        # 连接MySQL
        db = pymysql.connect(**config)
        cursor = db.cursor()

        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS maoyan DEFAULT CHARSET utf8mb4")
        cursor.execute("USE maoyan")

        # 创建表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                star VARCHAR(200),
                releasetime VARCHAR(100),
                score VARCHAR(10)
            )
        """)

        # 清空旧数据（避免重复插入）
        cursor.execute("TRUNCATE TABLE movies")

        # 插入数据
        sql = "INSERT INTO movies (name, star, releasetime, score) VALUES (%s, %s, %s, %s)"
        for movie in movies:
            cursor.execute(sql, (movie["name"], movie["star"], movie["releasetime"], movie["score"]))

        # 提交事务
        db.commit()
        print(f"【MySQL存储】成功！共插入 {len(movies)} 条数据到 maoyan.movies 表")

    except Exception as e:
        print(f"【MySQL存储】失败: {e}")
        if db:
            db.rollback()
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# ======================== PyMongo 存储 ========================

def save_to_mongodb(movies):
    """将电影数据存储到MongoDB数据库"""
    print("\n" + "=" * 50)
    print("【MongoDB存储】开始...")

    try:
        # 建立连接
        conn = pymongo.MongoClient("localhost", 27017, serverSelectionTimeoutMS=5000)

        # 创建库对象
        db = conn["maoyandb"]

        # 创建集合对象
        myset = db["maoyanset"]

        # 清空旧数据（避免重复插入）
        myset.delete_many({})

        # 插入数据
        myset.insert_many(movies)

        print(f"【MongoDB存储】成功！共插入 {len(movies)} 条数据到 maoyandb.maoyanset 集合")

        # 验证：查询并打印第一条数据
        first = myset.find_one()
        print(f"【MongoDB验证】第一条数据: {first}")

        conn.close()

    except Exception as e:
        print(f"【MongoDB存储】失败: {e}")


# ======================== 主程序 ========================

if __name__ == "__main__":
    print("=" * 50)
    print("  猫眼电影数据爬取与存储")
    print("=" * 50)

    # 1. 爬取数据
    print("\n【第一步】爬取猫眼电影榜单数据...\n")
    movies = crawl_maoyan()
    print(f"\n共获取 {len(movies)} 部电影数据")

    # 2. CSV存储
    save_to_csv(movies)

    # 3. MySQL存储
    save_to_mysql(movies)

    # 4. MongoDB存储
    save_to_mongodb(movies)

    print("\n" + "=" * 50)
    print("  所有存储操作完成！")
    print("=" * 50)
