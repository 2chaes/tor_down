# tor_down

파이썬으로 만들어진 토렌트 다운로드 스크립트입니다. <br/>
광고문구가 포함된 영상을 걸러내는 기능을 추가했습니다.

### Pre-requisites

OS : Ubuntu/Debian <br/>
Python Version >= 3.4

### Installation

* Transmission 설치

```
$ sudo apt-get install transmission-daemon
```

### Python bundle

* bs4 (BeautifulSoup)
* transmissionrpc

```
$ sudo pip3 install bs4
$ sudo pip3 install transmissionrpc
```

### Usage

tordown.py 검색어 [Option] 의 형태로 사용하시면 됩니다.

#### Option
* option이 0인경우 오늘자 날짜를 추가해서 가장 먼저 올라온 파일 다운로드 요청.
* option이 1인경우 어제자 날짜를 추가해서 가장 먼저 올라온 파일 다운로드 요청.
* option이 0이나 1이 아닌 경우 검색어 중 가장 나중에 올라온 파일 다운로드 요청.

#### 코드 중 해당변수를 트랜스미션 설정에 맞게 수정합니다.
* tor_addr='Your_transmission_address'
* tor_user='Your_transmission_id'
* tor_passwd='Your_transmission_passwd'

#### 수정가능한 변수들
* 'loop_num'은 검색이 성공할때까지 반복하는 횟수를 뜻합니다.
* 'loop_delay'는 검색이 실패했을때 다음검색 요청까지 기다리는 시간을 뜻합니다. (단위 : 초)
* 'pq'는 화질입니다. 기본적으로 '720'으로 설정되어 있습니다. </br>
  해당부분을 '360', '720', '1080' 으로 수정할수 있습니다. </br>
  '' 으로 수정한다면 화질 상관없이 검색합니다.

### Example
#### 1. 터미널에서 바로 다운로드를 요청할때 사용합니다.
* 터미널에서 바로 'Weekly Idol' 이라는 프로그램을 다운로드 요청할때 아래와 같이 사용합니다.
```
$ /SCRIPT/PATH/tordown.py Weekly Idol
```

#### 2. 옵션을 활용해서 crontab에 등록해서 자동 다운로드 용도로 사용합니다.
* 'ABC drama' 라는 프로그램이 매주 수,목 23시 10분에 종료된다. </br>
   ABC drama 를 검색어를 이용해서 아래와 같이 crontab에 걸어두면 됩니다.
```
# 옵션 0을 이용해서 오늘날짜(170304)를 추가한다.
# "170304 ABC drama $화질" 로 검색을 시도한다.
10 23 * * 3,4 /SCRIPT/PATH/tordown.py ABC drama 0
```

* 'My Little TV' 라는 프로그램은 일요일 0시 45분에 끝난다.
   다음날 프로그램이 종료되는 경우에는 1 옵션을 이용해서 걸어두면 됩니다.
```
# 옵션 1을 이용해서 어제날짜(170303)를 추가한다.
# "170303 My Little TV $화질" 로 검색을 시도한다.
45 0 * * 7 /SCRIPT/PATH/tordown.py My Little TV 1
```
