#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: agent_example
@File    : model_provider.py
@Author  : Liuyz
@Date    : 2024/6/28 17:12
@Function: 

@Modify History:
         
@Copyright：Copyright(c) 2024-2026. All Rights Reserved
=================================================="""
import os
import requests
import dashscope
import json
from prompt import user_prompt
from dashscope.api_entities.dashscope_response import Message


class ModelProvider(object):
    def __init__(self):
        self.api_key = os.environ.get('DASH_SCOPE_API_KEY')
        self.model_name = os.environ.get('MODEL_NAME')
        self._client = dashscope.Generation()
        self.max_retry_time = 3

    def chat(self, prompt, chat_history):
        cur_retry_time = 0
        while cur_retry_time < self.max_retry_time:
            cur_retry_time += 1
            try:
                # messages = [
                #     Message(role="system", content=prompt)
                # ]
                # for his in chat_history:
                #     messages.append(Message(role="user", content=his[0]))
                #     messages.append(Message(role="system", content=his[1]))
                # # 最后1条信息是用户的输入
                # messages.append(Message(role="user", content=user_prompt))
                # response = self._client.call(
                #     model=self.model_name,
                #     api_key=self.api_key,
                #     messages=messages
                # )
                a = ''
                b = ''
                for his in chat_history:
                    a = his[0]
                    b = his[1]

                url = 'http://localhost:11434/v1/chat/completions'

                # 构造请求数据
                payload = {
                    "model": self.model_name,
                    "messages": [
                        {
                            "role": "system",
                            "content": prompt
                        },
                        {
                            "role": "user",
                            "content": a
                        },
                        {
                            "role": "system",
                            "content": b
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    "stream": False
                }

                # 发送POST请求
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.post(url, headers=headers, data=json.dumps(payload))

                # 打印响应的文本内容
                print(response.text)

                # print("response:{}".format(response))
                tmp = json.loads(response.text).get('choices')[0].get('message').get('content')
                content = json.loads(tmp)
                return content
            except Exception as e:
                print("call llm exception:{}".format(e))
        return {}
