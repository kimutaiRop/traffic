import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf

keras = tf.keras
layers = keras.layers

data = pd.read_csv("./car_data.csv", parse_dates=True)

data['exit_time'] = pd.to_datetime(data['exit_time'])
data['entry_time'] = pd.to_datetime(data['entry_time'])

data['total_time'] = (data['exit_time'] - data['entry_time']).dt.seconds
print(data.tail(30))
print(data.groupby(['street', 'side'])['car'].agg("count"))
print(data.groupby(['street', 'side'])['total_time'].agg("mean"))
print(data.groupby(['car'])['total_time'].agg("mean"))

moi_ = data[data['street'] == 'moi avenue']
moi_ = moi_[moi_['side'] == "right"]
print(moi_.head(20))
print(moi_.tail(10))
print(moi_.shape[0])
plt.plot(data['entry_time'], data['total_time'])
plt.show()
