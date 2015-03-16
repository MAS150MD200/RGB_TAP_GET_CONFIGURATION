__author__ = 'atsvetkov'

#TEST_CHANGE
#TEST_CHANGE_2
#TEST_CHANGE_3


"""
    XMLRPCC

    #/opt/ripcode/bin/xmlrpcc localhost system.listMethods
    #/opt/ripcode/bin/xmlrpcc localhost system.methodHelp configuration.stream.package.show | sed 's/|/\n/g'
"""

import xmlrpc.client
from pprint import pprint as pp
import re
import sys
import time
import codecs

# СДЕЛАТЬ ПРОВЕРКУ input ID в IGSA и PA!!!

# При съеме конфигурации возможны разрывы в нумерации Input Groups, при заведении групп невозможно указать GID - они назначаются
# пакаджером автоматически по порядку, начиная с "1". Отсюда возможны проблемы с соответствием IG, IGS и P.

# Пустые группы в IGSA не выводятся, поэтому разрывы появляются за счет них и за счет удаленных групп.

# Пустые группы в IGA выводятся, поэтому это нужно учитывать и удалять пустые группы заранее.

# Кроме того пакаджи могут использовать IG в производьном порядке, а не по порядку их следования.

# В выводе PA, строки конфигурации отсортированы относительно соответствующих IG.

# В конфигурации P всегда будут только существующие группы, т.к. невозможно удалить группу входящую в пакадж.

# Несколько пакаджей могут использовать одну группу.

# OSA_id тоже могут иметь разрывы в нумерации, поэтому для PA для них тоже нужне маппинг.

# ИТОГО:
#   если удалены все пустые группы, то заводим IG. Получаем GID от 1 до N. Также формируем маппинг GID_old = GID_new.
#   заводим IGS, при этом используем GID от 1 до N.
#   в общем случаем на PA нужно использовать маппинг Input_GID и Output_ID.


# Основные функции:
    # IGA
    # IGSA
    # OSA
    # PA





IP_TAP_1 = "85.26.149.171"
IP_TAP_2 = "85.26.149.172"
IP_TAP_3 = "85.26.149.173"
IP_TAP_4 = "10.200.2.36"
IP_TAP_5 = "85.26.149.170"  #redundant

IP_TAP_LAB = "192.168.52.62"

login = "root"
password = "taXc0d3r!"


IP_TAP = IP_TAP_LAB           #!!!
server = xmlrpc.client.ServerProxy("http://"+IP_TAP)

"""
    HELP SECTION

listMethods = sorted(server.system.listMethods())
pp(listMethods)

helpMethod = server.system.methodHelp("configuration.package.add")
helpMethod_pretty = re.search(r"\[(.*)\]", helpMethod).group(1).split("|")
[print(i) for i in helpMethod_pretty]
print(",".join([i.split(":")[0] for i in helpMethod_pretty]))
"""

def LIST_METHODS():
    listMethods = sorted(server.system.listMethods())
    pp(listMethods)

def HELP_METHOD(method):
    helpMethod = server.system.methodHelp(method)
    helpMethod_pretty = re.search(r"\[(.*)\]", helpMethod).group(1).split("|")
    [print(i) for i in helpMethod_pretty]
    print(",".join([i.split(":")[0] for i in helpMethod_pretty]))

"""
    ALL METHODS

package_stop = server.configuration.package.stop(login, password, i)
package_start = server.configuration.package.start(login, password, i)
package_remove = server.configuration.package.remove(login, password, i)

package_add = server.configuration.package.add(username,password,name,packageType,packageMode,duration,segmentMode,segmentDuration,segmentLifeSpan,inputType,inputID,infileName,audioMap,outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId)

input_group_remove = server.configuration.input.group.remove(login, password, i)
input_group_add = server.configuration.input.group.add(login, password, name)
input_group_stream_add = server.configuration.input.group.stream.add(username,password,inputGID,pubVidBitRate,monitorOnly,name,protocol,castType,host,port,mcastSource1,mcastSource2,mcastSource3,mcastSource4,interface,format,program,videoPID,audioPID,dataPID)
output_stream_remove = server.configuration.output.stream.remove(login, password, i)
output_stream_add = server.configuration.output.stream.add(login, password, name, 8, 0, host, 0, 0, 10, 0, 1)
"""

def write_to_file(file_name, data):
    """ write with appending """

    ###
    with codecs.open(file_name, "a", "utf-8") as fd:
        fd.write(data + "\n")
    ###



###################################################################################
answer_yes = None
while not answer_yes:
    answer = input("Are you sure to RUN this script? (Y/N)")
    answer_yes = answer if answer.lower().startswith("y") else None
###################################################################################

