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
  
- **Docker:** A platform that enables developers to package, deploy, and run applications using containers.

## Prerequisites

- Set your mongodb connection string in "flask_app/.env" and "simple_worker/.env"

- In the main directory "SaleForecast", run :
  ```
  docker compose up
  ```

## Application Preview

<img align="center" src="https://github.com/Alok5102R/SaleForecast/blob/master/screenShot/SaleForecast1.jpg" alt="SaleForecast1">
<img align="center" src="https://github.com/Alok5102R/SaleForecast/blob/master/screenShot/SaleForecast2.jpg" alt="SaleForecast2">
<img align="center" src="https://github.com/Alok5102R/SaleForecast/blob/master/screenShot/SaleForecast3.jpg" alt="SaleForecast3">
<img align="center" src="https://github.com/Alok5102R/SaleForecast/blob/master/screenShot/SaleForecast4.jpg" alt="SaleForecast4">
<img align="center" src="https://github.com/Alok5102R/SaleForecast/blob/master/screenShot/SaleForecast5.jpg" alt="SaleForecast5">
<img align="center" src="https://github.com/Alok5102R/SaleForecast/blob/master/screenShot/SaleForecast6.jpg" alt="SaleForecast6">
<img align="center" src="https://github.com/Alok5102R/SaleForecast/blob/master/screenShot/SaleForecast7.jpg" alt="SaleForecast7">
<img align="center" src="https://github.com/Alok5102R/SaleForecast/blob/master/screenShot/SaleForecast8.jpg" alt="SaleForecast8">

## Contributors

- [Alok Kumar](https://github.com/Alok5102R)

## License

This project is licensed under the [MIT License](LICENSE).
