//+
SetFactory("OpenCASCADE");
//+
Box(1) = {0, 0, 0, 0.1, 0.1, 0.02};
//+
Physical Surface("top", 13) = {6};
//+
Physical Surface("bottom", 14) = {5};
//+
Physical Surface("sides", 15) = {4, 2, 3, 1};
//+
Physical Volume("volume", 16) = {1};
//+
Transfinite Curve {8, 9, 4, 11, 6, 10, 2, 12} = 20 Using Progression 1;
//+
Transfinite Curve {5, 1, 3, 7} = 20 Using Progression 1;
//+
Transfinite Surface {1,2,3,4,5,6};
Transfinite Volume{1}; // make box elements instead of tetra

//Mesh.RecombineAll = 1; // don't recombine; even though 4x more elements than hex, still 2x faster!! 
//Mesh.RecombinationAlgorithm = 3;
Mesh.OptimizeNetgen = 1;


Mesh 3; 

//RecombineMesh; 

Coherence;