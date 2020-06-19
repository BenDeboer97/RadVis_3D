RadViz_3D

RadViz_3D is a program in python to plot multidimensional datasets on a 3D dimensional axis

Dependencies
The following python dependencies are required:
- numpy
- pandas
- matplotlib
Dependencies can be installed by using pip3 install dependency provide python is installed and added to path

File Location:
- The RadViz_3D.py file should be in copied into your working directory 


Input:
- df (pandas df): A single pandas data frame, can contain all data types, only the numerical datatypes will be used


Features:
- colour (str): A column name from the dataframe, default null, the value of this column will not be used to calculate the radviz points, instead it will be used to determine the colour of the point
- dynamicScale (bool): Default False, When activated the RadViz will linearly scale the points so the outer most point will contact the surface of the sphere.
- grid (bool): Default False, Create lines from the center of the sphere to the data points, allows for visual recognition of what angle a axis is located at
- sphereOpacity (float): Default 0.1, Changes the opacity of the sphere used from visual recognition, a value over 0.2 is not recommended
- gridOpacity (float): Default 0.5, Changes the opacity of the grid lines
- plotSize (int): Default 900, The pixel size of the final plot, the set aspect ratio is 1:1 to ensure no warping of the sphere


Output:
- A single 3D radViz plot
- The plot combines multiple scatter and line plots, with a surface plot for the sphere


Example code:
"
from RadViz_3D import RadViz3D
import pandas as pd

data = pd.read_csv("qsar_fish_toxicity.csv")

print(data.columns.tolist())

RadViz3D(data, colour = "NdssC", grid = True, dynamicScale= True, plotSize=1000)
"
