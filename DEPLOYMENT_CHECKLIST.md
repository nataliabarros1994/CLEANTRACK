# CleanTrack - Production Deployment Checklist

## Pre-Deployment

### Security
- [ ] Set `DEBUG=False` in production
- [ ] Generate strong `SECRET_KEY` (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] Configure `ALLOWED_HOSTS` with actual domain
- [ ] Set up SSL certificate
- [ ] Configure `CSRF_TRUSTED_ORIGINS`
- [ ] Enable `SECURE_SSL_REDIRECT`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Review and update CORS settings

### Database
- [ ] Set up production PostgreSQL instance
- [ ] Configure database backups (daily minimum)
- [ ] Set up connection pooling
- [ ] Run migrations
- [ ] Create database indexes
- [ ] Configure database monitoring

### Environment Variables
- [ ] `SECRET_KEY` - Django secret key
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `REDIS_URL` - Redis connection string
- [ ] `STRIPE_PUBLIC_KEY` - Stripe publishable key
- [ ] `STRIPE_SECRET_KEY` - Stripe secret key (live mode)
- [ ] `STRIPE_WEBHOOK_SECRET` - Stripe webhook secret
- [ ] `RESEND_API_KEY` - Resend API key
- [ ] `DEFAULT_FROM_EMAIL` - Verified sender email
- [ ] `ALLOWED_HOSTS` - Production domain(s)
- [ ] `CSRF_TRUSTED_ORIGINS` - Production URLs

### Email (Resend)
- [ ] Verify domain in Resend
- [ ] Set up SPF records
- [ ] Set up DKIM records
- [ ] Test email delivery
- [ ] Configure email templates

### Stripe
- [ ] Create Stripe account
- [ ] Set up products and prices
- [ ] Configure webhook endpoint
- [ ] Test payment flow
- [ ] Set up subscription plans
- [ ] Configure tax settings (if applicable)

### Static Files
- [ ] Run `python manage.py collectstatic`
- [ ] Configure CDN (optional but recommended)
- [ ] Set up WhiteNoise for static file serving
- [ ] Verify static files load correctly

### Media Files
- [ ] Set up cloud storage (S3, GCS, etc.)
- [ ] Configure Django Storages (if using cloud)
- [ ] Set up media file backups
- [ ] Test file uploads

### Celery & Redis
- [ ] Set up production Redis instance
- [ ] Configure Celery workers
- [ ] Configure Celery Beat scheduler
- [ ] Set up Celery monitoring
- [ ] Configure task timeouts
- [ ] Set up dead letter queue

## Deployment

### Platform-Specific Setup

#### Render.com
```yaml
services:
  - type: web
    name: cleantrack
    env: docker
    plan: starter
    envVars:
      - key: DEBUG
        value: False
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: cleantrack-db
          property: connectionString
```

#### Fly.io
```bash
fly launch
fly postgres create
fly postgres attach
fly deploy
```

#### AWS ECS
- [ ] Create ECS cluster
- [ ] Set up task definitions
- [ ] Configure load balancer
- [ ] Set up auto-scaling
- [ ] Configure CloudWatch logging

### Application Deployment
- [ ] Build Docker image
- [ ] Push to container registry
- [ ] Deploy to production
- [ ] Run migrations
- [ ] Create superuser
- [ ] Test basic functionality
- [ ] Verify background tasks running

## Post-Deployment

### Verification
- [ ] Access admin panel
- [ ] Test user registration
- [ ] Test login/logout
- [ ] Create test account
- [ ] Add test equipment
- [ ] Log test cleaning
- [ ] Verify alerts working
- [ ] Generate test report
- [ ] Test payment flow (use Stripe test mode first)

### Monitoring
- [ ] Set up application monitoring (Sentry, etc.)
- [ ] Configure uptime monitoring
- [ ] Set up log aggregation
- [ ] Configure alerts for errors
- [ ] Monitor Celery task queue
- [ ] Monitor database performance
- [ ] Set up performance metrics

### Backups
- [ ] Database backup schedule configured
- [ ] Media file backup configured
- [ ] Test restore procedure
- [ ] Document backup/restore process

### Documentation
- [ ] Document deployment process
- [ ] Document environment variables
- [ ] Create runbook for common issues
- [ ] Document rollback procedure

### DNS & Domain
- [ ] Point domain to production server
- [ ] Configure DNS records
- [ ] Verify SSL certificate
- [ ] Test domain access

### Performance
- [ ] Run load tests
- [ ] Optimize database queries
- [ ] Enable query caching
- [ ] Configure CDN for static files
- [ ] Test response times
- [ ] Optimize images

### Security Scan
- [ ] Run security audit
- [ ] Check for exposed secrets
- [ ] Verify HTTPS everywhere
- [ ] Test authentication
- [ ] Review permissions
- [ ] Check CORS configuration

## Launch Checklist

### Before Public Launch
- [ ] Create initial demo account
- [ ] Prepare marketing materials
- [ ] Set up support email
- [ ] Create FAQ documentation
- [ ] Test all user flows
- [ ] Verify payment processing
- [ ] Set up analytics

### Launch Day
- [ ] Announce launch
- [ ] Monitor error logs
- [ ] Watch server metrics
- [ ] Be ready for support requests
- [ ] Monitor payment processing

### Post-Launch
- [ ] Collect user feedback
- [ ] Monitor usage patterns
- [ ] Track key metrics
- [ ] Address bugs promptly
- [ ] Plan next features

## Maintenance

### Daily
- [ ] Check error logs
- [ ] Monitor uptime
- [ ] Review failed tasks
- [ ] Check email delivery

### Weekly
- [ ] Review security logs
- [ ] Check backup integrity
- [ ] Monitor disk space
- [ ] Review performance metrics

### Monthly
- [ ] Update dependencies
- [ ] Review and optimize queries
- [ ] Audit user accounts
- [ ] Review subscription status
- [ ] Generate compliance reports

## Emergency Procedures

### If Site Goes Down
1. Check server status
2. Review error logs
3. Check database connectivity
4. Verify Redis connection
5. Review recent deployments
6. Rollback if necessary

### If Database Issues
1. Check database logs
2. Verify connectivity
3. Check disk space
4. Review slow queries
5. Restore from backup if needed

### If Payment Issues
1. Check Stripe dashboard
2. Verify webhook endpoint
3. Review webhook logs
4. Contact Stripe support

## Support

### User Support
- Email: support@cleantrack.app
- Response time: <24 hours
- Escalation path documented

### Technical Support
- Email: dev@cleantrack.app
- On-call rotation (if applicable)
- Incident response plan

## Scaling Plan

### When to Scale
- CPU > 70% for extended period
- Database connections > 80% of max
- Response time > 2 seconds
- Queue depth growing

### Scaling Options
- Horizontal scaling (more workers)
- Vertical scaling (bigger instances)
- Database read replicas
- Redis cluster
- CDN for static files

---

**Last Updated**: 2025-01-20
**Review This Checklist**: Before each deployment
