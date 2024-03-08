from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import network
import machine
import time
from machine import RTC
import urequests
import ntptime
import utime



fonts= {
    "气": [0x20,0x3F,0x40,0xBF,0x00,0x7F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xE0,0x00,0xC0,0x00,0x80,0x80,0x80,0x80,0xA0,0x60,0x20],
    "温": [0x0F,0x88,0x4F,0x08,0x0F,0x80,0x5F,0x15,0x35,0x55,0x95,0x3F,0x80,0x80,0x80,0x80,0x80,0x00,0xC0,0x40,0x40,0x40,0x40,0xE0],
    "湿": [0x80,0x5F,0x10,0x1F,0x90,0x5F,0x05,0x25,0x15,0x45,0x85,0x3F,0x00,0xC0,0x40,0xC0,0x40,0xC0,0x00,0x20,0x40,0x00,0x00,0xE0],
    "度": [0x02,0x7F,0x48,0x7F,0x48,0x4F,0x40,0x5F,0x48,0x44,0x43,0x9C,0x00,0xE0,0x80,0xE0,0x80,0x80,0x00,0xC0,0x40,0x80,0x00,0xE0],
    "日": [0x00,0x7F,0x40,0x40,0x40,0x7F,0x40,0x40,0x40,0x40,0x7F,0x40,0x00,0xC0,0x40,0x40,0x40,0xC0,0x40,0x40,0x40,0x40,0xC0,0x40],
    "期": [0x48,0x49,0xFD,0x49,0x79,0x49,0x79,0x49,0xFD,0x01,0x49,0x86,0x00,0xE0,0x20,0x20,0xE0,0x20,0x20,0xE0,0x20,0x20,0x20,0x60],
    "霾": [0x7F,0x04,0xFF,0xA4,0x30,0xD3,0x5A,0xE3,0x32,0xDB,0x28,0xDB,0xC0,0x00,0xE0,0xA0,0x00,0xE0,0xA0,0xE0,0xA0,0xE0,0x80,0xE0],
    "晴": [0x01,0xEF,0xA1,0xA7,0xA1,0xEF,0xA4,0xA7,0xA4,0xE7,0xA4,0x04,0x00,0xE0,0x00,0xC0,0x00,0xE0,0x40,0xC0,0x40,0xC0,0x40,0xC0],
    "多": [0x08,0x0F,0x11,0x22,0xD4,0x09,0x33,0xC4,0x1A,0x03,0x0C,0xF0,0x00,0x80,0x00,0x00,0x80,0x00,0xE0,0x40,0x80,0x00,0x00,0x00],
    "云": [0x00,0x3F,0x00,0x00,0x00,0xFF,0x04,0x08,0x11,0x20,0x7F,0x00,0x00,0x80,0x00,0x00,0x00,0xE0,0x00,0x00,0x00,0x80,0xC0,0x40],
    "阴": [0xF7,0x94,0x94,0xA7,0xA4,0x94,0x97,0x94,0x94,0xE4,0x88,0x91,0xC0,0x40,0x40,0xC0,0x40,0x40,0xC0,0x40,0x40,0x40,0x40,0xC0],
    "雪": [0x7F,0x04,0xFF,0xB5,0x04,0x75,0x00,0x7F,0x00,0x3F,0x00,0x7F,0xC0,0x00,0xE0,0xA0,0x00,0xC0,0x00,0xC0,0x40,0xC0,0x40,0xC0],
    "小": [0x04,0x04,0x04,0x04,0x24,0x24,0x44,0x44,0x84,0x04,0x04,0x1C,0x00,0x00,0x00,0x00,0x80,0x40,0x40,0x20,0x20,0x00,0x00,0x00],
    "中": [0x04,0x04,0x04,0x7F,0x44,0x44,0x44,0x7F,0x44,0x04,0x04,0x04,0x00,0x00,0x00,0xC0,0x40,0x40,0x40,0xC0,0x40,0x00,0x00,0x00],
    "雨": [0xFF,0x04,0x04,0xFF,0x84,0xA5,0x94,0x84,0xA5,0x94,0x84,0x80,0xE0,0x00,0x00,0xE0,0x20,0x20,0xA0,0x20,0x20,0xA0,0x20,0xE0],
    "大": [0x04,0x04,0x04,0x04,0xFF,0x04,0x0A,0x0A,0x11,0x11,0x20,0xC0,0x00,0x00,0x00,0x00,0xE0,0x00,0x00,0x00,0x00,0x00,0x80,0x60],
    "暴": [0x7F,0x40,0x7F,0x40,0x7F,0x11,0x7F,0x11,0xFF,0x24,0xD5,0x2C,0xC0,0x40,0xC0,0x40,0xC0,0x00,0xC0,0x00,0xE0,0x80,0x60,0x80],
    "风": [0x00,0x7F,0x40,0x42,0x62,0x54,0x48,0x48,0x54,0x62,0x40,0x80,0x00,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0xA0,0xA0,0x60,0x20],
    "转": [0x41,0x41,0xEF,0x42,0xA2,0xAF,0xF4,0x27,0x30,0xE6,0x21,0x20,0x00,0x00,0xC0,0x00,0x00,0xE0,0x00,0xC0,0x40,0x80,0x80,0x40],
    "夹": [0x04,0x04,0x7F,0x04,0x24,0x15,0x04,0xFF,0x0A,0x11,0x20,0xC0,0x00,0x00,0xC0,0x00,0x80,0x00,0x00,0xE0,0x00,0x00,0x80,0x60],
    "雾": [0x18,0x10,0x1F,0x61,0x18,0x07,0x08,0x1F,0x52,0x7F,0x02,0x3F,0x60,0x80,0xC0,0x30,0xC0,0x00,0xA0,0xC0,0x50,0xF0,0x00,0xE0],
    "度": [0x02,0x7F,0x48,0x7F,0x48,0x4F,0x40,0x5F,0x48,0x44,0x43,0x9C,0x00,0xE0,0x80,0xE0,0x80,0x80,0x00,0xC0,0x40,0x80,0x00,0xE0],
    "新": [0x10,0x7D,0x01,0x45,0x29,0xFD,0x11,0x7D,0x11,0x55,0x92,0x34,0x20,0xC0,0x00,0x00,0xE0,0x40,0x40,0x40,0x40,0x40,0x40,0x40],
    "密": [0x04,0xFF,0x88,0x05,0x52,0x54,0x8F,0x30,0x04,0x44,0x44,0x7F,0x00,0xE0,0x20,0x00,0x40,0xA0,0xA0,0x00,0x00,0x40,0x40,0xC0],    
    "星": [0x7F,0x40,0x7F,0x40,0x7F,0x04,0x44,0x7F,0x84,0x3F,0x04,0xFF,0xC0,0x40,0xC0,0x40,0xC0,0x00,0x00,0xC0,0x00,0x80,0x00,0xE0],
    "期": [0x48,0x49,0xFD,0x49,0x79,0x49,0x79,0x49,0xFD,0x01,0x49,0x86,0x00,0xE0,0x20,0x20,0xE0,0x20,0x20,0xE0,0x20,0x20,0x20,0x60],
}


