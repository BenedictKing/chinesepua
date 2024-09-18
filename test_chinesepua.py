import unittest
from chinesepua import ChinesePua

class TestChinesePua(unittest.TestCase):

    def setUp(self):
        self.plugin = ChinesePua()

    def test_on_handle_context_valid(self):
        # 模拟有效的上下文输入
        e_context = {
            "context": {
                "type": "text",
                "content": "PUA 测试词语",
            },
            "reply": None,
        }
        self.plugin.on_handle_context(e_context)
        self.assertIsNotNone(e_context["reply"])

    def test_on_handle_context_invalid(self):
        # 模拟无效的上下文输入
        e_context = {
            "context": {
                "type": "image",
                "content": "无效内容",
            },
            "reply": None,
        }
        self.plugin.on_handle_context(e_context)
        self.assertIsNone(e_context["reply"])

if __name__ == '__main__':
    unittest.main()
