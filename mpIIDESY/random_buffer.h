/**
   random_buffer.h

   Purpose: Reads plaintext files of pre-generated random numbers, with functions to read one random number at a time. This header file contains declarations of various functions and variables in RandomBuffer class.

   @author John Smeaton
   @version 03/02/2017

 */

#ifndef RANDOM_BUFFER_H
#define RANDOM_BUFFER_H

#include <string>
#include <fstream>
#include <iostream>


/**
   Singleton class to provide random numbers to Detector class, reading numbers from file.
 */
class RandomBuffer {
	
 private:

	static RandomBuffer* s_instance; // Pointer to instance of class

	// Filestreams for uniform, gaussian random number files.
	std::ifstream uniform_file;
	std::ifstream gaussian_file;
	
	// Constructor and destructor
	RandomBuffer();
	~RandomBuffer();

	
 public:
	
	static RandomBuffer* instance(); // Function to return pointer to class instance.
	
	void open_uniform_file(std::string); // Opens filestream for file of uniform random numbers.
	void open_gaussian_file(std::string); // Opens filestream for file of uniform random numbers.

	float get_uniform_number(); // Reads and returns next number in uniform file
	float get_gaussian_number(); // Reads and returns next number in gaussian file

};

#endif
