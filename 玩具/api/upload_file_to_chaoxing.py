# 超星云盘上传获得直链
# 参考：https://www.52pojie.cn/forum.php?mod=viewthread&tid=1260120&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26typeid%3D29
# -*- coding: utf-8 -*-
import requests,json
from ftplib import FTP
import os, time, sys
 
cookie = { #在下方引号内填入UID和uf两个cookies参数，仅上传200MB以上文件需要
    "UID": "",
    "uf": ""
    }
 
 
class Chaopan(object):
    def __init__(self, cookies):
        """登录超盘"""
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
        response = session.get('https://pan-yz.chaoxing.com/api/token/uservalid')
        retobj = json.loads(response.text)
        if not retobj["result"]:
            raise Exception("参数验证失败，登录状态失效")
        self.__token = retobj["_token"]
        self.__id = cookies["UID"]
        self.__session = session
 
    def __get_info(self):
        url = f'https://pan-yz.chaoxing.com/api/info?puid={self.__id}&_token={self.__token}'
        return self.__session.get(url).json()["data"]
 
    def get_disk_capacity(self):
        """获取总空间和已用空间大小"""
        url = f'https://pan-yz.chaoxing.com/api/getUserDiskCapacity?puid={self.__id}&_token={self.__token}'
        response = self.__session.get(url)
        retobj = json.loads(response.text)
        return retobj
 
    def list_dir(self, fldid='', orderby='d', order='desc', page=1, size=100, addrec=False, showCollect=1):
        """列举目录文件"""
        url = f'https://pan-yz.chaoxing.com/api/getMyDirAndFiles?puid={self.__id}&fldid={fldid}&orderby={orderby}&order={order}&page={page}&size={size}&_token={self.__token}&addrec={addrec}&showCollect={showCollect}'
        response = self.__session.get(url)
        retobj = json.loads(response.text)
        return retobj
 
    def __create_file_new(self, file: "本地文件", fldid=""):
        url = 'https://pan-yz.chaoxing.com/opt/createfilenew'
        BYTES_PER_CHUNK = 512 * 1024
        LIMIT = 1024 * 1024
        ffile = []
        rr = file.tell()
        size = file.seek(0, 2)
        file.seek(0, 0)
        ffile.append(file.read(BYTES_PER_CHUNK))
        file.seek(BYTES_PER_CHUNK + size - LIMIT, 0)
        ffile.append(file.read(BYTES_PER_CHUNK))
        file.seek(0, rr)
 
        path,name = os.path.split(file.name)
 
        files = {
            "file0":(ffile[0]),
            "file1":(ffile[1])
            }
        post_data = {
            "size": size,
            "fn": name,
            "puid":0,
            }
        if fldid:
            post_data["fldid"] = fldid
 
        response = self.__session.post(url, data=post_data, files=files)
        return json.loads(response.text)
 
    def __ftp_upload_file(self, file: "本地文件", timemil, callback=None):
        jindu = [file.seek(0, 2),0]
        def __callback(block):
            jindu[1] += 8192
            if jindu[1] < jindu[0]:
                callback(jindu[1] / jindu[0])
            else:
                callback(1)
        info = self.__get_info()
        upath = info["froot"]
        host = info["host"]
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(host, 21)
        ftp.login("usertemp", "0GYF0hBAbsXVBZCUPaSOVS")
        ftp.set_pasv(True)
        ftp.mkd(f'/{upath}/{timemil}')
        path,name = os.path.split(file.name)
        file.seek(0, 0)
        if callback:
            res = ftp.storbinary(f'STOR /{upath}/{timemil}/{name}', file, blocksize=8192, callback=__callback)
        else:
            res = ftp.storbinary(f'STOR /{upath}/{timemil}/{name}', file)
        ret =  res.find('226') != -1
        ftp.quit()
        return ret
 
    def __sync_upload(self, timemil, pntid=""):
        url = 'https://pan-yz.chaoxing.com/api/notification/rsyncsucss'
        post_data = {
            "puid": self.__id,
            "rf": timemil,
            "_token": self.__token
            }
        if pntid:
            post_data["pntid"] = pntid
 
        response = self.__session.post(url, data=post_data)
        return json.loads(response.text)
 
    def __crcstatus(self, crc):
        url = f'https://pan-yz.chaoxing.com/api/crcstatus?puid={self.__id}&crc={crc}&_token={self.__token}'
        response = requests.get(url)
        return json.loads(response.text)
 
    def upload_file(self, file: "本地文件", fldid="", callback=None):
        """上传文件"""
        size = Chaopan.__getsize(file)
        if size > 1024 * 1024 + 1024 * 1024:
            retobj = self.__create_file_new(file, fldid)
            if retobj["result"]:
                return retobj["data"]
 
            crc = retobj["crc"]
            timemil = retobj["timemil"]
 
            if self.__ftp_upload_file(file, timemil, callback):
                self.__sync_upload(timemil, fldid)
            return self.__crcstatus(crc)
 
        else:
            timemil = int(time.time() * 1000)
            self.__ftp_upload_file(file, timemil, callback)
            return  self.__sync_upload(timemil, fldid)
 
    def del_file(self, id: '文件id，多个请用英文逗号","分隔'):
        """删除网盘上文件"""
        url = 'https://pan-yz.chaoxing.com/api/delete'
        post_data = {
            "puid": self.__id,
            "resids": id,
            "_token": self.__token
            }
        response = self.__session.post(url, data=post_data)
        return json.loads(response.text)
 
    @staticmethod
    def upload_share_file(file: "本地文件或Bytes"):
        """上传本地文件转链接,不得大于200M"""
        size = Chaopan.__getsize(file)
        if size == 0 or size > 200000000:
            return {"status":False,"msg":"文件大小必须在0-200MB之间"}
        url = 'http://notice.chaoxing.com/pc/files/uploadNoticeFile'
        file_data = {
            'attrFile': file
            }
        response = requests.post(url, files=file_data)
        return json.loads(response.text)
 
    @staticmethod
    def __getsize(file):
        """获取文件大小"""
        import _io
        if isinstance(file, _io.BufferedReader):
            rr = file.tell()
            size = file.seek(0, 2)
            file.seek(0, rr)
            return size
        elif isinstance(file, bytes):
            return len(file)
        else:
            return 0
 
