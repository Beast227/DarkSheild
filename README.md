<h1 align="center">Dark Shield</h1>

DarkShield is a web application designed to analyze websites for the presence of dark patterns. Dark patterns are deceptive design practices that manipulate users into taking actions they might not have intended. DarkShield empowers users by exposing these dark patterns and promoting transparency in online experiences.

## Overview

- **URL Analysis:** Analyze entire websites by providing their URLs to uncover hidden manipulative design elements.
- **User-Friendly Interface:** Intuitive design for easy navigation and a seamless user experience.

## Technologies

- HTML, CSS, and JavaScript for the front-end
- MongoDB for the database
- Flask framework for creating web applications with Python.
- Beautiful Soup library for extracting data from HTML and XML documents.
- scikit-learn library for machine learning and data analysis.

## Machine Learning (ML) for Dark Pattern Classification

DarkShield utilizes logistic regression as a machine learning model to classify dark patterns on specific websites. The trained model is saved using the `pickle` module. Currently, it works for websites such as Amazon and Flipkart, and efforts are ongoing to make it compatible with other websites through regular updates.

## Installation

### Prerequisites

Before you proceed with the installation, ensure you have the following prerequisites:

- [Python](https://www.python.org/) installed (version 3.x recommended)

### Setting Up Virtual Environment

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Beast227/DarkSheild.git
    ```

2. Navigate to the project directory:

    ```bash
    cd DarkSheild
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

### Installing Dependencies

Install the required dependencies using:

```bash
pip install -r requirements.txt
```
## How to Use

1. Copy the link from an E-commerce website.

   ![Copy Link](static/images/copy-link.jpg)

2. Paste the link into the DarkShield website.

   ![Paste Link](static/images/link-ss.jpeg)

3. Click the "Check for Dark Pattern" button to analyze the website.

   ![Check Button](static/images/check-button.jpg)


## Note
This repository is not currently open for contributions.



<h6 align="center"> This project is currently in development.</h5>
