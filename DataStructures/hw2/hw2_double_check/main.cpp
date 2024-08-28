// Created by Alp Onder Yener

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "tree.h"

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
            word = check_for_nonalpha(word);

            process_vect(this_document_items, word, filename, unique_words);
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

        if (line == "ENDOFINPUT"){
            break;
        }

        if (line.length() > 6){
            if (line.substr(0,6) == "REMOVE"){
                removal = true;
            }
        }

        // Process the input string
        vector<string> words; // This vector will have the words that were given on the input
        int last_space_idx;
        string word = "";

        for (int i = 0; i < line.length(); i++) {

            if (isAlphabetic(line[i])) { // if alphabetic then add
                word = word + line[i];

            } else if (word.length() > 0) { // if not and if we have added some chars before, add the word to the vector
                last_space_idx = i;
                word = toLowerCase(word);
                word = strip(word);
                words.push_back(word);
                word = "";
            }
        }
        words.push_back(word); // add the last word

        // Now the vector of words is filled up

        // Remove the word from the tree if needed
        bool skip = false;
        if (removal){
            for (int i=1; i < words.size(); i++){
                tree.remove(words[i]);
                cout << words[i] << " has been REMOVED." << endl;
                skip = true;
            }
        }

        if (!skip) {
            // Output the queried words and how many times they were found
            vector<string> new_filenames;
            bool foundsome = false;
            for (int i = 0; i < filenames.size(); i++) {
                string name = filenames[i];
                string output = "in Document " + name + ", ";
                bool found_for_this_file = false;
                for (int j = 0; j < words.size(); j++) {
                    if (tree.find(words[j]) == words[j]) {
                        for (int k = 0; k < all_documents_items[i].size(); k++) {
                            if (all_documents_items[i][k].word == words[j] &&
                                all_documents_items[i][k].documentName == name &&
                                words[j].length() > 0 && words[j] != " ") {
                                DocumentItem target_item = all_documents_items[i][k];
                                output += target_item.word + " found " + to_string(target_item.count) + " times, ";
                                foundsome = true;
                                found_for_this_file = true;
                            }
                        }
                    }
                }
                if (found_for_this_file) {
                    output = output.substr(0, output.length() - 2) + ".\n";
                    cout << output;
                }
            }

            if (!foundsome) {
                cout << "No document contains the given query." << endl;
            }

        }
        cout << endl;

    }


    return 0;
}
