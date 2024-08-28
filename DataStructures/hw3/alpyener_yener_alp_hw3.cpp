// Created by Alp Onder Yener

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "tree.h"
#include "hash.h"
#include <chrono>

using namespace std;

// Update the unique words and document items vectors according to the given word.
// Update the count of that word + add it to unique words vector if that word was not seen before
void process_vect(vector<DocumentItem> & this_document_items, string word, string document_name, vector<string> & unique){
    bool was_there=false;
    for (int i=0; i < this_document_items.size(); i++){
        if (word == this_document_items[i].word) {
            was_there = true;
            this_document_items[i].count++;
        }
    }
    if (!was_there){
        DocumentItem new_item = DocumentItem(document_name, 1, word); // occurence is 1 at the start
        this_document_items.push_back(new_item);
    }

    bool unique_word = true;
    for (int i=0; i < unique.size(); i++){
        if (word == unique[i]){
            unique_word = false;
            break;
        }
    }
    if (unique_word){
        unique.push_back(word);
    }
}

// Turn strings to lower case
string toLowerCase(const string& input) {
    std::string result = input;
    for (char& c : result) {
        if (c >= 'A' && c <= 'Z') {
            c = c + 32; // Convert to lowercase using ASCII
        }
    }
    return result;
}

// Strip out the spaces from the string
string strip(string input){
    string stripped = ""; // Resulting string without spaces

    for (int i = 0; i < input.length(); i++) {
        if (input[i] != ' ') { // If the character is not a space, add it to the result
            stripped += input[i];
        }
    }

    return stripped;
}

// Strip out the non alphabetic characters in the given string
string check_for_nonalpha(string input){
    string result_str = "";
    for (int i = 0; i < input.size(); i++){
        if (input[i] >= 'a' && input[i] <= 'z'){
            result_str += input[i];
        }
    }
    return result_str;
}

// Is the char alphabetic or not
bool isAlphabetic(char c) {
    // Check if the character is in the range of 'A' to 'Z' or 'a' to 'z'
    return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
}

// seperate words by the non alphanumeric characters
vector<string> seperate_by_nonalpha(string chunk){
    vector<string> return_vect;
    string to_be_added_element = "";
    for (int i = 0; i < chunk.size(); i++){
        if (chunk[i] >= 'a' && chunk[i] <= 'z'){
            to_be_added_element += chunk[i];
        }
        else if (to_be_added_element.size() > 0){
            return_vect.push_back(to_be_added_element);
            to_be_added_element = "";
        }
    }
    if (to_be_added_element.size() > 0){return_vect.push_back(to_be_added_element);}
    return return_vect;
}