"""
### START SCRIPT ###

# t1 = time.time()

# for gid in range(1, 31): #1..30
#     for prof in range(1, 5): #1..4
#         print(server.configuration.input.group.stream.add(login,password,gid,0,0,"233.200.200.1.5000_" + str(prof),4,1,"233.200.200.1",int("500" + str(prof)),"","","","",255,3,1,102,104,""))


# for gid in range(31, 61): #31..60
#     for prof in range(1, 5): #1..4
#         print(server.configuration.input.group.stream.add(login,password,gid,0,0,"233.200.200.2.5000_" + str(prof),4,1,"233.200.200.2",int("500" + str(prof)),"","","","",255,3,1,102,104,""))


# for i in range(1, 31):    #1..30
#     print(server.configuration.input.group.add(login, password, "233.200.200.2.5000_" + str(i)))


# for i in range(1, 800):
#     print(server.configuration.output.stream.remove(login, password, i))


# for web_dav_target in web_dav:
#     name = web_dav_target.split("/")[2] #192.168.52.94:8080
#     for i in range(1, 51):         #1..50
#         print(server.configuration.output.stream.add(login, password, name + "_" + str(i), 8, 0, web_dav_target + str(i), 0, 0, 10, 0, 1))


# web_dav_target = web_dav_5
# name = web_dav_target.split("/")[2] #192.168.52.94:8080
# for i in range(1, 61):         #1..30
#     print(server.configuration.output.stream.add(login, password, name + "_" + str(i), 8, 0, web_dav_target + str(i), 0, 0, 10, 0, 1))


# for i in range(1, 31):  #1..30
#     inputID = i
#     outputID1 = i
#     print(server.configuration.package.add(login,password,"233.1.1." + str(i) + ".5000",1,1,0,1,0,300,1,inputID,"","all_lang",1,1,outputID1,0,0,0,0,0,0,1,0,0,"",0,"",0,0,0,"","","",0))


# for i in range(31, 61):  #31..60
#     inputID = i
#     outputID1 = i
#     name = "233.1.1." + str(i) + ".5000"
#     contentId = "".join(name.split(".")[1:4])   #1,2,3 fields
#     print(server.configuration.package.add(login,password,name,1,1,0,1,0,300,1,inputID,"","all_lang",1,1,outputID1,0,0,0,0,0,0,1,0,1,contentId,0,"",0,0,0,"","","",0))


# for i in range(31, 100):
#     print(server.configuration.package.remove(login, password, i))


# t1 = time.time()
#
# for i in range(31, 61):
#     try:
#         print(server.configuration.package.stop(login, password, i))
#     except Exception as e:
#         print("Oops, error: " + str(e))
#         continue
#
#
#
# t2 = time.time()
# print("TOTAL TIME: ", t2 - t1)
"""


#COLLECT CURRENT CONFIGURATION
def IGA_5_2_1p2():
    #configuration >> input >> group >> add (5.3)
    #username,password,name

    HELP_METHOD("configuration.input.group.add")

        #configuration >> input >> group >> show (5.3)
        #username,password,inputGID

    username_iga = login           #IGA
    password_iga = password        #IGA


    for GID in range(1, 200):

        try:
            IGA_DICT = server.configuration.input.group.show(login, password, GID)
        except Exception:
            continue    #goto next GID

        name_iga = IGA_DICT[0]["002:1:name:Name"]

        IGA_LIST = [username_iga,
                    password_iga,
                    name_iga]

        IGA_LIST_DATA_TYPES = ["s/",
                                "s/",
                                "s/"]

        IGA_ZIPPED = zip(IGA_LIST_DATA_TYPES, IGA_LIST)


        ###
        this_function_name = sys._getframe().f_code.co_name
        file_name = this_function_name + "_" + IP_TAP
        data = str(GID) + "\t" + "/opt/ripcode/bin/xmlrpcc localhost configuration.input.group.add " + "\t ".join([str(param[0] + str(param[1])) for param in IGA_ZIPPED])

        write_to_file(file_name, data)
        print(data)
        ###

def IGA_5_3():
    #configuration >> input >> group >> add (5.3)
    #username,password,name

    IGA_5_2_1p2()

def IGA_5_5():
    #configuration >> input >> group >> add (5.3)
    #username,password,name

    IGA_5_2_1p2()



