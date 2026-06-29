# FLAC 无损音乐下载器

> 网站：https://flac.music.hi.cn  
> 支持从酷我(kuwo)、网易云(wyy)搜索并下载 FLAC 无损 / MP3 音乐文件

## 触发条件

当用户提到以下任意需求时，加载此 skill：
- 下载 FLAC、无损音乐、高品质音乐
- 从 flac.music.hi.cn 下载歌曲
- 批量下载歌曲
- 搜索/下载某首歌的 FLAC 格式

---

## 核心工作流

### 第一步：确认 Cookie 是否有效

Cookie 约 **30天有效期**，过期症状：HTTP 468 错误 或 返回 HTML（Cloudflare挑战页）。

```python
import requests, json

COOKIE = '你的Cookie'  # 见下方Cookie管理

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Origin': 'https://flac.music.hi.cn',
    'Referer': 'https://flac.music.hi.cn/',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': COOKIE,
})
session.get('https://flac.music.hi.cn/', timeout=15)  # 必须先访问主页！

# 验证搜索
resp = session.post('https://flac.music.hi.cn/ajax.php?act=search',
    data={'platform': 'kuwo', 'keyword': '青花瓷', 'page': 1, 'size': 3},
    timeout=15)
data = resp.json()
total = data.get('data', {}).get('total', 0)
print('Cookie有效!' if total > 0 else 'Cookie可能失效')
```

---

### 第二步：搜索歌曲

```
POST https://flac.music.hi.cn/ajax.php?act=search
```

| 参数 | 值 | 说明 |
|------|-----|------|
| platform | `kuwo` 或 `wyy` | 酷我 / 网易云 |
| keyword | 歌曲名 | ⚠️ **必须用歌曲名！** 艺术家名会返回 total=0 |
| page | 从 **1** 开始 | ⚠️ 从1不是0！ |
| size | 30 | 每页数量 |

**响应结构：**
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "list": [
      {
        "id": "394586518",      // ← 用这个作 songid！不是 rid！
        "name": "青花瓷",
        "artist": "周杰伦",
        "minfo": [
          {"level": "ff", "bitrate": "2000", "format": "flac", "size": "57.26Mb"},
          {"level": "p",  "bitrate": "320",  "format": "mp3",  "size": "10.77Mb"}
        ],
        "time": 1774956057,     // ← 签名时间戳，获取URL时需要
        "sign": "b89c206d..."   // ← 签名，获取URL时需要
      }
    ]
  }
}
```

---

### 第三步：获取下载链接

```
POST https://flac.music.hi.cn/ajax.php?act=getUrl
```

| 参数 | 说明 |
|------|------|
| platform | kuwo / wyy |
| songid | 用搜索结果中的 `id` 字段 |
| format | flac 或 mp3 |
| bitrate | 从 minfo 中获取，如 2000 或 320 |
| time | 搜索结果中的 `time` 字段 |
| sign | 搜索结果中的 `sign` 字段 |

**响应：**
```json
{
  "code": 0,
  "data": {
    "url": "https://...实际下载链接..."
  }
}
```

---

## 一键批量下载脚本

> 脚本位于：`~/.workbuddy/skills/flac/scripts/batch_downloader.py`

```bash
# 使用前修改脚本顶部的 COOKIE 和 SONG_LIST
python3 ~/.workbuddy/skills/flac/scripts/batch_downloader.py
```

**修改歌单（仅需改这两项）：**
```python
COOKIE = 'sl-session=...你的Cookie...'

SONG_LIST = [
    ('青花瓷', '周杰伦'),   # (搜索关键词, 艺术家提示)
    ('十年', '陈奕迅'),
    ('小幸运', '田馥甄'),
]
```

---

## Cookie 管理

### 当前 Cookie（2026-03-31 获取，约30天有效）
```
sl-session=VcBpDxd2zGmNLPVtKRc3ag==; sl-challenge-server=cloud; sl_jwt_session=m90hd++6y2lru1q6u72KIg==; sl_jwt_sign=
```

### 更新 Cookie 的方法
1. 浏览器访问 https://flac.music.hi.cn/
2. 按 F12 打开开发者工具 → Network 标签
3. 在网页上随便搜索一首歌
4. 找到 `ajax.php` 请求 → Request Headers → 复制 `Cookie` 值

---

## 常见问题排查

| 现象 | 原因 | 解决方法 |
|------|------|---------|
| HTTP 468 错误 | Cookie 过期 | 按上面步骤更新 Cookie |
| total=0，搜不到歌 | 用了艺术家名搜索 | **改用歌曲名**搜索 |
| code=-4 "No Act" | 参数格式错误 | 用 `act=` 参数，page 从 1 开始 |
| 返回 HTML / Cloudflare挑战 | 未设置 Cookie | 在 Header 中加 Cookie |
| 有搜索结果但获取URL失败 | time/sign 字段缺失 | 确保用搜索返回的原始 time 和 sign |

---

## 环境配置

```bash
# 工作目录
cd /Users/user/WorkBuddy/20260331075819

# 激活虚拟环境
source venv_flac/bin/activate

# 安装依赖（首次）
pip install requests
```

---

## 已验证信息

- ✅ 平台：`kuwo`（酷我）、`wyy`（网易云）均可用
- ✅ 格式：FLAC（无损）、MP3（最高320kbps）
- ✅ 已成功下载：12首歌，总计约290MB（2026-03-31）
- ⚠️ 注意：部分歌曲搜索到的是翻唱版，建议检查艺术家名后再下载

---

## 更新历史

- 2026-03-31：创建 skill，完整验证 API 流程，12首全部下载成功
