Instructions to search:

when there are no stars in the query:

Examples
at
at or an
at and an
dragon not

These queries return the documents after AND, OR and NOT operation.

when there are stars

Examples
at*
at* or an*
at* and an*
an* not
at and an*
an* or at
at not

These queries return the terms as well as the documents which contain those elements.

all variations will work


steps involved:

1) created inverted index
2) converted inverted index to sparse boolean matrix.(could do it directly)
3) coded various operations on differnt operations in different functions



No special data structure has been used. This search engine is implemented on python dictionaries.
A dictionary for permuterm index has been created which points to the root word.
There is another dictionary each key of which points to a posting list.
So the search is in two hops. The root word resulting from permuterm dictionary is used as the key of the second dictionary and returns the final posting list.
Though the space taken by this approach is very much but is faster at the same time.

