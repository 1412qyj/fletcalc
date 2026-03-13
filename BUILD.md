# FletCalc - Python 计算器 App

## 项目结构

```
calculator/
├── src/
│   ├── main.py              # 主程序
│   └── calculator_logic.py  # 计算逻辑
├── requirements.txt          # 依赖
├── BUILD.md                  # 本地打包说明
└── .github/workflows/
    └── build.yml             # CI 自动构建 ✅ 推荐
```

## ⚠️ 本地打包问题

当前服务器网络较慢，Flutter SDK 下载困难。建议使用 **GitHub Actions 云编译**。

---

## 🚀 推荐：GitHub Actions 云打包

### 步骤 1: 推送代码到 GitHub

```bash
# 在本地终端执行 (不是在这里)
cd /path/to/calculator
git init
git add .
git commit -m "Init calculator app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fletcalc.git
git push -u origin main
```

### 步骤 2: 触发构建

1. 打开 `https://github.com/YOUR_USERNAME/fletcalc/actions`
2. 点击 `Build APK` workflow
3. 点击 `Run workflow` → `Run workflow`

### 步骤 3: 下载 APK

构建完成后，在 Artifacts 中下载 `fletcalc-apk`

---

## 💻 本地打包 (需要好网络)

需要先安装 Flutter SDK 和 Android SDK:

```bash
# 1. 安装依赖
~/miniconda3/bin/pip install flet

# 2. 打包 APK
cd /home/copaw/.openclaw/workspace/docs/calculator
yes | ~/miniconda3/bin/flet build apk --project fletcalc

# 输出: build/flutter-apk/app-release.apk
```

---

## 功能清单

- ✅ 加减乘除基本运算
- ✅ 小数支持
- ✅ 百分比计算
- ✅ 正负号切换
- ✅ 清除/退格功能
- ✅ 计算历史记录
- ✅ 浅色/深色主题切换
