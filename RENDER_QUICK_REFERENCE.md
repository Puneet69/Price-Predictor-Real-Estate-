# 🎨 **RENDER QUICK DEPLOY REFERENCE**

## ⚡ **5-Minute Deployment**

### **1. Sign Up (30 seconds)**
- Go to **[render.com](https://render.com)**
- Click **"Get Started for Free"**
- Sign up with **GitHub**

### **2. Deploy Backend (2 minutes)**
**New + → Web Service**
- **Repo**: `Puneet69/Price-Predictor-Real-Estate-`
- **Name**: `property-comparison-backend`
- **Root Directory**: `backend`
- **Build**: `pip install -r requirements.txt`
- **Start**: `gunicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variable**:
  ```
  MONGODB_URI=mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate
  ```

### **3. Deploy Frontend (2 minutes)**
**New + → Static Site**
- **Repo**: `Puneet69/Price-Predictor-Real-Estate-`
- **Name**: `property-comparison-frontend`
- **Root Directory**: `frontend`
- **Build**: `npm ci && npm run build`
- **Publish**: `build`
- **Environment Variable**:
  ```
  REACT_APP_API_URL=https://property-comparison-backend.onrender.com
  ```

### **4. Done! (30 seconds)**
✅ **Backend**: `https://property-comparison-backend.onrender.com`
✅ **Frontend**: `https://property-comparison-frontend.onrender.com`

---

## 💰 **Cost: $0/month**
- ✅ Backend: 750 hours/month FREE
- ✅ Frontend: Unlimited FREE
- ✅ MongoDB: FREE tier
- ✅ SSL: Included FREE

---

## 🔧 **Essential Settings**

### **Backend Configuration**
```
Runtime: Python 3
Plan: Free
Region: Oregon (US West)
Auto-Deploy: Yes
```

### **Frontend Configuration**
```
Environment: Static Site
Plan: Free
Region: Oregon (US West)
Auto-Deploy: Yes
```

---

## 🚀 **One-Click Deploy**
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Puneet69/Price-Predictor-Real-Estate-)

---

## 📊 **Expected URLs**
- **API Docs**: `https://property-comparison-backend.onrender.com/docs`
- **Health Check**: `https://property-comparison-backend.onrender.com/health`
- **Full App**: `https://property-comparison-frontend.onrender.com`

---

## 🛠️ **Quick Troubleshooting**
- **Build fails**: Check `requirements.txt` exists in `/backend`
- **Frontend blank**: Verify `REACT_APP_API_URL` is correct
- **API errors**: Check MongoDB URI environment variable
- **Service sleeping**: Free tier sleeps after 15min (wakes on first request)

---

## 🎉 **Deployment Complete!**
**Total time**: 5 minutes
**Total cost**: $0/month
**Maintenance**: Auto-deploy on git push

**Go deploy at [render.com](https://render.com)! 🚀**