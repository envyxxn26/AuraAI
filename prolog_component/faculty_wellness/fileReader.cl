/*******************************************************************************
* File Reader Helper Class
* Simple wrapper for reading text files
*******************************************************************************/

class fileReader
    open core

predicates
    readLineFromFile : (string FilePath, string Line [out]) procedure.

end class fileReader

