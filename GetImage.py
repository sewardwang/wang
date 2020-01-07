import sys
sys.path.append('e:/pyhton work/external-libraries')

import os
import re
import uuid
import requests
def download_image(key_word,download_max):
    #初始化下载数和十六进制形式的当前加载起始位置
    download_sum=0
    str_gsm='00'
    #把每个明星的图片单独存放在一个文件夹中
    save_path='e:/python work/aistudio/data/face_image'+key_word
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    while download_sum<download_max:
     #下载次数超过指定值就停止下载
        if download_sum>=download_max:
            break
        str_pn=str(download_sum)
        url='http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&' \
              'word=' + key_word + '&pn=' + str_pn + '&gsm=' + str_gsm + '&ct=&ic=0&lm=-1&width=0&height=0'
        print(url)
        print('正在下载%s的第%d张图片....'%(key_word,download_sum))
        try:
            #获取当前页面的源码
            result=requests.get(url,timeout=30).text
            #获取当前页面的图片URL
            img_urls=re.findall('"objURL":"(.*?)",',result,re.S)
            if len(img_urls)<1:
                break
            for img_url in img_urls:
                #获取图片内容
                img=requests.get(img_url,timeout=30)
                img_name=save_path+'/'+str(uuid.uuid1())+'.jpg'
                # 保存图片
                with open(img_name,'wb') as f:
                    f.write(img.content)
                with open('image_url_list.txt', 'a+', encoding='utf-8') as f:
                    f.write(img_name + '\t' + img_url + '\n')
                download_sum += 1
                if download_sum >= download_max:
                    break
        except Exception as e:
            print('【错误】当前图片无法下载，%s' % e)
            download_sum += 1
            continue
    print('下载完成')


# 最大图片下载数量
max_sum = 10
# 获取明星的名字
key_word = str(input('please input yourename: '))
# 使用明星的名字开始下载图片
download_image(key_word, max_sum)
print('全部图片以下载完成')