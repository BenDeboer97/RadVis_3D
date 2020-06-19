from RadViz_3D import RadViz3D
import pandas as pd

data = pd.read_csv("qsar_fish_toxicity.csv")

print(data.columns.tolist())

RadViz3D(data, colour = "NdssC", grid = True, dynamicScale= True, plotSize=1000)