def IGSA_5_2_1p2():
    #configuration >> input >> group >> stream >> add   (5.2.1p2) (отличие от 5.3 - scte35StreamID)
    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД (с разрывами) !!!
    #5_2_1p2    #username,password,inputGID,pubVidBitRate,monitorOnly,name,protocol,castType,host,port,mcastSource1,mcastSource2,mcastSource3,mcastSource4,interface,format,program,videoPID,audioPID,dataPID
    #5.3        #username,password,inputGID,pubVidBitRate,monitorOnly,name,protocol,castType,host,port,mcastSource1,mcastSource2,mcastSource3,mcastSource4,scte35StreamID,interface,format,program,videoPID,audioPID,dataPID
    HELP_METHOD("configuration.input.group.stream.add")
    local_id = 0

    username_igsa = login           #IGSA
    password_igsa = password        #IGSA


    for GID in range(1, 200):



        try:
            IGS_DICT = server.configuration.input.group.show(login, password, GID)
            local_id += 1   #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД
        except Exception:
            continue    #goto next GID

        # pp(IGS_DICT)  #DEBUG


        # inputGID_igsa = int(GID)         #IGSA    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!
        inputGID_igsa = local_id        #IGSA      #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!

        for prof in IGS_DICT[0]["003:1:inputStream:Input Stream"]:
            pubVidBitRate_igsa = int(prof["002:1:pubVidBitRate:Publishing Video Bit Rate"])          #IGSA
            monitorOnly_igsa = 0            #IGSA
            name_igsa = str(prof["006:1:name:Name"])         #IGSA
            protocol_igsa = 4           #IGSA
            castType_igsa = 1           #IGSA
            host_igsa = str(prof["007:1:host:Host"])         #IGSA
            port_igsa = int(prof["008:1:port:Port"])         #IGSA
            mcastSource1_igsa = ""          #IGSA
            mcastSource2_igsa = ""          #IGSA
            mcastSource3_igsa = ""          #IGSA
            mcastSource4_igsa = ""          #IGSA
            # scte35StreamID_igsa = ""            #IGSA
            interface_igsa = 255            #IGSA
            format_igsa = 3         #IGSA
            program_igsa = int(prof["018:3:Configuration:Configuration"]["001:3:program:Program"])           #IGSA
            videoPID_igsa = -1          #IGSA
            audioPID_igsa = -1          #IGSA
            dataPID_igsa = str(0)            #IGSA


            IGSA_LIST = [username_igsa,
                         password_igsa,
                         inputGID_igsa,
                         pubVidBitRate_igsa,
                         monitorOnly_igsa,
                         name_igsa,
                         protocol_igsa,
                         castType_igsa,
                         host_igsa,
                         port_igsa,
                         mcastSource1_igsa,
                         mcastSource2_igsa,
                         mcastSource3_igsa,
                         mcastSource4_igsa,
                         # scte35StreamID_igsa,
                         interface_igsa,
                         format_igsa,
                         program_igsa,
                         videoPID_igsa,
                         audioPID_igsa,
                         dataPID_igsa]

            IGSA_LIST_DATA_TYPES = ["s/",
                                    "s/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "s/",
                                    "i/",
                                    "i/",
                                    "s/",
                                    "i/",
                                    "s/",
                                    "s/",
                                    "s/",
                                    "s/",
                                    # "s/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "s/"]

            IGSA_ZIPPED = zip(IGSA_LIST_DATA_TYPES, IGSA_LIST)

            ###
            this_function_name = sys._getframe().f_code.co_name
            file_name = this_function_name + "_" + IP_TAP
            data = str(GID) + "\t" + "/opt/ripcode/bin/xmlrpcc localhost configuration.input.group.stream.add " + "\t ".join([str(param[0] + str(param[1])) for param in IGSA_ZIPPED])
            write_to_file(file_name, data)
            print(data)
            ###

def IGSA_5_3():
    #configuration >> input >> group >> stream >> add   (5.3)
    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД (с разрывами) !!!
    #username,password,inputGID,pubVidBitRate,monitorOnly,name,protocol,castType,host,port,mcastSource1,mcastSource2,mcastSource3,mcastSource4,scte35StreamID,interface,format,program,videoPID,audioPID,dataPID

    HELP_METHOD("configuration.input.group.stream.add")

    username_igsa = login           #IGSA
    password_igsa = password        #IGSA

    for GID in range(1, 200):

        try:
            IGS_DICT = server.configuration.input.group.show(login, password, GID)
        except Exception:
            continue    #goto next GID


        inputGID_igsa = int(GID)         #IGSA

        for prof in IGS_DICT[0]["003:1:inputStream:Input Stream"]:
            pubVidBitRate_igsa = int(prof["002:1:pubVidBitRate:Publishing Video Bit Rate"])          #IGSA
            monitorOnly_igsa = 0            #IGSA
            name_igsa = str(prof["006:1:name:Name"])         #IGSA
            protocol_igsa = 4           #IGSA
            castType_igsa = 1           #IGSA
            host_igsa = str(prof["007:1:host:Host"])         #IGSA
            port_igsa = int(prof["008:1:port:Port"])         #IGSA
            mcastSource1_igsa = ""          #IGSA
            mcastSource2_igsa = ""          #IGSA
            mcastSource3_igsa = ""          #IGSA
            mcastSource4_igsa = ""          #IGSA
            scte35StreamID_igsa = ""            #IGSA
            interface_igsa = 255            #IGSA
            format_igsa = 3         #IGSA
            program_igsa = int(prof["019:3:Configuration:Configuration"]["001:3:program:Program"])           #IGSA
            videoPID_igsa = -1          #IGSA
            audioPID_igsa = -1          #IGSA
            dataPID_igsa = str(0)            #IGSA


            IGSA_LIST = [username_igsa,
                         password_igsa,
                         inputGID_igsa,
                         pubVidBitRate_igsa,
                         monitorOnly_igsa,
                         name_igsa,
                         protocol_igsa,
                         castType_igsa,
                         host_igsa,
                         port_igsa,
                         mcastSource1_igsa,
                         mcastSource2_igsa,
                         mcastSource3_igsa,
                         mcastSource4_igsa,
                         scte35StreamID_igsa,
                         interface_igsa,
                         format_igsa,
                         program_igsa,
                         videoPID_igsa,
                         audioPID_igsa,
                         dataPID_igsa]

            IGSA_LIST_DATA_TYPES = ["s/",
                                    "s/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "s/",
                                    "i/",
                                    "i/",
                                    "s/",
                                    "i/",
                                    "s/",
                                    "s/",
                                    "s/",
                                    "s/",
                                    "s/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "s/"]

            IGSA_ZIPPED = zip(IGSA_LIST_DATA_TYPES, IGSA_LIST)


            ###
            this_function_name = sys._getframe().f_code.co_name
            file_name = this_function_name + "_" + IP_TAP
            data = str(GID) + "\t" + "/opt/ripcode/bin/xmlrpcc localhost configuration.input.group.stream.add " + "\t ".join([str(param[0] + str(param[1])) for param in IGSA_ZIPPED])
            write_to_file(file_name, data)
            print(data)
            ###

def IGSA_5_5():
    #configuration >> input >> group >> stream >> add   (5.5)
    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!
    #5.2.1.p2   #username,password,inputGID,pubVidBitRate,monitorOnly,name,protocol,castType,host,port,mcastSource1,mcastSource2,mcastSource3,mcastSource4,               interface,format,program,videoPID,audioPID,dataPID
    #5.3        #username,password,inputGID,pubVidBitRate,monitorOnly,name,protocol,castType,host,port,mcastSource1,mcastSource2,mcastSource3,mcastSource4,scte35StreamID,interface,format,program,videoPID,audioPID,dataPID
    #5.5        #username,password,inputGID,pubVidBitRate,monitorOnly,name,protocol,castType,host,port,mcastSource1,mcastSource2,mcastSource3,mcastSource4,scte35StreamID,interface,format,program,videoPID,audioPID,dataPID

    IGSA_5_3()  #??? NEED TO CHECK.



def OSA_5_2_1p2():
    #configuration >> output >> stream >> add
    #username,password,name,protocol,castType,host,vport,aport,ttl,maxClients,checkOutput,authName,authKey  (5.3)
    #username,password,name,protocol,castType,host,vport,aport,ttl,maxClients,checkOutput                   (5.2.1p2)

    HELP_METHOD("configuration.output.stream.add")

        #configuration >> output >> stream >> show
        #username,password,streamID,Display


    username_osa = login        #OSA
    password_osa = password     #OSA

    Display_oss = 0 #Display:Display:int(configuration(0),content(2))::Type of information desired.
    for OID in range(1, 200):

        try:
            OSS_DICT = server.configuration.output.stream.show(login, password, OID, Display_oss)
        except Exception:
            continue    #goto next OID

        id_osa = int(OSS_DICT[0]["001:1:outputID:Output ID"])

        name_osa = str(OSS_DICT[0]["002:1:name:Name"])      #OSA
        protocol_osa = 8    #webdav-light(8)                #OSA
        castType_osa = 0    #unicast(0),multicast(1)        #OSA
        host_psa = str(OSS_DICT[0]["003:1:host:Host"])      #OSA
        vport_osa = int(OSS_DICT[0]["004:1:vport:Video Port"])      #OSA
        aport_osa = int(OSS_DICT[0]["005:1:aport:Audio Port"])      #OSA
        ttl_osa = int(OSS_DICT[0]["008:1:ttl:Time To Live"])      #OSA
        maxClients_osa = int(OSS_DICT[0]["010:1:maxClients:Max Clients"])      #OSA
        checkOutput_osa = 1 #OSA
        # authName_osa = ""   #OSA
        # authKey_osa = ""    #OSA

        OSA_LIST = [username_osa,
                    password_osa,
                    name_osa,
                    protocol_osa,
                    castType_osa,
                    host_psa,
                    vport_osa,
                    aport_osa,
                    ttl_osa,
                    maxClients_osa,
                    checkOutput_osa]
                    # authName_osa,
                    # authKey_osa]

        OSA_LIST_DATA_TYPES = ["s/",
                                "s/",
                                "s/",
                                "i/",
                                "i/",
                                "s/",
                                "i/",
                                "i/",
                                "i/",
                                "i/",
                                "i/"]
                                # "s/",
                                # "s/"]

        OSA_ZIPPED = zip(OSA_LIST_DATA_TYPES, OSA_LIST)

        ###
        this_function_name = sys._getframe().f_code.co_name
        file_name = this_function_name + "_" + IP_TAP
        data = str(id_osa) + "\t" + "/opt/ripcode/bin/xmlrpcc localhost configuration.output.stream.add " + "\t ".join([str(param[0] + str(param[1])) for param in OSA_ZIPPED])
        write_to_file(file_name, data)
        print(data)
        ###

def OSA_5_3():
    #configuration >> output >> stream >> add
    #username,password,name,protocol,castType,host,vport,aport,ttl,maxClients,checkOutput,authName,authKey
    HELP_METHOD("configuration.output.stream.add")

        #configuration >> output >> stream >> show
        #username,password,streamID,Display


    username_osa = login        #OSA
    password_osa = password     #OSA

    Display_oss = 0 #Display:Display:int(configuration(0),content(2))::Type of information desired.
    for OID in range(1, 200):

        try:
            OSS_DICT = server.configuration.output.stream.show(login, password, OID, Display_oss)
        except Exception:
            continue    #goto next OID

        id_osa = int(OSS_DICT[0]["001:1:outputID:Output ID"])

        name_osa = str(OSS_DICT[0]["002:1:name:Name"])      #OSA
        protocol_osa = 8    #webdav-light(8)                #OSA
        castType_osa = 0    #unicast(0),multicast(1)        #OSA
        host_psa = str(OSS_DICT[0]["003:1:host:Host"])      #OSA
        vport_osa = int(OSS_DICT[0]["004:1:vport:Video Port"])      #OSA
        aport_osa = int(OSS_DICT[0]["005:1:aport:Audio Port"])      #OSA
        ttl_osa = int(OSS_DICT[0]["008:1:ttl:Time To Live"])      #OSA
        maxClients_osa = int(OSS_DICT[0]["010:1:maxClients:Max Clients"])      #OSA
        checkOutput_osa = 1 #OSA
        authName_osa = ""   #OSA
        authKey_osa = ""    #OSA

        OSA_LIST = [username_osa,
                    password_osa,
                    name_osa,
                    protocol_osa,
                    castType_osa,
                    host_psa,
                    vport_osa,
                    aport_osa,
                    ttl_osa,
                    maxClients_osa,
                    checkOutput_osa,
                    authName_osa,
                    authKey_osa]

        OSA_LIST_DATA_TYPES = ["s/",
                                "s/",
                                "s/",
                                "i/",
                                "i/",
                                "s/",
                                "i/",
                                "i/",
                                "i/",
                                "i/",
                                "i/",
                                "s/",
                                "s/"]

        OSA_ZIPPED = zip(OSA_LIST_DATA_TYPES, OSA_LIST)

        ###
        this_function_name = sys._getframe().f_code.co_name
        file_name = this_function_name + "_" + IP_TAP
        data = str(id_osa) + "\t" + "/opt/ripcode/bin/xmlrpcc localhost configuration.output.stream.add " + "\t ".join([str(param[0] + str(param[1])) for param in OSA_ZIPPED])
        write_to_file(file_name, data)
        print(data)
        ###

def OSA_5_5():  #EDIT!!!
    #configuration >> output >> stream >> add
    #5.5        #username,password,name,protocol,castType,host,vport,aport,ttl,maxClients,checkOutput,authName,authKey
    #5.3        #username,password,name,protocol,castType,host,vport,aport,ttl,maxClients,checkOutput,authName,authKey
    #5.2.1p2    #username,password,name,protocol,castType,host,vport,aport,ttl,maxClients,checkOutput

    OSA_5_3()



def PA_5_2_1p2():
    #configuration >> package >> add
    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!
    HELP_METHOD("configuration.package.add")
    #username,password,name,packageType,packageMode,duration,segmentMode,segmentDuration,segmentLifeSpan,redundancyMode,inputType,inputID,infileName,audioMap,subDirectory,outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,enableLinearTTML,keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId (5.3)
    #username,password,name,packageType,packageMode,duration,segmentMode,segmentDuration,segmentLifeSpan,inputType,inputID,infileName,audioMap,outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId  (5.2.1p2)
                # redundancyMode, subDirectory, enableLinearTTML

    # HELP_METHOD("configuration.package.show")

        #configuration >> package >> show
        #username,password,packageID,Display


    local_id = 0    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!

    username_pa = login        #PA
    password_pa = password     #PA

    Display_oss = 0 #Display:Display:int(configuration(0),content(2))::Type of information desired.


    PA_OUTPUT_LIST = list()
    for PID in range(1, 200):

        try:
            PS_DICT = server.configuration.package.show(login, password, PID, Display_oss)
            local_id += 1   #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД
        except Exception:
            continue    #goto next OID


        # pp(PS_DICT)

        name_pa = str(PS_DICT[0]["002:1:name:Name"])         #PA
        packageType_pa = 1 #Apple HTTP Live Streaming(1)           #PA
        packageMode_pa = 1  #live(1)                            #PA
        duration_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["003:1:duration:Duration"])   #PA
        segmentMode_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["000:1:segmentMode:Segment Mode"]
        segmentMode_pa = int(re.search(r"(?<=\().*(?=\))", segmentMode_pa).group(0))         #PA
        segmentDuration_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["001:1:segmentDuration:Segment Duration"]) #PA
        segmentLifeSpan_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["002:1:segmentLifeSpan:Segment Life Span"])    #PA
                    # redundancyMode_pa = 0   #none(0),single output(1),duplicate output(2)           #PA
        inputType_pa = 1    #stream(1),file(0)          #PA
        inputID_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["005:1:inputID:Input ID"])         #PA
        # inputID_pa = local_id #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД #PA    #НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ!!!
        infileName_pa = ""  #PA
        audioMap_pa = "Megafon_Audio_Map"   #НЕ ЗАБЫТЬ СОЗДАТЬ ЗАРЕНЕЕ  #PA
                    # subDirectory_pa = ""    #PA
        outContent1_pa = 1  #all(1) #PA
        outputType1_pa = 1  #all(1) #PA
        # outputID1_pa = local_id #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД #PA
        outputID1_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["009:1:outputs:Outputs"][0]["001:1:outputID:Output ID"])
        outContent2_pa = 0  #none(0),all(1),media only(2),manifests only(3) #PA
        outputType2_pa = 1  #stream(1),file(0)  #PA
        outputID2_pa =  0   #PA
        outContent3_pa = 0  #none(0),all(1),media only(2),manifests only(3) #PA
        outputType3_pa = 1  #stream(1),file(0)  #PA
        outputID3_pa =  0   #PA
        syncErrorRestart_pa = 1 #deprecated #PA
        thumbnail_pa = 0    #PA
                    # enableLinearTTML_pa = 0 #PA
        keyServerVendor_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["011:1:keyServerVendor:Key Server Vendor Name"]
        keyServerVendor_pa = int(re.search(r"(?<=\().*(?=\))", keyServerVendor_pa).group(0))         #PA
        contentId_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["013:1:contentId:Content ID"]    #PA
        contentIdType_pa = 0    #PA
        policyId_pa = ""    #PA
        keyRotation_pa = 0 #PA
        keyResourceId_pa = 0   #PA
        keyDeletePolicy_pa = 0 #NoDeletion(0),DeleteOnPackageStop(1)   #PA
        contentName_pa = "" #PA
        contentDescription_pa = ""  #PA
        subContentType_pa = ""  #PA
        policyGroupId_pa = 0    #PA


        PA_LIST = [username_pa,
                   password_pa,
                   name_pa,
                   packageType_pa,
                   packageMode_pa,
                   duration_pa,
                   segmentMode_pa,
                   segmentDuration_pa,
                   segmentLifeSpan_pa,
                   # redundancyMode_pa,
                   inputType_pa,
                   inputID_pa,
                   infileName_pa,
                   audioMap_pa,
                   # subDirectory_pa,
                   outContent1_pa,
                   outputType1_pa,
                   outputID1_pa,
                   outContent2_pa,
                   outputType2_pa,
                   outputID2_pa,
                   outContent3_pa,
                   outputType3_pa,
                   outputID3_pa,
                   syncErrorRestart_pa,
                   thumbnail_pa,
                   # enableLinearTTML_pa,
                   keyServerVendor_pa,
                   contentId_pa,
                   contentIdType_pa,
                   policyId_pa,
                   keyRotation_pa,
                   keyResourceId_pa,
                   keyDeletePolicy_pa,
                   contentName_pa,
                   contentDescription_pa,
                   subContentType_pa,
                   policyGroupId_pa]


        PA_LIST_DATA_TYPES = []
        [PA_LIST_DATA_TYPES.append("s/") if isinstance(param, str) else PA_LIST_DATA_TYPES.append("i/") for param in PA_LIST]

        PA_ZIPPED = zip(PA_LIST_DATA_TYPES, PA_LIST)

        ###
        data = "/opt/ripcode/bin/xmlrpcc localhost configuration.package.add " + "\t ".join([str(param[0] + str(param[1])) for param in PA_ZIPPED])
        ###

        PA_OUTPUT_LIST.append((inputID_pa, data))



    print("TRUE ORDER:")
    for line in [data for input_gid, data in sorted(PA_OUTPUT_LIST, key = lambda x: x[0])]:

        ###
        this_function_name = sys._getframe().f_code.co_name
        file_name = this_function_name + "_" + IP_TAP
        write_to_file(file_name, line)
        ###

        print(line)

