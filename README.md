# Business Card Generator

A web application that generates professional business cards with QR codes for contact information.

## Features

- Generate business cards with custom information
- QR code generation for easy contact sharing
- Custom template upload support
- Mobile-responsive design
- Download and print options

## Requirements

- Python 3.8+
- Flask
- Pillow
- qrcode
- vobject
- gunicorn

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python app.py
   ```
4. Visit `http://localhost:10000` in your browser

## Deployment

This application is configured for deployment on Render.com:

1. Create a new Web Service on Render
2. Connect your repository
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python Version: 3.8 or higher

## Environment Variables

No special environment variables are required for basic deployment.

## License

MIT License

## Technologies Used
- Python (Flask)
- HTML, CSS, JavaScript
- qrcode (Python library)
- PIL (Pillow for image processing)

## Contributing
Contributions are welcome! If you'd like to improve this project, follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Added new feature"`
4. Push to your branch: `git push origin feature-name`
5. Open a pull request.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/business-card-generator.git
   cd business-card-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000              