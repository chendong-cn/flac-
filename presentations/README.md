AI 客服 PPT 生成器

Files added:
- presentations/AI-customer-service-deck.md  -> 可直接粘贴到幻灯片或作为生成源
- presentations/generate_pptx.py            -> 使用 python-pptx 自动生成 PPTX（需安装 python-pptx）

使用说明：
1. 克隆仓库
2. 安装依赖：pip install python-pptx
3. 运行：python presentations/generate_pptx.py presentations/AI-customer-service-deck.md presentations/AI-customer-service-deck.pptx
4. 打开生成的 presentations/AI-customer-service-deck.pptx 并调整视觉样式与图表

注意：生成脚本会把 Markdown 每个“---”分隔的段落转成一页幻灯片，段落首行为标题，后续每行将作为要点。
