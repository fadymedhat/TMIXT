// Fast dictionary score for Tesseract OCR validation
// Chris G. Willcocks

#include <iostream>
#include <string>
#include <fstream>
#include <streambuf>
#include <sstream>
#include <algorithm>
#include <unordered_set>

using namespace std;

int main(int argc,char *argv[])
{
	// Get data from command line
	string dicFilename = argv[2];
	string srcFilename = argv[1];
	string dicStr;
	string srcStr;

	// 1. Read dictionary file
	ifstream t1(dicFilename.c_str());
	t1.seekg(0, ios::end);
	dicStr.reserve(t1.tellg());
	t1.seekg(0, ios::beg);
	dicStr.assign((istreambuf_iterator<char>(t1)),
	               istreambuf_iterator<char>());

	// 2. Read source text file
	ifstream t2(srcFilename.c_str());
	t2.seekg(0, ios::end);
	srcStr.reserve(t2.tellg());
	t2.seekg(0, ios::beg);
	srcStr.assign((istreambuf_iterator<char>(t2)),
	               istreambuf_iterator<char>());

	// Populate dictonary
	unordered_set<string> dict;
	istringstream f(dicStr);
	string line;
	while (getline(f, line)) {
		dict.insert(line);
	}

	// Source to lower
	transform(srcStr.begin(), srcStr.end(), srcStr.begin(), ::tolower);
	stringstream s(srcStr);
	string word;

	// Do the search
	int count = 0;
	for (int i = 0; s >> word; ++i)
	{
		// Only weight interesting words
		if (word.length() > 3)
		{
			// cout << word << endl;
			unordered_set<string>::const_iterator it = dict.find(word);
			if (it != dict.end())
				++count;
		}
	}

	std::cout << count << endl;

	return 0;
}
