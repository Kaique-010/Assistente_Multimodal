"""
Sistema de aprendizado incremental para o assistente multimodal.
"""

import json
import os
from datetime import datetime
from collections import defaultdict, Counter

class LearningSystem:
    def __init__(self, data_file="learning_data.json"):
        self.data_file = data_file
        self.interactions = []
        self.feedback_data = []
        self.usage_patterns = defaultdict(int)
        self.load_data()
    
    def load_data(self):
        """Carrega dados de aprendizado existentes."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.interactions = data.get('interactions', [])
                    self.feedback_data = data.get('feedback', [])
                    self.usage_patterns = defaultdict(int, data.get('usage_patterns', {}))
            except Exception as e:
                print(f"Erro ao carregar dados de aprendizado: {e}")
    
    def save_data(self):
        """Salva dados de aprendizado."""
        try:
            data = {
                'interactions': self.interactions,
                'feedback': self.feedback_data,
                'usage_patterns': dict(self.usage_patterns),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados de aprendizado: {e}")
    
    def record_interaction(self, user_input, intent, model_used):
        """Registra uma interação do usuário."""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'intent': intent,
            'model_used': model_used
        }
        self.interactions.append(interaction)
        self.usage_patterns[intent] += 1
        self.save_data()
    
    def record_feedback(self, user_input, response, feedback_type):
        """Registra feedback sobre uma resposta."""
        feedback = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'feedback_type': feedback_type,  # 'positive', 'negative', 'neutral'
        }
        self.feedback_data.append(feedback)
        self.save_data()
    
    def get_frequent_queries(self, limit=10):
        """Retorna as consultas mais frequentes."""
        query_counter = Counter()
        for interaction in self.interactions:
            query_counter[interaction['user_input']] += 1
        return [query for query, count in query_counter.most_common(limit)]
    
    def get_popular_intents(self, limit=5):
        """Retorna as intenções mais populares."""
        return dict(Counter(self.usage_patterns).most_common(limit))
    
    def get_success_rate(self):
        """Calcula taxa de sucesso baseada no feedback."""
        if not self.feedback_data:
            return 0.0
        
        positive_feedback = sum(1 for f in self.feedback_data if f['feedback_type'] == 'positive')
        total_feedback = len(self.feedback_data)
        return (positive_feedback / total_feedback) * 100
    
    def get_learning_insights(self):
        """Retorna insights do sistema de aprendizado."""
        return {
            'total_interactions': len(self.interactions),
            'total_feedback': len(self.feedback_data),
            'success_rate': self.get_success_rate(),
            'frequent_queries': self.get_frequent_queries(),
            'popular_intents': self.get_popular_intents(),
            'usage_patterns': dict(self.usage_patterns)
        }
    
    def identify_improvement_areas(self):
        """Identifica áreas que precisam de melhoria."""
        negative_feedback = [f for f in self.feedback_data if f['feedback_type'] == 'negative']
        
        # Analisar padrões de feedback negativo
        problem_intents = defaultdict(int)
        for feedback in negative_feedback:
            # Encontrar a intenção relacionada
            for interaction in self.interactions:
                if interaction['user_input'] == feedback['user_input']:
                    problem_intents[interaction['intent']] += 1
                    break
        
        return {
            'negative_feedback_count': len(negative_feedback),
            'problem_intents': dict(problem_intents),
            'recent_issues': negative_feedback[-5:] if negative_feedback else []
        }
    
    def get_recommendations(self):
        """Gera recomendações para melhorias."""
        insights = self.get_learning_insights()
        improvements = self.identify_improvement_areas()
        
        recommendations = []
        
        # Recomendar melhorias baseadas em feedback negativo
        if improvements['negative_feedback_count'] > 0:
            for intent, count in improvements['problem_intents'].items():
                if count >= 2:
                    recommendations.append(f"Melhorar ferramenta de {intent} - {count} feedbacks negativos")
        
        # Recomendar expansão de ferramentas populares
        for intent, usage in insights['popular_intents'].items():
            if usage > 10:
                recommendations.append(f"Expandir funcionalidades de {intent} - {usage} usos")
        
        return recommendations
    
    def export_analytics(self):
        """Exporta analytics para análise externa."""
        analytics = {
            'summary': self.get_learning_insights(),
            'improvements': self.identify_improvement_areas(),
            'recommendations': self.get_recommendations(),
            'export_date': datetime.now().isoformat()
        }
        
        filename = f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analytics, f, ensure_ascii=False, indent=2)
        
        return filename