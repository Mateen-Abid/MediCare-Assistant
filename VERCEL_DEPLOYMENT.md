# 🚀 Vercel Deployment Guide for MediCare Assistant

This guide will help you deploy your Django healthcare chatbot to Vercel.

## Prerequisites

1. A Vercel account ([Sign up here](https://vercel.com/signup))
2. GitHub account (to connect your repository)
3. Google Gemini API Key
4. Database (Supabase/PostgreSQL recommended for production)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure your code is pushed to GitHub:
- All sensitive files (`.env`) are in `.gitignore`
- `vercel.json` is in the root directory
- `api/index.py` exists for Vercel serverless function

### 2. Connect to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Vercel will auto-detect the project settings

### 3. Configure Environment Variables

In Vercel project settings, add these environment variables:

#### Required Variables:
```
API_KEY=your_gemini_api_key_here
SECRET_KEY=your_django_secret_key_here
DEBUG=False
```

#### Optional Variables (for Supabase/PostgreSQL):
```
USE_SUPABASE=true
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432
```

#### Generate Django Secret Key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Configure Build Settings

Vercel should auto-detect, but verify:
- **Framework Preset**: Other
- **Root Directory**: `./` (root)
- **Build Command**: Leave empty (or `python manage.py collectstatic --noinput`)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### 5. Deploy

1. Click **"Deploy"**
2. Wait for the build to complete
3. Your app will be live at `https://your-project.vercel.app`

### 6. Run Migrations

After first deployment, you need to run migrations. You can do this via:

**Option A: Vercel CLI**
```bash
npm i -g vercel
vercel login
vercel env pull .env.local
vercel --prod
```

**Option B: Vercel Functions (Recommended)**

Create a one-time migration script or use Vercel's function logs to run migrations.

**Option C: Use Django Admin or Management Command**

You may need to set up a separate endpoint or use Vercel's serverless function to run migrations.

### 7. Static Files

Static files are handled by WhiteNoise middleware. Make sure to run:
```bash
python manage.py collectstatic
```

This is typically done during the build process.

## Important Notes

### Database Considerations

- **SQLite**: Not recommended for production on Vercel (file system is read-only)
- **PostgreSQL/Supabase**: Highly recommended for production
- Set `USE_SUPABASE=true` in environment variables to use PostgreSQL

### Session Storage

Vercel's serverless functions are stateless. Consider:
- Using database-backed sessions
- Using external session storage (Redis)
- Using JWT tokens instead of sessions

### Cold Starts

Serverless functions may have cold starts. Consider:
- Using Vercel Pro for better performance
- Implementing connection pooling for databases
- Using edge functions for static content

### CSRF Protection

Update `CSRF_TRUSTED_ORIGINS` in settings if needed:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://your-project.vercel.app',
    'https://*.vercel.app',
]
```

## Troubleshooting

### Build Fails

1. Check build logs in Vercel dashboard
2. Ensure all dependencies are in `requirements.txt`
3. Verify Python version compatibility

### Static Files Not Loading

1. Ensure `whitenoise` is in `requirements.txt`
2. Run `collectstatic` during build
3. Check `STATIC_ROOT` and `STATIC_URL` settings

### Database Connection Issues

1. Verify environment variables are set correctly
2. Check database host allows Vercel IPs
3. Ensure SSL is enabled for Supabase connections

### 500 Errors

1. Check function logs in Vercel dashboard
2. Verify `SECRET_KEY` is set
3. Check `ALLOWED_HOSTS` includes your Vercel domain
4. Ensure migrations are run

## Post-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Test user registration/login
- [ ] Test chatbot functionality
- [ ] Verify API endpoints work
- [ ] Check error logs
- [ ] Set up custom domain (optional)

## Custom Domain Setup

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` environment variable

## Monitoring

- Use Vercel Analytics for performance monitoring
- Check Function Logs for errors
- Monitor API usage for Gemini API
- Set up error tracking (Sentry, etc.)

## Support

For issues:
- Check [Vercel Documentation](https://vercel.com/docs)
- Review Django deployment checklist
- Check project GitHub issues

---

**Note**: Vercel is optimized for serverless functions. For heavy database operations or long-running tasks, consider using additional services or upgrading to Vercel Pro.

