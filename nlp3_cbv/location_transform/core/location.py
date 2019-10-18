import json
from urllib.request import urlopen, quote
import requests
from urllib import parse
"""
利用百度接口做地址编码、地理名转经纬度数据
"""
def getlnglat(address , count = 100):
    rst = {"lng":None,"lat":None,"count":count,"address":None}
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'Q16tW6a9GdGqKWct0cVFUlzgEKFqSwpG'  # 浏览器端密钥
    address = quote(address)  # 由于本文地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    lat = temp['result']['location']['lat']
    lng = temp['result']['location']['lng']
    # return lat, lng
    rst['lng'] = lng
    rst['lat'] = lat
    rst['address'] =parse.unquote(address)
    return rst

rst = getlnglat("重庆市璧山区S108(璧青路)")
print(rst)





