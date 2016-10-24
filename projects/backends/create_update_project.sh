#!/bin/bash

function cpjetty()
{
    cp /mnt/jetty-distribution-9.2.9.v20150224.tar.gz /data/webapp/
    cd /data/webapp/ && tar xf jetty-distribution-9.2.9.v20150224.tar.gz
}

function judge_tar_dis()
{
if [ -e "/data/webapp/jetty-distribution-9.2.9.v20150224.tar.gz" ]; then
    cd /data/webapp/ && tar xf jetty-distribution-9.2.9.v20150224.tar.gz
else
    mount|grep -w "//10.249.152.137/user on /mnt" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        cpjetty
    else
        ping -c 1 -w 1 10.249.152.137 > /dev/null 2>&1
        if [ ! $? -eq 0 ]; then
            echo "ping samba server fail"
            exit 1
        fi
        mount -t cifs //10.249.152.137/user /mnt/ -o username=user,password=sambauser,iocharset=utf8
        cpjetty    
    fi
fi
}

function conf()
{
    if [ -e "$CONFIG_FILE" ]; then
        #sed -i "s%^db.url.master=.*%db.url.master=jdbc:mysql://$mysql_server:3306/$mysql_database?characterEncoding=utf8%" $1
        #sed -i "s%^db.url.slave=.*%db.url.slave=jdbc:mysql://$mysql_server:3306/$mysql_database?characterEncoding=utf8%" $1
        sed -ir "s/jdbc:mysql:\/\/\([0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\):3306\/.*?/jdbc:mysql:\/\/${mysql_server}:3306\/$mysql_database?/" $1
        sed -i "s%^db.user=.*%db.user=$mysql_user%" $1
        sed -i "s%^db.pass=.*%db.pass=$mysql_passwd%" $1
        sed -i "s%^memcache.address=.*%memcache.address=$mem_server:$mem_port%" $1
        #sed -i "s%^jdbc.url=.*%jdbc.url=jdbc:mysql://$mysql_server:3306/$mysql_database?characterEncoding=utf8%" $1
        sed -i "s%^jdbc.username=.*%jdbc.username=$mysql_user%" $1
        sed -i "s%^jdbc.password=.*%jdbc.password=$mysql_passwd%" $1
    else
        echo ""$CONFIG_FILE" Modify fail!! configure file is not exist or more then one! Please manual modify!!"
        #exit 1
    fi
}

function checkfw()
{
iptables -nL | grep ":$project_port" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "Port $project_port OK"
else
    PNR=`awk '{for(i=1;i<=NF;i++)if($i~/^[0-9]*[1-9][0-9]*$/) for(t=1;t<=NF;t++)if($t~/tcp/) for(k=1;k<=NF;k++)if($k~/INPUT/) for(a=1;a<=NF;a++)if($a~/ACCEPT/) if('$project_port'-$i<0 && $t=="tcp" && $k=="INPUT" && $a=="ACCEPT") print NR}' /etc/sysconfig/iptables |head -1`
    if [ ! $PNR ]; then
        echo "Add port fail! Check ports greater than $project_port in /etc/sysconif/iptables "
        exit 1
    fi
    sed -i ''$PNR'i -A INPUT -m state --state NEW -m tcp -p tcp --dport '$project_port' -j ACCEPT' /etc/sysconfig/iptables
    iptables-restore </etc/sysconfig/iptables
    iptables -nL | grep ":$project_port" > /dev/null 2>&1
    if [ ! $? -eq 0 ]; then
        echo -e "Add port $project_port fail!"
    else
        echo -e "Add port $project_port succeed!"
    fi
fi
}

function checkmysql()
{
    mysqllogin=`mysql -h${mysql_server} -u${mysql_user} -p${mysql_passwd} -e 'show databases;' 2>/dev/null | grep -w "$mysql_database" | grep -v 'Access denied'`
    if [[ $mysqllogin = $mysql_database ]] ;then
		echo -e "Mysql OK"
    else
		echo -e "Mysql not OK"
    fi
}

