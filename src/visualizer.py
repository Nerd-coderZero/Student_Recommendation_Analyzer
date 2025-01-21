import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, List
from analyzer import QuizAnalyzer

class QuizVisualizer:
    def __init__(self, analyzer: QuizAnalyzer, output_dir: str):
        self.analyzer = analyzer
        self.output_dir = output_dir

        
    def plot_topic_performance(self) -> None:
        """Create bar chart for topic-wise performance"""
        topic_perf = self.analyzer.analyze_topic_performance()
        topics = list(topic_perf.keys())
        correct = [perf['correct'] for perf in topic_perf.values()]
        incorrect = [perf['incorrect'] for perf in topic_perf.values()]
        
        # Create new figure
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(111)
        
        x = range(len(topics))
        width = 0.35
        
        ax.bar(x, correct, width, label='Correct', color='green', alpha=0.6)
        ax.bar([i + width for i in x], incorrect, width, label='Incorrect', color='red', alpha=0.6)
        
        ax.set_xlabel('Topics')
        ax.set_ylabel('Number of Questions')
        ax.set_title('Performance Across Topics')
        ax.set_xticks([i + width/2 for i in x])
        ax.set_xticklabels(topics, rotation=45)
        ax.legend()
        
        plt.tight_layout()
        # Save figure with full path
        student_id = self.analyzer.quiz_submission['id']
        save_path = os.path.join(self.output_dir, f'topic_performance_{student_id}.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        
    def plot_historical_trends(self) -> None:
        """Create line plot for historical performance trends"""
        trends = self.analyzer.analyze_historical_trends()
        
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(111)
        
        ax.plot(trends['accuracy_trend'], marker='o', label='Accuracy')
        ax.plot(trends['speed_trend'], marker='s', label='Speed')
        ax.plot(trends['score_trend'], marker='^', label='Score')
        
        ax.set_xlabel('Quiz Number')
        ax.set_ylabel('Performance Metrics')
        ax.set_title('Historical Performance Trends')
        ax.legend()
        ax.grid(True)
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, 'historical_trends.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        
    def plot_difficulty_distribution(self) -> None:
        """Create stacked bar chart for difficulty level performance"""
        diff_stats = self.analyzer.analyze_difficulty_distribution()
        
        difficulties = list(diff_stats.keys())
        correct = [stats['correct'] for stats in diff_stats.values()]
        incorrect = [stats['incorrect'] for stats in diff_stats.values()]
        
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        ax.bar(difficulties, correct, label='Correct', color='green', alpha=0.6)
        ax.bar(difficulties, incorrect, bottom=correct, label='Incorrect', color='red', alpha=0.6)
        
        ax.set_xlabel('Difficulty Level')
        ax.set_ylabel('Number of Questions')
        ax.set_title('Performance by Difficulty Level')
        ax.legend()
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, 'difficulty_distribution.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
    
    def plot_time_analysis(self) -> None:
        """Create time management analysis visualization"""
        time_stats = self.analyzer.analyze_time_management()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Attempt rate pie chart
        attempted = time_stats['questions_attempted']
        not_attempted = self.analyzer.quiz_submission['total_questions'] - attempted
        ax1.pie([attempted, not_attempted], 
                labels=['Attempted', 'Not Attempted'],
                autopct='%1.1f%%',
                colors=['#2ecc71', '#e74c3c'])
        ax1.set_title('Questions Attempted vs Not Attempted')
        
        # Time per question analysis
        ax2.bar(['Average Time per Question'], 
                [time_stats['avg_time_per_question']],
                color='#3498db')
        ax2.set_ylabel('Time (seconds)')
        ax2.set_title('Average Time per Question')
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, 'time_analysis.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close(fig)