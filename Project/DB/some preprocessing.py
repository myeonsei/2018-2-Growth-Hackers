# 슥 훑기

from os import listdir
csvs = listdir(r'C:\ProgramData\MySQL\MySQL Server 5.7\Uploads')

for i in csvs:
    print(i, list(pd.read_csv('C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Uploads\\'+i)))
    
# race_result: 체중은 증감 더해줘야 되고, code는 float으로 바뀐 거 다시 string으로 환원시켜줘야.
# 체중 데이터 중에서 결측치도 있는 것 같음.

def weight(x):
    idx1 = x.find('('); idx2 = x.find(')')
    #print(idx1, idx2)
    if idx1 == 3: return int(x[:idx1]) + int(x[idx1+1:idx2])
    else: return 0
    
df=pd.read_csv('C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Uploads\\race_result_noheader.csv')
df.iloc[:,3]=df.iloc[:,3].apply(lambda x: '0'+str(x)[:-2])
df.iloc[:,12]=df.iloc[:,12].apply(weight)
df.to_csv('C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Uploads\\race_result_noheader.csv', index=False)

# 가끔 전반적으로 소수 데이터 중에서 3.7.1 이런 식으로 되는 것들 뭔지 모르겠음.
