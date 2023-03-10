from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd

def get_prediction(input):

    df = pd.read_csv("traffic.csv")
    df.head()

# %matplotlib inline
# plt.scatter(df['Mileage'], df['Sell Price($)'])

    X = df[["localtime","src_addr","src_port","src_mac","dst_addr","dst_port","dst_mac","size"]]
    y = df['malicious']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()

    model.fit(X_train, y_train)

    prediction = model.predict(input)

    return prediction