def PA_5_3():           #NOT TRUE ORDER!!!  #DON NOT USE!!!
    #configuration >> package >> add
    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!
    HELP_METHOD("configuration.package.add")
    #username,password,name,packageType,packageMode,duration,segmentMode,segmentDuration,segmentLifeSpan,redundancyMode,inputType,inputID,infileName,audioMap,subDirectory,outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,enableLinearTTML,keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId (5.3)
    #username,password,name,packageType,packageMode,duration,segmentMode,segmentDuration,segmentLifeSpan,inputType,inputID,infileName,audioMap,outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId  (5.2.1p2)
    # HELP_METHOD("configuration.package.show")

        #configuration >> package >> show
        #username,password,packageID,Display


    local_id = 0    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!

    username_pa = login        #PA
    password_pa = password     #PA

    Display_oss = 0 #Display:Display:int(configuration(0),content(2))::Type of information desired.
    for PID in range(1, 200):

        try:
            PS_DICT = server.configuration.package.show(login, password, PID, Display_oss)
            local_id += 1   #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД
        except Exception:
            continue    #goto next OID


        pp(PS_DICT)

        name_pa = str(PS_DICT[0]["002:1:name:Name"])         #PA
        packageType_pa = 1 #Apple HTTP Live Streaming(1)           #PA
        packageMode_pa = 1  #live(1)                            #PA
        duration_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["004:1:duration:Duration"])   #PA
        segmentMode_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["000:1:segmentMode:Segment Mode"]
        segmentMode_pa = int(re.search(r"(?<=\().*(?=\))", segmentMode_pa).group(0))         #PA
        segmentDuration_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["001:1:segmentDuration:Segment Duration"]) #PA
        segmentLifeSpan_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["002:1:segmentLifeSpan:Segment Life Span"])    #PA
        redundancyMode_pa = 0   #none(0),single output(1),duplicate output(2)           #PA
        inputType_pa = 1    #stream(1),file(0)          #PA
        # inputID_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["006:1:inputID:Input ID"])         #PA
        inputID_pa = local_id #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД #PA
        infileName_pa = ""  #PA
        audioMap_pa = "Megafon_Audio_Map"   #НЕ ЗАБЫТЬ СОЗДАТЬ ЗАРЕНЕЕ  #PA
        subDirectory_pa = ""    #PA
        outContent1_pa = 1  #all(1) #PA
        outputType1_pa = 1  #all(1) #PA
        outputID1_pa = local_id #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД #PA
        outContent2_pa = 0  #none(0),all(1),media only(2),manifests only(3) #PA
        outputType2_pa = 1  #stream(1),file(0)  #PA
        outputID2_pa =  0   #PA
        outContent3_pa = 0  #none(0),all(1),media only(2),manifests only(3) #PA
        outputType3_pa = 1  #stream(1),file(0)  #PA
        outputID3_pa =  0   #PA
        syncErrorRestart_pa = 1 #deprecated #PA
        thumbnail_pa = 0    #PA
        enableLinearTTML_pa = 0 #PA
        keyServerVendor_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["013:1:keyServerVendor:Key Server Vendor Name"]
        keyServerVendor_pa = int(re.search(r"(?<=\().*(?=\))", keyServerVendor_pa).group(0))         #PA
        contentId_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["015:1:contentId:Content ID"]    #PA
        contentIdType_pa = 0    #PA
        policyId_pa = ""    #PA
        keyRotation_pa = 0 #PA
        keyResourceId_pa = 0   #PA
        keyDeletePolicy_pa = 0 #NoDeletion(0),DeleteOnPackageStop(1)   #PA
        contentName_pa = "" #PA
        contentDescription_pa = ""  #PA
        subContentType_pa = ""  #PA
        policyGroupId_pa = 0    #PA


        PA_LIST = [username_pa,
                   password_pa,
                   name_pa,
                   packageType_pa,
                   packageMode_pa,
                   duration_pa,
                   segmentMode_pa,
                   segmentDuration_pa,
                   segmentLifeSpan_pa,
                   redundancyMode_pa,
                   inputType_pa,
                   inputID_pa,
                   infileName_pa,
                   audioMap_pa,
                   subDirectory_pa,
                   outContent1_pa,
                   outputType1_pa,
                   outputID1_pa,
                   outContent2_pa,
                   outputType2_pa,
                   outputID2_pa,
                   outContent3_pa,
                   outputType3_pa,
                   outputID3_pa,
                   syncErrorRestart_pa,
                   thumbnail_pa,
                   enableLinearTTML_pa,
                   keyServerVendor_pa,
                   contentId_pa,
                   contentIdType_pa,
                   policyId_pa,
                   keyRotation_pa,
                   keyResourceId_pa,
                   keyDeletePolicy_pa,
                   contentName_pa,
                   contentDescription_pa,
                   subContentType_pa,
                   policyGroupId_pa]


        PA_LIST_DATA_TYPES = []
        [PA_LIST_DATA_TYPES.append("s/") if isinstance(param, str) else PA_LIST_DATA_TYPES.append("i/") for param in PA_LIST]

        PA_ZIPPED = zip(PA_LIST_DATA_TYPES, PA_LIST)

        ###
        this_function_name = sys._getframe().f_code.co_name
        file_name = this_function_name + "_" + IP_TAP
        data = "/opt/ripcode/bin/xmlrpcc localhost configuration.package.add " + "\t ".join([str(param[0] + str(param[1])) for param in PA_ZIPPED])
        write_to_file(file_name, data)
        print(data)
        ###

