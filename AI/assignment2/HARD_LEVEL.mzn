% Alp Onder Yener -- 31183
%% LEVEL: HARD

% Island number is 19 and grid size is 7x7 at the moment.
set of int: number_of_islands = 1..11;
set of int: grid = 0..6;
set of int: bridge = 1..16;
set of int: islands_without_last = 1..10; % for connectedness
% also calculate and change number of bridges according to thge problem

% Matrix of coordinates for the islands (USER-INPUT)
% (0,0) is the left bottom corner of the grid. (x,y) is the format.

array[number_of_islands,1..2] of var grid: coordinates = [|0,0,
                                                          |3,0,
                                                          |4,1,
                                                          |6,1,
                                                          |1,2,
                                                          |3,2,
                                                          |1,4,
                                                          |4,4,
                                                          |6,4,
                                                          |1,6,
                                                          |6,6,
                                                          |];

% Array of the numbers on those islands (USER-INPUT)
% Note: Must be aligned with coordinates. First element of coordinates must have the first number here
array[number_of_islands] of var 1..8: numbers_on_islands = [1,3,3,2,2,3,5,4,2,4,3];

% Matrix that represent bridges. Number of bridges = SUM(number_on_islands) / 2
% This is the variable to be decided
array[bridge,1..2] of var number_of_islands: bridges;

% CONSTRAINT: Connectedness
array[number_of_islands] of var number_of_islands: connected_path;
array[number_of_islands] of var bool: included;
constraint connected_path[1] = bridges[1,1] /\ included[bridges[1,1]] = true; % first island of the first bridge is the first element
% Now try to go to itself, going through all the islands
constraint forall(i in islands_without_last)(
                 forall(j in bridge)(
                      if bridges[j,1] = connected_path[i] /\ included[bridges[j,2]] = false then
                          included[bridges[j,2]] = true /\ connected_path[i+1] = bridges[j,2]
                      else if bridges[j,2] = connected_path[i] /\ included[bridges[j,1]] = false then
                          included[bridges[j,1]] = true /\ connected_path[i+1] = bridges[j,1]
                      endif endif
  ) 
);
constraint forall(i in number_of_islands) (
    included[i]
);



% CONSTRAINT 1: A bridge must begin and end at distinct islands as a straight line in between.
% CONSTRAINT 2: A bridge may only run vertically or horizontally
constraint forall(i in bridge)(
                 (coordinates[bridges[i,1],1] = coordinates[bridges[i,2],1]) != (coordinates[bridges[i,1],2] = coordinates[bridges[i,2],2])
);


% CONSTRAINT 3: At most two bridges connect a pair of islands.
constraint forall(i in bridge)(
       bridges[i, 1] < bridges[i, 2]
  
);
array[bridge] of var 1..2: bridgeOccurrences;
% At most two bridges connect a pair of islands.
constraint forall(i in bridge)(
   bridgeOccurrences[i] = sum(j in bridge)(
       if forall(k in 1..2)(bridges[i,k] = bridges[j,k]) then 1 else 0 endif
   )
);


% CONSTRAINT 4: The number of bridges connected to each island must match the number on that island.
constraint forall(k in number_of_islands)
                (numbers_on_islands[k] = sum(i in bridge, j in 1..2)
                  (if bridges[i,j] = k then 1 else 0 endif));
                  
                  
% CONSTRAINT 5

% Do not cross islands ONLY       
constraint forall(i in bridge)( %% if unstable x axis
 if coordinates[bridges[i,1],2] = coordinates[bridges[i,2],2] then
   bridges[i,2] - bridges[i,1] = 1
 else if bridges[i,2] - bridges[i,1] > 1 then %% unstable y axis with big enough space in between
forall(j in bridges[i,1]+1..bridges[i,2]-1)(
    coordinates[j,1] != coordinates[bridges[i,1],1]
 )
 endif endif
);


% No cross-bridgeing
constraint forall(i in bridge)(
 forall(j in bridge)(
   if bridges[j,1] < bridges[i,1] /\ bridges[i,2] < bridges[j,2] then
     coordinates[bridges[i,1],1] > coordinates[bridges[j,2],1] \/ coordinates[bridges[j,2],1] > coordinates[bridges[i,2],1]
   endif
 )
);

output [
  % Iterate over each element of the matrix and convert each element to string
  show(bridges[i,j]) ++ " " ++ if j == 2 then "\n" else "" endif
  | i in bridge, j in 1..2
];