import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf

keras = tf.keras
layers = keras.layers

data = pd.read_csv("./car_data.csv", parse_dates=True)

data['exit_time'] = pd.to_datetime(data['exit_time'])
data['entry_time'] = pd.to_datetime(data['entry_time'])

# data = pd.get_dummies(data)
data['total_time'] = (data['exit_time'] - data['entry_time']).dt.seconds
print(data.tail(30))
# data.drop(data.iloc(0), axis=0)
print(data.groupby(['street', 'side'])['car'].agg("count"))
print(data.groupby(['street', 'side'])['total_time'].agg("mean"))

plt.plot(data['entry_time'], data['total_time'])
plt.show()

plt.plot(data['num_cars_next_street'], data['num_cars_current_street'])
plt.show()

corr_ = data.corr().unstack()
print(corr_)
