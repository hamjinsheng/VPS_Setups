# -*- coding:utf-8 -*-
import random
import string
import subprocess
import sys,random

def install_docker():
    '''
    判断系统内核，安装docker
    :return:
    '''
    output = subprocess.getoutput('which docker')
    if len(output) < 2 or 'no docker' in output:
        print('正在安装docker中.......')
        output = subprocess.getoutput('lsb_release -a')
        if 'CentOS' in output:
            print('您的系统为：CentOS')
            docker_shell = 'yum install -y yum-utils device-mapper-persistent-data lvm2 &&' \
                           'yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo &&' \
                           'yum makecache fast &&' \
                           'yum install docker-ce -y'
            output = subprocess.getoutput(docker_shell)
        elif 'Ubuntu' in output:
            print('您的系统为：Ubuntu')
            docker_shell='apt-get update &&' \
                         'apt-get -y install apt-transport-https ca-certificates curl software-properties-common &&' \
                         'curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add - &&' \
                         'add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" &&' \
                         'apt-get  update &&' \
                         'apt-get -y install docker-ce'
        else:
            docker_shell ='apt-get -y install docker-ce && yum install docker-ce -y'
        output = subprocess.getoutput(docker_shell)
        subprocess.getoutput('systemctl enable docker && systemctl start docker && systemctl status docker')
        print("成功安装docker，正在安装CVNT------------>")
    else:
        print("您已经安装过docker了，无须安装，正在安装CVNT------------>")
def pull_docker():
    images_status = subprocess.getoutput("docker images|grep reg|awk '{print $(NF-6)}'")
    if images_status == "registry.cn-hangzhou.aliyuncs.com/cs_work/cvnt_work":
        print("已存在，跳过pull")
        return
    Change_docker_Source="sudo tee /etc/docker/daemon.json <<-'EOF'\n" \
                         "{\n" \
                         "  \"registry-mirrors\": [\"https://o4hd5pcr.mirror.aliyuncs.com\"]\n" \
                         "}\n" \
                         "EOF\n" \
                         "sudo systemctl daemon-reload\n" \
                         "sudo systemctl restart docker\n"
    subprocess.getoutput(Change_docker_Source)
    print("成功修改docker源......正在获取镜像.....请耐心等待几分钟......")
    output=subprocess.getoutput("docker pull registry.cn-hangzhou.aliyuncs.com/cs_work/cvnt_work:v1.0.0")
    print("正在拉取镜像，请勿动.........勿动...........")
    print("正在拉取镜像，请勿动.........勿动...........//")
    print("容器Images为：%s"%output)

def randomMAC():
    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def install_cvnt(docker_num,cvnt_uid,mount_dev):
    name_num = 45
    port_web = 60177
    port_list=[]
    for i in range(docker_num):
        if mount_dev == '':
            dokcer_mount = ''
        else:
            tmp_name = 'cvnt' + str(name_num)
            dir_name = mount_dev + '/' + tmp_name
            subprocess.getoutput(r'mkdir -p %s' % dir_name)
            dokcer_mount = r' -v %s:%s' % (dir_name, dir_name)
        mac = randomMAC()
        container_name = "cvnt{}".format(name_num)
        a = port_web + 1
        b = port_web + 2
        c = port_web + 3
        port_list.append(port_web)
        run_container = "docker run -d -it --name {}{} --restart=always " \
                        " --net bridge --mac-address {} -p " \
                        "{}:10000 -p {}:59606 -p {}:59608 -p {}:59843 " \
                        "-h {} " \
                        " registry.cn-hangzhou.aliyuncs.com/cs_work/cvnt_work:v1.0.0 ".format(container_name,dokcer_mount, mac, port_web,
                                                                                          a, b, c, container_name)
        # print(run_container,22222222222222222)
        container_Id = subprocess.getoutput(run_container)
        start_cvnt = r'docker exec %s bash -c "cd /usr/local/yyets_20190923/;cd conf;' \
                     r"echo -e '#本地账户信息\nuid       = %d\n# 登录后的token-系统生成\nsys_token =' > " \
                     r'user.conf;' \
                     r"echo -e 'nameserver 114.114.114.114\nnameserver 101.226.4.6 ' > /etc/resolv.conf;" \
                     r'cd /usr/local/yyets_20190923/;./install.sh start;"' % (container_Id,cvnt_uid)
        result=subprocess.getoutput(start_cvnt)
        print(result)

        port_web = c
        port_web += 1
        name_num += 1
    return port_list
def Check_input():
    input_check = "sucess"
    docker_num=0
    cvnt_uid=0
    try:
        docker_num=sys.argv[1]
        cvnt_uid = sys.argv[2]
    except Exception as e:
        print('请输入大于0的整数,如python3 installCvnt_open.py 3 123456               解释：其中3为虚拟个数,123456为UID')
        input_check='error'
    try:
        mount_dev = sys.argv[3]
    except Exception as fe:
        mount_dev=''
    try:
        docker_num=int(docker_num)
        cvnt_uid=int(cvnt_uid)
    except Exception as e:
        input_check="请输入大于0的整数,如python3 installCvnt_open.py 3 123456        解释：其中3为虚拟个数,123456为UID"
        input_check = 'error'
    if int(docker_num) == 0 or int(cvnt_uid)==0:
        input_check = "请输入大于0的整数,如python3 installCvnt_open.py 3 123456      解释：其中3为虚拟个数,123456为UID"
        input_check = 'error'
    return input_check,docker_num,cvnt_uid,mount_dev

def start_program():
    status,docker_num,cvnt_uid,mount_dev=Check_input()
    if status=='error':
        return
    print("输入正确----")
    install_docker()
    pull_docker()
    port_list=install_cvnt(docker_num,cvnt_uid,mount_dev)
    return port_list

port_list=start_program()
print(port_list)

