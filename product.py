# -*- coding: utf-8 -*-
import re,json
from excel import is_int


def translate(orderdata):
    col = ['订单类型','订单号','物流公司','物流单号','商品条形码','实发数量','净重','毛重','证件号码','收件人', '收货地区','收货地址', '收件人手机']
    # order = 0
    cols = list()
    cols.append(col)
    ordercol = orderdata[0]
    formats = ['0','@','@','@','@','0','0.0','0.0','@','@','@','@','@']
    for d in orderdata[1:]:
        # order += 1
        express = ''
        recipient = d[ordercol.index(u'收货人')]
        address = d[ordercol.index(u'地址')]
        area = address[0:6]
        phone = d[ordercol.index(u'电话')]
        custom_remark = d[ordercol.index(u'客服备注')]
        client_remark = d[ordercol.index(u'客户备注')]

        idnum1 = creditIdSearch(custom_remark)
        idnum2 = creditIdSearch(client_remark)
        if idnum1=='':
            idnum = idnum2
        else:
            idnum = idnum1

        products = productConfig(d[ordercol.index(u'货品摘要')])
        for product in products:
            productnum = product[0]
            # productname = product[1]
            productcode = product[2]
            weight = ''
            pureweight = ''
            productcol = ['0',to_str(express), '', to_str(express), to_str(productcode),to_str(productnum),to_str(weight),
                          to_str(pureweight), to_str(idnum), to_str(recipient), to_str(area), to_str(address),
                          to_str(phone)]
            cols.append(productcol)
    return cols,formats

def transform(orderdata):
    with open('data/columns.txt','r',encoding='utf-8') as f:
        colname = f.read().split(';')
    cols = list()
    cols.append(colname)
    ordercol = orderdata[0]
    colformat = list()
    for i in colname:
        if i.find(u'商品') > -1 and i.find(u'数量') > -1:
            colformat.append('0')
        elif i.find(u'手机')>-1:
            colformat.append('0')
        else:
            colformat.append('@')
    for d in orderdata[1:]:
        custom_remark = d[ordercol.index(u'客服备注')]
        client_remark = d[ordercol.index(u'客户备注')]
        config = d[ordercol.index(u'货品摘要')]
        clientnick = d[ordercol.index(u'网名')]
        recipient = d[ordercol.index(u'收货人')]
        address = d[ordercol.index(u'地址')]
        province = address[0:3]
        city = address[3:6]
        sendername = d[ordercol.index(u'所在店铺')]
        senderphone = findSender(sendername)
        phone = d[ordercol.index(u'电话')]
        if re.search(re.compile(r'[0-9 ]+'), custom_remark):
            idnum = re.search(re.compile(r'[0-9 ]+'), custom_remark).group()
        elif re.match(re.compile(r'[0-9 ]+'), client_remark):
            idnum = re.search(re.compile(r'[0-9 ]+'), client_remark).group()
        else:
            idnum = ''
        idnum = idnum.replace(' ', '')
        productcol = [pkg(clientnick) , pkg(sendername,True) , pkg(senderphone,True,True) , pkg(idnum) , pkg(recipient)
            , pkg(phone) , pkg(province) , pkg(city), pkg(address)]
        products = productConfig(config)
        for product in products:
            productnum = product[0]
            # productname = product[1]
            productcode = product[2]
            # weight = ''
            # pureweight = ''
            productcol.append(pkg(productcode))
            productcol.append(pkg(productnum))
        cols.append(productcol)
    return cols,colformat

def findSender(sender):
    with open('data/sender.json', 'r', encoding='utf-8') as f:
        senderList = json.loads(f.read())
    sender_phone = ''
    for senders in senderList[1:]:
        if sender == str(senders[0]):
            sender_phone = senders[1]
    return str(sender_phone)




def pkg(data ,  select=False , corresponding=False):
    package = dict()
    package['value'] =to_str(data)
    package['select'] = select
    package['corresponding'] = corresponding
    return package

def to_str(data):
    if isinstance(data,str):
        if is_int(data):
            return data.split('.')[0]
        else:
            return data
    else:
        return str(data)



def productConfig(pstr):
    config = []
    productlist = re.split(re.compile('\|'),pstr)
    if productlist:
        for p in productlist:
            pcount = str_search(r'\([0-9]\)',p)[1:-1]
            pname = str_search(r'\)[^\t\n\r\f\v\ ]*',p)[1:]
            pcode = str_search(r'[0-9]{5,100}',p)
            config.append([pcount,pname,pcode])
    return config


def str_search(pattern,s):
    if re.search(re.compile(pattern), s):
        return re.search(re.compile(pattern), s).group()
    else:
        return ''


