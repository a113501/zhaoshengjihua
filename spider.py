import requests
from lxml import etree
import json
import random
import time
from datetime import datetime
import pymongo
import concurrent.futures

ALL_PROXIES = [
'114.238.114.252:808',
                   '203.156.126.55:3129',
                   '115.220.144.201:808',
                   '182.34.21.52:808',
                   '175.153.20.65:808',
                   '59.175.72.237:8998',
                   '147.255.107.8:8118',
                   '122.241.73.176:808',
                   '60.178.131.183:8081',
                   '125.106.131.0:808',
                   '218.2.89.34:808',
                   '176.237.17.173:8080',
                   '43.241.227.180:8000',
                   '59.62.164.122:808',
                   '123.55.189.108:808',
                   '218.64.92.117:808',
                   '67.158.45.129:3128',
                   '147.255.107.211:8118',
                   '111.115.70.54:8998',
                   '14.105.243.209:8998',
                   '125.106.92.58:808',
                   '176.237.188.37:8080',
                   '147.255.107.120:8118',
                   '115.203.71.145:808',
                   '187.84.138.76:8080',
                   '147.255.107.26:8118',
                   '119.5.0.33:808',
                   '139.219.194.39:8088',
                   '117.43.0.252:808',
                   '222.94.145.69:808',
                   '123.163.160.59:808',
                   '147.255.107.144:8118',
                   '114.239.145.211:808',
                   '147.255.107.227:8118',
                   '121.226.163.253:808',
                   '147.255.107.92:8118',
                   '123.169.87.159:808',
                   '109.193.51.83:3128',
                   '171.13.36.135:808',
                   '147.255.107.35:8118',
                   '125.93.149.230:9000',
                   '60.178.173.37:8081',
                   '60.178.10.101:8081',
                   '114.230.219.187:808',
                   '83.128.78.174:80',
                   '27.18.174.126:8998',
                   '111.76.226.114:808',
                   '141.196.222.159:8080',
                   '147.255.107.29:8118',
                   '115.203.66.232:808',
                   '123.55.188.142:808',
                   '175.155.241.56:808',
                   '221.229.44.169:808',
                   '147.255.107.191:8118',
                   '147.255.107.59:8118',
                   '123.169.87.151:808',
                   '147.255.107.99:8118',
                   '81.128.165.5:3128',
                   '218.64.152.14:808',
                   '115.215.68.21:808',
                   '218.2.89.43:808',
                   '91.205.131.168:8080',
                   '123.55.190.58:808',
                   '147.255.107.63:8118',
                   '182.34.26.29:808',
                   '123.55.190.103:808',
                   '147.255.107.5:8118',
                   '60.184.174.216:808',
                   '125.93.149.214:9000',
                   '218.65.67.190:808',
                   '61.19.82.138:8080',
                   '115.203.204.51:808',
                   '115.215.69.222:808',
                   '60.184.173.237:808',
                   '182.45.176.229:808',
                   '119.5.0.14:808',
                   '123.169.90.79:808',
                   '182.34.21.128:808',
                   '141.196.70.167:8080',
                   '141.196.198.63:8080',
                   '115.212.83.223:808',
                   '119.85.184.200:8998',
                   '182.34.22.135:808',
                   '115.212.58.53:808',
                   '147.255.107.222:8118',
                   '110.83.46.37:808',
                   '115.220.0.92:808',
                   '114.239.148.114:808',
                   '61.232.254.39:3128',
                   '180.110.18.161:808',
                   '62.68.246.27:8080',
                   '175.43.106.155:808',
                   '147.255.107.248:8118',
                   '125.89.123.15:808',
                   '103.17.246.228:8080',
                   '141.196.150.114:8080',
                   '62.159.193.83:80',
                   '134.35.196.109:8080',
                   '118.89.239.139:3128',
                   '175.155.244.51:808',
                    "117.143.109.155:80",
                    "111.23.10.27:8080",
                    "61.6.7.183:53281",
                    "79.87.142.67:3128",
                    "94.177.236.166:1189",
                    "94.177.236.165:1189",
                    "80.220.27.37:3128",
                    "111.8.22.212:80",
                    "117.143.109.170:80",
                    "182.253.106.26:1080",
                    "103.10.169.92:3128",
                    "188.213.170.40:8080",
                    "31.131.27.145:3128",
                    "94.177.241.239:1189",
                    "114.230.31.158:808",
                    "198.199.67.99:3128",
                    "103.240.109.36:53281",
                    "203.170.67.181:8080",
                    "27.46.21.151:8888",
                    "94.177.237.131:1189"
                               ]
USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        ]
headers = {
            'User-Agent	': random.choice(USER_AGENTS),
            'Host': 'www.wmzy.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        }
PROXIES = {
        'http':'http://'+random.choice(ALL_PROXIES)
         }

class spider():


    def run(self, debug_mode=False):
        start_time = time.clock()
        all_info = {}
        all_links = []
        all_pages=[]
        # school_id 学校id
        # city_id城市id
        # branch_id 文理分科包括li理科wen文科
        # batch_id 批次分类 本科第一批1 本科第二批2 本科第三批5 专科第一批8 专科第二批9
        # time_now unix时间戳1497160999825形式
        branch_ids = {'文科': 'wen', '理科': 'li'}
        batch_ids = {'本科第一批': '1', '本科第二批': '2', '本科第三批': '5', '专科第一批': '8', '专科第二批': '9'}
        school_list_url = {
            '开发模式': 'http://www.wmzy.com/api/school/getSchList?prov_filter=37&type_filter=1&diploma_filter=0&flag_filter=985&page=1&page_len=100',
            '985学校': 'http://www.wmzy.com/api/school/getSchList?prov_filter=00&type_filter=0&diploma_filter=0&flag_filter=985&page=1&page_len=100',#985学校
            '所有学校': 'http://www.wmzy.com/api/school/getSchList?prov_filter=00&type_filter=0&diploma_filter=0&flag_filter=0&page=1&page_len=2570'#所有学校
        }
        if debug_mode==True:
            city_info_debug = {'广西': '45', '山东': '37'}
            school_ids = self.getSchoolID(school_list_url['开发模式'])
            mkdict_start_time = time.clock()
            for school_name, school_id in school_ids.items():
                # all_info.setdefault(school_name,{})
                for city_name, city_id in city_info_debug.items():  ########################
                    # all_info[school_name].setdefault(city_name,{})
                    for branch_name, branch_id in branch_ids.items():
                        # all_info[school_name][city_name].setdefault(branch_name,{})
                        for batch_name, batch_id in batch_ids.items():
                            # all_info[school_name][city_name][branch_name].setdefault(batch_name, {})
                            all_links.append(
                                [school_name, city_name, branch_name, batch_name, school_id, city_id, branch_id,
                                 batch_id])
            mkdict_end_time = time.clock()
            print('字典创建完成，共用时%s' % (mkdict_end_time - mkdict_start_time))
        else:
            city_info = {'广东': '44', '广西': '45', '海南': '46', '宁夏': '64', '贵州': '52', '陕西': '61', '浙江': '33', '山东': '37',
                         '青海': '63', '云南': '53', '河南': '41', '内蒙古': '15', '安徽': '34', '新疆': '65', '福建': '35', '西藏': '54',
                         '湖北': '42', '江苏': '32', '天津': '12', '湖南': '43', '四川': '51', '江西': '36', '黑龙江': '23', '甘肃': '62',
                         '北京': '11', '辽宁': '21', '重庆': '50', '上海': '31', '山西': '14', '吉林': '22', '河北': '13'}
            school_ids = self.getSchoolID(school_list_url['985学校'])
            mkdict_start_time = time.clock()
            for school_name, school_id in school_ids.items():
                # all_info.setdefault(school_name,{})
                for city_name, city_id in city_info.items():########################
                    # all_info[school_name].setdefault(city_name,{})
                    for branch_name, branch_id in branch_ids.items():
                        # all_info[school_name][city_name].setdefault(branch_name,{})
                        for batch_name, batch_id in batch_ids.items():
                            # all_info[school_name][city_name][branch_name].setdefault(batch_name, {})
                            all_links.append([school_name, city_name, branch_name, batch_name, school_id, city_id, branch_id, batch_id])
            mkdict_end_time = time.clock()
            print('字典创建完成，共用时%s'% (mkdict_end_time-mkdict_start_time))


        download_start_time = time.clock()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(self.getSchoolInfo, link): link for link in all_links}
            for future in concurrent.futures.as_completed(future_to_url):
                all_pages.append(future.result())
        download_end_time = time.clock()
        print('目录下载完成，共用时%s' % (download_start_time - download_end_time))

        parse_start_time = time.clock()
        for item in all_pages:
            print(item[0][4])
            enrollPlan = json.loads(item[0][4])['listHTML']['enrollPlan']
            enrollPlan_Result = self.EnrollPlanPageParser(enrollPlan)
            all_info.setdefault(item[0][0], {}).setdefault(item[0][1], {}).setdefault(item[0][2], {}).setdefault(item[0][3], {}).update(enrollPlan_Result)
        parse_end_time = time.clock()
        print('目录分析完成，共用时%s' % (parse_end_time - parse_start_time))
        end_time = time.clock()
        print('程序运行共用时%s' % (end_time - start_time))
        self.salver(all_info)


    def getSchoolID(self,school_list_url):
        all_school_link = []
        all_school_name = []

        link_page_content = json.loads(requests.get(school_list_url, headers=headers, proxies=PROXIES).text)
        text = link_page_content['htmlStr']
        html = etree.HTML(text)
        all_school_link_raw = html.xpath("//*//h3//a/@href")
        all_school_name_raw = html.xpath("//*//h3//a")
        for i in all_school_link_raw:
            all_school_link.append(i.lstrip('/api/school/').rstrip('.html'))
        for i in all_school_name_raw:
            all_school_name.append(i.text.strip())
        school_id = dict(zip(all_school_name, all_school_link))
        return school_id

    def getCityInfo(self):
        all_city_id = []
        all_city_name = []
        url = 'http://www.wmzy.com/api/school/getSchList?prov_filter=00&type_filter=0&diploma_filter=0&flag_filter=0&page=1&page_len=20'
        R = requests.session()
        content = json.loads(R.get(url).text)
        text = content['htmlStr']
        html = etree.HTML(text)
        all_city_name_raw = html.xpath("//*//ul[@id='prov_filter']//li")
        all_city_id_raw = html.xpath("//*//ul[@id='prov_filter']//li/@data-value")
        for i in all_city_id_raw:
            all_city_id.append(i)
        for i in all_city_name_raw:
            all_city_name.append(i.text)
        city_info = dict(zip(all_city_name, all_city_id))
        return city_info

    def getSchoolInfo(self, an_EnrollPlan):
        time_now = str(int(time.mktime(datetime.now().timetuple()) * 1000.0 + datetime.now().microsecond / 1000.0))
        #school_id 学校id
        # city_id城市id
        # branch_id 文理分科包括li理科wen文科
        # batch_id 批次分类 本科第一批1 本科第二批2 本科第三批5 专科第一批8 专科第二批9
        # time_now unix时间戳1497160999825形式
        return_information = []
        school_id = an_EnrollPlan[4]
        city_id = an_EnrollPlan[5]
        branch_id = an_EnrollPlan[6]
        batch_id = an_EnrollPlan[7]
        target_url = 'http://www.wmzy.com/api/school/enrollment-list?sch_id=' + school_id + '&diploma=7&province=' + city_id + '0000000000&ty=' + branch_id + '&year=&page=1&page_len=100&batch=' + batch_id + '&&_=' + time_now
        info = requests.get(target_url, headers=headers, proxies=PROXIES)
        return_information.append([an_EnrollPlan[0],an_EnrollPlan[1],an_EnrollPlan[2],an_EnrollPlan[3],info.text])
        time.sleep(random.random()+1)
        return return_information

    def EnrollPlanPageParser(self, content):
        major_names= []#专业名称
        major_categories = []#学科门类
        major_categories_2nd = []#二级门类
        plans = []#计划招生
        return_info = {}
        target_content = etree.HTML(content)
        for i in target_content.xpath('//table//tr//td//a'):
            major_names.append(i.text)
        for i in target_content.xpath('//table//tr//td[2]'):
            major_categories.append(i.text)
        for i in target_content.xpath('//table//tr//td[3]'):
            major_categories_2nd.append(i.text)
        for i in target_content.xpath('//table//tr//td[4]'):
            plans.append(i.text)
        for index, major_name in enumerate(major_names):
            return_info.setdefault(major_name,{})
            return_info[major_name].setdefault('专业名称', major_categories[index])
            return_info[major_name].setdefault('二级门类', major_categories_2nd[index])
            return_info[major_name].setdefault('计划招生', plans[index])

        return return_info

    def salver(self,all_info):
        client = pymongo.MongoClient('localhost', 27017)
        db = client.db
        collection = db.collection
        while len(all_info) != 0:
            tmp = all_info.pop()
            collection.insert(tmp)
        print('储存完成')


if __name__ == '__main__':
    g=spider()
    g.run(debug_mode=True)