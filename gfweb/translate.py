#!/usr/bin/python
# -*- coding:utf-8 -*-
import hashlib
import random
import time

import requests
import json


def translate(text):
    return _baidu_translate(text)


# 基础版QPS=1
def _baidu_translate(text):
    APP_ID = '20200427000431788'
    secret = 'OcrjDOB59NlYkHipeKfL'
    salt = random.Random()
    src_str = '%s%s%s%s' % (APP_ID, text, salt, secret)
    sign = hashlib.md5(src_str.encode(encoding="UTF-8")).hexdigest()
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    data = {
        "q": text,
        "from": "auto",
        "to": 'zh',
        "appid": APP_ID,
        "salt": salt,
        "sign": sign,
    }
    res = requests.post(url=url, data=data, headers=headers)
    json_data = json.loads(res.text, encoding="UTF-8")
    if "error_code" not in json_data:
        result = ""
        # print(list(json_data.values())[0])
        for r in json_data["trans_result"]:
            result += r["dst"]
            # print(r["dst"])
        return result
    elif json_data["error_code"] == "54003":
        # qps=1 error
        time.sleep(1)
        return _baidu_translate(text)


def main():
    text_jp = "「ゼルダ無双」（Wii U）、「ゼルダ無双 ハイラルオールスターズ」(ニンテンドー3DS)、\nそしてすべての追加コンテンツを収録した完全版がNintendo Switchで登場。\nリンクやゼルダ、ガノンドロフなど「ゼルダの伝説」シリーズお馴染みのキャラクターが登場し、\nハイラル大陸を舞台に一騎当千の爽快アクションがお楽しみいただけます。\n\nまた、Nintendo Switch向けに完全チューニング。\nフルHDで展開する迫力あるバトルやマイフェアリーの3D化などグラフィックも大きく進化。\nNintendo Switchならではのおすそわけプレイなど新たな魅力も加わり、\n「ゼルダ無双」をプレイしていない方だけでなく、シリーズ経験者もあらためて楽しんでいただける作品です"
    text_en = "Cut down enemy hordes as Legend of Zelda™ characters—in full 1080p TV mode—or in two-player on one system! Link and Zelda can battle in costumes from the Legend of Zelda: Breath of the Wild game, while Tetra and King Daphnes appear in scenes based on the Legend of Zelda™: The Wind Waker game. Find and care for fairies who will aid you in battle! All features and downloadable content from past versions of the game, including My Fairy mode and elements from The Legend of Zelda: The Wind Waker, can now be enjoyed in crisp HD on the Nintendo Switch™ system. This time, you won’t face the dark sorceress, Cia, alone. Command legendary heroes and villains in battle to achieve objectives as you unleash special attacks. Advance the story to unlock characters, each with their own moves and weapon types. Collect rupees and other items to upgrade weapons and craft badges, which bolster your warriors’ abilities. The fate of Hyrule rests in your hands!"
    result1 = translate(text_jp)
    result2 = translate(text_en)

    print(result1, result2)


if __name__ == "__main__":
    main()
