# capstone-project
Scissors - URL Shortener and Analytics
Scissors is a web application that allows you to shorten long URLs and track analytics for the generated short URLs. It provides a simple and convenient way to share and monitor the performance of your URLs.

Features
URL Shortening: Easily shorten long URLs into short and manageable links.
Custom URLs: Optionally create custom URLs for your links to make them more memorable and meaningful.
Analytics Tracking: Track the number of visits and view the recent visits for each short URL.
QR Code Generation: Generate QR codes for your short URLs for easy sharing and scanning.
Installation
Clone the repository:
bash
Copy code
git clone <repository-url>
Create and activate a virtual environment (optional):
bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install the required dependencies:
Copy code
pip install -r requirements.txt
Set up the database:
csharp
Copy code
flask db init
flask db migrate
flask db upgrade
Run the application:
arduino
Copy code
flask run
Usage
Access the application in your web browser at http://localhost:5000.
Register for an account or log in if you already have one.
Shorten a URL by entering it in the provided input field and clicking the "Shorten" button.
Optionally, customize the generated short URL by entering a custom code.
Once a short URL is created, you can copy it or click the QR code icon to generate a QR code for the URL.
Visit the Analytics page to view the visit count and recent visits for each short URL.
Technologies
Python
Flask - Web framework
SQLAlchemy - Database toolkit
SQLite - Database management system
HTML/CSS - Front-end development
JavaScript - Client-side scripting
Bootstrap - CSS framework
QR Code API - QR code generation
Contributing
Contributions to Scissors are welcome! If you find any bugs, have feature requests, or want to contribute to the project, please open an issue or submit a pull request. Follow the guidelines in the CONTRIBUTING.md file for more information.

License
This project is licensed under the MIT License.

Please refer to the LICENSE file for more details.

Contact
For any inquiries or questions, feel free to reach out to us at taiwooyenuga63@gmail.com.

We hope you find Scissors useful and enjoy using it for your URL shortening and analytics needs!

Happy Shortening!
