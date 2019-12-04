# -*- coding: utf-8 -*-
import re,json
from excel import is_int


def translate(data):
    orderdata = data.get('order_data',[])
    spec_dict = parseSpec(data.get('detail_data',[]))
    print(spec_dict)

    col = ['订单类型','订单号','物流公司','物流单号','商品条形码','实发数量','净重','毛重','证件号码','收件人', '收货地区','收货地址', '收件人手机','收货地址（完整）']
    # order = 0
    cols = list()
    cols.append(col)

    ordercol = orderdata[0]
    formats = ['0','@','@','@','@','0','0.0','0.0','@','@','@','@','@','@']
    for d in orderdata[1:]:
        # order += 1
        express = ''
        recipient = d[ordercol.index(u'收货人')]
        full_address = clear_invisible_blank(d[ordercol.index(u'地址')])
        area,address = parseArea(full_address)
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
            ordertype = '4'
            shipcop = ''
            productname = product[1]
            productcode = spec_dict.get(productname,'')
            print(productname,productcode)
            weight = '1'
            pureweight = '0'
            productcol = [to_str(ordertype),to_str(express), to_str(shipcop), to_str(express),
                          to_str(productcode),to_str(productnum),to_str(pureweight),
                          to_str(weight), to_str(idnum), to_str(recipient), to_str(area),
                          to_str(address),to_str(phone),to_str(full_address)]
            cols.append(productcol)
    return cols,formats

def transform(data):
    with open('data/columns.txt','r',encoding='utf-8') as f:
        colname = f.read().split(';')
    orderdata = data.get('order_data',[])
    spec_dict = parseSpec(data.get('detail_data',[]))
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
        address = clear_invisible_blank(d[ordercol.index(u'地址')])
        province = address[0:3]
        city = address[3:6]
        sendername = d[ordercol.index(u'所在店铺')]
        senderphone = findSender(sendername)
        phone = d[ordercol.index(u'电话')]
        idnum1 = creditIdSearch(custom_remark)
        idnum2 = creditIdSearch(client_remark)
        if idnum1 == '':
            idnum = idnum2
        else:
            idnum = idnum1
        productcol = [pkg(clientnick) , pkg(sendername,True) , pkg(senderphone,True,True) , pkg(idnum) , pkg(recipient)
            , pkg(phone) , pkg(province) , pkg(city), pkg(address)]
        products = productConfig(config)
        for product in products:
            productnum = product[0]
            productname = product[1]
            productcode = spec_dict.get(productname,'')
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

def parseArea(address):
    if address:
        i = 0
        res = list()
        pts = [u'[北天重上][京津庆海]市?|.*?省|.*?自治区',
                u'.*?市区?|.*?州|.*?区',
               u'.*?[市县区旗镇]']
        for pt in pts:
            word = address[i:]
            sr = re.search(re.compile(pt), word)
            if sr:
                res.append(sr.group())
                i += len(sr.group())
        if res:
            d = address.index(res[-1]) + len(res[-1])
        else:
            d = 0
        return '-'.join(res),address[d:]
    else:
        return '',''

def parseSpec(data):
    ordercol = data[0]
    pname_ind = ordercol.index(u'品名')
    spec_ind = ordercol.index(u'规格')
    res = dict()
    for d in data[1:]:
        pname = d[pname_ind]
        spec = d[spec_ind]
        res[pname] = spec
    return res

def clear_invisible_blank(string):
    """
    清除文本中的隐藏空字符
    :param string:
    :return:
    """
    invisible_blank = [u'\u200b',u'\u200e']
    for ib in invisible_blank:
        if ib in string:
            string = string.replace(ib,'')
    return string


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
            pcount = str_search(r'\((\d+)\)',p,1).strip()
            pname = str_search(r'\)([^\t\n\r\f\v]*)\~',p,1).strip()
            config.append([pcount,pname])
    return config


def str_search(pattern,s,*args):
    if re.search(re.compile(pattern), s):
        return re.search(re.compile(pattern), s).group(*args)
    else:
        return ''


def creditIdSearch(string):
    if string=='':
        return ''
    if string[-1]=='×':
        string = string[:-1]+'x'
    comp = '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]'
    pattern = re.compile(comp)
    matchString = string.replace(' ','')
    m = re.search(pattern,matchString)
    if m:
        return m.group()
    else:
        return ''

