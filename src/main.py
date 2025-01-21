from analyzer import QuizAnalyzer
from visualizer import QuizVisualizer
import os

def main():
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    # Create output directory
    output_dir = os.path.join(root_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Data paths
    data_dir = os.path.join(root_dir, 'data')
    quiz_endpoint_path = os.path.join(data_dir, "quiz_endpoint.json")
    quiz_submission_path = os.path.join(data_dir, "quiz_submission.json")
    historical_data_path = os.path.join(data_dir, "historical_quiz_data.json")
    
    try:
        # Create analyzer instance
        analyzer = QuizAnalyzer()
        
        # Load data
        analyzer.load_data_from_files(
            quiz_endpoint_path,
            quiz_submission_path,
            historical_data_path
        )
       
        student_id = analyzer.quiz_submission['user_id']
    
        print("\nAnalysis Results for Student ID:", student_id)
        
        # Generate analysis
        current_performance = analyzer.analyze_current_performance()
        topic_performance = analyzer.analyze_topic_performance()
        recommendations = analyzer.generate_recommendations()
        persona = analyzer.get_student_persona()
        difficulty_performance = analyzer.analyze_difficulty_distribution()
        time_stats = analyzer.analyze_time_management()
        
        # Print detailed results
        print("\nAnalysis Results:")
        print(f"Student Persona: {persona}")
        
        print("\nCurrent Performance:")
        for key, value in current_performance.items():
            print(f"{key}: {value}")
            
        print("\nTopic Performance:")
        for topic, stats in topic_performance.items():
            print(f"{topic}:")
            print(f"  Correct: {stats['correct']}")
            print(f"  Incorrect: {stats['incorrect']}")
        
        print("\nDifficulty Level Performance:")
        for diff, stats in difficulty_performance.items():
            print(f"{diff}:")
            print(f"  Correct: {stats['correct']}")
            print(f"  Incorrect: {stats['incorrect']}")
        
        print("\nTime Management Analysis:")
        for key, value in time_stats.items():
            print(f"{key}: {value}")

        
        insights = analyzer.generate_key_insights()
        
        print("\nKey Insights:")
        print("\nPerformance Highlights:")
        for highlight in insights["performance_highlights"]:
            print(highlight)
            
        print("\nImprovement Areas:")
        for gap in insights["improvement_gaps"]:
            print(gap)
            
        print("\nTrend Analysis:")
        for trend in insights["trend_insights"]:
            print(trend)
            
        print("\nBehavioral Insights:")
        for behavior in insights["behavioral_insights"]:
            print(behavior)
        
        print("\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")

        # Generate enhanced insights
        strengths = analyzer.analyze_student_strengths()
        weaknesses = analyzer.analyze_student_weaknesses()
        
        print("\nStrengths:")
        for topic, label in strengths.items():
            print(f"{topic}: {label}")
        
        print("\nAreas for Improvement:")
        for topic, label in weaknesses.items():
            print(f"{topic}: {label}")
        
        # Create visualizations with proper output directory
        visualizer = QuizVisualizer(analyzer, output_dir)
        
        # Generate all plots
        print("\nGenerating visualizations...")
        visualizer.plot_topic_performance()
        visualizer.plot_historical_trends()
        visualizer.plot_difficulty_distribution()
        visualizer.plot_time_analysis()
        
        print(f"\nVisualizations have been saved to: {output_dir}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()