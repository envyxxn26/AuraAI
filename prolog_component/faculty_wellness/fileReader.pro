/*******************************************************************************
* File Reader Helper Class Implementation
*******************************************************************************/

implement fileReader
    open core

clauses
    readLineFromFile(FilePath, Line) :-
        Stream = inputStream_file::openFileUtf8(FilePath),
        Line = Stream:readLine(),
        Stream:close(),
        !.

end implement fileReader

