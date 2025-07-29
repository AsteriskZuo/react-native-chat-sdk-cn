# react-native-chat-sdk-cn

**初始化项目:**

```bash
uv init .
uv venv
uv add ruff
uv sync
```

**运行脚本:**

```bash
# 将英文版本覆盖到中文版本上
sh restore.sh
# 通过该脚本还原部分不需要修改的中文版本，剩余部分通过手动方式修改
uv run smart_merge.py "/Users/asterisk/Codes/rn/react-native-chat-sdk-rn72/src" "/Users/asterisk/Codes/zuoyu/react-native-chat-sdk-cn/test"
```
