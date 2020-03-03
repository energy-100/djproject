
import pymysql
import re
import datetime

db = pymysql.connect("47.105.38.117", "root", "1234", "long_distance_data", port=3306, charset='utf8')
cursor = db.cursor()
user_tup='李臣浩'
sql = sqlgetsuserdata='select center,project from userdata where username='+"'"+user_tup+"'"
cursor.execute(sql)
all_users = cursor.fetchall()
print(all_users[0][1])
# cursor.close()
# db.close()
# has_user = 0
# i = 0
# while i < len(all_users):
#     if user_tup == all_users[i]:
#         sqlgetsuserdata="select * from userdata where username='李臣浩'"
#
#         has_user = 1
#     i += 1