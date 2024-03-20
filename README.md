# Automated Sales Forecast Generation Project

This project is an automated sales forecast generation system developed using Python, Flask, MongoDB, and Celery. It allows users to upload an Excel file containing sales data into MongoDB, trigger the forecast generation job through an API, and download the output Excel file.

## Functionality

- **Upload Excel Data:** Users can upload an Excel file containing sales data through a Flask-based web interface. The uploaded data is stored in MongoDB for further processing.
  
- **Trigger Forecast Generation:** An API endpoint is provided to trigger the forecast generation job. This job uses the uploaded sales data to generate sales forecasts using a predefined algorithm.
  
- **Download Output Excel:** Once the forecast generation job is completed, users can download the output Excel file containing the sales forecasts through another API endpoint.

## Technologies Used

- **Python:** The core programming language used for implementing the project logic.
  
- **Flask:** A lightweight web framework used for building the web interface and API endpoints.
  
- **MongoDB:** A NoSQL database used to store the uploaded sales data.
  
- **Celery:** A distributed task queue used to perform the asynchronous forecast generation job.

- **Install Dependencies:** Make sure you have Python installed on your system. Install Flask, pymongo, and Celery using pip:
   ```
   pip install Flask pymongo celery
   ```

## Contributors

- [Alok Kumar](https://github.com/Alok5102R)

## License

This project is licensed under the [MIT License](LICENSE).
