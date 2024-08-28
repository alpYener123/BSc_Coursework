// Created by Alp Onder Yener

using namespace std;
#include <iostream>
#include <vector>
#include "FrontierStack.h"
#include <random>
#include <string>
#include <fstream>

// get the inputs M, N and K
vector<int> get_inputs(){
    int row_num, col_num, maze_num;
    cout << "Enter the number of mazes: ";
    cin >> maze_num;
    cout << "Enter the number of rows and columns (M and N): ";
    cin >> row_num >> col_num;

    vector<int> inputs = {row_num, col_num, maze_num};

    return inputs;
}

// Check if the given coordinates are the coordinates of a cell in CLOSED
bool checkClosed(vector<Cell*> closed, int x, int y){
    for (int i=0; i < closed.size(); i++){
        if (closed[i]->x_coord==x && closed[i]->y_coord==y){
            return true;
        }
    }
    return false;
}

// Check if the given cell is whether in CLOSED or in FRONTIER
bool isCellVisited(FrontierStack<Cell> stack, vector<Cell*> closed, Cell* checking_cell){
    int x = checking_cell->x_coord;
    int y = checking_cell->y_coord;

    bool in_stack = stack.checkNode(x,y);
    bool in_closed = checkClosed(closed, x, y);
    if (in_stack){return true;}
    if (in_closed){return true;}

    return false;
}

// Pick a random direction given the available directions
// Example: right = true --> right is an available direction
string pick_random_direction(bool right, bool left, bool up, bool down){
    vector<string> directions;
    if (right){directions.push_back("right");}
    if (left){directions.push_back("left");}
    if (up){directions.push_back("up");}
    if (down){directions.push_back("down");}

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distrib(0, directions.size() - 1);
    string random_direction = directions[distrib(gen)];

    return random_direction;
}

// Generate the maze
vector<Cell*> generate_maze(int M, int N){
    // The cells which are closed are going to be added to closed (the ones that have all the successors checked)
    vector<Cell*> closed;

    // Add the first cell to the frontier stack
    Cell * initial_cell = new Cell(0,0);
    FrontierStack stack = FrontierStack<Cell>();
    stack.AddNode(initial_cell);

    // While there are still elements on the frontier stack (unexplored nodes)
    while (!stack.isEmpty()){
        // Get the top element and its coordinate values
        Cell * current_node = stack.TopElement();
        bool right=false, left=false, up=false, down=false;
        int x = current_node->x_coord; int y = current_node->y_coord;

        // Check the available directions:

        // check right:
        if (x+1 < N){
            Cell * dummy_cell = new Cell(x+1, y);
            if (!isCellVisited(stack, closed, dummy_cell)){
                right=true;
            }
        }

        // check left:
        if (x-1 > -1){
            Cell * dummy_cell = new Cell(x-1, y);
            if (!isCellVisited(stack, closed, dummy_cell)){
                left=true;
            }
        }

        // check up:
        if (y+1 < M){
            Cell * dummy_cell = new Cell(x, y+1);
            if (!isCellVisited(stack, closed, dummy_cell)){
                up=true;
            }

        }

        // check down:
        if (y-1 > -1){
            Cell * dummy_cell = new Cell(x, y-1);
            if (!isCellVisited(stack, closed, dummy_cell)){
                down=true;
            }
        }


        // If no available direction, close the cell
        if (!right && !left && !up && !down){
            Cell* closed_cell = stack.Pop();
            closed.push_back(closed_cell);
        }
        else{
            // Pick one of the available directions at random
            string direction = pick_random_direction(right, left, up, down);

            // Move the cell according to the direction, then add the new cell to frontier stack

            if (direction == "right"){
                int new_x = x+1; int new_y = y;
                Cell * new_cell = new Cell(new_x,new_y);
                current_node->right = new_cell;
                new_cell->left = current_node;
                stack.AddNode(new_cell);
            }
            else if (direction == "left"){
                int new_x = x-1; int new_y = y;
                Cell * new_cell = new Cell(new_x,new_y);
                current_node->left = new_cell;
                new_cell->right = current_node;
                stack.AddNode(new_cell);
            }
            else if (direction == "up"){
                int new_x = x; int new_y = y+1;
                Cell * new_cell = new Cell(new_x,new_y);
                current_node->up = new_cell;
                new_cell->down = current_node;
                stack.AddNode(new_cell);
            }
            else if (direction == "down"){
                int new_x = x; int new_y = y-1;
                Cell * new_cell = new Cell(new_x,new_y);
                current_node->down = new_cell;
                new_cell->up = current_node;
                stack.AddNode(new_cell);
            }
        }

    }

    return closed;
}

// After we get the maze, write the maze into a file
string write_maze_to_file(vector<Cell*> result, int M, int N){
    // Write the dimensions
    string write = to_string(M) + " " + to_string(N) + '\n';
    for (int i=result.size()-1; i >= 0; i--){
        string x = to_string(result[i]->x_coord);
        string y = to_string(result[i]->y_coord);
        string l,r,u,d;

        // When a cell points to nullptr (or when it is on the border of the maze) there is a wall
        if(x =="0" || result[i]->left == nullptr){l=to_string(1);} else{l=to_string(0);}
        if(x == to_string(N-1) || result[i]->right == nullptr){r=to_string(1);} else{r=to_string(0);}
        if(y == to_string(M-1) || result[i]->up == nullptr){u=to_string(1);} else{u=to_string(0);}
        if(y =="0" || result[i]->down == nullptr){d=to_string(1);} else{d=to_string(0);}

        // The given format: each coordinate and the walls on that coordinate
        write += "x="+x+" "+"y="+y+" "+"l="+l+" r="+r+" u="+u+" d="+d+'\n';
    }
    return write;
}

