import pymysql
import xlwt
import datetime
def writexls(time):
    db = pymysql.connect("47.105.38.117", "root", "1234", "long_distance_data", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = "select center,project,username,todaywork,todayproblems,tomorrowwork from {database}".format(database="table"+str(time))

    cursor.execute(sql)  # 执行sql语句
    userinf = cursor.fetchall()
    if len(userinf)==0:
        print("此时段无人上传日志！")
        return
    cursor.close()
    db.close()
    print("服务器数据总数：",len(userinf))
    # print(len(userinf[0]))
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(str(time)+"工作日志")

    sheet.write(1, 0, "序号")
    sheet.write(1, 1, "中心")
    sheet.write(1, 2, "项目名称")
    sheet.write(1, 3, "姓名")
    sheet.write(1, 4, "今日完成工作")
    sheet.write(1, 5, "待解决问题")
    sheet.write(1, 6, "明日工作计划")
    for i in range(len(userinf)):
        sheet.write(i+2, 0, str(i))
        for j in range(0, len(userinf[0])):
            sheet.write(i+2, j+1, userinf[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save('Excel_test.xls')

if __name__ == '__main__':
    time = input("请输入时间，如200212，下载今日日志请回车！")
    if time=="":
       time = datetime.date.today().strftime('%y%m%d')
    print("开始下载"+time+"数据...")
    writexls(time)
    print("已传输完成！")