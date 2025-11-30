/*******************************************************************************
* AI-Powered Faculty Stress Detector - Expert System Component
* Visual Prolog Implementation
*******************************************************************************/

implement main
    open core, stdio, string

clauses
    run() :-
        console::init(),
        stdio::write("============================================================\n"),
        stdio::write("AI-Powered Faculty Stress Detector - Expert System\n"),
        stdio::write("Wellness Recommendation System\n"),
        stdio::write("============================================================\n\n"),
        readStressLevel(),
        stdio::write("\n============================================================\n"),
        stdio::write("Thank you for using the Faculty Wellness Expert System!\n"),
        stdio::write("============================================================\n"),
        stdio::write("\nPress Enter to exit...\n"),
        _ = stdio::readLine().

    % Read stress level from file
    readStressLevel() :-
        % Try multiple possible file paths (check local directory first)
        (tryReadFile("stress_output.txt", StressLevel);
         tryReadFile("..\\..\\..\\integration\\stress_output.txt", StressLevel);
         tryReadFile("..\\..\\integration\\stress_output.txt", StressLevel);
         tryReadFile("integration\\stress_output.txt", StressLevel)),
        !,
        stdio::write("Reading stress level from ML component output...\n"),
        stdio::write("Stress Level Detected: ", StressLevel, "\n\n"),
        provideRecommendations(StressLevel).
    
    readStressLevel() :-
        % Fallback if file not found
        stdio::write("Warning: Could not read stress_output.txt\n"),
        stdio::write("Using default: Medium stress\n\n"),
        provideRecommendations("Medium").
    
    % Try to read file from given path
    tryReadFile(FilePath, StressLevel) :-
        fileReader::readLineFromFile(FilePath, Line),
        stdio::write("DEBUG: Read line from file: [", Line, "]\n"),
        parseStressLevel(Line, StressLevel).

    % Parse stress level from file
    parseStressLevel(Line, StressLevel) :-
        % Check for Low first (most specific)
        string::hasPrefix(Line, "STRESS_LEVEL=Low"),
        StressLevel = "Low",
        !.

    parseStressLevel(Line, StressLevel) :-
        % Check for Medium
        string::hasPrefix(Line, "STRESS_LEVEL=Medium"),
        StressLevel = "Medium",
        !.

    parseStressLevel(Line, StressLevel) :-
        % Check for High
        string::hasPrefix(Line, "STRESS_LEVEL=High"),
        StressLevel = "High",
        !.

    parseStressLevel(_, "Unknown").

    % Main recommendation logic
    provideRecommendations(StressLevel) :-
        stdio::write("Analyzing workload patterns and wellness indicators...\n\n"),
        stdio::write("Knowledge Base Facts:\n"),
        stdio::write("-------------------\n"),
        displayFacts(),
        stdio::write("\n"),
        stdio::write("Applying Expert Rules...\n\n"),
        stdio::write("============================================================\n"),
        stdio::write("PERSONALIZED WELLNESS RECOMMENDATIONS\n"),
        stdio::write("============================================================\n\n"),
        generateRecommendations(StressLevel),
        stdio::write("\n"),
        explainReasoning(StressLevel).

    % Display knowledge base facts
    displayFacts() :-
        fact(1, "High workload correlates with increased stress levels"),
        fact(2, "Adequate sleep (7+ hours) is essential for faculty wellness"),
        fact(3, "Excessive committee duties reduce time for core teaching activities"),
        fact(4, "Regular weekend work indicates work-life imbalance"),
        fact(5, "Large class sizes increase preparation and grading time"),
        fact(6, "Research activities require dedicated time blocks for productivity"),
        fact(7, "Administrative tasks can fragment work schedules"),
        fact(8, "Frequent meetings disrupt focused work periods"),
        fact(9, "Multiple subject preparations increase cognitive load"),
        fact(10, "Workload stress affects both teaching quality and personal health"),
        fact(11, "Time management strategies can mitigate stress"),
        fact(12, "Institutional support is crucial for faculty well-being"),
        fail.

    displayFacts().

    % Knowledge Base Facts
    fact(1, "High workload correlates with increased stress levels").
    fact(2, "Adequate sleep (7+ hours) is essential for faculty wellness").
    fact(3, "Excessive committee duties reduce time for core teaching activities").
    fact(4, "Regular weekend work indicates work-life imbalance").
    fact(5, "Large class sizes increase preparation and grading time").
    fact(6, "Research activities require dedicated time blocks for productivity").
    fact(7, "Administrative tasks can fragment work schedules").
    fact(8, "Frequent meetings disrupt focused work periods").
    fact(9, "Multiple subject preparations increase cognitive load").
    fact(10, "Workload stress affects both teaching quality and personal health").
    fact(11, "Time management strategies can mitigate stress").
    fact(12, "Institutional support is crucial for faculty well-being").

    % Expert Rules for Recommendations
    generateRecommendations("High") :-
        !,
        stdio::write("STRESS LEVEL: HIGH\n"),
        stdio::write("-----------------\n\n"),
        stdio::write("IMMEDIATE ACTIONS REQUIRED:\n\n"),
        stdio::write("1. WORKLOAD ADJUSTMENTS:\n"),
        stdio::write("   - Request reduction in number of subjects (target: 2-3)\n"),
        stdio::write("   - Negotiate smaller class sizes or teaching assistant support\n"),
        stdio::write("   - Delegate administrative tasks where possible\n"),
        stdio::write("   - Request temporary relief from committee assignments\n\n"),
        stdio::write("2. WELLNESS BREAKS:\n"),
        stdio::write("   - Schedule mandatory 15-minute breaks every 2 hours\n"),
        stdio::write("   - Take a complete day off each week (no work activities)\n"),
        stdio::write("   - Plan a 3-5 day wellness break within the next month\n"),
        stdio::write("   - Engage in daily 30-minute physical activity\n\n"),
        stdio::write("3. TIME MANAGEMENT:\n"),
        stdio::write("   - Implement time-blocking for core activities\n"),
        stdio::write("   - Batch similar tasks together (e.g., all grading in one session)\n"),
        stdio::write("   - Set boundaries for meeting times (max 2 hours/day)\n"),
        stdio::write("   - Use preparation templates to reduce prep time\n\n"),
        stdio::write("4. SLEEP AND RECOVERY:\n"),
        stdio::write("   - Prioritize 7-8 hours of sleep nightly\n"),
        stdio::write("   - Establish consistent sleep schedule\n"),
        stdio::write("   - Avoid work activities 2 hours before bedtime\n"),
        stdio::write("   - Consider consultation with healthcare provider\n\n"),
        stdio::write("5. INSTITUTIONAL SUPPORT:\n"),
        stdio::write("   - Schedule meeting with department head to discuss workload\n"),
        stdio::write("   - Request access to faculty wellness resources\n"),
        stdio::write("   - Explore options for sabbatical or reduced load\n"),
        stdio::write("   - Document workload for administrative review\n\n").

    generateRecommendations("Medium") :-
        !,
        stdio::write("STRESS LEVEL: MEDIUM\n"),
        stdio::write("-------------------\n\n"),
        stdio::write("PREVENTIVE MEASURES RECOMMENDED:\n\n"),
        stdio::write("1. TIME-BLOCKING STRATEGIES:\n"),
        stdio::write("   - Allocate specific time blocks for teaching prep (2-3 hours/day)\n"),
        stdio::write("   - Reserve morning hours for research (when cognitive load is highest)\n"),
        stdio::write("   - Group administrative tasks in afternoon slots\n"),
        stdio::write("   - Protect time blocks from interruptions\n\n"),
        stdio::write("2. WORK CYCLE MONITORING:\n"),
        stdio::write("   - Track weekly workload distribution\n"),
        stdio::write("   - Identify peak stress periods and plan accordingly\n"),
        stdio::write("   - Review workload monthly and adjust commitments\n"),
        stdio::write("   - Maintain work-life balance boundaries\n\n"),
        stdio::write("3. EFFICIENCY IMPROVEMENTS:\n"),
        stdio::write("   - Develop reusable teaching materials\n"),
        stdio::write("   - Use technology to streamline grading and communication\n"),
        stdio::write("   - Consolidate meetings when possible\n"),
        stdio::write("   - Set clear agendas and time limits for meetings\n\n"),
        stdio::write("4. WELLNESS MAINTENANCE:\n"),
        stdio::write("   - Maintain 7+ hours of sleep consistently\n"),
        stdio::write("   - Engage in regular physical activity (3-4 times/week)\n"),
        stdio::write("   - Practice stress-reduction techniques (meditation, deep breathing)\n"),
        stdio::write("   - Schedule regular social activities outside work\n\n"),
        stdio::write("5. PREVENTIVE PLANNING:\n"),
        stdio::write("   - Plan ahead for busy periods (exam weeks, deadlines)\n"),
        stdio::write("   - Build buffer time into schedules\n"),
        stdio::write("   - Learn to say 'no' to additional commitments\n"),
        stdio::write("   - Regular check-ins with supervisor about workload\n\n").

    generateRecommendations("Low") :-
        !,
        stdio::write("STRESS LEVEL: LOW\n"),
        stdio::write("----------------\n\n"),
        stdio::write("MAINTAINING OPTIMAL WELLNESS:\n\n"),
        stdio::write("1. ROUTINE MAINTENANCE:\n"),
        stdio::write("   - Continue current workload management practices\n"),
        stdio::write("   - Maintain balanced distribution of responsibilities\n"),
        stdio::write("   - Keep effective time management habits\n"),
        stdio::write("   - Preserve work-life balance boundaries\n\n"),
        stdio::write("2. PREVENTIVE WELLNESS PLANNING:\n"),
        stdio::write("   - Continue adequate sleep schedule (7+ hours)\n"),
        stdio::write("   - Maintain regular exercise routine\n"),
        stdio::write("   - Engage in professional development activities\n"),
        stdio::write("   - Pursue personal interests and hobbies\n\n"),
        stdio::write("3. SUSTAINABLE GROWTH:\n"),
        stdio::write("   - Consider taking on new challenges gradually\n"),
        stdio::write("   - Mentor colleagues who may be experiencing higher stress\n"),
        stdio::write("   - Share effective strategies with department\n"),
        stdio::write("   - Continue monitoring workload to prevent escalation\n\n"),
        stdio::write("4. LONG-TERM WELLNESS:\n"),
        stdio::write("   - Regular health check-ups and wellness assessments\n"),
        stdio::write("   - Continue stress management practices\n"),
        stdio::write("   - Maintain social connections and support networks\n"),
        stdio::write("   - Plan for career development and growth opportunities\n\n"),
        stdio::write("5. INSTITUTIONAL CONTRIBUTION:\n"),
        stdio::write("   - Participate in faculty wellness initiatives\n"),
        stdio::write("   - Advocate for workload policies that support all faculty\n"),
        stdio::write("   - Share best practices for work-life balance\n"),
        stdio::write("   - Support colleagues in maintaining wellness\n\n").

    generateRecommendations(_) :-
        stdio::write("Error: Unknown stress level. Please check the input file.\n").

    % Explain reasoning based on rules
    explainReasoning("High") :-
        !,
        stdio::write("============================================================\n"),
        stdio::write("REASONING EXPLANATION\n"),
        stdio::write("============================================================\n\n"),
        stdio::write("Rule Applied: HIGH_STRESS_RULE\n"),
        stdio::write("Conditions Met:\n"),
        stdio::write("  - Workload Stress Score (WSS) is 21-27\n"),
        stdio::write("  - Multiple high-intensity factors present\n"),
        stdio::write("  - Risk of burnout and health issues\n\n"),
        stdio::write("Conclusion: Immediate intervention required to prevent\n"),
        stdio::write("deterioration of health and teaching quality. Workload\n"),
        stdio::write("reduction and wellness breaks are essential.\n\n").

    explainReasoning("Medium") :-
        !,
        stdio::write("============================================================\n"),
        stdio::write("REASONING EXPLANATION\n"),
        stdio::write("============================================================\n\n"),
        stdio::write("Rule Applied: MEDIUM_STRESS_RULE\n"),
        stdio::write("Conditions Met:\n"),
        stdio::write("  - Workload Stress Score (WSS) is 15-20\n"),
        stdio::write("  - Moderate workload intensity\n"),
        stdio::write("  - Some risk factors present but manageable\n\n"),
        stdio::write("Conclusion: Preventive measures and better time management\n"),
        stdio::write("can prevent escalation to high stress. Monitoring and\n"),
        stdio::write("proactive adjustments are recommended.\n\n").

    explainReasoning("Low") :-
        !,
        stdio::write("============================================================\n"),
        stdio::write("REASONING EXPLANATION\n"),
        stdio::write("============================================================\n\n"),
        stdio::write("Rule Applied: LOW_STRESS_RULE\n"),
        stdio::write("Conditions Met:\n"),
        stdio::write("  - Workload Stress Score (WSS) is 9-14\n"),
        stdio::write("  - Balanced workload distribution\n"),
        stdio::write("  - Healthy work-life balance indicators\n\n"),
        stdio::write("Conclusion: Current practices are effective. Focus on\n"),
        stdio::write("maintaining routines and preventive wellness planning to\n"),
        stdio::write("sustain optimal performance and well-being.\n\n").

    explainReasoning(_) :-
        stdio::write("Reasoning explanation not available for this stress level.\n").

end implement main

goal
    console::runUtf8(main::run).
