import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import keras
from keras.models import Sequential
from keras.layers import Input, Dense, LSTM
from keras.models import Model
from keras.callbacks import CSVLogger
from sklearn.preprocessing import StandardScaler
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import datetime as dt

url="https://kabuoji3.com/stock/1301/2017/"
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
html_source = requests.get(url=url, headers=headers)
html_text = html_source.text
bs = BeautifulSoup(html_text,"html.parser")

tr_tags = bs.find_all("tr")

header_label = []
column = 6

stock_price = np.empty((0,column), dtype=np.int32)

for index,tr_tag in zip(range(1,len(tr_tags)+1),tr_tags):
    if index == 1:
        th_tags = tr_tag.find_all("th")
        for th_tag in th_tags:
            header_label.append(th_tag.text)
    else:
        array = np.empty((1,column),dtype=np.int32)
        td_tags = tr_tag.find_all("td")
        for idx,td_tag in zip(range(0,column+1),td_tags):
            if idx == 0:
                continue
            else:
                array[0][idx-1] = int(td_tag.text)
        stock_price = np.append(stock_price,array,axis=0)

# 特徴量の尺度を揃える：特徴データを標準化して配列に入れる
scaler = StandardScaler()
# 特徴データを標準化（平均0、分散1になるように変換）
data = scaler.fit_transform(stock_price)

x_data = []
y_data_price = []
y_data_updown = []
# 10 日分の日経平均株価を入力として、1 日後の日経平均株価を予測
for i in range(len(stock_price) - 10):
    x_data.append(data[i:i + 10])
    y_data_price.append(data[i + 10])
    y_data_updown.append(int((stock_price[i + 10 - 1][0] - stock_price[i + 10][0]) > 0))
    y_data_updown.append(int((stock_price[i + 10 - 1][1] - stock_price[i + 10][1]) > 0))
    y_data_updown.append(int((stock_price[i + 10 - 1][2] - stock_price[i + 10][2]) > 0))
    y_data_updown.append(int((stock_price[i + 10 - 1][3] - stock_price[i + 10][3]) > 0))
    y_data_updown.append(int((stock_price[i + 10 - 1][4] - stock_price[i + 10][4]) > 0))
    y_data_updown.append(int((stock_price[i + 10 - 1][5] - stock_price[i + 10][5]) > 0))

x_data = np.asarray(x_data).reshape((-1, 10, 6))
y_data_price = np.asarray(y_data_price).reshape(-1,6)
y_data_updown = np.asarray(y_data_updown).reshape(-1,6)

print(x_data.shape)
print(y_data_price.shape)
print(y_data_updown.shape)

# 学習データサイズ
train_size = int(len(data) * 0.8)
# 学習データ
x_train = x_data[:train_size]
y_train_price = y_data_price[:train_size]
y_train_updown = y_data_updown[:train_size]

print(x_train.shape)
print(y_train_price.shape)
print(y_train_updown.shape)

# テストデータ
x_test = x_data[train_size:]
y_test_price = y_data_price[train_size:]
y_test_updown = y_data_updown[train_size:]

print(x_train)
print(y_train_price)
print(y_train_updown)

model = Sequential()
# 各イテレーションのバッチサイズを32で学習を行なう
inputs = Input(shape=(10, 6))
# 日経平均株価の値を直接予測するため活性化関数は linear
# 中間層の数は 300（理由なし）
x = LSTM(300, activation='relu')(inputs)
price = Dense(6, activation='linear', name='price')(x)
updown = Dense(6, activation='sigmoid', name='updown')(x)
model = Model(inputs=inputs, outputs=[price, updown])
# 後で検証に使用するため 2 値予測も含んでいる
model.compile(loss={
    'price': 'mape',
    'updown': 'binary_crossentropy',
}, optimizer='adam', metrics={'updown': 'accuracy'})


hist = model.fit(x_train, [y_train_price, y_train_updown],
              validation_data=(x_test, [y_test_price, y_test_updown]), epochs=120, batch_size=10,
              callbacks=[CSVLogger('train.log.csv')])

# 損失のグラフ化
loss = hist.history['loss']
epochs = len(loss)
plt.rc('font', family='serif')
fig = plt.figure()
fig.patch.set_facecolor('white')
plt.plot(range(epochs), loss, marker='.', label='loss(training data)')
plt.show()

# 予測結果
predicted = model.predict(x_test)
pred = scaler.inverse_transform(predicted)
y_test_price = scaler.inverse_transform(y_test_price)

sample = pred[0].reshape(40,6)

# plot準備
result = pd.DataFrame({'pred': sample[:,3], 'test': y_test_price[:,3]})
result.plot()
plt.show()
