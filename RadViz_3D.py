import numpy as np
from numpy import arange, pi, sin, cos, arccos
import pandas as pd
import math
import matplotlib.pyplot as plt
import warnings

'''
To use PyQt5 instead of PyQt4 that is default
Used to make the window not resizable

'''
import matplotlib
matplotlib.use("Qt5Agg")

#Eliminates any warnings pandas would throw
warnings.filterwarnings(action='ignore', category=Warning)


class RadViz3D():
    def __init__(self, df, colour = None, dynamicScale = False, grid = False, sphereOpacity = 0.1, gridOpacity = 0.5, plotSize = 900, rotate = False):
        #Get the instance of the data frame
        #Copy is required so the first instance is not effected
        data = df.copy()

        #If you want to seperate the data based on a column copy the column
        colourData = False
        if colour != None and colour in data.columns.tolist():
            #Copy the data
            colourData = data[colour].copy()

            #Delete the data so that it isn't used to plot the points
            del data[colour]

        #Delete everything that is not a number and reset the index
        data = data.select_dtypes(exclude=['bool','object'])
        data.reset_index(drop = True, inplace = True)

        #####################################################
        #Create the co-ordinates and directions from the data
        #Create the distribution of points over the curve
        #####################################################
        #Number of points required to plot on the spheree
        N = data.shape[1]

        #Create points on the sphere based on the amount required
        spherePoints = self.pointSphereDistribution_Fibinacci(N)

        #Create normalized vectors
        vector_array = spherePoints[0]

        #Turn them into numpy arrays
        x = spherePoints[1]
        y = spherePoints[2]
        z = spherePoints[3]

        #Points for the outside of the circle
        sphere_Data = np.array([x,y,z])

        #Normalize the data in the columns from 0 to 1
        columnNames = data.columns.tolist()
        for i in range(0, data.shape[1]):
            #Map the values from 0 to 1 
            data[columnNames[i]] = ((data[columnNames[i]] - data[columnNames[i]].min()) / (data[columnNames[i]].max() - data[columnNames[i]].min()))

        #In the case where a field is empty fill the void with 0
        data = data.fillna(0)

        #######################################################
        #Calculate the points for the data
        #######################################################
        data_points_x = []
        data_points_y = []
        data_points_z = []

        #####################################################
        #Math 
        #####################################################
        #For each row in the data frame
        for i in range(0, data.shape[0]):
            x_dir = 0
            y_dir = 0
            z_dir = 0
            value_sum = 0
            #For each column in the data frame
            for j in range(0, data.shape[1]):
                #Get the data and respective value for the index in the column
                value = data.iloc[i, j]
                v = vector_array[j]

                #Create points by multiplying the data by the unit vector
                x_dir += v[0]*value
                y_dir += v[1]*value
                z_dir += v[2]*value
                value_sum += value

            #Put it back to unit vector form
            x_dir = x_dir/value_sum
            y_dir = y_dir/value_sum
            z_dir = z_dir/value_sum

            #Add it to the list
            data_points_x.append(x_dir)
            data_points_y.append(y_dir)
            data_points_z.append(z_dir)

        #Output the data points as 1D-arrays
        #Each x,y,z point represents a row in the inital data frame, the the respective order
        data_points_x = np.asarray(data_points_x)
        data_points_y = np.asarray(data_points_y)
        data_points_z = np.asarray(data_points_z)

        #IF dynamic scaling is enabled
        if dynamicScale:
            # Finds the maximum size vector
            dynamicScalingFactor = math.sqrt(np.amax(data_points_x**2 + data_points_y**2 + data_points_z**2))

            # Dividing the data by the scaling factor allows the maximum vector be located at the sphere surface
            data_points_x /= dynamicScalingFactor
            data_points_y /= dynamicScalingFactor
            data_points_z /= dynamicScalingFactor

        #Convery to np array
        point_Data = np.array([data_points_x, data_points_y, data_points_z])

        #Create a dataframe for np array
        pointDataFrame = pd.DataFrame(data = point_Data.T, columns = ["x","y","z"])

        #Is the colour is going to be seperated include it in the data frame
        if type(colourData) != bool:
            pointDataFrame["colour@Attribute"] = colourData

        ############################
        #Ploting with matplotlib
        ############################
        #Window size, the aspect ratio should be 1:1
        fig = plt.figure()
        win = fig.canvas.window()
        win.resize(plotSize,plotSize)
        win.setFixedSize(win.size())

        #Set up a 3D plot and define the axis's
        ax = fig.gca(projection='3d')              
        ax._axis3don = False
        ax.set_xlim3d(-1, 1)
        ax.set_ylim3d(-1, 1)
        ax.set_zlim3d(-1, 1)

        # make the panes transparent
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        # make the grid lines transparent
        ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

        # Create a sphere to plot as a reference image
        pi = np.pi
        cos = np.cos
        sin = np.sin
        phi, theta = np.mgrid[0.0:pi:50j, 0.0:2.0*pi:50j]
        x = sin(phi)*cos(theta)
        y = sin(phi)*sin(theta)
        z = cos(phi)
        ax.plot_surface(x, y, z,  rstride=1, cstride=1, color='b', alpha=sphereOpacity , linewidth=0)

        #Create the scatter plots of the dimensions, in black 
        ax.scatter(sphere_Data[0], sphere_Data[1], sphere_Data[2], color = "#000000")  

        #If center line enabled plot the center line
        if grid:
            #This creates a line from the sphere center to the sphere points
            for i in range(0, len(sphere_Data[0])):
                ax.plot([sphere_Data[0][i], 0], [sphere_Data[1][i], 0], [sphere_Data[2][i], 0], color = "#000000",linewidth=0.5, alpha=gridOpacity )

        #Add text to all the main data points
        for i, txt in enumerate(columnNames):
            ax.text(sphere_Data[0][i], sphere_Data[1][i], sphere_Data[2][i], txt, fontsize = 8, horizontalalignment='center', verticalalignment='top')

        #plot the scatter plot points based on the column selected for colour
        if "colour@Attribute" in pointDataFrame.columns.tolist():
            #For each unique value in the colour column do the following
            for j in pointDataFrame["colour@Attribute"].unique().tolist():
                #Get the values that correspond the colour value
                tempData = pointDataFrame.loc[pointDataFrame["colour@Attribute"] == j]

                #When matplotlib plots a scatter plot it is always a different colour than the last 
                ax.scatter(tempData["x"].tolist(), tempData["y"].tolist(), tempData["z"].tolist(), label=j)

            #Enable a legend
            ax.legend()

            #Output what the colours are based on
            title = str("Seperated by :"+ str(colour))
            ax.set_title(title)

        #If no colour is picked plot them all 
        else:
            ax.scatter(point_Data[0], point_Data[1], point_Data[2]) 
            #Output what the colours are based on
            title = "RadViz_3D"
            ax.set_title(title)

        fig.tight_layout()
        
        if rotate:
            for angle in range(0, 719, 2):
                ax.view_init(0, angle)
                plt.draw()
                plt.pause(.001)
        else:
            plt.show()


    def pointSphereDistribution_Fibinacci(self, N):
        #####################################################
        #Math 
        #####################################################
        #Create a numpy array from 
        i = arange(0, N, dtype=float) + 0.5
        phi = arccos(1 - 2*i/N)
        goldenRatio = (1 + 5**0.5)/2
        theta = 2 * pi * i / goldenRatio
        x = cos(theta) * sin(phi)
        y = sin(theta) * sin(phi)
        z = cos(phi)

        vector_list = []

        #####################################################
        #Create the points via math
        #####################################################
        for m in range(0, len(x)):
                #Create a unit vector for each direction
                normalized_divider = math.sqrt(x[m]**2 + y[m]**2 + z[m]**2)
                vector_list.append([(x[m]/normalized_divider),(y[m]/normalized_divider),(z[m]/normalized_divider)])

        #Create normalized vectors
        vector_array = np.array(vector_list)

        return (vector_array, x, y, z)
