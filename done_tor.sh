#!/bin/sh

# 전달받은 TOR_ID 이용해서 시드 제거
# 'transmission 주소:port -n id:passwd' 형식으로 작성
SERVER=''
transmission-remote $SERVER -t $TR_TORRENT_ID -r


# 사용하실분은 주석 제거후 사용하세요
#BUPUSH='' # 'PushBullet 키값'
#YMD=`date +%y%m%d`
#TIME=`date +%H:%M:%S`
#curl -u "$BUPUSH": https://api.pushbullet.com/v2/pushes -d type=note -d title="완료 : $TR_TORRENT_NAME" -d body="$YMD | $TIME | $TR_TORRENT_NAME 다운로드 완료" --insecure
