from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import json
import os
import pymongo
from pymongo import MongoClient

print(pymongo.__version__)

import base64

#open the Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
#3 dòng trên là để mở cửa sổ mãi không đóng, 1 cách làm hay từ stackoverflow
#Nếu viết như này : driver = webdriver.Chrome('chromedriver.exe') thì nó sẽ không chạy

#open the link
#mở đường link
driver.get("https://vav.unob.cz/departments/index")
sleep(8)

# print(base64.b64encode("password".encode("utf-8")))
# print(base64.b64decode("cGFzc3dvcmQ=").decode("utf-8"))

#Login part (decrypt login information in infor.txt)
infor = open('infor.txt')
lines=infor.readlines()
username=base64.b64decode(lines[0]).decode("utf-8")
password=base64.b64decode(lines[1]).decode("utf-8")


try:
    username_field=driver.find_element(By.ID,"username")
    username_field.send_keys(username)
    sleep(1)
    password_field=driver.find_element(By.ID,"password")
    password_field.send_keys(password)
    sleep(1)
    signin_field = driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/form/fieldset/div[4]/input")
    signin_field.click()
    sleep(1)
except NoSuchElementException:
    print("exception handled")




#1 Get links Katedry
department_links=[]
department_elems = driver.find_elements(By.CSS_SELECTOR," [width='70px'] [href]")
department_links = [department_elem.get_attribute("href") for department_elem in department_elems]
#1

# for department_elem in department_elems:
#     department_link = department_elem.get_dom_attribute("href")
#     if department_link not in department_links:
#         department_links.append(department_link)

#đã lấy xong

#function to get the links of each teacher in one department
#hàm lấy link giáo viên ở 1 department
def get_teacher_links_one_department(link_department):
    driver.get(link_department)
    sleep(2)
    table_actual_teacher=driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[3]/div[2]/div/div/div/div[3]/table[1]")
    teacher_elems=table_actual_teacher.find_elements(By.CSS_SELECTOR, "[style*='width: 150px; line-height: 16px; vertical-align: middle'] [href]")
    teacher_links = [teacher_elem.get_attribute("href") for teacher_elem in teacher_elems]
    return teacher_links

#Get all the links of all teachers and write to teacherlinks.txt
#1 lấy hết các links giáo viên và viết vào teacherlinks.txt
teacher_links = []
for department_link in department_links:
    teacher_links_1_department = get_teacher_links_one_department(department_link)
    teacher_links=teacher_links+teacher_links_1_department

if os.stat('teacherlinks.txt').st_size == 0:
    print('The file is empty')
    with open("teacherlinks.txt","w") as file_teacher_links:
        file_teacher_links.writelines("\n".join(teacher_links))
    
else:
    print('The file is not empty')

#1


# driver.get(f"https://{username}:{password}@apl.unob.cz/UOAPI/Rozvrhy/Osoba/243")

#function to get CLASSES for teachers
#hàm lấy lớp học cho giáo viên
def get_classes(link_rozvrhy):
    path=link_rozvrhy.replace("https://", "")
    link_rozvrhy_popup = "https://" + username + ":" + password + "@" + path
    driver.get(link_rozvrhy_popup) #xử lý pop-up thông báo
    sleep(2)
    total_lessons = len(driver.find_elements(By.CSS_SELECTOR,"tr"))
    classes = []
    for i in range(1,total_lessons):
        classes_lesson = driver.find_element(By.XPATH,f"/html/body/table/tbody/tr[{i}]/td[10]").text.split(",")
        for class_elem in classes_lesson:
            if class_elem not in classes:
                classes.append(class_elem)
          
    return classes

#fuction to get INFORMATION of each teacher
#và bây giờ là lấy thông tin 1 giáo viên / hàm lấy thông tin giáo viên
def infor_teacher(teacher_link):
    driver.get(teacher_link)
    sleep(2)
    teacher = {}
    teacher["name"]=driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[3]/div[2]/div/div/div/div[3]/h1").text.split("(")[0].strip()
    teacher["department"]=driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[3]/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]").text
    teacher["titles"]=driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[3]/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]").text
    teacher["telephones"]=driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[3]/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]").text.split(",")
    teacher["email"]=driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[3]/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]").text
    teacher["office"]=driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[3]/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[2]/td/table/tbody/tr[5]/td[2]").text
    try:
        teacher_link_rozvrhy=driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[3]/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]/a").get_attribute("href")
        teacher["classes"]= get_classes(teacher_link_rozvrhy)
    except NoSuchElementException:
        teacher["classes"]= []
    
    
    return teacher


#1 lấy toàn bộ thông tin giáo viên khi chưa có links gì/ lần đầu
# teachers_data=[]
# for teacher_link in teacher_links:
#     teacher_infor=infor_teacher(teacher_link)
#     teachers_data.append(teacher_infor)
#1

#Get teachers' informations
#1 lấy toàn bộ thông tin giáo viên khi đã có links trong txt
total_links = open('teacherlinks.txt')
teacher_links_in_file=total_links.readlines()
teachers_data=[]
for teacher_link in teacher_links_in_file:
    teacher_infor=infor_teacher(teacher_link)
    teachers_data.append(teacher_infor)
#1

#Viết thông tin vào teacherdata.txt
# with open("teacherdata.txt","w", encoding='utf-8') as f_t:
#     for teacher_data in teachers_data:
#         f_t.write(str(teacher_data) + '\n')

#write data to teacherdata.txt
#1Viết thông tin vào teacherdata.txt nhưng đẹp hơn       
with open("teacherdata.txt", "w", encoding="utf-8") as f:
    json.dump(teachers_data, f, indent = 4, ensure_ascii = False)   
#1

#write data to teacherdatas.json
#1 viết vào file json
with open("teacherdatas.json", "w", encoding="utf-8") as f:
    json.dump(teachers_data, f, indent = 4, ensure_ascii = False)
#1

#Write data to mongoDB
# Đọc dữ liệu từ file JSON và ghi vào mongoDB
with open("teacherdatas.json", "r",encoding="utf-8") as file:
    dat = json.load(file)

#connect to MOngoDB server
# Kết nối đến cơ sở dữ liệu MongoDB
client = MongoClient("mongodb+srv://hieu-daren:19052000Hieu@clusterhieu.6lbtk6j.mongodb.net/?retryWrites=true&w=majority")
# Lấy database mong muốn từ client
db = client["hieu1-csdl"]  
# Lấy collection mong muốn từ database
collection = db["teachers"] 

#add documents to collection
# Thêm danh sách "a" vào collection
if isinstance(dat, list):
    collection.insert_many(dat)
else:
    collection.insert_one(dat)

#close connect
# Đóng kết nối tới cơ sở dữ liệu MongoDB
client.close()
driver.quit()


