from rasa_sdk import Action,Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
# import json
# import requests
from datetime import datetime
from dateutil.parser import parse

class ActionGPTFallback(Action):
    def name(self) -> str:
        return "action_gpt_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        history = []
        user_messages = []
        bot_messages = []
        
        # Separate user messages and bot messages
        for event in tracker.events:
            if event.get("event") == "user":
                user_messages.append(event.get("text"))
            elif event.get("event") == "bot":
                bot_messages.append(event.get("text"))

        # Combine user and bot messages
        for user, bot in zip(user_messages, bot_messages):
            history.append([user, bot])

        print("*******************************")
        print(history)
        print("*******************************")
        
        # url = "http://127.0.0.1:8000"
        # req = json.dumps({
        #     "prompt": tracker.latest_message.get("text"),
        #     "history": history})
        # headers = {'content-type': 'application/json'}
        # r = requests.post(url, headers=headers, data=req)
        # a = json.loads(r.text).get('response')
        # history = json.loads(r.text).get('history')

        dispatcher.utter_message("服务端通过intent判断action, 不执行rasa端具体的action")

        return []
    
class ActionAskDate(Action):
    def name(self):
        return "action_ask_date"

    async def run(self, dispatcher, tracker, domain):
        # 获取当前日期
        today = datetime.now().date()
        # 获取星期几的信息
        week_day = today.strftime("%A")
        # 将星期几的英文名称转换为中文
        week_day_zh = {
            "Monday": "星期一",
            "Tuesday": "星期二",
            "Wednesday": "星期三",
            "Thursday": "星期四",
            "Friday": "星期五",
            "Saturday": "星期六",
            "Sunday": "星期日",
        }.get(week_day, "未知")
        # 将日期格式化为字符串
        date_str = today.strftime("%Y年%m月%d日")
        # 将日期和星期信息发送给用户
        dispatcher.utter_message(text=f"今天是 {date_str} {week_day_zh}。")


class ActionAskTime(Action):
    def name(self):
        return "action_ask_time"

    async def run(self, dispatcher, tracker, domain):
        # 获取当前时间
        now = datetime.now()
        # 将时间格式化为字符串
        time_str = now.strftime("%H:%M")
        # 将时间信息发送给用户
        dispatcher.utter_message(text=f"现在是 {time_str}。")

def parse_datetime(datetime_str):
    try:
        datetime_obj = parse(datetime_str, fuzzy=True)
        if "周" in datetime_str:  # 处理相对日期，如 "周五"
            today = datetime.now().date()
            weekday_diff = (datetime_obj.weekday() - today.weekday()) % 7
            datetime_obj = today + relativedelta(days=weekday_diff)
        return datetime_obj
    except ValueError:
        print("无法解析日期和时间")