# Carrinheiros

### Abstract  

"Carrinheiros" are collectors of recyclable materials that use human propulsion vehicles in the selective collection, following routes with specific stops. The problem is that route can be very tiring for waste pickers according to the increase in vehicle weight and the roads' slope. Therefore, this work proposes a route suggestion service to minimize the pickers' physical effort on the collection route. The characteristics of the scenario addressed in this proposal are the distance between collect points, the depot's geographical position, the inclination of the roads, and the use of vehicles with human propulsion. Besides, this work should consider the variation in vehicle weight along the route. According to the availability of materials in a specific coverage area of the waste picker, stopping points should be defined, following a data model based on the waste advertising platforms' scheme, such as Cataki and Destino Sustentável. The proposal's validation must be performed through computer simulations, using SUMO and geographic data from Open Street Map.

### Data  model

The route creation service works from recyclable material advertising systems. The data needed to create the routes are illustrated in the Class Diagram in Figure 1.

<center>
<img src="https://raw.githubusercontent.com/vivirodrigues/Carrinheiros/main/documentation/classDiagram.png">  
Figure 1 - class Diagram
</center>
 
The User class has the attributes described in Figure 1. These data are read through a JSON file, as in the following example:  

{  
    "id": "001",  
    "type": "collector",  
    "name": "Maria",  
    "email": "maria@email.com",  
    "interest": "dispose",  
    "attended ads": ["0001"],  
    "coordinates" : [-22.818317, -47.083415, 604.0],  
    "coordinates_depot" : [-22.818317, -47.083415, 604.0]  
}  
  
The Advertisement class has the attributes described in Figure 1. These data are read through a JSON file, as in the following example:  

{  
    "id" : "0001",  
    "user_id" : "002",  
    "type" : "offer",  
    "material_type" : "paper",  
    "material_subtype" : "cardboard box",  
    "amount" : 5,  
    "measure_unit" : "kg",  
    "available_days" : ["Mon"],  
    "user_attending" : "001",  
    "status" : "in progress",  
    "coordinates" : [0.0, 0.0, 0.0]  
}  

