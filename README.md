# ChinesePUA 插件

ChinesePUA 是一个为 chatgpt-on-wechat 设计的插件,灵感来源于李继刚和云中江树的创意。它能够为中文词语提供幽默而富有创意的新解释,并生成一张方便分享的文字卡片。此外，它还可以生成精美的社交名片。

特别感谢云中江树大神收录 [飞书文档: 玩转"汉语新解"？我用通义AI直出爆款文字卡片](https://langgptai.feishu.cn/wiki/WKaEwX5LMirfJlkenf6cKGDGnJg)

## 功能

- 输入 "吐槽 [词语]" 或者 "pua [词语]" 即可获得该词语的幽默新解释。默认生成云中江树版本的卡片，如果输入中包含 "claude"，则使用Claude模型生成李继刚版本的卡片。
- 采用李继刚和云中江树两位大神无私分享的prompt [飞书文档: 精美卡片-汉语新解（玩梗高手）](https://tffyvtlai4.feishu.cn/wiki/HvkuwNcKxiqvLKk5o9rcRjfjn1u)
- 输入 "设计 [个人信息]" 或 "名片 [个人信息]" 生成精美的社交名片 参照云中江树大神的 [飞书文档: 国内 AI 也能直出高颜值名片](https://langgptai.feishu.cn/wiki/WG7OwFMcOi1GQ1kHIsjctEUnnC1)
- 输入 "解字 [汉字]"、"字典 [汉字]" 或 "字源 [汉字]" 获取汉字的详细解释和字源信息 参照李继刚大神的 [即刻动态: 说文解字0.2](https://m.okjike.com/originalPosts/66e832842cacf9416a2500bf?s=eyJ1IjoiNjRiNWY5YzliOGM3NWExYmI4Nzk4OGQ0In0%3D)
- 增加了一些Claude模型专用的提示词 参照 [李继刚神级 Claude prompt合集](https://mp.weixin.qq.com/s/U7rl2LGN3MQbnfiMlzlwUg)

## 使用方法

1. 在聊天中输入 "吐槽 [词语]"，例如 "吐槽 加班"
2. 插件会返回该词语的幽默新解释和文字卡片
3. 输入 "设计 [姓名] [职位] [公司] [联系方式]" 或 "名片 [姓名] [职位] [公司] [联系方式]" 生成社交名片
4. 输入 "解字 [汉字]"，例如 "解字 敏" 获取汉字的详细解释和字源信息
5. 输入 "翻译 [内容]" 进行翻译
6. 输入 "论证 [内容]" 或 "分析 [内容]" 进行论证分析，例如 `分析 抖音对年轻人的影响利大于弊，因为它提供了一个创意表达的平台，促进了信息传播`
7. 输入 "思考 [内容]" 或 "撕考 [内容]" 调用撕考者
8. 输入 "沉思 [内容]" 或 "琢磨 [内容]" 调用沉思者
9. 输入 "概念 [内容]" 或 "概念解释 [内容]" 进行概念解释
10. 输入 "哲学家 [内容]" 或 "哲学 [内容]" 进行哲学思考
11. 输入 "互联网 [内容]" 或 "web2 [内容]" 调用互联网黑话专家
12. 输入 "知识 [内容]" 或 "知识卡 [内容]" 生成知识卡片
13. 输入 "单词 [内容]" 或 "单词卡 [内容]" 生成单词卡片

## 样例

以下是使用本插件生成的文字卡片样例：

![吐槽演员样例](images/example1.jpg)

社交名片样例：

输入 `设计 张三 法外狂徒 法学教授 普及法律知识 头像：https://s1-imfile.feishucdn.com/static-resource/v1/v2_493bb53e-6bb9-4910-a48c-da17a3d49aag~ 个人主页：https://langgptai.feishu.cn/wiki/WG7OwFMcOi1GQ1kHIsjctEUnnC1`

![社交名片样例](images/example2.jpg)

说文解字样例:

输入 `解字 敏`

![说文解字样例](images/example3.png)

## 安装

1. 将插件文件夹复制到 `plugins` 目录下
2. 安装playwright `pip install playwright`
3. 安装chromium `playwright install chromium`
4. 配置相关的key和base
4. 在 `config.json` 中启用插件
5. 重启 chatgpt-on-wechat

## 配置

可以在 `config.json` 中进行以下配置:

- `api_key`: API密钥
- `api_base`: API基础URL, 例如 `https://api.openai.com/v1`
- `api_model`: 使用的API模型, 默认 `gpt-4o-mini`
- `claude_key`: Claude API密钥（可选）
- `claude_base`: Claude API基础URL（可选）
- `claude_model`: 使用的Claude模型, 默认 `claude-3-5-sonnet-20240620`
- `with_text`: 是否在卡片中显示解释文本, 默认 `false`
- `max_tokens`: 生成的文本最大长度, 如果无法生成图片，可以适当增加这个值，例如4096

## 注意事项

- 本插件仅供娱乐使用,生成的内容可能具有讽刺或夸张性质
- 请遵守相关法律法规,不要生成违法或不当内容
- 本插件依赖于 `chatgpt-on-wechat` 项目，请确保你已经安装了该项目

## 贡献

欢迎提交 Issue 或 Pull Request 来帮助改进此插件!

## 许可证

MIT License

## 更新日志

### 0.5版本
- 新增更多Claude模型可用的提示词

### 0.4版本
- 新增"解字"、"字典"和"字源"触发词功能
- 增加了对Claude API的支持，某些功能可以选择使用Claude模型

### 0.3版本
- 新增"设计"和"名片"触发词功能
- 支持生成精美的社交名片，包含姓名、职位、公司和联系方式等个人信息
- 优化图片生成算法，提高名片设计的美观度和专业性