i2c = I2C(scl=Pin(5), sda=Pin(4))

oled = SSD1306_I2C(128, 64, i2c, addr=60)
oled.show()

# 连接到WiFi网络
sta_if = network.WLAN(network.STA_IF)
sta_if.disconnect()
sta_if.active(True)
sta_if.scan()
oled.text('Wifi Connecting', 0, 0)
oled.show()
sta_if.connect('张', 'zhang13939088771')
utime.sleep(5)
if sta_if.ifconfig()[0] == '0.0.0.0':
  sta_if.connect('小金豆', 'chinausa')
  utime.sleep(5)
print(sta_if.ifconfig()[0])
def link():
  try:
    ntptime.NTP_DELTA = 3155644800
    # ntptime.host = 'ntp1.aliyun.com'
    ntptime.settime()
    rep = urequests.get('https://api.seniverse.com/v3/weather/now.json?key=SSlw_VaRGD6k1B2mw&location=zhengzhou&language=zh-Hans&unit=c')
    rep.encoding = 'utf-8'
    print('返回结果:%s'%rep.json())
    print('天气：%s'%rep.json()['results'][0]['now']['text'])      
    print('温度：%s'%rep.json()['results'][0]['now']['temperature'])
    while True:
      def chinese(ch_str, x_axis, y_axis, ch_size=12):   
        offset_ = 0
        for k in ch_str:
            byte_data = fonts[k]
            # print(fonts[k], "offset=", offset_)
            for y in range(0, ch_size):
                # 进制转换、补全
                a_ = '{:0>8b}'.format(byte_data[y])
                b_ = '{:0>8b}'.format(byte_data[y+ch_size])
                # 绘制像素点 （按取模软件的行列式方式）
                for x in range(0, 8):
                    oled.pixel(x_axis + offset_ + x, y + y_axis, int(a_[x]))
                    oled.pixel(x_axis + offset_ + x + 8, y + y_axis, int(b_[x]))
            offset_ += ch_size
      localtime_now=utime.time()+8*3600
      localtime_now=utime.localtime(localtime_now)
      t = localtime_now
      oled.fill(0)  
      print(t)
      if (t[3]+8) // 24 >= 1:
        oled.text('{}-{}-{}'.format(t[0], t[1], t[2]+1), 30, 35)
        t6 = t[6] + 1
      elif (t[3]+8) // 24 < 1:
        oled.text('{}-{}-{}'.format(t[0], t[1], t[2]), 30, 35)
        t6 = t[6]
      oled.text('{}:{}:{}'.format((t[3])%24, t[4], t[5]), 30, 45)
      chinese('新密', 0, 0)
      chinese(rep.json()['results'][0]['now']['text'], 0, 15)
      oled.text(rep.json()['results'][0]['now']['temperature'], 60, 18)
      chinese('度', 80, 15)
      chinese('星期', 60, 0)
      #if t6 <= 6:
      oled.text('{}'.format(t[6]+1), 90, 3)
      '''elif t6 == 7:
        oled.text('1', 90, 3)
      elif t6 == 8:
        oled.text('2', 90, 3)'''
      if t[4]%5 == 0 and t[5] == 0:
        link()
      oled.show()
    
  except Exception as e:
    for i in range(5):
      oled.text('ERROR!', 0, 20)
      oled.text('{}'.format(e), 0, 30)
      print(e)
      oled.show()
    link()
    
link()




