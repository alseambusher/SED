import json
res = "../res/"
features = json.load("features.json")
# weights
w_location = 0.1
w_time = 0.4
w_sift = 0.1
w_tags = 1-w_location-w_time-w_sift
