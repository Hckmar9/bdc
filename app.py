from flask import Flask, render_template, request, send_file, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np
import io
import datetime
import matplotlib
import os

# The 'Agg' is used for Matplotlib to avoid issues with certain environments
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        story_points_input = request.form['storyPoints']
        
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        
        story_points = list(map(int, story_points_input.split(',')))
        initial_points = story_points[0] if story_points else 0
        
        sprint_days = [(start_date + datetime.timedelta(days=i)).date() for i in range((end_date - start_date).days + 1)]
        
        expected_points_per_day = initial_points / (len(sprint_days) - 1)
        remaining_points = [initial_points - i * expected_points_per_day for i in range(len(sprint_days))]

        # Extend the story_points array to match the length of sprint_days
        while len(story_points) < len(sprint_days):
            story_points.append(story_points[-1] if story_points else 0)

        # Calculate trend line
        x = np.arange(len(sprint_days))
        coef = np.polyfit(x, story_points, 1)
        trend = np.polyval(coef, x)

        # Generate chart and save to a file
        img_path = 'static/burndown_chart.png'
        plt.figure(figsize=(10, 6))
        plt.plot(sprint_days, story_points, label='Actual Burndown', marker='o', color='#007bff', linewidth=2, markersize=8)
        plt.plot(sprint_days, remaining_points, label='Expected Burndown', linestyle='--', color='#ff6347', linewidth=2)
        plt.plot(sprint_days, trend, label='Trend Line', linestyle='-', color='#ffa500', linewidth=2)
        plt.xlabel('Date', fontsize=14, fontweight='bold')
        plt.ylabel('Story Points', fontsize=14, fontweight='bold')
        plt.title('Burndown Chart', fontsize=16, fontweight='bold')
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator())
        plt.ylim(0, max(initial_points, max(story_points)) + 10)  # Adjust the y-axis to start from 0 and go slightly above the max points

        # Shows the story points for actual burndown
        for i, txt in enumerate(story_points):
            plt.annotate(f'{txt}', (sprint_days[i], story_points[i]), textcoords="offset points", xytext=(0,10), ha='center')

        # Shows the story points for expected burndown
        for i, txt in enumerate(remaining_points):
            plt.annotate(f'{int(txt)}', (sprint_days[i], remaining_points[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='#ff6347')

        plt.tight_layout()
        plt.savefig(img_path, format='png')
        plt.close()

        return redirect(url_for('index', show_chart=True))

    return render_template('index.html', show_chart=request.args.get('show_chart', False))

@app.route('/download')
def download_chart():
    img_path = 'static/burndown_chart.png'
    return send_file(img_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)