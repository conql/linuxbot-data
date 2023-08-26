import re

text = """
1、以长格式列目录时，若文件test的权限描述为：drwxrw-r–，则文件test的类型及文件主的权限是__A____。

A.目录文件、读写执行 B.目录文件、读写 C.普通文件、读写 D.普通文件、读

2、当字符串用单引号（’’）括起来时，SHELL将__C____。

A.解释引号内的特殊字符 B.执行引号中的命令 C.不解释引号内的特殊字符 D.结束进程

3、/etc/shadow文件中存放_B_____。

A.用户账号基本信息 B.用户口令的加密信息 C.用户组信息 D.文件系统信息

4、Linux系统中，用户文件描述符 0 表示____A__。

A.标准输入设备文件描述符 B.标准输出设备文件描述符 C.管道文件描述符 D.标准错误输出设备文件描述符

5、为卸载一个软件包，应使用___B__。

A.rpm -i B.rpm -e C.rpm -q D.rpm -V

6、若当前目录为 /home,命令 ls–l 将显示 home 目录下的（ D ）。

A.所有文件 B.所有隐含文件 C.所有非隐含文件 D.文件的具体信息

7、下面关于文件 “/etc/sysconfig/network-scripts/ifcfg-eth0” 的描述哪个是正确的?( D )。

A.它是一个系统脚本文件 B.它是可执行文件

C.它存放本机的名字 D.它指定本机eth0的IP地址

8、如何快速切换到用户John的主目录下？( D)

A.cd @John B.cd #John C.cd &John D.cd ~John
"""

# Split the text into questions
questions = re.split(r"\n\d+、", text)

for i, question in enumerate(questions[1:], start=1):
    # Extract the answer
    answer = re.search(r"[_（]\s*([A-D])\s*[_）]", question)
    if answer:
        answer = answer.group(1)
        # Remove the answer from the question
        cleaned_question = re.sub(r"[_（]\s*[A-D]\s*[_）]", "___", question)
        print(f"{i}、{cleaned_question}")
        print(f"正确答案：{answer}\n")
