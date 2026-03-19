# Testing Guide

## ✅ Feature Testing Checklist

This guide helps you test all features of the Hypertension Prediction System.

## 🔐 Authentication Testing

### Test 1: User Registration
- [ ] Open http://localhost:5000
- [ ] Click "Sign Up"
- [ ] Enter:
  - Username: `testuser1`
  - Email: `test@example.com`
  - Password: `test123456`
  - Confirm Password: `test123456`
- [ ] Click "Sign Up"
- [ ] Verify success message
- [ ] Verify redirect to login

### Test 2: Registration Validation
- [ ] Try registering with:
  - [ ] Same username (should fail)
  - [ ] Same email (should fail)
  - [ ] Mismatched passwords (should fail)
  - [ ] Empty fields (should fail)

### Test 3: User Login
- [ ] Enter username: `testuser1`
- [ ] Enter password: `test123456`
- [ ] Click "Sign In"
- [ ] Verify success message
- [ ] Verify redirect to dashboard
- [ ] Verify username displayed in header

### Test 4: Login Validation
- [ ] Try login with:
  - [ ] Wrong password (should fail)
  - [ ] Non-existent user (should fail)
  - [ ] Empty fields (should fail)

### Test 5: Token Management
- [ ] Open browser DevTools (F12)
- [ ] Go to Console
- [ ] Run: `localStorage.getItem('access_token')`
- [ ] Verify token is stored after login
- [ ] Run: `localStorage.clear()`
- [ ] Try accessing dashboard (should redirect to login)

## 📊 Prediction Testing

### Test 6: Valid Prediction
- [ ] Login with test account
- [ ] Fill prediction form:
  - Age: `45`
  - Systolic: `140`
  - Diastolic: `90`
  - Heart Rate: `72`
  - Cholesterol: `220`
  - Glucose: `110`
- [ ] Click "Get Prediction"
- [ ] Verify result displays
- [ ] Verify status (Normal or High BP)
- [ ] Verify health tips appear
- [ ] Verify doctor list appears
- [ ] Verify confidence score

### Test 7: Healthy Profile Prediction
- [ ] Fill prediction form with normal values:
  - Age: `30`
  - Systolic: `120`
  - Diastolic: `80`
  - Heart Rate: `70`
  - Cholesterol: `180`
  - Glucose: `90`
- [ ] Verify result shows "HEALTHY BLOOD PRESSURE"
- [ ] Verify appropriate tips (fitness-focused)
- [ ] Verify "Keep up the good health habits" message

### Test 8: High BP Profile Prediction
- [ ] Fill prediction form with high values:
  - Age: `60`
  - Systolic: `180`
  - Diastolic: `110`
  - Heart Rate: `90`
  - Cholesterol: `300`
  - Glucose: `150`
- [ ] Verify result shows "HIGH BLOOD PRESSURE DETECTED"
- [ ] Verify urgent action message
- [ ] Verify cardiologist recommendations
- [ ] Verify "Contact consultant" message

### Test 9: Form Validation
- [ ] Try submitting with:
  - [ ] Empty fields (should prevent submission)
  - [ ] Negative numbers (behavior check)
  - [ ] Very large numbers (e.g., 999999)
  - [ ] Non-numeric characters in number fields

### Test 10: Multiple Predictions
- [ ] Make 3-4 predictions with different values
- [ ] Verify each produces different results
- [ ] Verify no data loss
- [ ] Verify database stores all predictions

## 📈 History Testing

### Test 11: Prediction History
- [ ] Click on "History" tab
- [ ] Verify all previous predictions display
- [ ] Verify predictions sorted by newest first
- [ ] Verify timestamps are correct
- [ ] Verify icons show prediction type (High/Normal)
- [ ] Verify confidence percentages display

### Test 12: History Persistence
- [ ] Logout
- [ ] Login again
- [ ] Go to History tab
- [ ] Verify previous predictions still show
- [ ] Verify data not lost after logout

## 📚 Resources Testing

### Test 13: Resources Tab
- [ ] Click on "Resources" tab
- [ ] Verify all 4 resource sections appear:
  - [ ] Diet Tips
  - [ ] Exercise Guidelines
  - [ ] Stress Management
  - [ ] Lifestyle Habits
- [ ] Verify all tips display correctly
- [ ] Verify proper formatting

## 🚪 Navigation Testing

### Test 14: Dashboard Navigation
- [ ] Click each navigation button:
  - [ ] New Prediction (should show form)
  - [ ] History (should show predictions)
  - [ ] Resources (should show tips)
- [ ] Verify active state changes
- [ ] Verify content switches correctly

### Test 15: Logout
- [ ] Click "Logout" button
- [ ] Confirm logout dialog
- [ ] Verify redirect to login page
- [ ] Verify localStorage cleared (check DevTools)
- [ ] Verify cannot access dashboard directly