function checkmem()
{
    /usr/bin/which nc > /dev/null 2>&1
    if [ ! $? -eq 0 ];then
        yum install nc -y > /dev/null 2>&1
		if [ ! $? -eq 0 ]; then
			echo "The nc install fail! Check memcached fail!"
			return 1
		fi
    fi
    
    if [[ -n `nc -vw 2 ${mem_server} -z ${mem_port} 2>/dev/null | grep -w 'succeeded!'` ]] ;then
    	echo -e "Mem Ok"
    else
    	echo -e "Mem not OK"
    fi
}

function deploywar()
{
    echo "********************************************************"
    echo -e "Ready for <<<Deploy>>> project!"

    cd $PROJECT_PATH/webapps/$project_name
    jar xf /root/$project_name.war
    dirpro=`ls $PROJECT_PATH/webapps/$project_name`
    if [ -z "$dirpro" ]; then
        echo Unpack has failure! check your compressed package!
        exit 1
    fi
    sed -i "s/^jetty.port=.*/jetty.port=$project_port/" $PROJECT_PATH/start.ini

    if [ ! $CONFIG_FILE ]; then
        echo "Hint!!: Variable PROJECT_PATH is null,please manually modify the configuration file!"
    else
        conf $CONFIG_FILE
    fi

    id jetty > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        useradd -u 502 jetty
    fi
    chown -R jetty:jetty $PROJECT_PATH
    checkfw
    #checkmysql
    #checkmem
}

function startproject()
{    
    #echo -en "To \033[0;32;25mStart\033[0m the project? [y/n]:"
    #read char
    #if [ $char == y ]; then
    echo "******************Start project info********************"
    /data/webapp/jetty-root.sh start $project_title

    #fi
}

function whdeploypj()
{    
    echo -en "Make sure Deploy the project? [y/n]:"
    read char
    if [ $char != y ]; then
        exit 1
    fi
}

function whupdatepj()
{    
    echo -en "Make sure Update the project? [y/n]:"
    read char
    if [ $char != y ]; then
        exit 1
    fi
}

function checkmount()
{
	if [ ! $mount_s -o ! $mount_d ]; then
		echo "The project no mount!"
	else
		case $1 in
			myumount)
				umount $mount_d
				if [ ! $? -eq 0 ]; then
					echo "umount $mount_d failed!"
					exit 1
				else
					echo "umount $mount_d succeed!"
					sleep 1
				fi
			;;
			mymount)
				mount -t nfs $mount_s $mount_d
				if [ ! $? -eq 0 ]; then
					echo "mount $mount_s failed!"
					exit 1
				else
					echo "mount $mount_s succeed!"
					sleep 1
				fi
			;;
		esac
	fi
}

