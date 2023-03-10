import predict_malicious_traffic
import numpy as np
import pandas as pd

input = [[1,1,1,1,1,1,1,1]]
df1 = pd.DataFrame(input, columns=["localtime","src_addr","src_port","src_mac","dst_addr","dst_port","dst_mac","size"])

print(input)
prediction = predict_malicious_traffic.get_prediction(input)

print(prediction)

