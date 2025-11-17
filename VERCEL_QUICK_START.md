# 🚀 Quick Vercel Deployment Guide

## Step 1: Generate Django Secret Key

Run this command in your terminal to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the output** - you'll need it for Step 3.

## Step 2: Go to Vercel Dashboard

1. Visit: https://vercel.com/dashboard
2. Sign in (or create account if needed)
3. Click **"Add New Project"** or **"Import Project"**

## Step 3: Import Your GitHub Repository

1. Click **"Import Git Repository"**
2. Select **"Mateen-Abid/MediCare-Assistant"** from the list
3. Click **"Import"**

## Step 4: Configure Project Settings

Vercel should auto-detect, but verify:

- **Framework Preset**: Other (or leave blank)
- **Root Directory**: `./` (leave as default)
- **Build Command**: Leave empty
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

## Step 5: Add Environment Variables

**BEFORE clicking Deploy**, click **"Environment Variables"** and add:

### Required Variables:

| Name | Value | Notes |
|------|-------|-------|
| `API_KEY` | `your_gemini_api_key` | Your Google Gemini API key |
| `SECRET_KEY` | `paste_generated_key_here` | The key from Step 1 |
| `DEBUG` | `False` | Must be False for production |

### Optional (if using Supabase):

| Name | Value |
|------|-------|
| `USE_SUPABASE` | `true` |
| `DB_NAME` | `your_db_name` |
| `DB_USER` | `your_db_user` |
| `DB_PASSWORD` | `your_db_password` |
| `DB_HOST` | `db.xxxxx.supabase.co` |
| `DB_PORT` | `5432` |

**Important**: 
- Add variables for **Production**, **Preview**, and **Development** environments
- Click **"Save"** after adding each variable

## Step 6: Deploy

1. Click **"Deploy"** button
2. Wait for build to complete (2-5 minutes)
3. Your app will be live at: `https://your-project-name.vercel.app`

## Step 7: Run Database Migrations

After first deployment, you need to run migrations. Here are your options:

### Option A: Vercel CLI (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login:
```bash
vercel login
```

3. Link your project:
```bash
vercel link
```

4. Run migrations:
```bash
vercel env pull .env.local
python manage.py migrate
```

### Option B: Create Migration Endpoint (Temporary)

Add this to your `app/views.py` temporarily:

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def run_migrations(request):
    """One-time migration endpoint - REMOVE AFTER USE"""
    from django.core.management import call_command
    import io
    out = io.StringIO()
    call_command('migrate', stdout=out)
    return Response({'output': out.getvalue()})
```

Then call it once via API and remove it.

### Option C: Use Vercel Function Logs

Check deployment logs in Vercel dashboard for any migration errors.

## Step 8: Verify Deployment

1. Visit your deployed URL
2. Test signup/login
3. Test chatbot functionality
4. Check Vercel dashboard for any errors

## Troubleshooting

### Build Fails

- Check build logs in Vercel dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version (should be 3.12)

### 500 Errors

- Check function logs in Vercel dashboard
- Verify `SECRET_KEY` is set correctly
- Ensure `DEBUG=False` in production
- Check `ALLOWED_HOSTS` includes your Vercel domain

### Static Files Not Loading

- Static files should work automatically with WhiteNoise
- If issues persist, check `STATIC_ROOT` and `STATIC_URL` settings

### Database Connection Issues

- Verify environment variables are correct
- Check database host allows connections
- Ensure SSL is enabled for Supabase

## Post-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Test user registration
- [ ] Test login
- [ ] Test chatbot
- [ ] Verify API endpoints
- [ ] Check error logs
- [ ] Set custom domain (optional)

## Need Help?

- Check Vercel logs: Dashboard → Your Project → Functions → Logs
- Review full guide: `VERCEL_DEPLOYMENT.md`
- Vercel Docs: https://vercel.com/docs

---

**Your app URL will be**: `https://medicare-assistant.vercel.app` (or similar)

