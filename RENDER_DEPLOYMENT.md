# Render Deployment Guide for NJA PLATFORM

This guide will help you deploy your Django application to Render.

## Prerequisites

✅ All deployment files are ready:
- `requirements.txt` - Clean dependencies list
- `Procfile` - Tells Render how to run your app
- `build.sh` - Build script for deployment
- `create_superuser.py` - Script to create admin user after deployment

## Step-by-Step Deployment

### 1. Push Your Code to GitHub/GitLab

Make sure all your code is committed and pushed to your repository:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up or log in
3. Connect your GitHub/GitLab account

### 3. Create a PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Choose a name (e.g., `nja-platform-db`)
3. Select a free plan (or paid if needed)
4. Click **"Create Database"**
5. **Important**: Note down the **Internal Database URL** - you'll need it later

### 4. Create a Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your repository
3. Select the repository containing your NJA PLATFORM code
4. Configure the service:

#### Basic Settings:
- **Name**: `nja-platform` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (or set if your Django app is in a subdirectory)
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn nja_platform.wsgi`

#### Environment Variables:
Click **"Advanced"** → **"Add Environment Variable"** and add:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | `eet*o%xj7s4b8t7p9v7f$u@ns4s0cvxcw1b_9g(tpw%=(%om9^` | **Generate a new one!** Use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` | Set to False for production |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` | Replace with your actual Render domain |
| `DATABASE_URL` | (Auto-filled) | Automatically set when you link the PostgreSQL database |

**To link the database:**
- In the Web Service settings, scroll to **"Add Environment Variable"**
- Click **"Link Database"** and select your PostgreSQL database
- Render will automatically add `DATABASE_URL`

#### Additional Security Settings (Optional but Recommended):
Add these for better security:

| Key | Value |
|-----|-------|
| `SECURE_HSTS_SECONDS` | `31536000` |
| `SECURE_SSL_REDIRECT` | `True` |
| `SESSION_COOKIE_SECURE` | `True` |
| `CSRF_COOKIE_SECURE` | `True` |

### 5. Deploy

1. Click **"Create Web Service"**
2. Render will start building your application
3. Watch the build logs for any errors
4. Once deployed, you'll get a URL like: `https://your-app-name.onrender.com`

### 6. Create a Superuser (Admin Account)

After successful deployment, you need to create an admin user:

**Option A: Using Render Shell (Recommended)**
1. Go to your Web Service in Render dashboard
2. Click on **"Shell"** tab
3. Run:
   ```bash
   python create_superuser.py
   ```
4. Follow the prompts to create your admin user

**Option B: Using Django Management Command**
1. In Render Shell, run:
   ```bash
   python manage.py createsuperuser
   ```
2. Follow the prompts

### 7. Verify Deployment

1. Visit your app URL: `https://your-app-name.onrender.com`
2. Try logging in with your superuser credentials
3. Check the admin panel: `https://your-app-name.onrender.com/admin`

## Troubleshooting

### Build Fails with "Could not open requirements file"
**This is the most common error!** It means Render can't find `requirements.txt`. Solutions:

1. **Verify files are committed and pushed:**
   ```bash
   git status
   git add requirements.txt Procfile build.sh
   git commit -m "Add deployment files"
   git push origin main
   ```

2. **Check Root Directory in Render:**
   - Go to your Web Service settings in Render
   - Scroll to **"Root Directory"**
   - **Leave it EMPTY** (or set to `.` if your Django app is in the repo root)
   - If your Django app is in a subdirectory, set Root Directory to that subdirectory

3. **Verify file location:**
   - `requirements.txt` must be in the same directory as `manage.py`
   - `Procfile` must be in the same directory as `manage.py`
   - `build.sh` must be in the same directory as `manage.py`

4. **Check build logs:**
   - Look at the build logs in Render dashboard
   - The error will show which directory Render is looking in
   - Compare with where your files actually are

### Build Fails (Other Issues)
- Check build logs in Render dashboard
- Ensure `requirements.txt` is in the root directory
- Verify `build.sh` has execute permissions (Render handles this)
- Make sure all files are committed to git and pushed to your repository

### Static Files Not Loading
- Ensure `collectstatic` ran during build (check build logs)
- Verify WhiteNoise is in `MIDDLEWARE` in `settings.py`
- Check `STATIC_ROOT` and `STATIC_URL` settings

### Database Connection Errors
- Verify `DATABASE_URL` environment variable is set
- Check that PostgreSQL database is linked to your web service
- Ensure `psycopg2-binary` is in `requirements.txt`

### 500 Internal Server Error
- Check application logs in Render dashboard
- Verify `DEBUG=False` and `ALLOWED_HOSTS` includes your domain
- Check that migrations ran successfully

### Can't Access Admin Panel
- Ensure you created a superuser (Step 6)
- Check that you're using the correct URL: `/admin`

## Post-Deployment Checklist

- [ ] Application is accessible at your Render URL
- [ ] Admin panel is accessible at `/admin`
- [ ] Can log in with superuser credentials
- [ ] Static files (CSS, JS) are loading correctly
- [ ] Database migrations completed successfully
- [ ] Can create/edit members, contributions, etc.
- [ ] Media uploads work (if applicable)

## Environment Variables Summary

**Required:**
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False`
- `ALLOWED_HOSTS` - Your Render domain
- `DATABASE_URL` - Auto-set when linking PostgreSQL

**Optional (Security):**
- `SECURE_HSTS_SECONDS` - HSTS security
- `SECURE_SSL_REDIRECT` - Force HTTPS
- `SESSION_COOKIE_SECURE` - Secure cookies
- `CSRF_COOKIE_SECURE` - Secure CSRF cookies

## Support

If you encounter issues:
1. Check Render's build and runtime logs
2. Review Django error logs in Render dashboard
3. Verify all environment variables are set correctly
4. Ensure all files are committed and pushed to your repository

---

**Generated Secret Key for Reference:**
```
eet*o%xj7s4b8t7p9v7f$u@ns4s0cvxcw1b_9g(tpw%=(%om9^
```
⚠️ **Important**: Generate a NEW secret key for production! Don't use this one.

