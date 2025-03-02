import pandas as pd
import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver import ActionChains
import appium.webdriver.extensions.android.nativekey as androidkey

capabilities = {
    'platformName' : 'Android', #被测试设备平台是Android
    'platformVersion' : '15', #具体版本
    'deviceName' : 'Rainbow\'s android phone', #设备名称，自定义即可
    'appPackage' : 'com.xingin.xhs', #目标app的包名 可以通过进入adb shell；pm list package | grep -i "公司部分名字"查看 或者直接百度搜索对应app的包名也可以
    'appActivity' : '.index.v2.IndexActivityV2', #目标app的Activity页(页面)路径，
    #自动化测试Android App中 很关键的一点就是确定目标app的包名和app的Activity路径 因为相当于这就是你的自动化逻辑打向的目标地方target
    'unicodeKeyboard': True, #使用自带的输入法，支持中文的时候可以设置成True
    'resetKeyboard': True, #结束测试时恢复输入法
    'noReset': True, #不清除app的数据
    'newCommandTimeout': 20000, #设置命令超时时间 基本上不会触发 因为连接的环境都很稳定
    'automationName': 'uiautomator2' #使用uiautomator2自动化测试
}

options = UiAutomator2Options().load_capabilities(capabilities) #加载配置

driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', options=options) #连接Appium Server，初始化环境

driver.implicitly_wait(20) #设置隐式等待时间，单位为秒，默认为0，浏览器打开后立即开始查找元素，不等待，最大等待时间为这个时间

driver.find_element(value= "hmf").click() #点击搜索按钮

inputBar = driver.find_element(value= "fam") #定位输入框

searchTitle = '香港银行'
inputBar.send_keys(searchTitle) #向搜索框输入内容

# driver.press_keycode(androidkey.AndroidKey.ENTER) #模拟Android回车 相当于执行搜索 方式1
driver.find_element(value= "luy").click() #直接定位搜索🔍按钮点击 方式2

titles = driver.find_elements(value= "g8r") #定位每个标题

titlesStringList = []
print("title length: ", len(titles))
for title in titles:
    print(title.text)
    titlesStringList.append(title.text)

driver.quit()

# 当前时间，用于生成文件名
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 构造文件名
file_name = f"{current_time} 小红书搜索: {searchTitle} 标题结果.xlsx"

# 将列表转换为 DataFrame, 使用pandas库插入sheet页的标题字段
df = pd.DataFrame(titlesStringList, columns=['标题Title'])

# 使用pandas库保存导出为 Excel 文件
df.to_excel(file_name, index=False)

print(f"测试结果已保存为 {file_name}")