// Return the cell* that have the given x and y coordinates
Cell* return_cell(vector<Cell*> maze, int x, int y){
    Cell* found_cell;
    for (int i = 0; i<maze.size(); i++){
        Cell* current = maze[i];
        if (current->x_coord == x && current->y_coord == y){found_cell = current;}
    }

    return found_cell;

}

// Give the path from start to end coordinates.
// Tries finding the path via a similar method as maze generation. Uses a stack and returns it.
FrontierStack<Cell> give_path(vector<Cell*> maze, int x_start, int y_start, int x_end, int y_end){
    vector<Cell*> closed;

    Cell* starting_cell = return_cell(maze, x_start, y_start);
    FrontierStack stack = FrontierStack<Cell>();
    stack.AddNode(starting_cell);


    while (!stack.isEmpty()){

        Cell * current_node = stack.TopElement();
        bool right=false, left=false, up=false, down=false;
        int x = current_node->x_coord; int y = current_node->y_coord;

        // check right:
        if (current_node->right != nullptr){
            Cell * dummy_cell = new Cell(x+1, y);
            if (!isCellVisited(stack, closed, dummy_cell)){
                right=true;
            }
        }

        // check left:
        if (current_node->left != nullptr){
            Cell * dummy_cell = new Cell(x-1, y);
            if (!isCellVisited(stack, closed, dummy_cell)){
                left=true;
            }
        }

        // check up:
        if (current_node->up != nullptr){
            Cell * dummy_cell = new Cell(x, y+1);
            if (!isCellVisited(stack, closed, dummy_cell)){
                up=true;
            }

        }

        // check down:
        if (current_node->down != nullptr){
            Cell * dummy_cell = new Cell(x, y-1);
            if (!isCellVisited(stack, closed, dummy_cell)){
                down=true;
            }
        }

        if (!right && !left && !up && !down){
            Cell* closed_cell = stack.Pop();
            closed.push_back(closed_cell);
        }
        else{
            string direction = pick_random_direction(right, left, up, down);

            int new_x, new_y;

            if (direction == "right"){
                new_x = x+1; new_y = y;
                Cell * new_cell = return_cell(maze, new_x, new_y);
                stack.AddNode(new_cell);
            }
            else if (direction == "left"){
                new_x = x-1;  new_y = y;
                Cell * new_cell = return_cell(maze, new_x, new_y);
                stack.AddNode(new_cell);
            }
            else if (direction == "up"){
                new_x = x;  new_y = y+1;
                Cell * new_cell = return_cell(maze, new_x, new_y);
                stack.AddNode(new_cell);
            }
            else if (direction == "down"){
                new_x = x;  new_y = y-1;
                Cell * new_cell = return_cell(maze, new_x, new_y);
                stack.AddNode(new_cell);
            }

            if (new_x == x_end && new_y == y_end){
                break;
            }

        }

    }
    return stack;

}



int main() {
    // get inputs
    vector<int> inputs = get_inputs();

    int M = inputs[0], N = inputs[1], K = inputs[2];

    // If K=5, there will be 5 vectors here. Each indicate a maze.
    vector<vector<Cell*>> all_results;

    // K times, generate a maze and write it into a file
    for (int i = 0; i < K; i++){
        vector<Cell*> result = generate_maze(M,N);
        all_results.push_back(result);

        string write = write_maze_to_file(result, M, N);
        string filename = "maze_"+to_string(i+1)+".txt";
        ofstream outfile(filename);
        outfile << write;
        outfile.close();

    }

    cout << "All mazes are generated." << endl << endl;

    // Get inputs for path finding
    int maze_num, x_start, y_start, x_end, y_end;
    cout << "Enter a maze ID between 1 to "  << K << " inclusive to find a path: ";
    cin >> maze_num;
    cout << "Enter x and y coordinates of entry points (x,y) or (column, row): ";
    cin >> x_start >> y_start;
    cout << "Enter x and y coordinates of exit points (x,y) or (column, row): ";
    cin >> x_end >> y_end;

    // Get the path from entry to exit points
    FrontierStack path = give_path(all_results[maze_num-1], x_start, y_start, x_end, y_end);

    // Get the path as a vector of vector. The inner vectors are of 2 elements, x and y
    vector<vector<unsigned int>> to_write = path.get_path();

    // Write the path to a file
    string path_to_txt = "";
    for (int i = to_write.size() - 1; i >= 0; i--){
        path_to_txt += to_string(to_write[i][0]) + " " + to_string(to_write[i][1]) + '\n';
    }
    string append_to_filename = to_string(x_start) + "_" + to_string(y_start) + "_" + to_string(x_end) + "_" + to_string(y_end) + ".txt";
    string path_filename = "maze_"+to_string(maze_num)+"path_" + append_to_filename;
    ofstream outfile(path_filename);
    outfile << path_to_txt;
    outfile.close();




    return 0;

}