int main() {
    // Get user input
    int no_of_files;
    cout << "Enter number of input files: "; cin >> no_of_files;

    // Data structures that the document items and unique words will be stored
    vector<vector<DocumentItem>> all_documents_items;
    vector<string> unique_words;

    // Gather filenames, open the file, read the words and update all_document_items according to the words found
    vector<string> filenames;
    for (int i=0; i < no_of_files; i++){

        vector<DocumentItem> this_document_items; // Specific vector for this document

        string filename;
        cout << "Enter " << to_string(i+1) << ". file name: ";
        cin >> filename;
        filenames.push_back(filename);
        ifstream file(filename);

        string word;
        while (file >> word) { // Read word by word from the file
            word = toLowerCase(word); // Process the word

            vector<string> words_seperated_by_nonalpha = seperate_by_nonalpha(word); // seperate words by the non alphanumeric characters
            // word = check_for_nonalpha(word);

            for (int j = 0; j < words_seperated_by_nonalpha.size(); j++){
                string word2 = words_seperated_by_nonalpha[j];
                process_vect(this_document_items, word2, filename, unique_words);
            }

        }

        all_documents_items.push_back(this_document_items); // Add it to the general all_document_items
    }

    // Our not_found value is DNE
    AvlTree<string> tree = AvlTree<string>("DNE");

    // Insert the unique words in the tree
    for (int i = 0; i < unique_words.size(); i++){
        if (unique_words[i] != " "){
            tree.insert(unique_words[i]);
        }
    }
    cout << endl;

    // Same for hashtable
    HashTable<string> hash_tabl = HashTable<string>("DNE", 101);


    for (int i = 0; i < unique_words.size(); i++){
        if (unique_words[i] != " "){

            if (i == unique_words.size() - 1){hash_tabl.insert(unique_words[i], true);}
            else{hash_tabl.insert(unique_words[i]);}
        }
    }

    // Get the queried words from the user, either remove a word, find the words or end the program
    while(true)
    {
        bool removal = false;
        cout << "Enter queried words in one line: ";
        string line;

        cin.clear();
        if (cin.peek() == '\n') {
            cin.ignore();
        }
        getline(cin, line);

        if (line.length() > 6){
            if (line.substr(0,6) == "REMOVE"){
                removal = true;
            }
        }

        if (line == "ENDOFINPUT"){
            break;
        }


        line = toLowerCase(line);

        // Process the input string
        vector<string> words; // This vector will have the words that were given on the input

        words = seperate_by_nonalpha(line);


        // Now the vector of words is filled up

        // Remove the word from the tree if needed
        bool skip = false;
        if (removal){
            for (int i=1; i < words.size(); i++){
                tree.remove(words[i]);
                hash_tabl.remove(words[i]);
                cout << words[i] << " has been REMOVED." << endl;
                skip = true;
            }
        }

        if (!skip) {
            // Output the queried words and how many times they were found
            vector<string> new_filenames;
            bool foundsome = false;

            // Test finding time for BST
            auto start = std::chrono::high_resolution_clock::now();
            for (int i = 0; i < words.size(); i++){
                if (hash_tabl.find(words[i]) == words[i]){
                    continue;
                }
            }
            auto BSTTime = std::chrono::duration_cast<std::chrono::nanoseconds>
                    (std::chrono::high_resolution_clock::now() - start);


            // Find and create output for BST
            for (int i = 0; i < filenames.size(); i++) {
                string name = filenames[i];
                string output = "in Document " + name + ", ";

                int cnt = 0;

                bool found_for_this_file = false;
                for (int j = 0; j < words.size(); j++) {

                    // Find for tree
                    if (tree.find(words[j]) == words[j]) { // if word is in the tree
                        for (int k = 0; k < all_documents_items[i].size(); k++) {
                            if (all_documents_items[i][k].word == words[j] &&
                                all_documents_items[i][k].documentName == name &&
                                words[j].length() > 0 && words[j] != " ") {
                                DocumentItem target_item = all_documents_items[i][k];
                                output += target_item.word + " found " + to_string(target_item.count) + " times, ";

                                found_for_this_file = true;
                                cnt ++;
                            }
                        }
                    }


                }
                if (found_for_this_file && cnt == words.size()) {
                    output = output.substr(0, output.length() - 2) + ".\n";
                    cout << output;
                    foundsome = true;
                }
            }


            // Test finding time for hashtable
            start = std::chrono::high_resolution_clock::now();
            for (int i = 0; i < words.size(); i++){
               if (hash_tabl.find(words[i]) == words[i]){
                   continue;
               }
            }
            auto HTTime = std::chrono::duration_cast<std::chrono::nanoseconds>
                    (std::chrono::high_resolution_clock::now()- start);

            // Find and create output for hashtable
            for (int i = 0; i < filenames.size(); i++) {
                string name = filenames[i];
                string output = "in Document " + name + ", ";

                int cnt = 0;

                bool found_for_this_file = false;
                for (int j = 0; j < words.size(); j++) {

                    // Find for tree
                    if (hash_tabl.find(words[j]) == words[j]) { // if word is in the tree
                        for (int k = 0; k < all_documents_items[i].size(); k++) {
                            if (all_documents_items[i][k].word == words[j] &&
                                all_documents_items[i][k].documentName == name &&
                                words[j].length() > 0 && words[j] != " ") {
                                DocumentItem target_item = all_documents_items[i][k];
                                output += target_item.word + " found " + to_string(target_item.count) + " times, ";

                                found_for_this_file = true;
                                cnt ++;
                            }
                        }
                    }


                }
                if (found_for_this_file && cnt == words.size()) {
                    output = output.substr(0, output.length() - 2) + ".\n";
                    cout << output;
                }
            }


            double how_faster = (static_cast<double>(BSTTime.count()) / HTTime.count());




            if (!foundsome) {
                cout << "No document contains the given query." << endl;
                cout << "No document contains the given query." << endl;
            }


            cout << endl << "Time: " << BSTTime.count() << endl << "Time: " << HTTime.count() << endl << "Speed Up: " << how_faster << endl;


        }
        cout << endl;

    }


    return 0;
}