function updatepj()
{
    echo "********************************************************"
    echo -e "Ready for <<<Update>>> project!"
    echo "******************stop project info*********************"
    /data/webapp/jetty-root.sh stop $project_title

    sleep 1
	checkmount myumount
    cd $PROJECT_PATH/webapps/
    if [[ ! $CONFIG_FILE ]]; then
        echo "Hint!!: Variable CONFIG_FILE is empty,configure file haven't backup!"
    else
        if [ -d "/tmp/$project_name" ]; then
            /bin/cp -rf ${CONFIG_FILE} /tmp/$project_name/
            if [ ! $? -eq 0 ]; then
                echo "Copy configure file to /tmp/$project_name/ failed!"
                exit 1
            fi
        else
            mkdir /tmp/$project_name
            /bin/cp -rf ${CONFIG_FILE} /tmp/$project_name/
            if [ ! $? -eq 0 ]; then
                echo "Copy configure file to /tmp/$project_name/ failed!"
                exit 1
            fi
        fi
    fi

    if [ ! -d "/data/backup" ]; then
        mkdir -p /data/backup
    fi
    /bin/mv $project_name /data/backup/$project_name'_'`date +"%Y-%m-%d_%H%M"`
    if [ ! $? -eq 0 ]; then
        exit 1
    fi

    mkdir $project_name
    if [ ! $? -eq 0 ]; then
        exit 1
    fi
    cd $project_name
    jar xf /root/$project_name.war
    dirpj=`ls $PROJECT_PATH/webapps/$project_name`
    if [ -z "$dirpj" ]; then
        echo "Unpack has failure! check your compressed package!"
        exit 1
    fi

    if [[ ! $CONFIG_FILE ]]; then
        echo "Hint!!: Variable CONFIG_FILE is empty,configure file haven't recopy!"
    else
        /bin/cp -rf /tmp/$project_name/${CONFIG_FILE##*/} ${CONFIG_FILE%/*}/
        if [ ! $? -eq 0 ]; then
            echo "ReCopy configure file from /tmp/$project_name/ has failed! Please manually copy!"
        fi
    fi
    chown -R jetty:jetty $PROJECT_PATH
    checkmount mymount
    checkfw
    #checkmysql
    #checkmem
}

function printinfo()
{
	echo "################################################################################"
    echo "Project path: $PROJECT_PATH"
    echo "mysql info  : $mysql_server $mysql_database $mysql_user $mysql_passwd"
    echo "memcached   : $mem_server:$mem_port"
    echo "################################################################################"
}

function checkjettysh()
{
    if [ ! -f "/data/webapp/jetty-root.sh" ]; then		#判断jetty启动脚本是否存在
        echo "Please check the /data/webapp/jetty-root.sh is exist!"
        exit 1
    else
        chmod a+x /data/webapp/jetty-root.sh
    fi
}

if [ $# != 1 ] ; then		#参数检测
    echo "create_project.sh: at least 1 parameters"
    echo "Syntax: create_project.sh [Project_ID]"
    exit 1;
fi

project_title=${1}
project_info=${2}
project_name=${3}
project_port=${4}
mysql_server=${5}
mysql_database=${6}
mysql_user=${7}
mysql_passwd=${8}
mem_server=${9}
mem_port=${10}
PROJECT_PATH=${11}
CONFIG_FILE=${12}

mount_s=`cat /proc/mounts |grep $PROJECT_PATH|awk '{print $1}'`
mount_d=`cat /proc/mounts |grep $PROJECT_PATH|awk '{print $2}'`

checkjettysh
/bin/cp /mnt/$project_name.war /root/
if [ ! $? -eq 0 ]; then
    echo "Copy $project_name.war failed! Make sure /mnt has mounted or $project_name.war is exist! "
    exit 1
fi

if [ -e "/root/$project_name.war" ]; then	#判断war包是否存在
    if [ ! -d "$PROJECT_PATH" ]; then		#判断项目路径是否存在 如：/data/webapp/jetty-bjjc
        judge_tar_dis				#判断jetty-distribution是否存在，并准备好jetty实例目录
        cp -r /data/webapp/jetty-distribution-9.2.9.v20150224 $PROJECT_PATH
        rm -f $PROJECT_PATH/webapps/README.TXT
    fi

    if [ -d "$PROJECT_PATH/webapps/$project_name" ]; then	#判断项目根目录是否存在
        dir=`ls $PROJECT_PATH/webapps/$project_name`		#判断项目根目录是否为空
        if [ -z "$dir" ]; then
			#whdeploypj
            deploywar        #部署项目
            startproject
            #printinfo
        else
			#whupdatepj
            updatepj         #更新项目
            startproject
            #printinfo
        fi
    else
		#whdeploypj
        mkdir $PROJECT_PATH/webapps/$project_name > /dev/null 2>&1      #创建目录后部署
        deploywar            #部署项目
        startproject
        #printinfo
    fi
    rm -f /root/$project_name.war
else
    echo "Please check $project_name.war in /root/ path!"
fi