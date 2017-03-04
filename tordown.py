#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import os, sys, subprocess
import time, datetime
import transmissionrpc
import urllib.request
from bs4 import BeautifulSoup


# 불량 파일을 체크하는 부분
def Ban_Check():

    # 검색 성공한 title_mag 리스트를 가져와서 처리.
    for i in range(0,len(title_mag)):
        # 다운로드 요청 및 torrent ids 처리
        res=tc.add_torrent('magnet:?xt=urn:btih:'+title_mag[i][1])
        tor_id=int(re.search(r'Torrent\ (\d*).?>>',str(res.files)).group(1))

        # 불량 파일인지 아닌지 검사함.
        if ban_option:
            per=0


            # 최대 5분동안 15% 다운되길 기다림.
            for j in range(0,20):
                time.sleep(15)

                try:
                    tor_stat=tc.get_files(tor_id)[tor_id][0]
                    per=tor_stat['completed']/tor_stat['size']
                    #print(per)
                except:
                    continue

                # 다운로드 퍼센트 15프로 넘으면 탈출
                if per > 0.15:
                    break

            # 똑같은걸로 인코딩 하는지 head부분에 동일한 정보 남음
            # 해당 내용으로 불량여부 검사
            try:
                head=subprocess.check_output("""head -1 '""" + tor_path + tor_stat['name'] + """.part' 2> /dev/null""", shell=True)
                is_ban=re.search(r'H.264/MPEG-4 AVC codec - Copyleft 2003-2014 - http://www.videolan.org/x264.html',str(head))
            except: # 문제 발생시 에러코드 -1 전달
                return (tor_stat['name'].strip(),-1)

        else: # 불량파일 검사 x
            return (0,0)

        # is_ban의 결과가 None인 경우 성공
        # 그렇지 않다면 해당파일 제거후 밴마그넷 처리
        if is_ban == None:
            return (tor_stat['name'].strip(),0)
        else:
            tc.remove_torrent(tor_id, delete_data=True)
            ban_list.append(title_mag[i])
            #print('deleted!')
            #print(ban_list)
            continue
    return 1


if len(sys.argv) <= 1:
    print("검색어를 입력하세요!")
    exit()

dname=' '
ban_list=[]
ban_option=1
d=datetime.datetime.today()

# transmission addr, id, passwd
tor_addr='Your_transmission_address'
tor_user='Your_transmission_id'
tor_passwd='Your_transmission_passwd'

# 반복횟수, 검색주기 설정 (단위: 초)
loop_num=60
loop_delay=300

# transmission 호출
tc=transmissionrpc.Client(address=tor_addr, user=tor_user, password=tor_passwd)
tor_path=tc.get_session().download_dir + '/'


# 파라미터로 검색어 가공
# 마지막 숫자가 0이면 오늘날짜
# 마지막 숫자가 1이면 어제날짜
# 마지막 숫자가 없으면 그냥검색
for i in sys.argv[1:-1]:
    dname+=i+" "

if sys.argv[-1] == "0":
    dname=d.strftime('%y%m%d')+dname+'720'
elif sys.argv[-1] == "1":
    d=d-datetime.timedelta(1)
    dname=d.strftime('%y%m%d')+dname+'720'
else:
    ban_option=0
    loop_num=1
    dname=dname + sys.argv[-1]
    dname=dname.strip()

dname=urllib.parse.quote(dname)


# 토렌트 검색 요청
for n in range(loop_num):
    title_mag=[]

    # referer 추가 및 검색
    req = urllib.request.Request("https://torrentkim5.net/bbs/rss.php?k="+dname, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
    html = urllib.request.urlopen(req).read().decode("utf-8")

    # 검색 결과 파싱 및 재검색시 밴 마그넷 제거
    schlist = BeautifulSoup(html,"html.parser").findAll('item')
    for i in schlist:
        tm_tmp=(i.find('showrss:showname').text.strip(),i.find('showrss:info_hash').text.strip())

        # 밴리스트에 추가된 마그넷일 경우 넣지 않는다.
        if not (tm_tmp in ban_list):
            title_mag.append(tm_tmp)

    # 가장 먼저 올라온 파일부터 요청함
    # 그냥 검색시 가장 최신 결과만 가져옴
    if ban_option:
        title_mag.reverse()


    # Ban_Check()의 결과가 0이면 다운로드 요청 성공, 1이면 다운로드 요청 실패
    # -1인 경우는 다운로드 요청은 했지만, 불량 여부는 검사하지 못한 상태.
    r=Ban_Check()

    if r == 1: # 요청 실패
        if ban_option: # loop_delay에 만큼 대기후 검색시작
            #print("Wait")
            time.sleep(loop_delay)
        else: # 바로 검색했을시 실패
            print("검색실패")

    else: # 요청 성공
        if r[1] == -1: # Ban_Check 실패
            print("Ban_Check Error  : \"" + r[0] + "\"")
        elif r[1] == 0: # 바로검색시 출력문 없음
            pass
        else: # Ban_Check가 완료된 파일 다운로드 요청
            #print("Download Success : \"" + r[0] + "\"")
            pass
        exit()

