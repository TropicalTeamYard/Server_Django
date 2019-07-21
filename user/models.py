from datetime import datetime, timezone

from django.db import models

from user import utils


class User(models.Model):
    user_type_choices = (
        (0, 'normal'),
        (1, 'admin'),
        (2, 'superadmin'),
    )

    name = models.CharField(max_length=64, unique=True)  # 用户名，只能包含数字，大小写英文，下划线。（长度限制为2~32个字符）
    uid = models.CharField(max_length=64)  # 唯一标识名，由系统自己生成。（uid生成方式：时间戳+hash+10-99的随机数)）
    password = models.CharField(max_length=128)  # 密码，md5
    nickname = models.CharField(max_length=64)  # 昵称，1-32个任意字符
    email = models.CharField(null=True, default='', max_length=64)  # 邮箱
    create_time = models.DateTimeField()  # 创建时间
    user_type = models.PositiveSmallIntegerField(default=0, choices=user_type_choices)  # 用户类型
    exp = models.PositiveIntegerField(default=0)  # 用户经验
    tags = models.TextField(null=True, default='')  # 用户认证标签
    extras = models.TextField(null=True, default='')  # 无关紧要的额外的信息，以键值对形式存储，键为str，值为jsonobject/str

    def __str__(self):
        return f'{self.name} (n:{self.nickname},u:{self.uid})'

    @staticmethod
    def created(name: str):
        query_set = User.objects.filter(name=name)
        if len(query_set) > 0:
            return True
        else:
            return False

    def to_json(self):
        return {
            'name': self.name,
            'uid': self.uid,
            'nickname': self.nickname,
            'email': self.email,
            'create_time': utils.format_time(self.create_time),
            'user_type': User.user_type_choices[self.user_type][1],
            'exp': self.exp,
            'tags': self.tags,
            'extras': self.extras
        }


class UserActivity(models.Model):
    device_type_choices = (
        (0, 'mobile'),
        (1, 'pc'),
        (2, 'web'),
        (3, 'pad'),
    )

    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)  # 外键，对应持有该活动信息用户。
    software = models.CharField(max_length=32)  # 对应的软件名称，默认支持'test'和'index'，其他支持需要询问平台配置。
    access_ip = models.CharField(max_length=32)  # 最后活动的ip地址
    # access_uid = models.CharField(max_length=64)  # -无效- 第一次登录时生成的uid，用于自动登录时的检测所用。
    device_type = models.PositiveSmallIntegerField(default=0, choices=device_type_choices)
    # 设备平台名称，默认支持'mobile','pc','web','pad'四个平台的设备。
    access_time = models.DateTimeField()  # 最后活动的时间

    def __str__(self):
        return f'{self.user.name}-{self.software}-{UserActivity._get_device_type_des(self.device_type)}'

    @staticmethod
    def find_and_update(user: User, software: str, device_type: str, access_ip):
        query_set = UserActivity.objects.filter(
            user=user,
            software=software,
            device_type=UserActivity._get_device_type_value(device_type))
        if len(query_set) > 0 and (datetime.now().astimezone() - query_set[0].access_time).days < 30:
            first = query_set[0]
        else:
            return False
        first.access_ip = access_ip
        first.access_time = datetime.now()
        first.save()
        return True

    @staticmethod
    def update(user: User, software: str, device_type: str, access_ip: str):
        query_set = UserActivity.objects.filter(
            user=user,
            software=software,
            device_type=UserActivity._get_device_type_value(device_type))
        if len(query_set) > 0:
            first = query_set[0]
        else:
            first = UserActivity(
                user=user,
                software=software,
                device_type=UserActivity._get_device_type_value(device_type))
        first.access_ip = access_ip
        first.access_time = datetime.now()
        first.save()

    @staticmethod
    def _get_device_type_des(value: int):
        for item in UserActivity.device_type_choices:
            if item[0] == value:
                return item[1]
        raise KeyError()

    @staticmethod
    def _get_device_type_value(des: str):
        for item in UserActivity.device_type_choices:
            if item[1] == des:
                return item[0]
        raise KeyError()


class UserBinding(models.Model):
    state_choices = (
        (0, 'success'),
        (1, 'fail'),
    )

    user = models.ForeignKey(User, related_name='bindings', on_delete=models.CASCADE)  # 外键，对应持有该绑定信息的用户
    name = models.CharField(max_length=128)  # 绑定平台的名称，绑定的平台需要访问配置信息。
    uid = models.CharField(max_length=128)  # 唯一标识符，注意，此字段是唯一绑定的关键信息
    password = models.CharField(max_length=128)  # 绑定的密码
    state = models.PositiveSmallIntegerField(default=0, choices=state_choices)  # 绑定状态，'success','fail'.


class UserLog(models.Model):
    user = models.ForeignKey(User, related_name='logs', on_delete=models.CASCADE)  # 外键，对应持有该日志的用户
    action_type = models.CharField(max_length=64)  # 用户日志类别，所有兼容的类别都会在设置内写出
    time = models.DateTimeField()  # 打log的时间
    content = models.TextField()  # 用户日志内容

    def __str__(self):
        return f'{self.user.name}-{self.action_type}'

    @staticmethod
    def write(user: User, action_type: str, content: str):
        log = UserLog(user=user, action_type=action_type, content=content, time=datetime.now())
        log.save()

