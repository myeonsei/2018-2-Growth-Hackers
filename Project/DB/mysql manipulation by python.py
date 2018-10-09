# 초기 설정 부분
import pymysql
db = pymysql.connect(host = "35.221.101.110", user = "root", passwd = "growthhackers", db = "horserace",  charset = "utf8") # 현재 서버 ip는 35.221.101.110
cursor = db.cursor()

# 테이블에 row 1줄 삽입하기
format = 'insert into contract values(%s, %s, %s)'; d = (123, '2018-06-06', None)
cursor.execute(format, d)

# 데이터 없으면 튜플 원소 None으로 하면 됨. 그러면 mysql table에는 NULL로 들어감.
# 추가로 mysql에서의 datetime 자료형으로 넣어주려면 애당초 입력값을 ‘2018-01-02’처럼 문자열로 바꾸든지, 아니면 x가 datetime 자료형이라면 str(x)로 바꿔서 입력값 넣어줘야 함. 여기서 말하는 입력값은 위에서 튜플의 원소를 의미함.

# 테이블 뼈대는 남긴 채로 안에 데이터만 삭제
cursor.execute(‘truncate table (테이블명);’)

# 테이블 내의 개별 row 삭제
cursor.execute(‘delete from (테이블명) where (조건)’)

# 마무리
db.commit() # 조작한 거를 mysql db로 flush
db.close()

# 클라우드에서 mysql 오픈
gcloud sql connect 인스턴스 이름(testdb-002) --user=root
좀 기다린 다음에 -> 비밀번호 치면 됨 (growthhackers)

# 한 테이블에서 데이터 뽑아오기(SQL 명령어)
select (칼럼명1), (칼럼명2), .. from (테이블명) where (조건문) order by (칼럼명) asc or desc;

# 여러 테이블 join해서 불러오기(SQL 명령어)
select 테이블명1.칼럼명1, 테이블명2.칼럼명2 … from 테이블명1, 테이블명2, … where 테이블명1.칼럼명x = 테이블명2.칼럼명y;

# 칼럼 데이터를 조작해서 가져오기(SQL 명령어)
select case when (조건문1) then (반환값1) when (조건문2) then (반환값) … else (반환값) end from (테이블명);
사칙연산 이런 거는 그냥 select (칼럼명1) + (칼럼명2) from (테이블명) 이런 식으로 하면 됨.

# 데이터 수정(SQL 명령어)
update (테이블명) set (칼럼명) = (넣고자 하는 값) where (조건);

# group by(SQL 명령어)
select name, count(name), sum(name) from sample group by name;
