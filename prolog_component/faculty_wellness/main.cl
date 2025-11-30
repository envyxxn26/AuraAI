/*******************************************************************************
* AI-Powered Faculty Stress Detector - Expert System Component
* Visual Prolog Class Interface
*******************************************************************************/

class main
    open core

predicates
    run : ().

predicates
    readStressLevel : ().

predicates
    tryReadFile : (string FilePath, string StressLevel [out]) determ.

predicates
    parseStressLevel : (string Line, string StressLevel [out]).

predicates
    provideRecommendations : (string StressLevel) procedure.

predicates
    displayFacts : ().

predicates
    fact : (integer Id, string Description) determ.

predicates
    generateRecommendations : (string StressLevel).

predicates
    explainReasoning : (string StressLevel).

end class main
