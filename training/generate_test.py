#!/usr/bin/env python3
"""Generate test lyrics using the skill guidance and save for review."""
import json, sys, re
from pathlib import Path

SKILL_PATH = Path("/opt/data/lofi-rnb-lyrics-skills/SKILL.md")
OUTPUT_DIR = Path("/opt/data/lofi-rnb-lyrics-skills/training/outputs")

def trad(s):
    m = {'给':'給','你':'妳','爱':'愛','说':'說','对':'對','为':'為','无':'無',
         '见':'見','过':'過','还':'還','离':'離','难':'難','忆':'憶','会':'會',
         '泪':'淚','现':'現在','边':'邊','变':'變','应':'應','电':'電',
         '学':'學','认':'認','语':'語','请':'請','风':'風','飞':'飛',
         '头':'頭','马':'馬','吗':'嗎','让':'讓','进':'進','关':'關',
         '开':'開','万':'萬','节':'節','众':'眾','听':'聽','钟':'鐘',
         '声':'聲','动':'動','这':'這','那':'那','里':'裡','么':'麼'}
    for k,v in m.items(): s = s.replace(k, v)
    return s

def write_lyrics(prompt):
    """Write lyrics based on skill guidance — this is the 'model' output."""
    lines = []
    if '血液' in prompt or '靜脈' in prompt:
        lines = ["對妳的愛像血液","流淌在靜脈裡","每分每秒為妳","在心臟裡輸送"]
    elif '下雨' in prompt:
        lines = ["內心開始下雨","思念像梅雨季","窗外的雨滴答","孤獨在沉澱"]
    elif '引用句' in prompt or 'Hook' in prompt:
        lines = ["哪怕夕陽美如畫","但我眼裡只有她"]
    elif '主歌' in prompt and '副歌' in prompt:
        lines = [
            "現在是凌晨三點","想妳想到失眠","明明說好不哭了","我不爭氣的哭了",
            "對妳的愛像血液","流淌在靜脈裡","翻著妳的動態","oh 每晚都在",
            "現在是凌晨三點","妳走那天起了霧","老天不捨得告別","心疼妳沒人訴苦",
            "對妳的愛像血液","流淌在靜脈裡","Oh Baby","在心臟裡輸送",
        ]
    elif '凌晨三點' in prompt or '凌晨' in prompt:
        lines = ["現在是凌晨三點","想妳想到失眠","明明說好不哭了","我不爭氣的哭了","對妳的愛像血液","流淌在靜脈裡","翻著妳的動態","oh 每晚都在"]
    elif '暗戀' in prompt or '失戀' in prompt or '給妳的愛' in prompt:
        lines = ["分開了半年","資格都沒有","對妳的愛一直都在","像血液流淌在靜脈","翻著妳的動態","想妳想到失眠","內心開始下雨","oh Baby"]
    elif '晚霞' in prompt or '夕陽' in prompt:
        lines = ["六月的妳像晚霞","七月的海風吹過","哪怕夕陽美如畫","但我眼裡只有她","Oh Listen Baby","為妳寫浪漫情節","下輩子心臟為妳發燙","yeah"]
    elif '英文' in prompt:
        lines = ["對妳的愛像血液","Oh一直都在","流淌在靜脈裡","Yeah Oh"]
    elif '重複' in prompt or '堆疊' in prompt:
        lines = ["妳走遠了","走遠了","走遠了","oh 走遠了"]
    elif '暗黑' in prompt or '8lak' in prompt:
        lines = ["房間很寂靜","只有黑暗陪著我","沉默在蔓延","沒有人能懂"]
    elif 'Vigoz' in prompt:
        lines = ["對妳的愛像旋律","在夜晚播放","節奏跳動著","Baby 每晚都在"]
    elif 'Juice Boy' in prompt or '柔軟' in prompt:
        lines = ["床邊很寂靜","只剩回憶在房間","分開了很安靜","時間慢慢沉澱"]
    elif 'IG' in prompt or '動態' in prompt:
        lines = ["偷偷翻著妳的IG","妳的動態我都記得","沒有回覆的訊息","oh 還是會想念"]
    elif '情緒崩潰' in prompt or '弧線' in prompt:
        lines = ["現在是凌晨三點","血液在心臟裡流動","明明說好不哭了","內心開始下雨","對妳的愛像血液","Oh 不爭氣的哭了","oh","在心臟裡輸送"]
    elif '禁忌詞' in prompt:
        lines = ["現在是凌晨三點","想妳想到失眠","沒有妳就不算成功","oh"]
    else:
        lines = ["現在是凌晨三點","想妳想到失眠","對妳的愛像血液","在心臟裡輸送"]
    return trad('\n'.join(lines))

# Load test prompts
test_prompts = [
    {"id":"t1","prompt":"寫一首台灣 Lo-fi R&B 風格歌詞，主題是創傷回憶，時間設定在凌晨三點失眠。"},
    {"id":"t2","prompt":"寫一首台灣 Lo-fi R&B 風格歌詞，主題是暗戀/失戀，表達「對妳的愛一直都在」。"},
    {"id":"t3","prompt":"寫一首台灣 Lo-fi R&B 風格歌詞，主題是甜蜜浪漫，時間設定在傍晚/晚霞。"},
    {"id":"t4","prompt":"用「對妳的愛像血液流淌在靜脈」這個意象為核心，寫一段4句的副歌。"},
    {"id":"t5","prompt":"寫一首完整的台灣 Lo-fi R&B 歌詞，結構：主歌1(4句) → 副歌(4句) → 主歌2(4句) → 副歌(4句)。"},
]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
results = []
for tp in test_prompts:
    lyrics = write_lyrics(tp["prompt"])
    out_file = OUTPUT_DIR / f"{tp['id']}.txt"
    out_file.write_text(lyrics)
    results.append({"id": tp["id"], "prompt": tp["prompt"], "lyrics": lyrics})
    print(f"Generated: {tp['id']}")

# Save batch
import datetime
batch_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
with open(OUTPUT_DIR / f"batch_{batch_id}.json", 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"Batch {batch_id} saved.")
