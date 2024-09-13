import io
import random
import re
import time
import threading

import plugins
import requests
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from common.tmp_dir import TmpDir
from playwright.sync_api import sync_playwright
from plugins import *

from .prompts import chinese_teacher, chinese_teacher_claude


def read_file(path):
    with open(path, mode="r", encoding="utf-8") as f:
        return f.read()


@plugins.register(
    name="chinesepua",
    desc="A plugin that generates satirical explanation cards for Chinese phrases",
    version="0.1",
    author="BenedictKing",
    desire_priority=115,
)
class ChinesePua(Plugin):
    def __init__(self):
        super().__init__()

        gconf = super().load_config()
        if not gconf:
            curdir = os.path.dirname(__file__)
            tm_path = os.path.join(curdir, "config.json.template")
            if os.path.exists(self.json_path):
                # 读取config.json配置文件
                gconf = json.loads(read_file(self.json_path))
            elif os.path.exists(tm_path):
                # 读取config.json.template配置文件
                gconf = json.loads(read_file(tm_path))

        try:
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            self.api_key = gconf.get("api_key")
            self.api_base = gconf.get("api_base")
            self.api_model = gconf.get("api_model")
            logger.debug("[chinesepua] inited")
        except Exception as e:
            logger.error(f"[chinesepua] init error: {e}")

    def on_handle_context(self, e_context: EventContext):
        context = e_context["context"]
        logger.debug(f"[chinesepua] 获取到用户输入：{context.content}")
        # 过滤不需要处理的内容类型
        context = e_context["context"]
        if context.type not in [ContextType.TEXT]:
            return
        if context.content.startswith(("PUA", "pua", "吐槽", "槽点")):
            match = re.search(r"(PUA|pua|吐槽|槽点)(.+)", context.content)
            if match:
                keyword = match.group(2).strip()  # 获取搜索关键词
                logger.debug(f"[chinesepua] 吐槽: {keyword}")
                if len(keyword) > 8:
                    _set_reply_text("输入太长了，简短一些吧", e_context, level=ReplyType.TEXT)
                    return
                try:
                    response = requests.post(
                        f"{self.api_base}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        },
                        json={
                            "model": self.api_model,
                            "messages": [
                                {"role": "system", "content": chinese_teacher},
                                {"role": "assistant", "content": "说吧, 他们又用哪个词来忽悠你了?"},
                                {"role": "user", "content": keyword},
                            ],
                        },
                    )
                    response.raise_for_status()
                    text = response.json()["choices"][0]["message"]["content"]
                    logger.debug(f"[chinesepua] 回复: {text}")
                    # 提取SVG内容
                    html_match = re.search(r"```html(.*?)```", text, re.DOTALL)
                    if html_match:
                        html_content = html_match.group(1).strip()
                    else:
                        html_content = ""

                    reply_text = re.split("```", text)[-1].strip()
                    if not reply_text:
                        reply_text = re.split("```", text)[0].strip()

                    if html_content:
                        # 创建新线程来处理HTML渲染
                        thread = threading.Thread(target=self.render_html_to_image, args=(html_content, e_context))
                        thread.start()

                        reply_text+="\n\n卡片正在生成中, 稍后奉上"
                    
                    _set_reply_text(reply_text, e_context, level=ReplyType.TEXT)

                except Exception as e:
                    logger.error(f"[chinesepua] 错误: {e}")
                    _set_reply_text("生成卡片失败，请稍后再试。。。", e_context, level=ReplyType.TEXT)


    def render_html_to_image(self, html_content, e_context):
        try:
            tmp_path = (
                TmpDir().path() + f"chinesepua_{int(time.time())}_{random.randint(1000, 9999)}.png"
            )

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(
                    viewport={"width": 1080, "height": 1280},
                    device_scale_factor=2,
                )
                page.set_content(html_content)

                # 等待.card元素加载完成
                card_element = page.wait_for_selector(".card")

                if card_element:
                    card_element.screenshot(path=tmp_path)
                else:
                    # 如果没有找到.card元素，则截取整个页面
                    page.screenshot(path=tmp_path)

                browser.close()

            # 读取生成的图片文件
            with open(tmp_path, "rb") as image_file:
                img_byte_arr = io.BytesIO(image_file.read())

            _send_img(e_context, img_byte_arr)

        except Exception as e:
            logger.error(f"HTML渲染为图片失败: {e}")
            # 如果转换失败，可以在这里发送一条错误消息
            _set_reply_text("图片生成失败，请稍后再试。", e_context, level=ReplyType.ERROR)


def _set_reply_text(content: str, e_context: EventContext, level: ReplyType = ReplyType.ERROR):
    reply = Reply(level, content)
    e_context["reply"] = reply
    e_context.action = EventAction.BREAK_PASS


def _send_img(e_context: EventContext, content: any):
    reply = Reply(ReplyType.IMAGE, content)
    channel = e_context["channel"]
    channel.send(reply, e_context["context"])