def PA_5_5():           #EDIT!!!
    #configuration >> package >> add
    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!

    HELP_METHOD("configuration.package.add")

    #5.5        #username,password,name,packageType,packageMode,duration,startTime,endTime,segmentMode,segmentDuration,segmentLifeSpan,redundancyMode,redundancyPeer,inputType,inputID,infileName,audioMap,subDirectory,outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,enableLinearTTML,keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId
    #5.2.1p2    #username,password,name,packageType,packageMode,duration,                  segmentMode,segmentDuration,segmentLifeSpan,                              inputType,inputID,infileName,audioMap,             outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,                 keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId

    # HELP_METHOD("configuration.package.show")

        #configuration >> package >> show
        #username,password,packageID,Display


    local_id = 0    #НЕ ЗАБЫТЬ ПРО GID !!! НУМЕРАЦИЯ МОЖЕТ БЫТЬ НЕ ПОДРЯД !!!

    username_pa = login        #PA
    password_pa = password     #PA

    Display_oss = 0 #Display:Display:int(configuration(0),content(2))::Type of information desired.


    PA_OUTPUT_LIST = list()
    for PID in range(1, 200):

        try:
            PS_DICT = server.configuration.package.show(login, password, PID, Display_oss)
            local_id += 1   #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД
        except Exception:
            continue    #goto next OID


        # pp(PS_DICT)           #DEBUG.

        name_pa = str(PS_DICT[0]["002:1:name:Name"])         #PA
        packageType_pa = 1 #Apple HTTP Live Streaming(1)           #PA
        packageMode_pa = 1  #live(1)                            #PA
        duration_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["006:1:duration:Folder Duration"])   #PA
        startTime_pa = str(PS_DICT[0]["008:1:Configuration:Configuration"]['007:1:startTime:Start Time'])   #PA
        endTime_pa = str(PS_DICT[0]["008:1:Configuration:Configuration"]['008:1:endTime:End Time']) #PA
        segmentMode_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["001:1:segmentMode:Segment Mode"]  #PA
        segmentMode_pa = int(re.search(r"(?<=\().*(?=\))", segmentMode_pa).group(0))         #PA
        segmentDuration_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["002:1:segmentDuration:Segment Duration"]) #PA
        segmentLifeSpan_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["003:1:segmentLifeSpan:Segment Life Span"])    #PA
        redundancyMode_pa = 0   #none(0),single output(1),duplicate output(2)           #PA
        redundancyPeer_pa = ""  #PA
        inputType_pa = 1    #stream(1),file(0)          #PA
        inputID_pa = int(PS_DICT[0]["008:1:Configuration:Configuration"]["010:1:inputID:Input ID"])         #PA
        # inputID_pa = local_id #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД #PA    #НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ!!!
        infileName_pa = ""  #PA
        audioMap_pa = "Megafon_Audio_Map"   #НЕ ЗАБЫТЬ СОЗДАТЬ ЗАРЕНЕЕ  #PA
        subDirectory_pa = ""    #PA
        outContent1_pa = 1  #all(1) #PA
        outputType1_pa = 1  #all(1) #PA
        outputID1_pa = local_id #ДЕЛАЕМ НУМЕРАЦИЮ ПОДРЯД #PA    #ПЕРЕДЕЛАТЬ КАК В 5.2.1p2 !!!
        outContent2_pa = 0  #none(0),all(1),media only(2),manifests only(3) #PA
        outputType2_pa = 1  #stream(1),file(0)  #PA
        outputID2_pa =  0   #PA
        outContent3_pa = 0  #none(0),all(1),media only(2),manifests only(3) #PA
        outputType3_pa = 1  #stream(1),file(0)  #PA
        outputID3_pa =  0   #PA
        syncErrorRestart_pa = 1 #deprecated #PA
        thumbnail_pa = 0    #PA
        enableLinearTTML_pa = 0 #PA
        keyServerVendor_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["017:1:keyServerVendor:Key Server Vendor Name"]
        keyServerVendor_pa = int(re.search(r"(?<=\().*(?=\))", keyServerVendor_pa).group(0))         #PA
        contentId_pa = PS_DICT[0]["008:1:Configuration:Configuration"]["019:1:contentId:Content ID"]    #PA
        contentIdType_pa = 0    #PA
        policyId_pa = ""    #PA
        keyRotation_pa = 0 #PA
        keyResourceId_pa = 0   #PA
        keyDeletePolicy_pa = 0 #NoDeletion(0),DeleteOnPackageStop(1)   #PA
        contentName_pa = "" #PA
        contentDescription_pa = ""  #PA
        subContentType_pa = ""  #PA
        policyGroupId_pa = 0    #PA


        PA_LIST = [username_pa,
                   password_pa,
                   name_pa,
                   packageType_pa,
                   packageMode_pa,
                   duration_pa,
                   startTime_pa,
                   endTime_pa,
                   segmentMode_pa,
                   segmentDuration_pa,
                   segmentLifeSpan_pa,
                   redundancyMode_pa,
                   redundancyPeer_pa,
                   inputType_pa,
                   inputID_pa,
                   infileName_pa,
                   audioMap_pa,
                   subDirectory_pa,
                   outContent1_pa,
                   outputType1_pa,
                   outputID1_pa,
                   outContent2_pa,
                   outputType2_pa,
                   outputID2_pa,
                   outContent3_pa,
                   outputType3_pa,
                   outputID3_pa,
                   syncErrorRestart_pa,
                   thumbnail_pa,
                   enableLinearTTML_pa,
                   keyServerVendor_pa,
                   contentId_pa,
                   contentIdType_pa,
                   policyId_pa,
                   keyRotation_pa,
                   keyResourceId_pa,
                   keyDeletePolicy_pa,
                   contentName_pa,
                   contentDescription_pa,
                   subContentType_pa,
                   policyGroupId_pa]


        PA_LIST_DATA_TYPES = []
        [PA_LIST_DATA_TYPES.append("s/") if isinstance(param, str) else PA_LIST_DATA_TYPES.append("i/") for param in PA_LIST]

        PA_ZIPPED = zip(PA_LIST_DATA_TYPES, PA_LIST)

        ###
        data = "/opt/ripcode/bin/xmlrpcc localhost configuration.package.add " + "\t ".join([str(param[0] + str(param[1])) for param in PA_ZIPPED])
        ###

        PA_OUTPUT_LIST.append((inputID_pa, data))



    print("TRUE ORDER:")
    for line in [data for input_gid, data in sorted(PA_OUTPUT_LIST, key = lambda x: x[0])]:

        ###
        this_function_name = sys._getframe().f_code.co_name
        file_name = this_function_name + "_" + IP_TAP
        write_to_file(file_name, line)
        ###

        print(line)



