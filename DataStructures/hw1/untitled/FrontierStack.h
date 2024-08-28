//
// Created by Alp Onder Yener on 3/11/2024.
//

#ifndef HW1_FRONTIER_H
#define HW1_FRONTIER_H

#include <vector>
#include <iostream>
using namespace std;

// Cells of the maze
struct Cell {
    // coordinate values and pointers to other cells
    // if nullptr, there is a wall
    unsigned int x_coord, y_coord;
    Cell* up;
    Cell* down;
    Cell* left;
    Cell* right;

    // Parameterized constructor of the cell, with 4 walls surrounding it
    Cell(unsigned int x, unsigned int y) : x_coord(x), y_coord(y), up(nullptr), down(nullptr), left(nullptr), right(nullptr){}
};

template<typename T>
class FrontierStack {
private:
    struct Frontier_Node{
        T* which_item; // The node has a pointer which points to something (template)
        // For this homework we will use Cell*
        Frontier_Node* below_node; // The node beneath this in the stack

        // Parameterized constructor
        Frontier_Node(T* item) : which_item(item), below_node(nullptr){}
    };

    Frontier_Node* top_node;
    int size; // Size of the stack

public:
    FrontierStack(T*); // Parameterized constructor
    FrontierStack(); // Default constructor
    void AddNode(T*); // Add node to the stack
    T* Pop(); // Pop the top node
    T* TopElement(); // Return the top element
    bool isEmpty(); // Checks if stack is empty
    bool checkNode(unsigned int x, unsigned int y); // Check if there is a node in the stack where the x and y values are the ones in the parameter
    vector<vector<unsigned int>> get_path(); // Get the x and y values of the cells on the stack
    ~FrontierStack();
};

// Constructor
template<typename T>
FrontierStack<T>::FrontierStack() {
    top_node = nullptr;
}

// Add node to stack
template<typename T>
void FrontierStack<T>::AddNode(T* cell) {
    if (isEmpty()){
        Frontier_Node* new_element = new Frontier_Node(cell);
        new_element->below_node = nullptr;
        top_node = new_element;
        size++;
        return;
    }

    Frontier_Node* new_element = new Frontier_Node(cell);
    new_element->below_node = top_node;
    top_node = new_element;
    size++;
}

// Pop the top node
template<typename T>
T* FrontierStack<T>::Pop() {

    if (isEmpty()){
        cout << "Was already empty" << endl;
        return nullptr;
    }
    Frontier_Node* deleted_node = top_node;
    T* cell_popped = top_node->which_item;
    top_node = top_node->below_node;
    delete deleted_node;
    size--;
    return cell_popped;
}

// Return the top element
template<typename T>
T* FrontierStack<T>::TopElement() {
    return top_node->which_item;
}

// Check if the stack is empty
template<typename T>
bool FrontierStack<T>::isEmpty() {
    if (top_node == nullptr){return true;}
    return false;
}

// Destructor
template<typename T>
FrontierStack<T>::~FrontierStack() {

    while(top_node != nullptr){
        Frontier_Node* temp = top_node;
        top_node = top_node->below_node;
        temp = nullptr;
    }
}

// Check if the given x and y parameters are in the stack
template<typename T>
bool FrontierStack<T>::checkNode(unsigned int x, unsigned int y) {
    Frontier_Node* dummy = top_node;
    while (dummy != nullptr){
        T* current_cell = dummy->which_item;
        if (current_cell->x_coord == x && current_cell->y_coord == y){return true;}
        dummy = dummy->below_node;
    }
    return false;

}

// Get the x and y values of the cells on the stack
template<typename T>
vector<vector<unsigned int>> FrontierStack<T>::get_path() {
    vector<vector<unsigned int>> path_to_goal;
    Frontier_Node* top = top_node;
    while (top != nullptr){
        vector<unsigned int> push = {top->which_item->x_coord, top->which_item->y_coord};
        path_to_goal.push_back(push);
        top = top->below_node;
    }

    return path_to_goal;
}

#endif //HW1_FRONTIER_H