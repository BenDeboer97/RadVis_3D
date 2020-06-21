<h1> RadViz_3D </h1>

<p>RadViz_3D is a program in python to plot multidimensional datasets on a 3D dimensional axis</p>

<h2>Dependencies</h2>
<p>The following python dependencies are required:</p>
<ul>
<li>numpy</li>
<li>pandas</li>
<li>matplotlib</li>
</ul>
<p>Dependencies can be installed by using pip3 install dependency provide python is installed and added to path</p>

<h2>File Location:</h2>
<ul>
<li> The RadViz_3D.py file should be in copied into your working directory </li>
</ul>

<h2>Input:</h2>
<ul>
<li><b>df (pandas df):</b> A single pandas data frame, can contain all data types, only the numerical datatypes will be used</li>
</ul>

<h2>Features:</h2>
<ul>
<li><b>colour (str):</b> A column name from the dataframe, default null, the value of this column will not be used to calculate the radviz points, instead it will be used to determine the colour of the point</li>
<li><b>dynamicScale (bool):</b> Default False, When activated the RadViz will linearly scale the points so the outer most point will contact the surface of the sphere.</li>
<li><b>grid</b> (bool):</b> Default False, Create lines from the center of the sphere to the data points, allows for visual recognition of what angle a axis is located at</li>
<li><b>sphereOpacity (float):</b> Default 0.1, Changes the opacity of the sphere used from visual recognition, a value over 0.2 is not recommended
<li><b>gridOpacity (float):</b> Default 0.5, Changes the opacity of the grid lines</li>
<li><b>plotSize (int):</b> Default 900, The pixel size of the final plot, the set aspect ratio is 1:1 to ensure no warping of the sphere</li>
<li><b>rotate</b> (bool):</b> Default False, Rotates the plot around the Z axis 720 degrees
</ul>

<h2>Output:</h2>
<ul>
<li>A single 3D radViz plot</li>
<li>The plot combines multiple scatter and line plots, with a surface plot for the sphere</li>
</ul>

<h2>Example code:</h2>
<p>
from RadViz_3D import RadViz3D
import pandas as pd

data = pd.read_csv("qsar_fish_toxicity.csv")

print(data.columns.tolist())

RadViz3D(data, colour = "NdssC", grid = True, dynamicScale= True, plotSize=1000)
</p>
