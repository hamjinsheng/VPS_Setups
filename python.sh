#!/bin/bash
cat /etc/lsb-release >/dev/null 2>&1
str=`echo $?`
python3.6 --version >/dev/null 2>&1
str1=`echo $?`
#判断是否已经安装python3.6
if [ $str1 -ne 0 ]; then
    #判断当前系统为ubuntu还是centos
    if [ $str -eq 0 ]; then
        #ubuntu下安装
        apt-get update >/dev/null
        echo "正在安装软件依赖包，请稍等。。"
        #安装依赖包
        apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev build-essential checkinstall >/dev/null
        cd /usr/local
        #下载python源码包
        wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz >/dev/null
        #解压源码包
        echo "正在安装编译软件，请勿动"
        tar -zxvf Python-3.6.6.tgz >/dev/null
        cd Python-3.6.6
        #编译安装
        ./configure --prefix=/usr/local/python3 >/dev/null
        make && make install >/dev/null
        #做软连接,可以直接使用命令
        rm /usr/bin/python3
        ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3
        ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3.6
        ln -s /usr/local/python3/bin/pip3.6 /usr/bin/pip3
        cp /usr/lib/python3/dist-packages/lsb_release.py /usr/local/python3/lib/python3.6/ >/dev/null
        echo "软件安装成功"
    else
        #centos下安装
        yum repolist
        #安装依赖包
        echo "正在安装软件依赖包，请稍等。。"
        yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make >/dev/null
        cd /usr/local/
        #下载python源码包
        wget http://mirrors.sohu.com/python/3.6.0/Python-3.6.0.tgz >/dev/null
        #解压源码包 
        echo "正在安装编译软件，请勿动"
        tar -zxvf Python-3.6.0.tgz >/dev/null
        cd Python-3.6.0/
        #编译安装
        ./configure --prefix=/usr/local/python3 >/dev/null
        make && make install >/dev/null
        cd /usr/local/python3/
        #做软连接,可以直接使用命令
        ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
        rm /usr/bin/python3
        ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3
        ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3.6
        cp /usr/lib/python3/dist-packages/lsb_release.py /usr/local/python3/lib/python3.6/ >/dev/null
        echo "软件安装成功"
    fi
else
    echo "python3.6 已经安装"
fi
