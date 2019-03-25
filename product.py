# -*- coding: utf-8 -*-
import re



def translate(orderdata):
    col = ['订单数', '物流单号', '商品条形码', '实发数量', '净重', '毛重', '证件号码', '收件人', '收货地区', '收货地址', '收件人手机']
    order = 0
    cols = list()
    cols.append(col)
    ordercol = orderdata[0]

    for d in orderdata[1:]:
        order += 1
        express = ''
        recipient = d[ordercol.index(u'收货人')]
        address = d[ordercol.index(u'地址')]
        area = address[0:6]
        phone = d[ordercol.index(u'电话')]
        if d[ordercol.index(u'客服备注')] != '':
            idnum = re.search(re.compile(r'[0-9 ]+'),d[ordercol.index(u'客服备注')]).group()
        elif d[ordercol.index(u'客户备注')] != '':
            idnum = re.search(re.compile(r'[0-9 ]+'),d[ordercol.index(u'客户备注')]).group()
        else:
            idnum = ''
        idnum = idnum.replace(' ','')
        products = productConfig(d[ordercol.index(u'货品摘要')])
        for product in products:
            productnum = product[0]
            # productname = product[1]
            productcode = product[2]
            weight = ''
            pureweight = ''
            productcol = [order, express, productcode, productnum, weight, pureweight, idnum, recipient, area, address,
                          phone]
            cols.append(productcol)
    return cols

def colFormat():
    formats = ['0', '@', '@', '0', '0.0', '0.0', '@', '@', '@', '@', '@']
    return formats


def productConfig(pstr):
    config = []
    productlist = re.split(re.compile('\|'),pstr)
    if productlist:
        for p in productlist:
            count = re.search(re.compile(r'\([0-9]\)'),p).group()
            pcount = re.search(re.compile(r'[0-9]'),count).group()
            pname = re.search(re.compile(r'\)[^\t\n\r\f\v\ ]*'),p).group()[1:]
            pcode = re.search(re.compile(r'[0-9]{5,100}'),p).group() or ''
            config.append([pcount,pname,pcode])
    return config