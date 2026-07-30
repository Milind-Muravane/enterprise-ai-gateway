"""
Query Analyzer
Performs lightweight analysis of a user's request
without calling any LLM.
"""


from src.schemas import AnalysisResult

class QueryAnalyzer:
    def analyze(self, question : str) -> AnalysisResult:
        question_lower = question.lower()

        #Basic calculation required for query analysis
        prompt_length = len(question)

        estimated_tokens = max(1,prompt_length // 4)

        sentence_count = len([s for s in question.replace("?", ".").split(".") if s.strip()])

        question_count = question.count("?")

        #commmon words that are in prompt that are useful for the analysis of the query

        search_keywords = [
            "today",
            "latest",
            "news",
            "recent",
            "current",
            "this week",
            "yesterday",
            "tomorrow",
        ]

        rag_keywords = [
            "company",
            "employee",
            "handbook",
            "policy",
            "policies",
            "internal",
            "guideline",
            "guidelines",
            "reimbursement",
            "expense",
            "travel policy",
            "leave",
            "remote work",
            "procurement",
            "hr",
            "manual",
        ]

        reasoning_keywords = [
            "compare",
            "difference",
            "analyze",
            "calculate",
            "recommend",
            "optimize",
            "evaluate",
            "pros",
            "cons",
            "best",
        ]

        travel_keywords = [
            "flight",
            "hotel",
            "travel",
            "trip",
            "booking",
        ]

        programming_keywords = [
            "python",
            "java",
            "sql",
            "function",
            "class",
            "algorithm",
            "api",
        ]

        finance_keywords = [
            "cost",
            "budget",
            "price",
            "expense",
            "profit",
            "revenue",
        ]

        ai_keywords = [
            "ai",
            "llm",
            "gemini",
            "groq",
            "openai",
            "claude",
            "agent",
        ]

        #checking which facilities are required 

        requires_web_search = any(keyword in question_lower for keyword in search_keywords)
        
        requires_reasoning = any(keyword in question_lower for keyword in reasoning_keywords)

        requires_rag = any(keyword in question_lower for keyword in rag_keywords)


        #Detecting multiple topics
        detected_topics = []
        if any(word in question_lower for word in travel_keywords):
            detected_topics.append("Travel")

        if any(word in question_lower for word in programming_keywords):
            detected_topics.append("Programming")

        if any(word in question_lower for word in finance_keywords):
            detected_topics.append("Finance")

        if any(word in question_lower for word in ai_keywords):
            detected_topics.append("AI")

        #complexity scoring 
        complexity_score = 1                                                                        

        reasoning_trace = []

        if prompt_length > 300:
            complexity_score += 1
            reasoning_trace.append("Long prompt detected.")

        if prompt_length > 1500:
            complexity_score += 2
            reasoning_trace.append("Very long prompt detected.")

        if requires_reasoning:
            complexity_score += 2
            reasoning_trace.append("Reasoning task detected.")

        if requires_web_search:
            complexity_score += 1
            reasoning_trace.append("Web search required.")

        if requires_rag:
            complexity_score += 1
            reasoning_trace.append("Enterprise knowledge retrieval required.")

        if question_count >= 2:
            complexity_score += 1
            reasoning_trace.append("Multiple questions detected.")

        if sentence_count >= 5:
            complexity_score += 1
            reasoning_trace.append("Multiple sentences detected.")

        if not reasoning_trace:
            reasoning_trace.append("Simple informational request.")
        
        #returning analysis of the query
        return AnalysisResult(
            prompt_length=prompt_length,
            estimated_input_tokens=estimated_tokens,
            sentence_count=sentence_count,
            question_count=question_count,
            requires_web_search=requires_web_search,
            requires_rag=requires_rag,
            requires_reasoning=requires_reasoning,
            complexity_score=complexity_score,
            detected_topics=detected_topics,
            reasoning_trace=reasoning_trace,

        )


       