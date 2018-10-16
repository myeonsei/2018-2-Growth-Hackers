import numpy as np
import datetime
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import xgboost as xgb
import pymysql

db = pymysql.connect(host = "35.221.101.110", user = "root", passwd = "growthhackers", db = "horserace",  charset = "utf8") # SQL 설정
cursor = db.cursor()

cursor.execute("select race_result.code, race_result.date, race_result.round, race_result.record, race_result.lane, race_result.sex, race_result.age, race_result.jockey_w, \
               race_result.rating, race_result.dandivi, race.weather, race.humidity, race.level, race.distance, race.horses, horse.total, \
               jockey.recent_all, jockey.recent_winrate, jockey.recent_winrate2, jockey.recent_winrate3, jockey.total_all, jockey.total_winrate, jockey.total_winrate2, jockey.total_winrate3 \
               from race_result, race, horse, jockey where race_result.date = race.date and race_result.round = race.round, race_result.code = horse.code and race_result.jockey = jockey.code")
# 0-7/8-15/16-23
# weather, level one-hot 필요.
# 최근 3경기 결과, 최근 1개월 내 질병 여부, 거리별 승률 별도로 뽑을 것.

df = np.array(cursor.fetchall()) # array 형태로 받음

enc = OneHotEncoder() 
enc.fit(df[:,10]) # weather one-hot & append
np.append(df, enc.transform(df[:10].toarray()), axis=1)
enc.fit(df[:,12]) # level one-hot & append
np.append(df, enc.transform(df[:12].toarray()), axis=1)

final_append = []

for i in len(df):
    tmp = []
    
    # 최근 3개 경기 결과 평균 - 일단 record만 함
    cursor.execute("select record from race_result where date <= %s, code = %s order by date desc limit 3", (df[i,1], df[i,0]))
    tmp.append(mean([i[0] for i in cursor.execute() if i[0] is not None])) # 허수들을 잘 배제해줄지 모르겠음.
    
    # 최근 1개월 내 질병 여부
    cursor.execute("select date from diagnosis where date <= %s and code = %s order by date desc limit 1", (df[i,1], df[i,0]))
    if (df[i,1] - cursor.fetchone()[0]) <= datetime.datetime(0,1,0,0,0,0): # 최근 진료가 1개월 이내일 경우
        tmp.append(1)
    else: tmp.append(0)
        
    # 해당 거리 승률 및 기록
    cursor.execute("select winrate%s, winrate2%s, winrate3%s, max%s, avg%s from record where code = %s", ((df[i,13])*5).append(df[i,0]))
    tmp.extend(cursor.fetchone())
    
    final_append.append(tmp)
    
np.append(df, final_append, axis=1) # 위에 세 개 만든 거 붙임
np.delete(df, (10, 12), 1) # one-hot 한 column들 날림

train, test = train_test_split(df, test_size = 0.3, random_state=datetime.datetime.now().second)
real = test[:,0]
train = xgb.DMatrix(train[:,1:], label=train[:,0]) # xgb에서 쓸 수 있게 자료형 변경
test = xgb.DMatrix(test[:,1:], label=test[:,0])

# 이제 xgboost 돌리자~
param = {'max_depth':2, 'eta':1, 'gamma':0, 'lambda':1, 'silent':1, 'objective':'reg:linear'} # parameter 설정: 공부 필요
num_round = 2

bst = xgb.train(param, train, num_round) # train
preds = bst.predict(dtest) # test

print(((preds - real)**2).mean()**0.5) # rmse 출력
