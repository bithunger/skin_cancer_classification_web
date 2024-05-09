# Skin Cancer Detection Web Application

This repository contains the source code for a web-based application designed to detect and classify skin cancer using advanced machine learning models, including InceptionV3 and Xception. The application allows users to upload images of skin lesions, which are then processed by our machine learning models to provide a classification that indicates potential skin cancer types.

## Features

- **Image Upload:** Users can upload images of skin lesions through a user-friendly interface.
- **Machine Learning Analysis:** Utilizes state-of-the-art machine learning models (InceptionV3 and Xception) to analyze skin lesions.
- **PDF Report Generation:** After the analysis, the application generates a detailed PDF report outlining the classification results.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Django
- **Machine Learning:** TensorFlow, Keras
- **PDF Generation:** Python PDF Libraries

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

**Clone the repository:**
git clone https://github.com/bithunger/skin_cancer_classification.git

**Install the required packages:**
pip install -r requirements.txt

**Navigate to the project directory and run the development server:**
python manage.py runserver
