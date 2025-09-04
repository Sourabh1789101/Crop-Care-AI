# Vercel Deployment Guide

## Recent Fixes Applied

### 1. Vercel Configuration (`vercel.json`)
- Added `maxLambdaSize` configuration for larger deployments
- Improved routing patterns for static files
- Added function timeout configuration
- Fixed builds vs functions conflict

### 2. API Structure (`api/index.py`)
- Removed duplicate function definitions
- Cleaned up export statements
- Added proper health check endpoints
- Simplified dependency requirements

### 3. Deployment Optimization
- Created `.vercelignore` to exclude unnecessary files
- Minimized package dependencies for faster builds
- Ensured Python 3.12 compatibility

## Common Vercel Error Solutions

### FUNCTION_INVOCATION_FAILED (500)
- **Fix Applied**: Simplified API structure and removed circular imports
- **Prevention**: Clean function definitions without duplicates

### DEPLOYMENT_NOT_READY_REDIRECTING (303)
- **Fix Applied**: Improved routing configuration
- **Prevention**: Proper build configuration in vercel.json

### FUNCTION_PAYLOAD_TOO_LARGE (413)
- **Fix Applied**: Added maxLambdaSize configuration
- **Prevention**: Minimize dependencies and payload size

### Router Errors (502)
- **Fix Applied**: Improved routing patterns for static files
- **Prevention**: Clear separation between API and static routes

## Testing Deployment

1. **Local Test**: 
   ```bash
   cd api
   python -c "from index import app; print('API import successful')"
   ```

2. **API Endpoints**:
   - Health: `/api/health`
   - Root: `/api/`
   - Crop Recommendation: `/api/recommend_crop`
   - Fertilizer: `/api/recommend_fertilizer`

3. **Frontend**: 
   - Main page: `/`
   - All static files: `/*.html`, `/*.js`, `/*.css`

## Next Steps

If deployment still fails:
1. Check Vercel dashboard for specific error logs
2. Verify all dependencies are compatible with Python 3.12
3. Test individual API endpoints after deployment
4. Monitor function execution time and memory usage

## Emergency Rollback

If issues persist, use the previous working configuration:
```json
{
  "version": 2,
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  }
}
```
