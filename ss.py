#
#
# a = {"error_code":0,"data":{"result":{"number":"75111130894977","type":"中通快递","list":[{"time":"2018-11-29 12:14:55","status":"【成都市】  快件已在 【都江堰青城山镇】 签收, 签收人: 菜鸟, 如有疑问请电联:18180845107 \/ 028-87217460, 您的快递已经妥投, 如果您对我们的服务感到满意, 请给个五星好评, 鼓励一下我们【请在评价快递员处帮忙点亮五颗星星哦~】"},{"time":"2018-11-24 10:57:47","status":"【成都市】  【都江堰青城山镇】 的程杨（18180845107） 正在第1次派件, 请保持电话畅通,并耐心等待"},{"time":"2018-11-24 10:56:39","status":"【成都市】  快件到达 【都江堰青城山镇】"},{"time":"2018-11-23 14:56:53","status":"【成都市】  快件离开 【都江堰】 发往 【都江堰青城山镇】"},{"time":"2018-11-23 14:17:24","status":"【成都市】  快件到达 【都江堰】"},{"time":"2018-11-23 07:24:30","status":"【成都市】  快件离开 【成都中转】 发往 【都江堰】"},{"time":"2018-11-23 07:24:06","status":"【成都市】  快件到达 【成都中转】"},{"time":"2018-11-21 20:53:54","status":"【北京市】  快件离开 【北京】 发往 【成都中转】"},{"time":"2018-11-21 20:53:41","status":"【北京市】  快件到达 【北京】"},{"time":"2018-11-21 19:13:50","status":"【北京市】  快件离开 【北京市场二部】 发往 【北京】"},{"time":"2018-11-21 17:56:09","status":"【北京市】  【北京市场二部】（010-56998340、010-56998360、010-56998367） 的 云仓 （13241120509） 已揽收"}],"deliverystatus":"4"}},"reason":"success"}
# c = a['data']['result']['list']
# f= dict(c)
# for b in c:
# 	# print(b)
# 	print(b['time'])
# 	print(b['status'])
#
#

a = "20"
b = 2
c = a*b
print(c)