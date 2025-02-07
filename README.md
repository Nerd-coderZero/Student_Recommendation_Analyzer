# Student Performance Analysis & Recommendation System

## Project Overview
This Python-based solution analyzes NEET student quiz performance data and provides personalized recommendations to improve their preparation. The system processes both current and historical quiz data to generate insights, visualizations, and actionable recommendations for improvement.

## Features
- Comprehensive performance analysis across multiple dimensions:
  - Topic-wise performance tracking
  - Difficulty level distribution
  - Time management analysis
  - Historical trend analysis
- Personalized recommendations based on performance patterns
- Student persona identification
- Strength and weakness analysis with creative labels
- Visual insights through various charts and graphs
- Detailed performance metrics and statistics

## Project Structure
```
student_recommendation_analyzer/
├── src/
│   ├── analyzer.py      # Core analysis logic
│   ├── visualizer.py    # Visualization components
│   └── main.py         # Main execution script
├── data/
│   ├── quiz_endpoint.json
│   ├── quiz_submission.json
│   └── historical_quiz_data.json
└── output/             # Generated visualizations
```

## Setup Instructions

### Prerequisites
- Python 3.7+
- Required Python packages:
  ```bash
  pip install pandas numpy matplotlib seaborn
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Nerd-coderZero/Student_Recommendation_Analyzer.git
   cd student-recommendation-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Place your JSON data files in the `data/` directory:
   - `quiz_endpoint.json`: Current quiz data
   - `quiz_submission.json`: Quiz submission details
   - `historical_quiz_data.json`: Historical performance data

2. Run the analysis:
   ```bash
   python src/main.py
   ```

3. Check the `output/` directory for generated visualizations and analysis results.

## Features in Detail

### 1. Data Analysis
- Explores quiz performance patterns across:
  - Topics
  - Difficulty levels
  - Response accuracy
  - Time management

### 2. Generated Insights
- Performance highlights
- Improvement gaps
- Trend insights
- Behavioral patterns
- Topic mastery levels
- Time management efficiency

### 3. Recommendations
- Personalized actionable steps
- Topic-specific focus areas
- Time management suggestions
- Study strategy recommendations

### 4. Visualizations
- Topic performance charts
- Historical trend analysis
- Difficulty distribution graphs
- Time management analysis

## Technical Implementation

### Core Components

#### Analyzer (analyzer.py)
- Processes quiz data
- Generates performance metrics
- Creates personalized recommendations
- Identifies student personas

#### Visualizer (visualizer.py)
- Creates performance visualizations
- Generates topic-wise analysis charts
- Plots historical trends
- Shows difficulty distribution

#### Main Script (main.py)
- Orchestrates the analysis process
- Handles data loading
- Generates comprehensive reports
- Saves visualizations

## Output Examples

The system generates various visualizations including:
- Topic performance charts (`topic_performance_{student_id}.png`)
- Historical trends (`historical_trends.png`)
- Difficulty distribution (`difficulty_distribution.png`)
- Time analysis (`time_analysis.png`)

## Contributing
Feel free to submit issues and enhancement requests!

## License
[MIT License](LICENSE)
