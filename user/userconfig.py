from enum import Enum

# 模式
mode = 'debug'

# 安全
default_key = '128def9a2d7702f6'  # AES加密的默认密钥

# 其他配置
software = (
    'index'  # 默认
    'test'  # 测试使用
    'community'  # 社交软件
    'myday'  # 日程软件
)


class ActivityName(Enum):
    Login = "login"


