#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "autocomplete.h"

//Qsort Alphabetical
int compare_terms(const void *a, const void *b) {
    return strcmp(((term*)a)->term, ((term*)b)->term);
}

// Comparator function for sorting by weight
int compare_by_weight(const void *a, const void *b) {
    term *termA = (term *)a;
    term *termB = (term *)b;
    return termB->weight - termA->weight;
}


void read_in_terms(term **terms, int *pnterms, char *filename){
    //Opening the file
    FILE *fp = fopen(filename,"r");

    //Fail case for if the file does not open
    if (fp == NULL){
        perror ("Error opening file");
        return;
    }

    //Reading the first line of the textfile: the number of terms
    fscanf(fp, "%d", pnterms);

    //Allocating memory for the terms
    *terms  = (term *)malloc(*pnterms * sizeof(term));
    if (!*terms){
        perror("Memory allocation failed");
        exit(1);
    }


    //Reading the terms
    int i = 0;
    while (i < *pnterms && fscanf(fp, "%lf %[^\n]", &((*terms)[i].weight), (*terms)[i].term) == 2) 
    {
        i++;
    }
    
    //Sorting the terms
    qsort(*terms, *pnterms, sizeof(term), compare_terms);

    //Closing the file
    fclose(fp);
}

int lowest_match(term *terms, int nterms, char *substr){
    //Binary search for the lowest match
 
    int low = 0;
    int high = nterms - 1;
    int mid;
    int result = -1;

    while (low <= high) {
        mid = (low + high) / 2;

        if (strncmp(terms[mid].term, substr, strlen(substr)) == 0) {
            result = mid;  
            high = mid - 1; 
        } else if (strcmp(terms[mid].term, substr) < 0) {
            low = mid + 1; 
        } else {
            high = mid - 1; 
        }
    }
    
    return result;
}

int highest_match(struct term *terms, int nterms, char *substr){
    //Binary search for the highest match

    int low = 0;
    int high = nterms - 1;
    int mid;
    int result = -1;

    while (low <= high) {
        mid = (low + high) / 2;

        if (strncmp(terms[mid].term, substr, strlen(substr)) == 0) {
            result = mid;  
            low = mid + 1; 
        } else if (strcmp(terms[mid].term, substr) < 0) {
            low = mid + 1; 
        } else {
            high = mid - 1; 
        }
    }
    
    return result;
}

void autocomplete(term **answer, int *n_answer, term *terms, int nterms, char *substr){
    int low = lowest_match(terms, nterms, substr); 
    int high = highest_match(terms, nterms, substr); 
    
    if (low == -1|| high == -1|| low > high) {
        *n_answer = 0;  
        *answer = NULL;
        return;
    }

    *n_answer = high - low + 1;
    *answer = (term *)malloc(*n_answer * sizeof(term));

    if (*answer == NULL) {
        perror("Error allocating memory");
        *n_answer = 0;
        return;
    }

    for (int i = 0; i < *n_answer; i++) {
        strcpy((*answer)[i].term, terms[low + i].term);
        (*answer)[i].weight = terms[low + i].weight;
    }
    
    qsort(*answer, *n_answer, sizeof(term), compare_by_weight);
}