def IGSM_5_3():
    #IGSM TAP 5.3
    #username,password,inputGID,index,pubVidBitRate,monitorOnly,name,protocol,castType,host,port,mcastSource1,mcastSource2,mcastSource3,mcastSource4,scte35StreamID,interface,format,program,videoPID,audioPID,dataPID
    username_igsm = login           #IGSM
    password_igsm = password        #IGSM


    for GID in range(1, 200):

        try:
            IGS_DICT = server.configuration.input.group.show(login, password, GID)
        except Exception:
            continue    #goto next GID


        print("#NEW CHANNEL")
        inputGID_igsm = int(GID)         #IGSM

        for prof in IGS_DICT[0]["003:1:inputStream:Input Stream"]:
            index_igsm = int(prof["001:1:index:Index"])          #IGSM
            pubVidBitRate_igsm = int(prof["002:1:pubVidBitRate:Publishing Video Bit Rate"])          #IGSM
            monitorOnly_igsm = 0            #IGSM
            name_igsm = str(prof["006:1:name:Name"])         #IGSM
            protocol_igsm = 4           #IGSM
            castType_igsm = 1           #IGSM
            host_igsm = str(prof["007:1:host:Host"])         #IGSM
            port_igsm = int(prof["008:1:port:Port"])         #IGSM
            mcastSource1_igsm = ""          #IGSM
            mcastSource2_igsm = ""          #IGSM
            mcastSource3_igsm = ""          #IGSM
            mcastSource4_igsm = ""          #IGSM
            scte35StreamID_igsm = ""            #IGSM
            interface_igsm = 255            #IGSM
            format_igsm = 3         #IGSM
            program_igsm = int(prof["019:3:Configuration:Configuration"]["001:3:program:Program"])           #IGSM
            videoPID_igsm = -1          #IGSM
            audioPID_igsm = -1          #IGSM
            dataPID_igsm = str(0)            #IGSM


            IGSM_LIST = [username_igsm,
                         password_igsm,
                         inputGID_igsm,
                         index_igsm,
                         pubVidBitRate_igsm,
                         monitorOnly_igsm,
                         name_igsm,
                         protocol_igsm,
                         castType_igsm,
                         host_igsm,
                         port_igsm,
                         mcastSource1_igsm,
                         mcastSource2_igsm,
                         mcastSource3_igsm,
                         mcastSource4_igsm,
                         scte35StreamID_igsm,
                         interface_igsm,
                         format_igsm,
                         program_igsm,
                         videoPID_igsm,
                         audioPID_igsm,
                         dataPID_igsm]

            IGSM_LIST_DATA_TYPES = ["s/",
                                    "s/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "s/",
                                    "i/",
                                    "i/",
                                    "s/",
                                    "i/",
                                    "s/",
                                    "s/",
                                    "s/",
                                    "s/",
                                    "s/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "i/",
                                    "s/"]

            IGSM_ZIPPED = zip(IGSM_LIST_DATA_TYPES, IGSM_LIST)


            # print("/opt/ripcode/bin/xmlrpcc localhost configuration.input.group.stream.modify " + " ".join([str(param[0] + str(param[1])) for param in IGSM_ZIPPED]))
            print("/opt/ripcode/bin/xmlrpcc localhost configuration.input.group.stream.modify " + "\t ".join([str(param[0] + str(param[1])) for param in IGSM_ZIPPED]))

            # print(IGSM_LIST)            #MAIN_PRINT



