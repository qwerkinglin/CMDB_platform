#!/usr/bin/env python
#^v^! coding: utf-8 ^v^!
__author__ = 'Alex hao'

import commands,re,socket,sys
from multiprocessing import Pool

def check_socket(ip,port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.settimeout(1)
    try:
      skt.connect((ip,port))
      return 'connection success'
    except Exception:
      return 'connection fail'
    skt.close()

def get_jetty_port(startini_path):
    startini_path_full = startini_path+'start.ini'
    port_status = commands.getstatusoutput('ls '+ startini_path_full)
    if port_status[0] == 0:
        jetty_port_word = commands.getstatusoutput('cat '+ startini_path_full +"|grep ^jetty.port=[0-9]")
        jetty_port_num = jetty_port_word[1].split('=')
        if jetty_port_word[0] == 0:
            return jetty_port_num[1]
        else:
            return '"jetty.port="_not exist'
    else:
        return 'start.ini_not_exist'

def if_None(key_words):
    if not key_words:
        key_words = "None"
        return key_words
    else:
        return key_words
        
def fill_match_dict(match_dict_check):
    key_list = ['mysqlHost','mysqlDBName','mysqlUser','mysqlPasswd','memHost','memPort','memNameSpace','debug_status']
    for keyword in key_list:
        if keyword not in match_dict_check.keys():
            match_dict_check[keyword] = ""

def app_status(jetty_path): 
    appstatus = commands.getstatusoutput('ps -ef|grep -v "grep"|grep '+jetty_path)
    if appstatus[0] == 0:
        return "running"
        #return "\033[0;32;25mrunning\033[0m"
    else:
        return "stopped"
        #return "\033[0;31;25mstopped\033[0m"

def mysql_check(db_ip,db_name,db_user,db_pd):
    if db_ip == "None" or db_name == "None" or db_user == "None" or db_pd == "None":        
        return 'NoneDB'
        #return '\033[0;32;25mNonDB\033[0m'
    else:
        conn_status = check_socket(db_ip,3306)
        if conn_status == "connection success":
            status = commands.getstatusoutput('mysql -u'+db_user+' -p'+db_pd+' -h'+db_ip+' -e "show databases;"|grep -w '+db_name+' |grep -v "Access denied"')
            if status[0] == 0:
                return "DB.OK"
                #return "\033[0;32;25mDB.OK\033[0m"                
            else:
                return "DB.ER"
                #return "\033[0;31;25mDB.ER\033[0m"
        else:
            return "DB.conER"
            #return "\033[0;31;25mDB.conER\033[0m"

def mem_check(memip,memport):
    if memip == "None" or memport == "None":
        return 'NonMEM'
        #return '\033[0;32;25mNonMEM\033[0m'
    else:
        memport = int(memport)
        conn_status = check_socket(memip,memport)
        if conn_status == "connection success":
            return 'Mem.OK'
            #return '\033[0;32;25mMEM.OK\033[0m'
        else:
            return 'Mem.ER'
            #return '\033[0;31;25mMEM.ER\033[0m'

def jettyport_check(jetty_port):
    jetty_port = int(jetty_port)
    jettyport_status = check_socket('127.0.0.1',jetty_port)
    if jettyport_status == "connection success":
        return "Port.OK"
        #return "\033[0;32;25mPort.OK\033[0m"
    else:
        return "Port.ER"
        #return "\033[0;31;25mPort.ER\033[0m"

def fire_wall_check(jetty_port):
    fire_wall_status = commands.getstatusoutput('iptables -nL |grep :'+jetty_port)
    if fire_wall_status[0] == 0:
        return "Fw.OK"
        #return "\033[0;32;25mFw.OK\033[0m"
    else:
        return "Fw.ER"
        #return "\033[0;31;25mFw.ER\033[0m"
            
def multi_process(k,v,t,jetty_name_ch,root_name_ch):
    jetty_dirs_dict_key = k
    jetty_dirs_dict_value = v
    config_template = t
    if jetty_dirs_dict_value[0] == 0:
        jetty_title = re.split('[/]',jetty_dirs_dict_key)[3]
        jetty_port = get_jetty_port(jetty_dirs_dict_key)
        sub_dir_list = jetty_dirs_dict_value[1].split('\n')
        app_status_result = app_status(jetty_dirs_dict_key)
        jetty_port_status = jettyport_check(jetty_port)
        fw_status = fire_wall_check(jetty_port)
        for sub_dir in sub_dir_list:
            for conf_path,conf_keyword in config_template.iteritems():
                configfile_check_list = commands.getstatusoutput('ls '+jetty_dirs_dict_key+'webapps/'+sub_dir+'/'+conf_path)
                if configfile_check_list[0] == 0:
                    conf_path_status = configfile_check_list[1]
                    conf_keyword_list = conf_keyword
                    break
                else:
                    conf_path_status = "conf_unknow"
            if conf_path_status != "conf_unknow":
                match_dict = {}
                f = open(conf_path_status,'rb')
                for conf_line in f.readlines():
                   conf_line=conf_line.strip()
                   for k, v in conf_keyword_list.iteritems():
                       for match_item in v:
                           match = re.search("^" + match_item + "(.*)", conf_line)
                           if match:
                               match_value = match.group(1)
                               match_dict[k] = match_value
                               break
                f.close()
                fill_match_dict(match_dict)     #fill the matched dict for all info                               
                mysql_host = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', match_dict['mysqlHost'])   #mysql host fill the value
                if mysql_host:
                    mysql_host = mysql_host.group()
                else:
                    mysql_host = "None"                    
                mysql_DbName = re.search('\d+\/(.*?)\?',match_dict['mysqlHost'])    #mysql database name  fill the value
                if mysql_DbName:
                    mysql_DbName = mysql_DbName.group(1)
                else:
                    mysql_DbName = "None"                    
                mysql_user = match_dict['mysqlUser']    #mysql user fill the value
                mysql_user = if_None(mysql_user)                   
                mysql_pd = match_dict['mysqlPasswd']    #mysql password fill the value
                mysql_pd = if_None(mysql_pd)                    
                mem_host = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', match_dict['memHost'])   #memcached host fill the value
                if mem_host:
                    mem_host = mem_host.group()
                else:
                    mem_host = "None"
                #mem_port = re.search('\:+(\d{1,5})', match_dict['memPort'])     #memcached port fill the value
                mem_port = re.search('\d{4,5}', match_dict['memPort'])     #memcached port fill the value
                if mem_port:
                    mem_port = mem_port.group(0)
                else:
                    mem_port = "0"                   
                mem_name = match_dict['memNameSpace']   #memcached nameSpace fill the value
                mem_name = if_None(mem_name)                    
                debug_state = match_dict['debug_status']
                debug_state = if_None(debug_state)                                
                myslq_status = mysql_check(mysql_host,mysql_DbName,mysql_user,mysql_pd)
                mem_status = mem_check(mem_host,mem_port)                
                if jetty_title == 'jetty-'+jetty_name_ch and sub_dir == root_name_ch:
                    print jetty_title,sub_dir,app_status_result,jetty_port,jetty_port_status,fw_status,mysql_host,mysql_DbName,mysql_user,mysql_pd,myslq_status,mem_host+':'+mem_port,mem_status,debug_state,mem_name,conf_path_status
            else:
                if jetty_title == 'jetty-'+jetty_name_ch and sub_dir == root_name_ch:
                    print jetty_title,sub_dir,app_status_result,jetty_port,jetty_port_status,fw_status,conf_path_status
                
jetty_dirs = commands.getstatusoutput('ls -d /data/webapp/*/ | grep ^/data/webapp/jetty | grep -v distribution')
jetty_dirs_state = jetty_dirs[0]
jetty_dirs_list = jetty_dirs[1].split('\n')
jetty_sub_dirs = map(lambda x: commands.getstatusoutput('ls '+x+'/webapps/'), jetty_dirs_list)
jetty_dirs_dict = dict(zip(jetty_dirs_list,jetty_sub_dirs))
config_template = {
    'WEB-INF/classes/config/setup.properties':{'mysqlHost':('db.url=','db.url.master=',),
                                               'mysqlDBName':('db.url=','db.url.master=',),
                                               'mysqlUser':('db.user=',),
                                               'mysqlPasswd':('db.pass=',),
                                               'memHost':('memcache.address=',),
                                               'memPort':('memcache.address=',),
                                               'memNameSpace':('memcache.nameSpace=',),
                                               'debug_status':('debug=',)
    },
    'WEB-INF/classes/config/wx.properties':{'mysqlHost':('wychatcenter.driverUrl=',),
                                            'mysqlDBName':('wychatcenter.driverUrl=',),
                                            'mysqlUser':('wychatcenter.user=',),
                                            'mysqlPasswd':('wychatcenter.password=',),
                                            'memHost':('redis.ip =',),
                                            'memPort':('redis.port =',),
                                            'memNameSpace':('None',),
                                            'debug_status':('dev=',)
    },
    'WEB-INF/jdbc.properties':{'mysqlHost':('app.jdbc.url=',),
                               'mysqlDBName':('app.jdbc.url=',),
                               'mysqlUser':('app.jdbc.username=',),
                               'mysqlPasswd':('app.jdbc.password=',),
                               'memHost':('None',),
                               'memPort':('None',),
                               'memNameSpace':('None',),
                               'debug_status':('None',)
    },

}                

if __name__ == '__main__':
    if len(sys.argv) == 3:
        jetty_name_ch = sys.argv[1]
        root_name_ch = sys.argv[2]
        p = Pool(20)
        for jetty_dirs_dict_key,jetty_dirs_dict_value in jetty_dirs_dict.iteritems():
            p.apply_async(multi_process, args=(jetty_dirs_dict_key,jetty_dirs_dict_value,config_template,jetty_name_ch,root_name_ch))
        p.close()
        p.join()
    else:
        sys.exit("2 arguments expected but %s given" % len(sys.argv))


