from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("traffic.csv")
df.head()

# %matplotlib inline
# plt.scatter(df['Mileage'], df['Sell Price($)'])

X = df[['Mileage', 'Age(yrs)']]
y = df['Sell Price($)']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()

model.fit(X_train, y_train)

prediction = model.predict(X_test)
score = model.score(X_test, y_test)

print(prediction)
