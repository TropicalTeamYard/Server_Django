from django.shortcuts import render
import time
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from django.utils import timezone, timesince
from . import models, utils, userconfig

response_ae = JsonResponse(
    {'msg': 'arguments mismatch.',
     'shortcut': 'ae'},
    status=400)


# Create your views here.
def index(request):
    return HttpResponse('hello world!')


def check_name(request: HttpRequest):
    """
    检查用户名是否已被注册
    :param request:
    :return:
    """

    try:
        if request.method == 'GET':
            name = request.GET['name']
        else:
            return Http404()
        m_user = models.User
        # :step 1 检查数据是否合法
        if not utils.check_name(name):
            return JsonResponse(
                {'msg': 'the format of name is invalid.',
                 'shortcut': 'fe'},
                status=400
            )
        else:
            if m_user.created(name):
                return JsonResponse(
                    {'msg': f'the user [{name}] has been registered.',
                     'shortcut': 'ur'}
                )
            else:
                return JsonResponse(
                    {'msg': f'the user [{name}] has not been registered.',
                     'shortcut': 'ok'}
                )

    except KeyError:
        return response_ae


def create(request: HttpRequest):
    """
    创建一个用户，使用(name,nickname,password)注册的方式.
    :param request:
    :return:
    """
    try:
        # region 获取字段值name, nickname, password, email
        if request.method == 'GET':
            if userconfig.mode == 'debug':
                name = request.GET['name']
                nickname = request.GET['nickname']
                password = request.GET['password']
                email = request.GET['email']
            else:
                return Http404()
        elif request.method == 'POST':
            name = request.POST['name']
            nickname = request.POST['nickname']
            password = request.POST['password']
            email = request.POST['email']
        else:
            return Http404()
        # endregion
        # region 检查输入并返回值
        m_user = models.User
        msgs = []
        # :step 1 检查数据是否合法
        if not utils.check_name(name):
            msgs.append('arg(name) is invalid')
        if not utils.check_nickname(nickname):
            msgs.append('arg(nickname) is invalid')
        if not utils.check_md5(password):
            msgs.append('arg(password) is invalid')
        if not utils.check_email(email):
            msgs.append('arg(email) is invalid')

        if len(msgs) == 0:
            # :step 2 检查用户名是否有重复
            if m_user.created(name):
                return JsonResponse(
                    {'msg': f'the user [{name}] has been registered.',
                     'shortcut': 'ur'}
                )
            else:
                # :step 3 添加用户并返回相应的数据
                user = models.User(
                    name=name,
                    uid=utils.make_uid(name, time.time()),
                    password=password,
                    nickname=nickname,
                    email=email,
                    create_time=timezone.now(),
                )
                user.save()
                return JsonResponse(
                    {'msg': 'ok, you have create a user, let\'s fun',
                     'shortcut': 'ok',
                     'data': user.to_json()}
                )
        else:
            # 输入参数格式不正确
            return JsonResponse(
                {'msg': 'arguments format error:{0}'.format(';'.join(msgs)),
                 'shortcut': 'fe'},
                status=400
            )

        # endregion
    except KeyError:
        # 输入参数错误
        return response_ae


def login(request: HttpRequest):
    """
    登录用户，并返回必要的用户信息和token
    登录需要: name, password, software, device_type
    :param request:
    :return:
    """
    try:
        # region 获取字段值name, password, software, device_type
        if request.method == 'GET':
            if userconfig.mode == 'debug':
                name = request.GET['name']
                password = request.GET['password']
                software = request.GET['software']
                device_type = request.GET['device_type']
            else:
                return Http404()
        elif request.method == 'POST':
            name = request.POST['name']
            password = request.POST['password']
            software = request.POST['software']
            device_type = request.POST['device_type']
        else:
            return Http404()
        # endregion
        msgs = []
        if not utils.check_name(name):
            msgs.append('arg(name) is invalid.')
        if not utils.check_md5(password):
            msgs.append('arg(password) is invalid.')
        if not utils.check_software(software):
            msgs.append(f'software({software}) is not supported.')
        if not utils.check_device_type(device_type):
            msgs.append(f'device_type({device_type}) is not supported.')

        if len(msgs) == 0:
            query_set_user = models.User.objects.filter(name=name)
            if len(query_set_user) > 0:
                first_user = query_set_user[0]
                log_template: str = 'state={0}::' \
                    f'access_ip={utils.get_request_ip(request)}::' \
                    f'access_time={utils.format_time(timezone.now())}'
                if first_user.password == password:
                    models.UserActivity.update(first_user, software, device_type, utils.get_request_ip(request))
                    token = utils.encrypt_token(first_user.uid, time.time(), software, device_type)
                    jsondump = first_user.to_json()
                    jsondump['access_time'] = utils.format_time(timezone.now())
                    jsondump['token'] = token
                    # LOG: 记录登录失败日志
                    models.UserLog.write(first_user, 'login', log_template.format('success'))
                    return JsonResponse(
                        {'msg': 'login ok. let\'s fun.',
                         'shortcut': 'ok',
                         'data': jsondump}
                    )
                else:
                    # LOG: 记录登录失败日志
                    models.UserLog.write(first_user, 'login', log_template.format('fail'))
                    return JsonResponse(
                        {'msg': 'password error.',
                         'shortcut': 'upe'}
                    )
            else:
                return JsonResponse(
                    {'msg': 'user not existed.',
                     'shortcut': 'une'}
                )
        else:
            return JsonResponse(
                {'msg': 'argument format error:{0}'.format(';'.join(msgs)),
                 'shortcut': 'fe'},
                status=400
            )
    except KeyError:
        return response_ae
