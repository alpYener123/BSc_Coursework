//
// Created by Alp Onder Yener on 5/13/2024.
//

#ifndef HW3_NODE_H
#define HW3_NODE_H

#include <string>
#include <vector>
using namespace std;

template <class Comparable>
class AvlTree;

// containts the name of the file (document), the count for the word in that file and the word itself
struct DocumentItem {
    string documentName;
    int count;
    string word;

    DocumentItem(string file_name, int occurence_count, string keyword): documentName(file_name), count(occurence_count), word(keyword){}

};

// contains the item which is a template (will be string in our case) and a vector of document items
template <class Comparable>
struct WordItem {
    Comparable word;
    vector<DocumentItem> document_items;

    WordItem(string keyword, vector<DocumentItem> documents): word(keyword), document_items(documents){}

};

// element as the data that is stored by the node, left and right pointers and an integer signaling the height of the node on the tree
template <class Comparable>
class AvlNode
{
public:
    Comparable element;
    AvlNode   		*left;
    AvlNode   		*right;
    int        		height;

    AvlNode( const Comparable & theElement, AvlNode *lt, AvlNode *rt, int h = 0 )
            : element( theElement ), left( lt ), right( rt ), height( h ){ }

    friend class AvlTree<Comparable>;
};



#endif //HW3_NODE_H