def callback(per):
    hashes = '#' * int(per * 30)
    spaces = ' ' * (30 - len(hashes))
    sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, per*100))
    sys.stdout.flush()
 
filepath = input("请输入文件路径： ")
 
try:
    with open(filepath, 'rb') as f:
        size = f.seek(0, 2)
        f.seek(0, 0)
        if size <= 200000000:
            print("正在上传中，请等待...")
            ret = Chaopan.upload_share_file(f)
            if ret["status"]:
                print(f'下载直链为(http替换为https仍然可用)： {ret["att_file"]["att_clouddisk"]["downPath"]}')
                print(f'分享链接为： {ret["att_file"]["att_clouddisk"]["shareUrl"]}')
            else:
                print(f'转直链失败，原因为{ret["msg"]}')
        else:
            print("您的文件大于200M, 正在以登录状态上传，请等待...")
            cp = Chaopan(cookie)
            retobj = cp.upload_file(f, callback=callback)
            print("")
            print(f'下载直链为(http替换为https仍然可用)： http://d0.ananas.chaoxing.com/download/{retobj["objectId"]}')
            print(f'分享链接为： http://cloud.ananas.chaoxing.com/view/fileview?objectid={retobj["objectId"]}')
            print('正在清理网盘空间(清理后上传的文件不会占用您的网盘空间)')
            time.sleep(3)
            if "id" in retobj:
                cp.del_file(retobj["id"])
            elif "resid" in retobj:
                cp.del_file(retobj["resid"])
            print('清理完成')
 
except Exception as e: 
    print(f'出现错误，原因为:{str(e)}')