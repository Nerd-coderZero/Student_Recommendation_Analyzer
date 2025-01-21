import pandas as pd
import numpy as np
import json
from typing import Dict, List, Tuple
from datetime import datetime


class QuizAnalyzer:
    def __init__(self):
        self.current_quiz_data = None
        self.quiz_submission = None
        self.historical_data = None
        
    def analyze_difficulty_distribution(self) -> Dict:
        """Analyze performance across difficulty levels"""
        if not self.current_quiz_data or not self.quiz_submission:
            return {}
            
        difficulty_stats = {}
        for question in self.current_quiz_data['quiz']['questions']:
            diff_level = question['difficulty_level'] or 'undefined'
            if diff_level not in difficulty_stats:
                difficulty_stats[diff_level] = {'correct': 0, 'incorrect': 0, 'total': 0}
            
            question_id = str(question['id'])
            if question_id in self.quiz_submission['response_map']:
                difficulty_stats[diff_level]['total'] += 1
                selected_option = self.quiz_submission['response_map'][question_id]
                
                # Check if answer was correct
                for option in question['options']:
                    if option['id'] == selected_option:
                        if option['is_correct']:
                            difficulty_stats[diff_level]['correct'] += 1
                        else:
                            difficulty_stats[diff_level]['incorrect'] += 1
                        break
                        
        return difficulty_stats
    
    def analyze_time_management(self) -> Dict:
        """Analyze time spent per question"""
        if not self.quiz_submission:
            return {}
            
        started = datetime.fromisoformat(self.quiz_submission['started_at'])
        ended = datetime.fromisoformat(self.quiz_submission['ended_at'])
        total_time = (ended - started).total_seconds()
        
        questions_attempted = len(self.quiz_submission['response_map'])
        
        return {
            'total_time_seconds': total_time,
            'questions_attempted': questions_attempted,
            'avg_time_per_question': total_time / questions_attempted if questions_attempted > 0 else 0,
            'attempt_rate': (questions_attempted / self.quiz_submission['total_questions']) * 100
        }
        
    def load_data_from_files(self, quiz_endpoint_path: str, quiz_submission_path: str, historical_data_path: str):
        """Load data from JSON files"""
        try:
            with open(quiz_endpoint_path, 'r', encoding="utf-8") as f:
                self.current_quiz_data = json.load(f)
            with open(quiz_submission_path, 'r', encoding="utf-8") as f:
                self.quiz_submission = json.load(f)
            with open(historical_data_path, 'r', encoding="utf-8") as f:
                self.historical_data = json.load(f)
            print("Data loaded successfully!")
        except FileNotFoundError as e:
            print(f"Error loading files: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            raise

    def analyze_current_performance(self) -> Dict:
        """Analyze current quiz performance"""
        if not self.quiz_submission:
            return {}
            
        current_stats = {
            'accuracy': float(self.quiz_submission['accuracy'].strip(' %')),
            'speed': float(self.quiz_submission['speed']),
            'correct_answers': self.quiz_submission['correct_answers'],
            'incorrect_answers': self.quiz_submission['incorrect_answers'],
            'total_questions': self.quiz_submission['total_questions'],
            'topic': self.quiz_submission['quiz']['topic'],
            'duration': self.quiz_submission['duration'],
            'mistakes_corrected': self.quiz_submission['mistakes_corrected'],
            'initial_mistake_count': self.quiz_submission['initial_mistake_count']
        }
        return current_stats
    
    def analyze_topic_performance(self) -> Dict:
        """Analyze performance by topics"""
        if not self.current_quiz_data or not self.quiz_submission:
            return {}

        # Create a mapping of question IDs to topics
        topic_map = {}
        for question in self.current_quiz_data['quiz']['questions']:
            topic_map[question['id']] = {
                'topic': question['topic'],
                'difficulty_level': question['difficulty_level']
            }
        
        # Analyze responses by topic
        topic_performance = {}
        for q_id, option_id in self.quiz_submission['response_map'].items():
            q_id = int(q_id)
            if q_id in topic_map:
                topic = topic_map[q_id]['topic']
                if topic not in topic_performance:
                    topic_performance[topic] = {'correct': 0, 'incorrect': 0}
                
                # Check if the answer was correct by matching with options
                correct = False
                for question in self.current_quiz_data['quiz']['questions']:
                    if question['id'] == q_id:
                        for option in question['options']:
                            if option['id'] == option_id and option['is_correct']:
                                correct = True
                                break
                        break
                
                if correct:
                    topic_performance[topic]['correct'] += 1
                else:
                    topic_performance[topic]['incorrect'] += 1
                    
        return topic_performance
    
    def analyze_historical_trends(self) -> Dict:
        """Analyze historical performance trends"""
        if not self.historical_data:
            return {'accuracy_trend': [], 'speed_trend': [], 'score_trend': []}
            
        trends = {
            'accuracy_trend': [],
            'speed_trend': [],
            'score_trend': []
        }
        
        for submission in self.historical_data:
            trends['accuracy_trend'].append(float(submission['accuracy'].strip(' %')))
            trends['speed_trend'].append(float(submission['speed']))
            trends['score_trend'].append(float(submission['final_score']))
            
        return trends
    
    def generate_recommendations(self) -> List[str]:
        """Generate personalized recommendations based on analysis"""
        if not all([self.current_quiz_data, self.quiz_submission, self.historical_data]):
            return ["Unable to generate recommendations: Missing data"]
            
        current_stats = self.analyze_current_performance()
        topic_performance = self.analyze_topic_performance()
        historical_trends = self.analyze_historical_trends()
        
        recommendations = []
        
        # Accuracy-based recommendations
        accuracy = current_stats.get('accuracy', 0)
        if accuracy < 70:
            recommendations.append("Focus on improving accuracy by spending more time reviewing questions before submitting answers")
        elif accuracy < 85:
            recommendations.append("Your accuracy is good, but aim for excellence by reviewing the questions you got wrong")
        else:
            recommendations.append("Excellent accuracy! Challenge yourself with more difficult questions")
        
        # Speed-based recommendations
        speed = current_stats.get('speed', 0)
        if speed < 80:
            recommendations.append("Work on improving your speed by practicing more timed quizzes")
        elif speed == 100:
            recommendations.append("Great speed! Make sure to maintain accuracy while working quickly")
        
        # Topic-based recommendations
        for topic, perf in topic_performance.items():
            total_questions = perf['correct'] + perf['incorrect']
            accuracy_rate = (perf['correct'] / total_questions) * 100 if total_questions > 0 else 0
            
            if accuracy_rate < 50:
                recommendations.append(f"Priority: Review fundamentals of {topic}")
            elif accuracy_rate < 75:
                recommendations.append(f"Focus on strengthening your understanding of {topic}")
            elif accuracy_rate < 90:
                recommendations.append(f"Good progress in {topic}. Practice more complex questions")
        
        # Time management recommendations
        if current_stats.get('total_questions', 0) > 0:
            attempted_ratio = (current_stats['correct_answers'] + current_stats['incorrect_answers']) / current_stats['total_questions']
            if attempted_ratio < 0.5:
                recommendations.append("Work on time management to attempt more questions")
        
        # Mistake correction recommendations
        mistakes_corrected = current_stats.get('mistakes_corrected', 0)
        initial_mistakes = current_stats.get('initial_mistake_count', 0)
        if initial_mistakes > 0:
            correction_rate = (mistakes_corrected / initial_mistakes) * 100
            if correction_rate < 100:
                recommendations.append(f"Focus on learning from mistakes - you corrected {mistakes_corrected} out of {initial_mistakes} initial mistakes")
        
        # If no recommendations generated, add a default one
        if not recommendations:
            recommendations.append("Keep up the good work! Try attempting more challenging questions to further improve")
        
        return recommendations
    
    def get_student_persona(self) -> str:
        """Define student persona based on performance patterns"""
        current_stats = self.analyze_current_performance()
        if not current_stats:
            return "Unable to determine persona: Missing data"
            
        accuracy = current_stats.get('accuracy', 0)
        speed = current_stats.get('speed', 0)
        
        if accuracy > 90 and speed > 90:
            return "Advanced Achiever"
        elif accuracy > 80 and speed > 70:
            return "Steady Performer"
        elif accuracy < 60 and speed > 90:
            return "Quick but Needs Accuracy"
        elif accuracy > 80 and speed < 60:
            return "Accurate but Needs Speed"
        else:
            return "Developing Learner"
    def analyze_student_strengths(self) -> Dict:
        """Enhanced strength analysis with creative labels"""
        topic_perf = self.analyze_topic_performance()
        strengths = {}
        
        for topic, stats in topic_perf.items():
            total = stats['correct'] + stats['incorrect']
            if total > 0:
                accuracy = (stats['correct'] / total) * 100
                if accuracy >= 90:
                    strengths[topic] = "Master"
                elif accuracy >= 80:
                    strengths[topic] = "Expert"
                elif accuracy >= 70:
                    strengths[topic] = "Proficient"
        
        return strengths
    
    def analyze_student_weaknesses(self) -> Dict:
        """Enhanced weakness analysis with creative labels"""
        topic_perf = self.analyze_topic_performance()
        weaknesses = {}
        
        for topic, stats in topic_perf.items():
            total = stats['correct'] + stats['incorrect']
            if total > 0:
                accuracy = (stats['correct'] / total) * 100
                if accuracy < 50:
                    weaknesses[topic] = "Needs Focus"
                elif accuracy < 60:
                    weaknesses[topic] = "Developing"
                elif accuracy < 70:
                    weaknesses[topic] = "Emerging"
        
        return weaknesses

    def generate_key_insights(self) -> Dict:
        """Generate highlighted insights from the student's performance data"""
        insights = {
            "performance_highlights": [],
            "improvement_gaps": [],
            "trend_insights": [],
            "behavioral_insights": []
        }
        
        # Current performance insights
        current_stats = self.analyze_current_performance()
        if current_stats:
            accuracy = current_stats.get('accuracy', 0)
            speed = current_stats.get('speed', 0)
            
            # Performance highlights
            if accuracy >= 80 and speed >= 90:
                insights["performance_highlights"].append("⭐ Exceptional performance with high accuracy and speed")
            elif accuracy >= 80:
                insights["performance_highlights"].append("⭐ Strong accuracy demonstrated")
            elif speed >= 90:
                insights["performance_highlights"].append("⭐ Excellent speed performance")
                
            # Improvement gaps
            if accuracy < 70:
                insights["improvement_gaps"].append("⚠️ Accuracy needs improvement - consider slower, more careful approach")
            if speed < 70:
                insights["improvement_gaps"].append("⚠️ Speed enhancement needed - practice timed mock tests")
                
        # Topic mastery insights
        topic_perf = self.analyze_topic_performance()
        for topic, stats in topic_perf.items():
            total = stats['correct'] + stats['incorrect']
            if total > 0:
                accuracy = (stats['correct'] / total) * 100
                if accuracy >= 85:
                    insights["performance_highlights"].append(f"🎯 Mastery demonstrated in {topic}")
                elif accuracy <= 50:
                    insights["improvement_gaps"].append(f"📚 Significant revision needed in {topic}")
                    
        # Historical trend insights
        trends = self.analyze_historical_trends()
        if trends and trends['accuracy_trend']:
            recent_accuracy = trends['accuracy_trend'][-3:]  # Last 3 attempts
            if all(acc >= 80 for acc in recent_accuracy):
                insights["trend_insights"].append("📈 Consistent high performance in recent attempts")
            elif all(acc > recent_accuracy[0] for acc in recent_accuracy[1:]):
                insights["trend_insights"].append("📈 Showing steady improvement in recent attempts")
            elif all(acc < recent_accuracy[0] for acc in recent_accuracy[1:]):
                insights["trend_insights"].append("📉 Performance declining in recent attempts")
                
        # Time management insights
        time_stats = self.analyze_time_management()
        if time_stats:
            attempt_rate = time_stats.get('attempt_rate', 0)
            avg_time = time_stats.get('avg_time_per_question', 0)
            
            if attempt_rate < 50:
                insights["behavioral_insights"].append("⏰ Low question attempt rate indicates time management issues")
            if avg_time > 120:  # More than 2 minutes per question
                insights["behavioral_insights"].append("⏱️ Spending too much time per question")
                
        # Mistake correction insights
        if current_stats:
            mistakes_corrected = current_stats.get('mistakes_corrected', 0)
            initial_mistakes = current_stats.get('initial_mistake_count', 0)
            if initial_mistakes > 0:
                correction_rate = (mistakes_corrected / initial_mistakes) * 100
                if correction_rate >= 75:
                    insights["behavioral_insights"].append("✅ Excellent mistake correction rate")
                elif correction_rate <= 50:
                    insights["behavioral_insights"].append("❗ Need to focus on learning from mistakes")
        
        return insights
           
