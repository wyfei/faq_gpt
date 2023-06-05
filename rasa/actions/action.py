from rasa_sdk import Action,Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted

from typing import Any, Text, Dict, List
import json
# import requests
from datetime import datetime
from dateutil.parser import parse

class ActionGPTAsk(Action):
    def name(self) -> str:
        return "action_gpt_ask"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message = tracker.latest_message["text"]
        result = {"message": message, "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)

    
class ActionGPTSummary(Action):
    def name(self) -> str:
        return "action_gpt_summary"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message = tracker.latest_message["text"]
        result = {"message": message, "type":"summary"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)

    
class ActionGPTChitchat(Action):
    def name(self) -> str:
        return "action_gpt_chitchat"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message["text"]
        result = {"message": message, "type":"chitchat"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
       
    
class ActionGPTDemoQ1(Action):
    def name(self) -> str:
        return "action_gpt_demo_q1"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = {"message": "我视频播放超过500了怎么没有显示？", "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)

class ActionGPTDemoQ2(Action):
    def name(self) -> str:
        return "action_gpt_demo_q2"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = {"message": "我的视频发到B站流量很差，但我这条视频在抖音发布，播放量都是百万的，B站播放只有几千很低啊", "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
        
class ActionGPTDemoQ3(Action):
    def name(self) -> str:
        return "action_gpt_demo_q3"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = {"message": "我的视频流量很差，你们是不是把我限流了", "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
        
class ActionGPTDemoQ4(Action):
    def name(self) -> str:
        return "action_gpt_demo_q4"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = {"message": "我到100万播放了，为什么没有点亮第二关？", "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
     
class ActionGPTDemoQ5(Action):
    def name(self) -> str:
        return "action_gpt_demo_q5"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = {"message": "我完成任务了，怎么没收到钱啊？", "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
           
class ActionGPTDemoQ6(Action):
    def name(self) -> str:
        return "action_gpt_demo_q6"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = {"message": "有什么推荐的活动可以获得流量吗？", "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
        
class ActionGPTDemoQ71(Action):
    def name(self) -> str:
        return "action_gpt_demo_q7_1"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = {"message": "我的视频播放特别低，具体什么原因，还有给一些创作的建议", "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
        
class ActionGPTDemoQ72(Action):
    def name(self) -> str:
        return "action_gpt_demo_q7_2"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = {"message": "视频BV1ko4y137YR概括以及评估其创作风格", "type":"question"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
        
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
        
        result = {"message": f"今天是 {date_str} {week_day_zh}。", "type":"utter"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)
       


class ActionAskTime(Action):
    def name(self):
        return "action_ask_time"

    async def run(self, dispatcher, tracker, domain):
        # 获取当前时间
        now = datetime.now()
        # 将时间格式化为字符串
        time_str = now.strftime("%H:%M")
        # 将时间信息发送给用户
        result = {"message": f"现在是 {time_str}。", "type":"utter"}
        dump_result = json.dumps(result, ensure_ascii=False)
        print(dump_result)
        dispatcher.utter_message(dump_result)


class ActionRestarted(Action):  
    def name(self):         
        return 'action_restarted'   
    def run(self, dispatcher, tracker, domain): 
        return[Restarted()] 