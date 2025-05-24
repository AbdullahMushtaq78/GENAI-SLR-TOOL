# SLR Analysis Tool

A Flask-based web application for Systematic Literature Review (SLR) analysis using AI agents.

## Features

- PDF upload and analysis
- AI-powered SLR evaluation
- Interactive chat interface
- Results visualization
- PRISMA guidelines compliance checking

## Local Development

### Prerequisites

- Python 3.8+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd GENAI-SLR-TOOL
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
python flask_app.py
```

The application will be available at `http://localhost:5001`

## Deployment to Render.com

### Prerequisites

- GitHub account
- Render.com account
- OpenAI API key

### Steps

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin deployed_app
   ```

2. **Create a new Web Service on Render.com:**
   - Go to [Render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the `deployed_app` branch

3. **Configure the service:**
   - **Name:** `slr-analysis-tool` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn app:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Instance Type:** Choose based on your needs (Free tier available)

4. **Set Environment Variables:**
   - Go to the "Environment" tab
   - Add the following variables:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `FLASK_ENV`: `production`
     - `PYTHONPATH`: `/opt/render/project/src`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for the deployment to complete (usually 5-10 minutes)

### Important Notes

- The free tier on Render.com may have limitations (sleep after inactivity, limited resources)
- For production use, consider upgrading to a paid plan
- The application uses OpenAI API, which incurs costs based on usage
- Uploaded files are stored temporarily and may be cleared on redeploys

## Environment Variables

- `OPENAI_API_KEY`: Required for AI functionality
- `PORT`: Application port (set automatically by Render.com)
- `FLASK_ENV`: Set to `production` for deployment

## File Structure

```
├── app.py                 # Production entry point
├── flask_app.py          # Main Flask application
├── requirements.txt      # Python dependencies
├── build.sh             # Render.com build script
├── backend/             # Backend logic and AI agents
├── frontend/            # Frontend templates and styles
├── uploads/             # Uploaded files (temporary)
└── results/             # Analysis results (temporary)
```

## Usage

1. Upload a PDF research paper
2. Enter the paper title
3. Wait for AI analysis to complete
4. Review the results and scores
5. Use the chat interface for additional questions

## Support

For issues or questions, please create an issue in the GitHub repository.