## 🎨 UI/UX Testing

### Test 16: Responsive Design
- [ ] Test on different screen sizes:
  - [ ] Desktop (1920x1080)
  - [ ] Tablet (768x1024)
  - [ ] Mobile (375x667)
- [ ] Verify layout adapts correctly
- [ ] Verify buttons are clickable
- [ ] Verify text is readable

### Test 17: Color & Styling
- [ ] Verify unhealthy prediction shows warning colors
- [ ] Verify healthy prediction shows success colors
- [ ] Verify buttons have proper hover effects
- [ ] Verify form inputs have focus states
- [ ] Verify doctor cards display properly

## 🔧 API Testing (Using cURL or Postman)

### Test 18: API Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"apitest","email":"api@test.com","password":"api123"}'
```
Expected: 201 Created

### Test 19: API Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"apitest","password":"api123"}'
```
Expected: 200 OK with access_token

### Test 20: API Prediction (requires token from Test 19)
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{"age":45,"systolic":140,"diastolic":90,"heart_rate":72,"cholesterol":220,"glucose":110}'
```
Expected: 200 OK with prediction

### Test 21: API History
```bash
curl -X GET http://localhost:5000/api/prediction-history \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```
Expected: 200 OK with list of predictions

## 📊 Database Testing

### Test 22: Database Verification
- [ ] Open file explorer
- [ ] Navigate to project folder
- [ ] Verify `hypertension.db` exists
- [ ] Use SQLite viewer to check:
  - [ ] Users table has entries
  - [ ] Predictions table has entries
  - [ ] Data matches UI display

### Test 23: Database Integrity
```sql
-- Check users table
SELECT COUNT(*) as user_count FROM users;

-- Check predictions table
SELECT COUNT(*) as prediction_count FROM predictions;

-- Verify foreign key relationship
SELECT u.username, COUNT(p.id) as prediction_count 
FROM users u 
LEFT JOIN predictions p ON u.id = p.user_id 
GROUP BY u.id;
```

## ⚠️ Error Handling Testing

### Test 24: Network Error Handling
- [ ] Disconnect internet
- [ ] Try to make prediction
- [ ] Verify error message displays
- [ ] Reconnect internet

### Test 25: Server Error Handling
- [ ] Stop Flask server (Ctrl+C)
- [ ] Try to make request
- [ ] Verify appropriate error
- [ ] Restart server

### Test 26: Session Expiration
- [ ] Login and wait (token expires after 30 days in config)
- [ ] Or temporarily set short expiration for testing
- [ ] Verify auto-logout on expired token

## 🔒 Security Testing

### Test 27: SQL Injection Prevention
- [ ] Try login with: `admin' --`
- [ ] Try registration with special characters: `'; DROP TABLE users; --`
- [ ] Verify system handles safely

### Test 28: XSS Prevention
- [ ] Try entering HTML/JavaScript in forms:
  - `<script>alert('xss')</script>`
  - `<img src=x onerror=alert('xss')>`
- [ ] Verify tagged as text, not executed

### Test 29: Unauthorized Access
- [ ] Create two user accounts
- [ ] Login with user1
- [ ] Open DevTools and copy token
- [ ] Logout
- [ ] Modify token and try to use
- [ ] Verify access denied

## 📈 Performance Testing

### Test 30: Load Testing
- [ ] Make 10 rapid predictions
- [ ] Verify all complete
- [ ] Check response times
- [ ] Verify no data loss

### Test 31: Large Dataset
- [ ] Create 100+ predictions
- [ ] Go to History tab
- [ ] Verify page loads smoothly
- [ ] Verify no lag

## 🎯 End-to-End Test Scenario

**Complete User Journey:**
1. [ ] New user registration
2. [ ] Successful login
3. [ ] First prediction
4. [ ] Check history
5. [ ] Read resources
6. [ ] Make second prediction with different values
7. [ ] Verify history updated
8. [ ] Logout
9. [ ] Login again
10. [ ] Verify predictions still there

---

## 📝 Test Results Template

```
Date: ___________
Tester: ___________
Environment: [ ] Local [ ] Staging [ ] Production

Results Summary:
- Total Tests: 31
- Passed: ___
- Failed: ___
- Skipped: ___

Issues Found:
1. Test #___ - Issue: ___________
2. Test #___ - Issue: ___________

Recommendation: [ ] PASS [ ] FAIL [ ] RETEST
```

## 🚀 Ready for Production?

- [ ] All 31 tests passed
- [ ] No critical issues
- [ ] Minor issues documented
- [ ] Performance acceptable
- [ ] Security review passed
- [ ] Database backup tested
- [ ] Error handling verified

Good luck with testing! 🎉
