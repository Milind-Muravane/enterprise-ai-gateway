"""
Provider Ranking
Ranks all provider candidates based on score.
"""
from src.schemas import ProviderRanking, ProviderScore

class ProviderRanker:
    
    def rank(self,scores : list[ProviderScore],)-> ProviderRanking:
        ranked = sorted(scores, key = lambda score : score.total_score,reverse = True,)
        
        return ProviderRanking(rankings = ranked,)