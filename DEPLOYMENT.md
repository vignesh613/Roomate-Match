# Roommate Match - Deployment Guide

## 🚀 Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Railway** is the easiest way to deploy your FastAPI app with a generous free tier.

#### Steps:
1. **Sign up**: Go to [railway.app](https://railway.app) and create an account
2. **Install Railway CLI**: `npm install -g @railway/cli`
3. **Login**: `railway login`
4. **Deploy**:
   ```bash
   cd backend
   railway init
   railway up
   ```
5. **Set Environment Variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_key_here
   ```

#### Free Tier Limits:
- 512MB RAM
- 1GB disk space
- 100 hours/month
- Automatic HTTPS

---

### Option 2: Render (Good Alternative)

**Render** provides reliable free hosting for web services.

#### Steps:
1. **Sign up**: Go to [render.com](https://render.com) and create an account
2. **Connect GitHub**: Link your GitHub repository
3. **Create Web Service**:
   - Choose "Web Service"
   - Connect your repo
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key

#### Free Tier Limits:
- 750 hours/month
- 512MB RAM
- Automatic HTTPS

---

### Option 3: Fly.io (Advanced)

**Fly.io** offers global deployment with good performance.

#### Steps:
1. **Install Fly CLI**: `curl -L https://fly.io/install.sh | sh`
2. **Sign up**: `fly auth signup`
3. **Deploy**:
   ```bash
   cd backend
   fly launch
   fly deploy
   ```
4. **Set Environment Variables**:
   ```bash
   fly secrets set OPENAI_API_KEY=your_key_here
   ```

#### Free Tier Limits:
- 256MB RAM
- 3GB disk space
- Global CDN

---

## 🔧 Environment Setup

### Required Environment Variables:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Getting OpenAI API Key:
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an account
3. Go to API Keys section
4. Create a new secret key
5. Copy the key (starts with `sk-`)

---

## 📁 Project Structure for Deployment

Make sure your project structure looks like this:
```
backend/
├── main.py
├── requirements.txt
├── railway.json (for Railway)
├── fly.toml (for Fly.io)
├── routes/
│   └── api.py
├── ai_agents/
│   ├── matching_agent.py
│   └── trust_agent.py
├── db/
│   └── database.py
└── models/
    └── models.py

frontend/
└── index.html

data/
└── mock_listings.csv
```

---

## 🚀 Quick Deploy Commands

### Railway (Recommended):
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
cd backend
railway init
railway up

# Set API key
railway variables set OPENAI_API_KEY=your_key_here
```

### Render:
1. Push code to GitHub
2. Connect repo to Render
3. Set build/start commands
4. Add environment variables

---

## ⚠️ Important Notes

1. **API Key Security**: Never commit your OpenAI API key to GitHub
2. **Free Tier Limits**: Monitor usage to avoid unexpected charges
3. **Database**: The app uses SQLite (file-based), which works on all platforms
4. **Static Files**: Frontend is served by FastAPI, no separate hosting needed

---

## 🎯 Recommended Choice

**Railway** is recommended because:
- ✅ Easiest deployment process
- ✅ Automatic HTTPS
- ✅ Good free tier limits
- ✅ Excellent FastAPI support
- ✅ Built-in environment variable management