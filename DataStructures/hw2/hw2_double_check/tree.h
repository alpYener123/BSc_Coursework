//
// Created by alpye on 4/13/2024.
//

#ifndef HW2_DOUBLE_CHECK_TREE_H
#define HW2_DOUBLE_CHECK_TREE_H

#include <string>
#include <vector>
using namespace std;
#include "node.h"


template <class Comparable>
class AvlTree{
public:
    explicit AvlTree( const Comparable & notFound ); // Constructor
    AvlTree( const AvlTree & rhs );
    ~AvlTree( );

    const Comparable & findMin( ) const; // Find minimum element
    const Comparable & findMax( ) const; // Find maximum element
    const Comparable & find( const Comparable & x ) const; // Finds the element at the parameter
    bool isEmpty( ) const; // Check if the tree is empty

    void makeEmpty( ); // Make the tree empty
    void insert( const Comparable & x ); // Insert an element
    void remove( const Comparable & x ); // Remove an element

private:
    AvlNode<Comparable> *root; // Root of the tree
    const Comparable ITEM_NOT_FOUND;

    const Comparable & elementAt( AvlNode<Comparable> *t ) const; // Returns the data stored in that node

    void insert( const Comparable & x, AvlNode<Comparable> * & t ) const; // Insert node
    void remove(const Comparable & x, AvlNode<Comparable> * & t ) const; // Remove node

    AvlNode<Comparable> * findMin( AvlNode<Comparable> *t ) const; // Find minimum node with respect to its element
    AvlNode<Comparable> * findMax( AvlNode<Comparable> *t ) const; // Find max, same logic as min
    AvlNode<Comparable> * find( const Comparable & x, AvlNode<Comparable> *t ) const; // Find a specific element
    void makeEmpty( AvlNode<Comparable> * & t ) const; // Make the tree empty

    // AVL manipulations
    int height( AvlNode<Comparable> *t ) const; // Return the height
    int max( int lhs, int rhs ) const; // Return the max
    void rotateWithLeftChild( AvlNode<Comparable> * & k2 ) const; // Left and right rotations of the AVL tree
    void rotateWithRightChild( AvlNode<Comparable> * & k1 ) const;
    void doubleWithLeftChild( AvlNode<Comparable> * & k3 ) const;
    void doubleWithRightChild( AvlNode<Comparable> * & k1 ) const;

};


// Constructor
template <class Comparable>
AvlTree<Comparable>::AvlTree(const Comparable & notFound ) : ITEM_NOT_FOUND( notFound ), root( NULL ) {}

// Returns the data stored at that node
template <class Comparable>
const Comparable & AvlTree<Comparable>::elementAt( AvlNode<Comparable> *t ) const
{
    return t == NULL ? ITEM_NOT_FOUND : t->element;
}

// Input is the element we want to find.
// Returns the output of the internal find method which traverses the tree
template <class Comparable>
const Comparable & AvlTree<Comparable>::find( const Comparable & x ) const
{
    return elementAt( find( x, root ) );
}

// The internal method of find.
// Recursively traverses the tree until the given element (or null) is found
template <class Comparable>
AvlNode<Comparable> *AvlTree<Comparable>::find( const Comparable & x, AvlNode<Comparable> * t ) const
{
    if ( t == NULL )
        return NULL;
    else if( x < t->element )
        return find( x, t->left );
    else if( t->element < x )
        return find( x, t->right );
    else
        return t;    // Match
}

// find minimum element
template <class Comparable>
const Comparable & AvlTree<Comparable>::findMin( ) const
{
    return elementAt( findMin( root ) );
}

// Internal method. Recursively traverses the tree to find the min item
template <class Comparable>
AvlNode<Comparable> *AvlTree<Comparable>::findMin( AvlNode<Comparable> *t )const
{
    if( t == NULL )
        return NULL;
    if( t->left == NULL )
        return t;
    return findMin( t->left );
}

// Same as findmin, but for max
template <class Comparable>
const Comparable & AvlTree<Comparable>::findMax( ) const
{
    return elementAt( findMax( root ) );
}

// Same as findmin, but for max
template <class Comparable>
AvlNode<Comparable> *AvlTree<Comparable>::findMax( AvlNode<Comparable> *t )const
{
    if( t == NULL )
        return NULL;
    if( t->right == NULL )
        return t;
    return findMax( t->right );
}

// Returns the height of the node, to decide whether to leftRotate or rightRotate
template <class Comparable>
int AvlTree<Comparable>::height( AvlNode<Comparable> *t ) const
{
    if (t == NULL)
        return -1;

    return t->height;
}

// Returns the maximum of left and right nodes
template <class Comparable>
int AvlTree<Comparable>::max( int lhs, int rhs ) const
{
    if (lhs > rhs)
        return lhs;

    return rhs;
}

// insertion for AVL tree
template <class Comparable>
void AvlTree<Comparable>::insert( const Comparable & x )
{
    insert( x, root );
}

// remove the node from the tree
template <class Comparable>
void AvlTree<Comparable>::remove( const Comparable & x )
{
    remove( x, root );
}

