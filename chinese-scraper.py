import pandas as pd
import csv

for i in range(178,200):  # 爬取全部177页数据
    url = 'http://s.askci.com/stock/a/?reportTime=2017-12-31&pageNum=%s' % (str(i))
    tb = pd.read_html(url)[3]
    tb.to_csv(r'chinese-stocks.csv', mode='a', encoding='utf_8_sig', header=1, index=0)
    print('第'+str(i)+'页抓取完成')
