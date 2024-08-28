//
// Created by Alp Onder Yener on 5/13/2024.
//

#ifndef HW3_HASH_H
#define HW3_HASH_H
#include <string>
#include <vector>
#include <cmath>
#include <iostream>

using namespace std;

template <class HashedObj>
class HashTable
{
public:
    explicit HashTable( const HashedObj & notFound, int size = 101);
    HashTable( const HashTable & rhs )
            : ITEM_NOT_FOUND( rhs.ITEM_NOT_FOUND ),
              array( rhs.array ), currentSize( rhs.currentSize ) { }

    const HashedObj & find( const HashedObj & x ) const;

    void insert( const HashedObj & x , bool final_insert = false);
    void remove( const HashedObj & x );

    enum EntryType { ACTIVE, EMPTY, DELETED };
private:
    struct HashEntry
    {
        HashedObj element;
        EntryType info;

        HashEntry( const HashedObj & e = HashedObj( ),
                   EntryType i = EMPTY )
                : element( e ), info( i ) { }
    };

    vector<HashEntry> array;
    int currentSize;
    const HashedObj ITEM_NOT_FOUND;

    bool isActive( int currentPos ) const;
    int findPos( const HashedObj & x ) const;
    void rehash( );
};


// Test to see if the number is prime
bool isPrime( int n )
{
    if ( n == 2 || n == 3 )
        return true;

    if ( n == 1 || n % 2 == 0 )
        return false;

    for ( int i = 3; i * i <= n; i += 2 )
        if ( n % i == 0 )
            return false;

    return true;
}

// Return prime at least as large as n
int nextPrime( int n )
{
    if ( n % 2 == 0 )
        n++;

    for ( ; ! isPrime( n ); n += 2 )
        ;

    return n;
}

// Constructor
template <class HashedObj>
HashTable<HashedObj>::HashTable( const HashedObj & notFound,
                                 int size )
        : ITEM_NOT_FOUND( notFound ), array( nextPrime( size ) )
{
    currentSize = 0;
}

int hashy( const string & key, int tableSize ){
    int result_val = 0;
    for (int i = 0; i < key.length(); i++){
        result_val += key[i];
    }

    return (result_val % tableSize);
}

// Quadratic Probing
template <class HashedObj>
int HashTable<HashedObj>::findPos( const HashedObj & x ) const
{

    int collisionNum = 0;
    int currentPos = hashy( x, array.size( ) );

    while ( array[ currentPos ].info != EMPTY &&
            array[ currentPos ].element != x )
    {
        currentPos += pow(++collisionNum, 2) ;  //add the difference
        if ( currentPos >= array.size( ) )              // perform the mod
            currentPos = currentPos % array.size( );                // if necessary
    }

    return currentPos;
}

// Is the current position active
template <class HashedObj>
bool HashTable<HashedObj>::isActive( int currentPos ) const
{
    return array[ currentPos ].info == ACTIVE;
}

// Remove x, x has to be in the hashtable
template <class HashedObj>
void HashTable<HashedObj>::remove( const HashedObj & x )
{
    int currentPos = findPos( x );
    if ( isActive( currentPos ) )
        array[ currentPos ].info = DELETED;
}

// Find an item
template <class HashedObj>
const HashedObj & HashTable<HashedObj>::find( const HashedObj & x )
const
{
    int currentPos = findPos( x );
    if (isActive( currentPos ))
        return array[ currentPos ].element;

    return   ITEM_NOT_FOUND;
}

// Insert an item
template <class HashedObj>
void HashTable<HashedObj>::insert( const HashedObj & x, bool final_insert)
{
    // Insert x as active
    int currentPos = findPos( x );

    if ( isActive( currentPos ) )
        return;
    array[ currentPos ] = HashEntry( x, ACTIVE );

    // enlarge the hash table if necessary
    currentSize = currentSize + 1;
    double load_factor = (static_cast<double>(currentSize) / array.size());
    if (load_factor > 0.85)
        rehash( );

    if (final_insert){
        cout << endl << "After preprocessing, the unique word count is " << currentSize << ". Current load ratio is " << load_factor << endl;
    }
}

// Expand the hashtable
template <class HashedObj>
void HashTable<HashedObj>::rehash( )
{
    cout << "rehashed..." << endl;
    vector<HashEntry> oldArray = array;

    // Create new double-sized, empty table
    array.resize( nextPrime( 2 * oldArray.size( ) ) );

    cout << "previous table size:" << oldArray.size() << ", new table size: " << array.size();
    for ( int j = 0; j < array.size( ); j++ )
        array[ j ].info = EMPTY;

    // Copy table over
    currentSize = 0;
    for ( int i = 0; i < oldArray.size( ); i++ )
        if ( oldArray[ i ].info == ACTIVE )
            insert( oldArray[ i ].element , false);

    double load_factor = (static_cast<double>(currentSize) / array.size());
    cout << ", current unique word count " << currentSize << "," << endl << "current load factor: " << load_factor << endl;
}


#endif //HW3_HASH_H
