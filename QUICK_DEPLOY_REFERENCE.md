# 📋 **QUICK REFERENCE: Railway Backend + Vercel Frontend**

## 🚂 **RAILWAY BACKEND (5 minutes)**

### **Deploy Steps:**
1. [railway.app](https://railway.app) → Sign in with GitHub
2. "New Project" → "Deploy from GitHub repo"
3. Select: `Puneet69/Price-Predictor-Real-Estate-`
4. **Root Directory**: `backend`
5. Deploy

### **Environment Variable:**
- **Name**: `MONGODB_URI`
- **Value**: `mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate`

### **Test Backend:**
- Visit: `[backend-url]/docs`
- Should see FastAPI documentation

---

## ⚡ **VERCEL FRONTEND (5 minutes)**

### **Deploy Steps:**
1. [vercel.com](https://vercel.com) → Sign up with GitHub
2. "New Project" → Select: `Puneet69/Price-Predictor-Real-Estate-`
3. **Framework**: Create React App
4. **Root Directory**: `frontend`
5. **Build Command**: `npm run build`
6. **Output Directory**: `build`

### **Environment Variable:**
- **Name**: `REACT_APP_API_URL`
- **Value**: [Your Railway backend URL]
- **Environment**: All

### **Test Frontend:**
- Visit: `https://your-app.vercel.app`
- Test property comparison

---

## 🧪 **QUICK TEST**

**Property Comparison Test:**
- Property 1: `123 Main St, San Francisco, CA`
- Property 2: `456 Oak Ave, Los Angeles, CA`

**Success Criteria:**
- ✅ Properties load
- ✅ Prices display
- ✅ Charts render
- ✅ No console errors

---

## 💰 **COSTS**
- **Railway**: $0 (free $5 credit)
- **Vercel**: FREE
- **MongoDB**: FREE
- **Total**: $0/month

---

## 🛠️ **IF ISSUES**

**Railway Build Fails:**
- Check root directory is `backend`
- Verify `requirements.txt` exists

**Vercel Build Fails:**
- Check root directory is `frontend`
- Verify `package.json` exists

**API Connection Fails:**
- Check `REACT_APP_API_URL` is set
- Test backend URL directly

---

## 🎯 **FINAL URLS**

**Frontend**: `https://your-app.vercel.app`
**Backend**: `https://backend-xxx.up.railway.app`
**API Docs**: `https://backend-xxx.up.railway.app/docs`

**Total Time**: 10 minutes
**Total Cost**: $0/month