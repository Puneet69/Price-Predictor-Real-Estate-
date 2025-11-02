# 🚀 **Manual Deployment Guide: Render Backend + Vercel Frontend**

## 📋 **Deployment Overview**

- **Backend**: Render (FastAPI with MongoDB)
- **Frontend**: Vercel (React with Tailwind CSS)
- **Database**: MongoDB Atlas (already configured)
- **Repository**: https://github.com/Puneet69/Price-Predictor-Real-Estate-

---

## 🖥️ **PART 1: Deploy Backend to Render**

### **Step 1: Create Render Account & Connect GitHub**
1. Go to [render.com](https://render.com)
2. Sign up or log in with your GitHub account
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository: `Puneet69/Price-Predictor-Real-Estate-`

### **Step 2: Configure Backend Service**
Fill in the following settings:

#### **Basic Settings:**
- **Name**: `property-comparison-backend`
- **Root Directory**: `backend`
- **Environment**: `Python 3`
- **Region**: `Oregon (US West)` or closest to you
- **Branch**: `main`

#### **Build & Deploy:**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --host 0.0.0.0 --port $PORT
  ```

#### **Advanced Settings:**
- **Auto-Deploy**: ✅ Yes
- **Health Check Path**: `/health`

### **Step 3: Environment Variables**
Add these environment variables in Render:

```env
MONGODB_URI=mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate

PYTHON_VERSION=3.11
```

### **Step 4: Deploy Backend**
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Note your backend URL: `https://property-comparison-backend.onrender.com`

### **Step 5: Test Backend**
Visit these URLs to verify:
- Health: `https://property-comparison-backend.onrender.com/health`
- Properties: `https://property-comparison-backend.onrender.com/properties?limit=5`

---

## 🌐 **PART 2: Deploy Frontend to Vercel**

### **Step 1: Create Vercel Account**
1. Go to [vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Click **"Add New..."** → **"Project"**
4. Import `Puneet69/Price-Predictor-Real-Estate-`

### **Step 2: Configure Frontend Project**
#### **Project Settings:**
- **Framework Preset**: `Create React App`
- **Root Directory**: `frontend`
- **Build Command**: `npm ci && npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm ci`

### **Step 3: Environment Variables**
Add this environment variable in Vercel:

```env
REACT_APP_API_URL=https://property-comparison-backend.onrender.com
```

**How to add:**
1. Go to **Project Settings** → **Environment Variables**
2. Add **Name**: `REACT_APP_API_URL`
3. Add **Value**: `https://property-comparison-backend.onrender.com`
4. Select **Production**, **Preview**, **Development**
5. Click **Save**

### **Step 4: Deploy Frontend**
1. Click **"Deploy"**
2. Wait for build (3-5 minutes)
3. Get your frontend URL: `https://your-project-name.vercel.app`

---

## 🧪 **PART 3: Test Complete System**

### **Step 1: Verify Backend**
Test these endpoints:
```bash
curl https://property-comparison-backend.onrender.com/health
curl https://property-comparison-backend.onrender.com/properties?limit=3
```

### **Step 2: Test Frontend**
1. Visit your Vercel URL
2. Select two properties
3. Click "Compare Properties"
4. Verify AI predicted prices are different from market values!

### **Step 3: Test Property Comparison**
Look for:
- ✅ Market values displayed
- ✅ AI predicted prices (different from market)
- ✅ Property comparison charts
- ✅ Investment analysis
- ✅ Property features and amenities

---

## 🎯 **Expected Results**

### **Backend Features Working:**
- ✅ 24 properties loaded from MongoDB
- ✅ AI price prediction algorithm
- ✅ Property comparison with charts
- ✅ Health monitoring and statistics
- ✅ CORS enabled for frontend

### **Frontend Features Working:**
- ✅ Property selection and comparison
- ✅ AI predicted price display (with gradient styling)
- ✅ Market vs AI price comparison indicators
- ✅ Interactive property cards
- ✅ Responsive design

---

## 🔧 **Troubleshooting**

### **Backend Issues:**
- **Build Fails**: Check `requirements.txt` compatibility
- **Database Error**: Verify MongoDB URI in environment variables
- **Timeout**: Free tier has cold starts, wait 30 seconds

### **Frontend Issues:**
- **API Connection**: Check `REACT_APP_API_URL` environment variable
- **Build Fails**: Ensure Node.js version compatibility
- **CORS Error**: Verify backend CORS settings allow your domain

### **Common Solutions:**
1. **Redeploy Backend**: Go to Render → Manual Deploy
2. **Clear Build Cache**: Vercel → Project Settings → Functions → Clear Cache
3. **Check Logs**: Both platforms provide deployment logs

---

## 🎉 **Success Indicators**

Your deployment is successful when:
- ✅ Backend health check returns 200 OK
- ✅ Frontend loads without errors
- ✅ Property comparison works end-to-end
- ✅ AI predictions show different values from market prices
- ✅ Charts generate and display properly

---

## 📞 **Next Steps After Deployment**

1. **Custom Domain** (Optional): Add your domain in Vercel settings
2. **Monitoring**: Set up uptime monitoring for both services
3. **Analytics**: Add Google Analytics to track usage
4. **SSL**: Both Render and Vercel provide free SSL certificates

**Your AI Property Comparison System is now live! 🚀**