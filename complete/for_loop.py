import os
# read the csv file exp file:csv_example new csv file:csv_examples
import csv
import random,string
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sender_email = "158120.Moodle@gmail.com"
password = "moodle123"

os.system("sudo pip3 install pandas")
print("panas install finished")

import pandas as pd
import pymysql


with open('StudentData.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        # create empty list
        list_of_students = []
        # for each student, append as list to list (list of lists)
        for row in reader:
                list_of_students.append(row)
                # Remove metadata from top row
        list_of_students.pop(0)
n=10000
m=1000000
num=len(list_of_students)
s = string.ascii_lowercase
adr=[]
pas=[]
pasftp=[]
for i in range(100000,999999):
    pasftp.append(i)
pasftp=random.sample(pasftp,len(list_of_students))
for i in random.sample(range(1,n),n-1):
    if len(str(i))>=4 and len(adr)<num:
        adr.append(str(i)+random.choice(s))
for i in random.sample(range(1,m),m-1):
    if len(str(i))>=6 and len(pas)<num:
        pas.append(str(i))
data = pd.read_csv(r'StudentData.csv')
data1 = adr
data2 = pas
data3 = pasftp
data['moodle_name'] = data1
data['password'] = data2
data['ftppassword'] = data3
data.to_csv(r"StudentDatas.csv",mode = 'a',index =False)
with open('StudentDatas.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        # create empty list
        list_of_students = []
        # for each student, append as list to list (list of lists)
        for row in reader:
                list_of_students.append(row)
                # Remove metadata from top row
        list_of_students.pop(0)



print("new csv file finish")



# find external ip
r = os.popen("curl ifconfig.me")
ip = r.read()
r.close()


os.chdir('/etc/mysql/')
os.system("sudo chmod o+w debian.cnf")
os.system("sudo chmod o+r debian.cnf")

data=""
pwdfile = open('/etc/mysql/debian.cnf',"r")
pwdcontent = pwdfile.read()

pos = pwdcontent.find("[mysql_upgrade]\nhost     = localhost")
lenth=len('[mysql_upgrade]\nhost     = localhost')
UAP=(pwdcontent[pos+lenth:])

pos_user=UAP.find('user     = ')
pos_pwd=UAP.find('password = ')
pos_socket=UAP.find('socket')

TopUser=UAP[pos_user+len('user     = '):pos_pwd].strip()
TopPwd=UAP[pos_pwd+len('password = '):pos_socket].strip()

os.system("sudo chmod o-w debian.cnf")
os.system("sudo chmod o-r debian.cnf")
print("top pwd find finish",TopUser,TopPwd)



conn = pymysql.connect(host='127.0.0.1',port=3306, user=TopUser,passwd=TopPwd)
cursor=conn.cursor()



print(list_of_students)
os.chdir("/var")
for i in list_of_students:
        if os.path.exists("data"+str(i[0])) or i[0]=="student id":
            print("exits data%s"%(i[0]))
        else:
                str1="create database student%s default character set utf8 collate utf8_general_ci;"%i[0]
                print(str1)
                SQLcmd1=cursor.execute(str1)
                str2="create user %s@'%%' identified by '%s';"%(i[4],i[5])
                print(str2)
                SQLcmd3=cursor.execute(str2)
                str3="GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,CREATE TEMPORARY TABLES,DROP,INDEX,ALTER ON student%s.* TO %s@'%%' IDENTIFIED BY '%s';"%(i[0],i[4],i[5])
                SQLcmd4=cursor.execute(str3)
                SQLcmd6=cursor.execute("flush privileges;")
conn.commit()
cursor.close()
conn.close()
print("create mysql user finished")




count=0
for i in list_of_students:
        os.system("sudo cp -R /opt/moodle /var/www/html/"+str(i[4]))


        os.chdir("/var")
        if os.path.exists("data"+str(i[0])) or i[0]=="student id":
            print("exits")
        else:

            os.system("mkdir data"+str(i[0]))

            os.chdir("/var/www/html/")

            os.system("sudo chown -R www-data /var/data"+str(i[0]))
            os.system("sudo chmod -R 777 /var/data"+str(i[0]))
            os.chdir("/var/www/html/")
            os.chmod(str(i[4]),777)
            os.chdir(str(i[4]))
            if os.path.isfile("config.php"):
                    os.system("rm -rf config.php")

            os.system("touch config.php ")
            data="<?php  // Moodle configuration file\n" \
                    "unset($CFG);\n" \
                    "global $CFG;\n" \
                    "$CFG = new stdClass();\n" \
                    "$CFG->dbtype    = 'mysqli';\n" \
                    "$CFG->dblibrary = 'native';\n" \
                    "$CFG->dbhost    = 'localhost';\n" \
                    "$CFG->dbname    = 'student"+str(i[0])+"';\n" \
                    "$CFG->dbuser    = '"+str(i[4])+"';\n" \
                    "$CFG->dbpass    = '"+str(i[5])+"';\n" \
                    "$CFG->prefix    = 'mdl_';\n" \
                    "$CFG->dboptions = array (\n" \
                    "  'dbpersist' => 0,\n" \
                    "  'dbport' => '',\n" \
                    "  'dbsocket' => '',\n" \
                    "  'dbcollation' => 'utf8mb4_unicode_ci',\n" \
                    ");\n" \
                    "$CFG->wwwroot   = 'http://"+str(ip)+"/"+str(i[4])+"';\n" \
                    "$CFG->dataroot  = '/var/data"+str(i[0])+"';\n" \
                    "$CFG->admin     = 'admin';\n" \
                    "$CFG->directorypermissions = 0777;\n" \
                    "require_once(__DIR__ . '/lib/setup.php');\n"
            content = data
            file = open('config.php', "w")
            file.write(content)
            file.close()

            os.system("useradd -m %s"%(i[0]))
            os.system("echo %s:%s| chpasswd"%(i[0],str(i[6])))
            os.system("chown -R %s:%s /var/www/html/%s"%(i[0],i[0],i[4]))
            os.system("chmod -R 777 /home/%s"%(i[0]))

            os.system("touch /etc/userconfig/"+i[0])

            user = open("/etc/userconfig/"+i[0], "w")
            user.write("local_root=/var/www/html/"+i[4])

            user.close()
            count=count+1
            os.system("sudo chmod -R 777 /var/www/html")
            print("loop finish for data%s"%(i[0]))

            #send an email with user login info
            message = MIMEMultipart("alternative")
            message["Subject"] = "Moodle account information"
            message["From"] = sender_email
            message["To"] = str(i[3])


            text = """
                FTP server login information:
                Username: """ + str(i[0]) + """
                Password: """ + str(i[6]) + """
                phpMyAdmin login information:
                Username: """ + str(i[4]) + """
                Password: """ + str(i[5])+ """
                Access your Moodle site through this URL:"""+ 'http://'+str(ip)+'/'+str(i[4])

            part1 = MIMEText(text, "plain")
            message.attach(part1)
            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(
                            sender_email, str(i[3]), message.as_string()
            )