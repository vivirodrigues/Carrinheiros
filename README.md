
# Carrinheiros

"Carrinheiros" are collectors of recyclable materials that use human propulsion vehicles in the selective collection. The problem is that route can be very tiring for waste pickers according to the increase in vehicle weight and the roads' slope. Therefore, this work proposes a route suggestion service to minimize the collection time or the pickers' physical effort on the route. The characteristics of the scenario addressed in this proposal are the distance between collect points, the depot's geographical position, the inclination of the roads, and the use of vehicles with human propulsion. Besides, this work should consider the variation in vehicle weight along the route.

<img src="https://raw.githubusercontent.com/vivirodrigues/Carrinheiros/main/documentation/carrinheiro.png">

Tools employed in this work:

* This work used the osmnx package to construct geographic graphs in Python. The osmnx documentation is available on https://osmnx.readthedocs.io/en/stable/.

* The tool Networkx is used to manipulate and construct graphs in Python. The Networkx documentation is available on https://networkx.org/documentation/stable/.

* The geographic data was obtained from Open Street Map (https://www.openstreetmap.org/), and Brazil's elevation data was obtained from Topodata (http://www.dsr.inpe.br/topodata/index.php).

* The proposal's validation was performed through computer simulations using Simulation of Urban MObility (SUMO). The SUMO documentation is available on https://sumo.dlr.de/docs/.



```python
from IPython.display import Image
```

To execute the simulations, access 'Main.py' file. The Main.py has the "get_seed" function, which provides the random seed to guarantee the reproducibility of the simulation. The seed_id input is the index of 'seeds' vector.


```python
def get_seed(seed_id):
    
    seeds = [960703545, 1277478588, 1936856304,
             186872697, 1859168769, 1598189534,
             1822174485, 1871883252, 694388766,
             188312339, 773370613, 2125204119,
             2041095833, 1384311643, 1000004583,
             358485174, 1695858027, 762772169,
             437720306, 939612284, 425414105,
             1998078925, 981631283, 1024155645,
             558746720, 1349341884, 678622600,
             1319566104, 538474442, 722594620,
             1700738670, 1995749838, 1147024708,
             346983590, 565528207, 513791680,
             1996632795, 2081634991, 1769370802,
             349544396, 1996610406, 1973272912,
             1972392646, 605846893, 934100682,
             222735214, 2101442385, 2009044369,
             1895218768, 701857417, 89865291,
             144443207, 720236707, 822780843,
             898723423, 1644999263, 985046914,
             1859531344, 1024155645, 764283187,
             778794064, 683102175, 1334983095,
             1072664641, 999157082]
    
    return seeds[seed_id]
```

The 'main' function executes the experiments on the SUMO simulator. First of all, it sets the characteristics of the scenario: number of collect points, values of vehicle weight increment, city of the scenario, number of repetitions of the simulations, etc. Then, it creates pseudo-random collect points/stop points of the scenario. Finally, it calls the 'create_route' function.


```python
def main():
    
    # number of collect points
    n_points = 10

    # maximum increment of vehicle weight at the collect point (material mass)
    max_mass_material = 50

    # random seed of mass increment
    random.seed(get_seed(0))

    # scenarios: 'Belo Horizonte' and 'Belem'
    city = 'Belo Horizonte'

    # mean of the gaussian function that creates the collect points
    if city == 'Belo Horizonte':
        mean_lon = [-43.9438]
        mean_lat = [-19.9202]
    elif city == 'Belem':
        mean_lon = [-48.47000]
        mean_lat = [-1.46000]

    # standard deviation of the gaussian function that creates the collect points
    sigma = 0.005    

    # vector with vehicle weight increment in the collect points
    mass_increments = [random.randint(0, max_mass_material) for i in range(n_points-2)]

    # add unit of measurement of vehicle weight increment in the collect points
    material_weights = [(mass_increments[i], 'Kg') for i in range(n_points-2)]

    # the arrival point must not increment the vehicle weight
    material_weights.append((0, 'Kg'))
    
    # the starting point must not increment the vehicle weight
    material_weights.insert(0, (0, 'Kg'))
    
    # number of repetitions of the simulations
    n_seeds = 30
    
    json_files = []
    materials = {}

    for n in range(0, n_seeds):
        
        # gets the current random seed
        random.seed(get_seed(n))
        
        # creates a vector with pseudo-random longitude and latitude values
        longitudes = [random.gauss(mean_lon[0], sigma) for i in range(n_points)]
        latitudes = [random.gauss(mean_lat[0], sigma) for i in range(n_points)]
        
        # creates the collect points with longitude and latitudes values
        stop_points = [(float(latitudes[i]), float(longitudes[i])) for i in range(len(latitudes))]
        
        # creates a dict with vehicle mass increment in each collect point
        [materials.update([((latitudes[i], longitudes[i]), material_weights[i])]) for i in range(len(latitudes))]
        
        # creates the routes and writes the simulation results on json file. It returns the name of the file
        json_files = create_route(stop_points, materials, json_files, n)


```

The "create route" function generates two graphs: the geographic scenario graph and the ordering graph. It uses the osmnx to creates the geographic graph based on Open Street Map data. Besides, the networkx is used to generates the ordering graph, which is complete, and each vertex corresponds to a collection point. The Nearest Neighbor search is the heuristic used to order the vertexes. Also, the Shortest Path Faster Algorithm is employed to create a route between two collection points in the geographic graph.

Figure 1 shows the ordering graph with a red connection between 8 and 9 vertexes. This connection corresponds to the path in the geographic graph exhibited in Figure 2.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/vivirodrigues/Carrinheiros/main/documentation/grafo1.png">
        </td>
        <td>
            <img src="https://raw.githubusercontent.com/vivirodrigues/Carrinheiros/main/documentation/grafo_a.png">
        </td>
    </tr>
    <tr>
        <td>
            <p>Figure 1: Ordering graph</p>
        </td>
        <td>
            <p>Figure 2: Geogrpahic graph</p>
        </td>
    </tr>
</table>

The combination of SPFA and nearest neighbor provides routes based on three edge costing policies: Less Work Policy (LWP), Less Impedance Policy (LIP), and Short Distance Policy (SDP). The LWP minimizes the work required to push the vehicle, LIP avoids steep slopes and SDP minimizes the total distance. Using the first random seed (960703545), the algorithm generates three routes based on the policies:

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/vivirodrigues/Carrinheiros/main/documentation/weight.png">
        </td>
        <td>
            <img src="https://raw.githubusercontent.com/vivirodrigues/Carrinheiros/main/documentation/impedance.png">
        </td>
        <td>
            <img src="https://raw.githubusercontent.com/vivirodrigues/Carrinheiros/main/documentation/distance.png">
        </td>
    </tr>
    <tr>
        <td>
            <p>Figure 3: Route generated using LWP</p>
        </td>
        <td>
            <p>Figure 4: Route generated using LIP</p>
        </td>
        <td>
            <p>Figure 5: Route generated using SDP</p>
        </td>
    </tr>
</table>


```python

```