// private method for remove
template <class Comparable>
void AvlTree<Comparable>::remove( const Comparable & x, AvlNode<Comparable> * & t )const
{
    if( t == NULL )
        return;   // Item not found, do nothing
    if( x < t->element ) {
        remove(x, t->left);

        if (height(t->left) - height(t->right) == 2) // check left tree height
        {
            if ( x < t->left->element ){
                rotateWithLeftChild( t );
            }
            else{
                doubleWithLeftChild( t );
            }
        }
    }

    else if( t->element < x ) {
        remove(x, t->right);
        if ( height( t->right ) - height( t->left ) == 2 ) // check right tree height
        {
            if ( t->right->element < x )
            {
                rotateWithRightChild( t );
            }
            else
            {
                doubleWithRightChild( t );
            }
        }
    }
    else if( t->left != NULL && t->right != NULL ) // Two children
    {
        t->element = findMin( t->right )->element; // get the min element from right subtree
        remove( t->element, t->right ); // remove that element from the right subtree
        if ( height( t->right ) - height( t->left ) == 2 ) // check right tree height
        {
            if ( t->right->element < x )
            {
                rotateWithRightChild( t );
            }
            else
            {
                doubleWithRightChild( t );
            }
        }
    }
    else // one or no children
    {
        AvlNode<Comparable> *oldNode = t;
        t = ( t->left != NULL ) ? t->left : t->right;
        delete oldNode;
    }
}

// AVL tree insertion, private method
template <class Comparable>
void AvlTree<Comparable>::insert( const Comparable & x, AvlNode<Comparable> * & t ) const {
    if (t == NULL)
        t = new AvlNode<Comparable>(x, NULL, NULL); // if the node is null, add it there

    else if (x < t->element) { // x should be inserted to the left since it is smaller
        insert(x, t->left);

        // left subtree grew in height. If there is an imbalance, rotate
        if (height(t->left) - height(t->right) == 2) {
            if (x < t->left->element) { rotateWithLeftChild(t); }
            else { doubleWithLeftChild(t);
            }
        }
    }
    else if( t->element < x ) // x should be inserted to the right since it is bigger
    {
        insert( x, t->right );
        if ( height( t->right ) - height( t->left ) == 2 ) // right subtree grew in height. If there is an imbalance, rotate
        {
            if (t->right->element < x) { rotateWithRightChild(t); } // if x was inserted to right-right subtree
            else { doubleWithRightChild(t); }
        } // if x was inserted to right-left subtree
    }


    // update the height the node
    t->height = max( height( t->left ), height( t->right ) ) + 1;
}

// rotate according to the case on function insert
// case 1 on slides
template <class Comparable>
void AvlTree<Comparable>::rotateWithLeftChild(AvlNode<Comparable> * & k2 ) const
{
    AvlNode<Comparable> *k1 = k2->left;
    k2->left = k1->right;
    k1->right = k2;
    k2->height = max( height( k2->left ), height( k2->right ) ) + 1;
    k1->height = max( height( k1->left ), k2->height ) + 1;
    k2 = k1;
}

// rotate according to the case on function insert
// case 4 on slides
template <class Comparable>
void AvlTree<Comparable>::rotateWithRightChild
        ( AvlNode<Comparable> * & k1 ) const
{
    AvlNode<Comparable> *k2 = k1->right;
    k1->right = k2->left;
    k2->left = k1;
    k1->height = max( height( k1->left ), height( k1->right ) ) + 1;
    k2->height = max( height( k2->right ), k1->height ) + 1;
    k1 = k2;
}

// rotate according to the case on function insert
// case 2 on slides
template <class Comparable>
void AvlTree<Comparable>::doubleWithLeftChild( AvlNode<Comparable> * & k3 ) const
{
    rotateWithRightChild( k3->left );
    rotateWithLeftChild( k3 );
}

// rotate according to the case on function insert
// case 3 on slides
template <class Comparable>
void AvlTree<Comparable>::doubleWithRightChild( AvlNode<Comparable> * & k1 ) const
{
    rotateWithLeftChild( k1->right );
    rotateWithRightChild( k1 );
}

// make the tree empty
template <class Comparable>
void AvlTree<Comparable>::makeEmpty( )
{
    makeEmpty( root );
}

// internal make empty function
template <class Comparable>
void AvlTree<Comparable>::makeEmpty( AvlNode<Comparable> * & t ) const
{
    if( t != NULL )
    {
        makeEmpty( t->left );
        makeEmpty( t->right );
        delete t;
    }
    t = NULL;
}

// check if the tree is empty
template <class Comparable>
bool AvlTree<Comparable>::isEmpty( ) const
{
    if (root != NULL){return false;}
    return true;
}

// destructor
template <class Comparable>
AvlTree<Comparable>::~AvlTree( )
{
    makeEmpty( );
}

// copy constructor
template <class Comparable>
AvlTree<Comparable>::AvlTree( const AvlTree<Comparable> & rhs ) : root( NULL ), ITEM_NOT_FOUND( rhs.ITEM_NOT_FOUND )
{
    *this = rhs;
}


#endif //HW2_DOUBLE_CHECK_TREE_H
