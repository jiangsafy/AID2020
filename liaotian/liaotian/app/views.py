# Create your views here.
from django.shortcuts import render, HttpResponse  # 引入HttpResponse
from dwebsocket.decorators import accept_websocket  # 引入dwbsocket的accept_websocket装饰器
import uuid
import json
# def to_sendmsg(request):
#     return render(request, 'sendmsg.html')
#
#
# def to_recmsg(request):
#     return render(request, 'recmsg.html')
#
#
# clients = {}  # 创建客户端列表，存储所有在线客户端
#
#
# # 允许接受ws请求
# @accept_websocket
# def link(request):
#     # 判断是不是ws请求
#     if request.is_websocket():
#         userid = str(uuid.uuid1())
#         # 判断是否有客户端发来消息，若有则进行处理，若发来“test”表示客户端与服务器建立链接成功
#         while True:
#             message = request.websocket.wait()
#             if not message:
#                 break
#             else:
#                 print("客户端链接成功：" + str(message, encoding="utf-8"))
#                 # 保存客户端的ws对象，以便给客户端发送消息,每个客户端分配一个唯一标识
#                 clients[userid] = request.websocket
#
#
# def send(request):
#     # 获取消息
#     msg = request.POST.get("msg")
#     # 获取到当前所有在线客户端，即clients
#     # 遍历给所有客户端推送消息
#     for client in clients:
#         clients[client].send(msg.encode('utf-8'))
#     return HttpResponse({"msg": "success"})
# ##########################################################
# #聊天界面
# def to_chat(request):
#     return render(request,'chat.html')
#
# # 服务器方法，允许接受ws请求
# @accept_websocket
# def chat(request):
#     # 判断是不是ws请求
#     if request.is_websocket():
#         # 保存客户端的ws对象，以便给客户端发送消息,每个客户端分配一个唯一标识
#         userid=str(uuid.uuid1())[:8]
#         clients[userid] = request.websocket
#         # 判断是否有客户端发来消息，若有则进行处理，表示客户端与服务器建立链接成功
#         while True:
#             '''获取消息，线程会阻塞，
#             他会等待客户端发来下一条消息,直到关闭后才会返回，当关闭时返回None'''
#             message=request.websocket.wait()
#             if not message:
#                 break
#             else:
#                 msg=str(message, encoding = "utf-8")
#                 print(msg)
#                 #1、发来test表示链接成功
#                 if msg == "test":
#                     print("客户端链接成功："+userid)
#                     #第一次进入，返回在线列表和他的id
#                     request.websocket.send(json.dumps({"type":0,"userlist":list(clients.keys()),"userid":userid}).encode("'utf-8'"))
#                     #更新所有人的userlist
#                     for client in clients:
#                         clients[client].send(json.dumps({"type":0,"userlist":list(clients.keys()),"user":None}).encode("'utf-8'"))
#     #客户端关闭后从列表删除
#     if userid in clients:
#         del clients[userid]
#         print(userid + "离线")
#         # 更新所有人的userlist
#         for client in clients:
#             clients[client].send(
#                 json.dumps({"type": 0, "userlist": list(clients.keys()), "user": None}).encode("'utf-8'"))
# #消息发送方法
# def msg_send(request):
#     msg = request.POST.get("txt")
#     useridto = request.POST.get("userto")
#     useridfrom = request.POST.get("userfrom")
#     type=request.POST.get("type")
#     #发来{type:"2",msg:data,user:user},表示发送聊天信息，user为空表示群组消息，不为空表示要发送至的用户
#     if type == "1":
#         #群发
#         for client in clients:
#             clients[client].send(json.dumps({"type": 1, "data": {"msg": msg, "user": useridfrom}}).encode('utf-8'))
#     else:
#         # 私聊，对方显示
#         clients[useridto].send(json.dumps({"type": 1, "data": {"msg": msg, "user": useridfrom}}).encode('utf-8'))
#         # 私聊，自己显示
#         clients[useridfrom].send(json.dumps({"type": 1, "data": {"msg": msg, "user": useridfrom}}).encode('utf-8'))
#     return HttpResponse(json.dumps({"msg":"success"}))
#
#
#

#聊天界面
def to_chat(request):
    return render(request,'chat.html')
#创建客户端列表，存储所有在线客户端
clients={}
@accept_websocket
def chat(request):
    userid = str(request.COOKIES.get('username'))
    print("username:"+userid)
    if request.is_websocket():
        print("web请求")
        # userid=str(uuid.uuid1())[:8]
        # print ("aaaaaaaaaaaaaaaaaaaaaa")
        # print (userid)
        # print ("AAAAAAAAAAAAAAAAAAAAAA")
        clients[userid] = request.websocket

        while True:

            message=request.websocket.wait()
            # print ("bbbbbbbbbbbbbbbbb")
            # print (message)
            # print ("BBBBBBBBBBBBBBBBB")
            if not message:
                break
            else:
                msg=str(message, encoding = "utf-8")
                print(msg)
                #1、发来test表示链接成功
                if msg == "test":
                    print("客户端链接成功："+userid)
                    #第一次进入，返回在线列表和他的id'
                    # ass = {"a":"nihao","b":"adas"}
                    # print (json.dumps(ass))

                    re = request.websocket.send(json.dumps({"type":0,"userlist":list(clients.keys()),"userid":userid}).encode("'utf-8'"))
                    # print ("cccccccccccccccccccccccccccccccc")
                    # print (re)
                    # print ("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")

                    for client in clients:
                        clients[client].send(json.dumps({"type":0,"userlist":list(clients.keys()),"user":None}).encode("'utf-8'"))
    # 客户端关闭后从列表删除
    if userid in clients:
        del clients[userid]
        print(userid + "离线")
        # 更新所有人的userlist
        for client in clients:
            clients[client].send(
                json.dumps({"type": 0, "userlist": list(clients.keys()), "user": None}).encode("'utf-8'"))


def msg_send(request):
    msg = request.POST.get("txt")
    # print (msg)
    useridto = request.POST.get("userto")
    # print (useridto)
    useridfrom = request.POST.get("userfrom")
    # print (useridfrom)
    type=request.POST.get("type")
    # print (type)
    if type == "1":
        #群发
        for client in clients:
            clients[client].send(json.dumps({"type": 1, "data": {"msg": msg, "user": useridfrom}}).encode('utf-8'))

    else:
        # 私聊，对方显示
        clients[useridto].send(json.dumps({"type": 1, "data": {"msg": msg, "user": useridfrom}}).encode('utf-8'))
        # 私聊，自己显示
        clients[useridfrom].send(json.dumps({"type": 1, "data": {"msg": msg, "user": useridfrom}}).encode('utf-8'))
    return HttpResponse(json.dumps({"msg":"success"}))

def tiao(request):
    return render(request,"tiao.html")

