from bs4 import BeautifulSoup
import urllib.request
import webbrowser
import datetime
import time

name_list = ["牛巻りこ",
             "花京院ちえり",
             "神楽すず",
             "カルロピノ",
             "木曽あずき",
             "北上双葉",
             "金剛いろは",
             "猫乃木もち",
             "もこ田めめめ",
             "八重沢なとり",
             "ヤマトイオリ",
             "夜桜たま"]

youtube_dict = {"牛巻りこ": "https://www.youtube.com/channel/UCKUcnaLsG2DeQqza8zRXHiA/live",
                "花京院ちえり": "https://www.youtube.com/channel/UCP9ZgeIJ3Ri9En69R0kJc9Q/live",
                "神楽すず": "https://www.youtube.com/channel/UCUZ5AlC3rTlM-rA2cj5RP6w/live",
                "カルロピノ": "https://www.youtube.com/channel/UCMzxQ58QL4NNbWghGymtHvw/live",
                "木曽あずき": "https://www.youtube.com/channel/UCmM5LprTu6-mSlIiRNkiXYg/live",
                "北上双葉": "https://www.youtube.com/channel/UC5nfcGkOAm3JwfPvJvzplHg/live",
                "金剛いろは": "https://www.youtube.com/channel/UCiGcHHHT3kBB1IGOrv7f3qQ/live",
                "猫乃木もち": "https://www.youtube.com/channel/UC02LBsjt_Ehe7k0CuiNC6RQ/live",
                "もこ田めめめ": "https://www.youtube.com/channel/UCz6Gi81kE6p5cdW1rT0ixqw/live",
                "八重沢なとり": "https://www.youtube.com/channel/UC1519-d1jzGiL1MPTxEdtSA/live",
                "ヤマトイオリ": "https://www.youtube.com/channel/UCyb-cllCkMREr9de-hoiDrg/live",
                "夜桜たま": "https://www.youtube.com/channel/UCOefINa2_BmpuX4BbHjdk9A/live"}

hash_dict = {"牛巻りこ": 'hashtag/%E7%89%9B%E5%B7%BB%E3%82%8A%E3%81%93?src=hash',
             "花京院ちえり": 'hashtag/%E8%8A%B1%E4%BA%AC%E9%99%A2%E3%81%A1%E3%81%88%E3%82%8A?src=hash',
             "神楽すず": 'hashtag/%E7%A5%9E%E6%A5%BD%E3%81%99%E3%81%9A?src=hash',
             "カルロピノ": 'hashtag/%E3%82%AB%E3%83%AB%E3%83%AD%E3%83%94%E3%83%8E?src=hash',
             "木曽あずき": 'hashtag/%E6%9C%A8%E6%9B%BD%E3%81%82%E3%81%9A%E3%81%8D?src=hash',
             "北上双葉": 'hashtag/%E5%8C%97%E4%B8%8A%E5%8F%8C%E8%91%89?src=hash',
             "金剛いろは": 'hashtag/%E9%87%91%E5%89%9B%E3%81%84%E3%82%8D%E3%81%AF?src=hash',
             "猫乃木もち": 'hashtag/%E7%8C%AB%E4%B9%83%E6%9C%A8%E3%82%82%E3%81%A1?src=hash',
             "もこ田めめめ": 'hashtag/%E3%82%82%E3%81%93%E7%94%B0%E3%82%81%E3%82%81%E3%82%81?src=hash',
             "八重沢なとり": 'hashtag/%E5%85%AB%E9%87%8D%E6%B2%A2%E3%81%AA%E3%81%A8%E3%82%8A?src=hash',
             "ヤマトイオリ": 'hashtag/%E3%83%A4%E3%83%9E%E3%83%88%E3%82%A4%E3%82%AA%E3%83%AA?src=hash',
             "夜桜たま": 'hashtag/%E5%A4%9C%E6%A1%9C%E3%81%9F%E3%81%BE?src=hash'}
yotei_dict = {}

###################################################
# スクレイピング処理
###################################################
# ベースURLからデータを取得
url_data = urllib.request.urlopen("https://twitter.com/dotLIVEyoutuber")

# HTMLデータを取得
html = url_data.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
div = soup.find_all("div", class_="js-tweet-text-container")

# 生放送スケジュールの最新ツイートを取得
str1 = ""
for i in range(100):
    div2 = str(div[i].find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"))
    if div2.find("生放送スケジュール") != -1:
        month = div2[div2.find("月") - 2:div2.find("月")]
        day = div2[div2.find("日") - 2:div2.find("日")]
        if month[0] == " ":
            month = month[1]
        if day[0] == "月":
            day = day[1]

        now = datetime.datetime.now()
        if str(now.month) == month and str(now.day) == day:  # 配信予定日と今日の日付を合わせる
            str1 = div2
            break

# ツイートから配信者と配信時間をyotei_dictに取得
# ~：<a class="twitter-hashtag pretty-link js-nav" data-query-source="hashtag_click" dir="ltr" href="/hashtag/%E5%A4%9C%E6%A1%9C%E3%81%9F%E3%81%BE?src=hash"><s>#</s><b>
# 上の文字列を　前半部　ハッシュ部　後半部　の三つに分ける

# ~：<a class="twitter-hashtag pretty-link js-nav" data-query-source="hashtag_click" dir="ltr" href="/
# 前半部 piece1の文字数は99文字
piece1 = len('~：<a class="twitter-hashtag pretty-link js-nav" data-query-source="hashtag_click" dir="ltr" href="/')

# "><s>#</s><b>
# 後半部　piece2の文字数は13
piece2 = len('"><s>#</s><b>')

# piece1 + hash + piece2　だから　piece1 + piece2の長さを求める
mix_len = piece1 + piece2

for i in name_list:
    hash_len = len(hash_dict[i])
    finder = str1.find(i)
    if finder != -1:
        yotei_dict[str(str1[finder - hash_len - mix_len - 5:finder - hash_len - mix_len])] = i
yotei_dict = sorted(yotei_dict.items())

#########################################################
# 日付処理
#########################################################
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

print("今日の配信")
for i in yotei_dict:
    print(i)
print("\n")

for i in range(len(yotei_dict)):
    yoyaku_time = str(year) + "-" + str(month) + "-" + str(day) + " " + yotei_dict[i][0]
    yoyaku_time = datetime.datetime.strptime(yoyaku_time, "%Y-%m-%d %H:%M")
    delta = yoyaku_time - now

    if str(delta).find("-") == -1:
        print("配信者：" + str(yotei_dict[i][1]))
        print("配信時刻　" + str(yoyaku_time))
        print("現在時刻　" + str(now))
        print("あと" + str(delta) + "\n")
        # 5分前に開きたいから-300
        time.sleep(delta.total_seconds())
        # time.sleep(10)
        webbrowser.open(youtube_dict[yotei_dict[i][1]])
    else:
        print("配信中または配信済み：" + str(yotei_dict[i][1] + "\n"))
        webbrowser.open(youtube_dict[yotei_dict[i][1]])

print("本日の配信は以上です")

wait = input("ENTERで終了")
# exeファイル化は　pyinstaller IdolClubWatcher.py --onefile　
