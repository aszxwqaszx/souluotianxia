# 🦞 搜罗天下

> 发现生活中的每一份优惠与美好

搜罗天下是一个专注于发现和分享全网优质优惠信息的平台。

## 🎯 网站功能

- 🎁 **优惠折扣** — 汇集全网最新优惠券、折扣信息
- 🤖 **AI工具** — 收录优质AI工具与使用技巧（筹备中）
- 🛠️ **实用工具** — 在线工具大全（筹备中）
- 📥 **资源下载** — 精选软件、模板、素材资源（筹备中）

## 🛠️ 技术栈

- 纯静态网站（HTML + CSS + JavaScript）
- 部署于 GitHub Pages
- 无需后端服务器，完全免费托管

## 📂 目录结构

```
souluotianxia/
├── index.html      # 首页
├── deals.html      # 优惠折扣列表页
├── about.html      # 关于我们
├── styles.css      # 样式文件
├── deals.json      # 优惠数据
└── README.md
```

## 🚀 绑定自定义域名

如需绑定自定义域名，请在仓库 Settings → Pages → Custom domain 中添加你的域名。

## 📝 更新优惠内容

优惠数据存储在 `deals.json` 文件中，格式如下：

```json
{
    "platform": "平台名称",
    "title": "优惠标题",
    "desc": "优惠描述",
    "type": "coupon|discount|free|event",
    "typeText": "标签文字",
    "link": "跳转链接",
    "date": "日期"
}
```

## 📄 开源协议

本项目基于 MIT 协议开源。