def PAM_5_5():
    """
    Just add "packageID" field.

    В данной версии предполагается, что нумерация пакаджей идет от 1 до N, без разрывов.
    """

    #5.5 package_add        username,password,          name,packageType,packageMode,duration,startTime,endTime,segmentMode,segmentDuration,segmentLifeSpan,redundancyMode,redundancyPeer,inputType,inputID,infileName,audioMap,subDirectory,outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,enableLinearTTML,keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId
    #5.5 package_modify     username,password,packageID,name,packageType,packageMode,duration,startTime,endTime,segmentMode,segmentDuration,segmentLifeSpan,redundancyMode,redundancyPeer,inputType,inputID,infileName,audioMap,subDirectory,outContent1,outputType1,outputID1,outContent2,outputType2,outputID2,outContent3,outputType3,outputID3,syncErrorRestart,thumbnail,enableLinearTTML,keyServerVendor,contentId,contentIdType,policyId,keyRotation,keyResourceId,keyDeletePolicy,contentName,contentDescription,subContentType,policyGroupId

    HELP_METHOD("configuration.package.modify")






def map_gid_PA():

    #количество пакаджей в общем случае не равно количеству групп на входе.

    #GID from IGA.
    group_GIDs = """
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
"""

    #GIDs from PA.
    PA_GIDs = """
 i/1
 i/2
 i/3
 i/4
 i/5
 i/6
 i/7
 i/8
 i/9
 i/10
 i/11
 i/16
 i/17
 i/15
 i/23
 i/19
 i/18
 i/20
 i/21
 i/47
 i/24
 i/12
 i/26
 i/27
 i/22
 i/28
 i/29
 i/30
 i/31
 i/32
 i/25
 i/33
 i/34
 i/35
 i/36
 i/37
 i/38
 i/39
 i/40
 i/41
 i/42
 i/43
 i/13
 i/44
 i/14
"""

    group_GIDs_list = group_GIDs.splitlines()
    group_GIDs_list = list(filter(lambda x : x, group_GIDs_list))
    group_GIDs_list = list(map(lambda x : str(x).strip(" i/"), group_GIDs_list))

    PA_GIDs_list = PA_GIDs.splitlines()
    PA_GIDs_list = list(filter(lambda x : x, PA_GIDs_list))
    PA_GIDs_list = list(map(lambda x : str(x).strip(" i/"), PA_GIDs_list))

    print("group_GIDs_list: " + str(len(group_GIDs_list)), "PA_GIDs_list: " + str(len(PA_GIDs_list)))

    for p_gid in PA_GIDs_list:
        if p_gid in group_GIDs_list:
            print(" " + "i/" + str(group_GIDs_list.index(p_gid) + 1))

        else:
            print("None")






if __name__ == "__main__":
    ### FOR 5.2.1p2 ###
    # IGA_5_2_1p2()
    # IGSA_5_2_1p2()
    # OSA_5_2_1p2()
    # PA_5_2_1p2()
    ###



    ### FOR 5.3 ###


    ###



    ### FOR 5.5 ###
    # IGA_5_5()
    # IGSA_5_5()
    # OSA_5_5()
    PA_5_5()
    # PAM_5_5()


    ### MAP GID ###
    # map_gid_PA()


    ###