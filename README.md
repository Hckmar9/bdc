# Burndown Chart Generator

<div align="center">
  <a href="#">
    <img src="/static/img/BDC.jpg" alt="about-me" width="300" height="300">
  </a>
</div>

This web application allows users to generate burndown charts for project management and sprint tracking. Users can input the sprint start and end dates along with daily story points to visualize the actual progress against the expected burndown.

## Features

- Generate a burndown chart based on the input start and end dates and story points.
- Download the generated chart as a PNG file.
- Responsive design for both desktop and mobile browsers.

## Installation

### Prerequisites

- Python 3.x
- Flask
- Matplotlib
- NumPy

### Setup

Clone the repository to your local machine:

```bash
git clone https://github.com/hckmar9/bdc-generator.git
cd bdc-generator
python3 -m venv env
pip3 install requirements.txt
source venv/bin/activate
python3 app.py
```
