# Tasks: Integrate Supabase Authentication

## Phase 1: Supabase Project Setup (Day 1)

- [ ] **Task 1.1**: Create Supabase project
  - Create new project in Supabase Dashboard
  - Select appropriate region (us-west-1 or closer to users)
  - Note down project URL and API keys
  - **Validation**: Can access Supabase Dashboard, API keys visible

- [ ] **Task 1.2**: Configure Google OAuth provider
  - Create Google OAuth credentials in Google Cloud Console
  - Add authorized redirect URIs in Google Console
  - Configure Google provider in Supabase Auth settings
  - Add Client ID and Client Secret to Supabase
  - **Validation**: Google OAuth appears as enabled in Supabase Dashboard

- [ ] **Task 1.3**: Configure GitHub OAuth provider
  - Create GitHub OAuth App in GitHub Developer Settings
  - Add callback URL: `https://[project-ref].supabase.co/auth/v1/callback`
  - Configure GitHub provider in Supabase Auth settings
  - Add Client ID and Client Secret to Supabase
  - **Validation**: GitHub OAuth appears as enabled in Supabase Dashboard

- [ ] **Task 1.4**: Configure redirect URLs
  - Add development redirect URL: `http://localhost:5173/auth/callback`
  - Add production redirect URL (when ready)
  - Configure site URL in Supabase settings
  - **Validation**: Redirect URLs saved in Supabase Auth settings

- [ ] **Task 1.5**: Update environment variables
  - Add `VITE_SUPABASE_URL` to frontend `.env`
  - Add `VITE_SUPABASE_ANON_KEY` to frontend `.env`
  - Add `SUPABASE_URL` to backend `.env`
  - Add `SUPABASE_JWT_SECRET` to backend `.env`
  - Create `.env.example` templates
  - **Validation**: Environment variables loaded correctly, no undefined values

## Phase 2: Frontend Integration (Days 2-4)

- [ ] **Task 2.1**: Install Supabase SDK
  - Run `npm install @supabase/supabase-js`
  - Verify package added to `package.json`
  - **Validation**: No installation errors, package version >= 2.0

- [ ] **Task 2.2**: Create Supabase client configuration
  - Create `src/lib/supabase.ts`
  - Initialize Supabase client with URL and anon key
  - Configure auth options (persistSession, autoRefreshToken)
  - Export typed Supabase client
  - **Validation**: Run `npm run type-check`, no TypeScript errors

- [ ] **Task 2.3**: Refactor AuthContext to use Supabase
  - Update `src/contexts/AuthContext.tsx`
  - Replace custom JWT logic with Supabase Auth
  - Implement `onAuthStateChange` listener
  - Add `signInWithEmail`, `signUpWithEmail`, `signOut` methods
  - Add `getAccessToken` method for API requests
  - **Validation**: Context compiles without errors, provides expected interface

- [ ] **Task 2.4**: Update auth service layer
  - Update `src/services/auth.ts`
  - Add `syncUserWithBackend` function
  - Remove custom JWT token management
  - Add error handling for Supabase errors
  - **Validation**: Service functions return correct types

- [ ] **Task 2.5**: Update LoginPage with Supabase integration
  - Update `src/pages/LoginPage.tsx`
  - Replace form submit handler to use Supabase
  - Add loading states during authentication
  - Update error handling to display Supabase errors
  - **Validation**: Manual test - can log in with existing Supabase user

- [ ] **Task 2.6**: Update RegisterPage with Supabase integration
  - Update `src/pages/RegisterPage.tsx`
  - Replace form submit handler to use Supabase
  - Add loading states during registration
  - Update error handling
  - **Validation**: Manual test - can register new user

- [ ] **Task 2.7**: Add OAuth login buttons to LoginPage
  - Add Google login button with Google icon
  - Add GitHub login button with GitHub icon
  - Implement `signInWithGoogle` and `signInWithGithub`
  - Add separator between email and OAuth login
  - Style buttons according to brand guidelines
  - **Validation**: Buttons render correctly, clicking triggers OAuth flow

- [ ] **Task 2.8**: Create OAuth callback page
  - Create `src/pages/AuthCallbackPage.tsx`
  - Handle OAuth redirect and session detection
  - Show loading state while processing callback
  - Redirect to home page after successful auth
  - Handle OAuth errors gracefully
  - **Validation**: OAuth flow completes successfully, user redirected to home

- [ ] **Task 2.9**: Update API request interceptor
  - Update axios/fetch interceptor to use Supabase JWT
  - Get access token from Supabase session
  - Add `Authorization: Bearer <token>` header
  - Handle token refresh automatically
  - **Validation**: API requests include correct Authorization header

- [ ] **Task 2.10**: Update route protection logic
  - Update protected route component/hook
  - Check Supabase session instead of custom token
  - Redirect to login if session invalid/expired
  - **Validation**: Protected routes accessible only when authenticated

- [ ] **Task 2.11**: Add OAuth provider icons
  - Install `react-icons` package (if not already)
  - Import Google and GitHub icons
  - Apply consistent icon sizing and spacing
  - **Validation**: Icons display correctly in all browsers

## Phase 3: Backend Integration (Days 5-6)

- [ ] **Task 3.1**: Install required Python packages
  - Add `python-jose[cryptography]` to `requirements.txt`
  - Add `httpx` for async HTTP requests
  - Run `pip install -r requirements.txt`
  - **Validation**: Packages install without errors

- [ ] **Task 3.2**: Create Supabase JWT verifier
  - Create `app/core/supabase.py`
  - Implement `SupabaseJWTVerifier` class
  - Add `get_jwks()` method with caching
  - Add `verify_token()` method
  - Handle JWT verification errors
  - **Validation**: Unit test - verify valid and invalid JWTs

- [ ] **Task 3.3**: Update get_current_user dependency
  - Update `app/api/deps.py`
  - Replace custom JWT verification with Supabase JWT verifier
  - Extract `supabase_user_id` from JWT payload
  - Query user by `supabase_user_id`
  - Auto-create user if not exists
  - **Validation**: Unit test - dependency returns correct User object

- [ ] **Task 3.4**: Add database migration for User model
  - Create Alembic migration: add `supabase_user_id` column
  - Create Alembic migration: add `avatar_url` column
  - Add unique index on `supabase_user_id`
  - (Optional) Mark `hashed_password` as nullable
  - **Validation**: Run `alembic upgrade head`, migration succeeds

- [ ] **Task 3.5**: Update User model
  - Update `app/models/user.py`
  - Add `supabase_user_id` field (String, unique, indexed)
  - Add `avatar_url` field (String, nullable)
  - Make `hashed_password` optional/nullable
  - **Validation**: Model reflects database schema

- [ ] **Task 3.6**: Create user sync endpoint
  - Update `app/api/v1/endpoints/auth.py`
  - Add `POST /api/v1/auth/sync-user` endpoint
  - Extract user info from JWT
  - Create or update local User record
  - Return UserResponse
  - **Validation**: Manual test - call endpoint with valid JWT, user created/updated

- [ ] **Task 3.7**: Remove custom JWT generation logic
  - Update `app/services/auth_service.py`
  - Remove `create_tokens()` function
  - Remove `verify_refresh_token()` function
  - Keep `register_user()` and `authenticate_user()` as deprecated (for migration)
  - **Validation**: Code compiles, unused functions removed

- [ ] **Task 3.8**: Update auth endpoints
  - Update `/register` endpoint to return deprecation warning
  - Update `/login` endpoint to return deprecation warning
  - Remove `/refresh` endpoint
  - Document migration path for existing users
  - **Validation**: Endpoints return 410 Gone or deprecation notice

- [ ] **Task 3.9**: Update all protected endpoints
  - Verify all endpoints use `Depends(get_current_user)`
  - Ensure no endpoints rely on custom JWT logic
  - Test each endpoint with Supabase JWT
  - **Validation**: All protected endpoints accept Supabase JWT

## Phase 4: Testing (Days 7-8)

- [ ] **Task 4.1**: Write frontend unit tests
  - Test AuthContext methods (signIn, signUp, signOut)
  - Test OAuth sign-in functions
  - Mock Supabase client responses
  - **Validation**: Run `npm run test`, all tests pass

- [ ] **Task 4.2**: Write backend unit tests
  - Test `SupabaseJWTVerifier.verify_token()`
  - Test `get_current_user` dependency
  - Test user sync logic
  - Mock Supabase JWKS responses
  - **Validation**: Run `pytest`, all tests pass

- [ ] **Task 4.3**: Write integration tests
  - Test complete email login flow
  - Test complete Google OAuth flow (with test account)
  - Test API request with Supabase JWT
  - Test token refresh flow
  - **Validation**: All integration tests pass

- [ ] **Task 4.4**: Manual end-to-end testing
  - Test email registration and login
  - Test Google OAuth login
  - Test GitHub OAuth login
  - Test accessing protected pages
  - Test API requests (create generation job)
  - Test sign out and session cleanup
  - **Validation**: All manual test cases pass, no errors in console

- [ ] **Task 4.5**: Test error scenarios
  - Test invalid email/password
  - Test expired JWT
  - Test OAuth cancellation
  - Test network errors during auth
  - **Validation**: Error messages are user-friendly, no crashes

- [ ] **Task 4.6**: Performance testing
  - Measure JWT verification latency
  - Measure OAuth redirect time
  - Measure user sync endpoint latency
  - **Validation**: All operations complete within acceptable time (<500ms)

- [ ] **Task 4.7**: Security audit
  - Verify JWT signature validation works correctly
  - Verify API keys are not exposed in client-side code
  - Verify HTTPS is enforced for OAuth callbacks
  - Check for XSS/CSRF vulnerabilities
  - **Validation**: No security issues found

## Phase 5: Documentation and Deployment (Day 9)

- [ ] **Task 5.1**: Update developer documentation
  - Document Supabase setup steps
  - Document environment variable requirements
  - Document OAuth provider configuration
  - Add troubleshooting section
  - **Validation**: Another developer can follow docs to set up locally

- [ ] **Task 5.2**: Update API documentation
  - Update `/auth/login` and `/auth/register` as deprecated
  - Document new `/auth/sync-user` endpoint
  - Update authentication section in OpenAPI docs
  - **Validation**: API docs reflect current endpoints

- [ ] **Task 5.3**: Create deployment guide
  - Document production Supabase project setup
  - Document environment variable configuration for production
  - Document OAuth redirect URL updates for production
  - Add rollback plan
  - **Validation**: Deployment guide is complete and clear

- [ ] **Task 5.4**: Deploy to staging environment
  - Create staging Supabase project (or use same project with staging URL)
  - Deploy frontend and backend to staging
  - Update environment variables in staging
  - **Validation**: Staging deployment successful, no errors

- [ ] **Task 5.5**: Smoke test on staging
  - Test email login on staging
  - Test Google OAuth on staging
  - Test GitHub OAuth on staging
  - Test API requests on staging
  - **Validation**: All critical flows work on staging

- [ ] **Task 5.6**: Prepare rollback plan
  - Tag current production code before deployment
  - Document rollback steps
  - Prepare database rollback migration (if needed)
  - **Validation**: Rollback plan is documented and tested

- [ ] **Task 5.7**: Deploy to production
  - Deploy backend with new auth logic
  - Deploy frontend with Supabase integration
  - Update production environment variables
  - Monitor error logs during deployment
  - **Validation**: Production deployment successful

- [ ] **Task 5.8**: Post-deployment monitoring
  - Monitor authentication success/failure rates
  - Monitor JWT verification errors
  - Monitor user sync endpoint latency
  - Check for any unexpected errors
  - **Validation**: No critical errors, metrics look healthy

- [ ] **Task 5.9**: User communication
  - Notify users of new login options (Google, GitHub)
  - (Optional) Send migration email to existing users
  - Update login page with announcement banner
  - **Validation**: Users are aware of new features

## Optional: User Migration (Future)

- [ ] **Task 6.1**: Design user migration strategy
  - Design one-time password reset flow
  - Design email notification for migration
  - Plan gradual rollout

- [ ] **Task 6.2**: Implement migration endpoint
  - Create `/auth/migrate` endpoint
  - Verify user's email ownership
  - Create Supabase user with same email
  - Link to local user record

- [ ] **Task 6.3**: Send migration emails
  - Prepare email template
  - Send batched emails to existing users
  - Provide clear migration instructions

- [ ] **Task 6.4**: Deprecate old auth endpoints
  - Set `/auth/login` and `/auth/register` to return 410 Gone
  - Remove old auth service code
  - Clean up database (remove hashed_password column)

## Summary

- **Total Tasks**: 53 (including optional migration tasks)
- **Estimated Duration**: 9 working days (excluding migration)
- **Key Milestones**:
  - Day 1: Supabase project ready
  - Day 4: Frontend integration complete
  - Day 6: Backend integration complete
  - Day 8: Testing complete
  - Day 9: Production deployment

## Dependencies Between Tasks

- Task 2.3 depends on Task 2.2 (AuthContext depends on Supabase client)
- Task 2.9 depends on Task 2.3 (API interceptor depends on AuthContext)
- Task 3.3 depends on Task 3.2 (get_current_user depends on JWT verifier)
- Task 3.6 depends on Task 3.4, 3.5 (sync endpoint depends on updated User model)
- All Phase 4 tasks depend on Phase 2 and 3 completion
- All Phase 5 tasks depend on Phase 4 completion

## Parallel Work Opportunities

- Tasks 1.2 and 1.3 can be done in parallel (OAuth provider setup)
- Tasks 2.5 and 2.6 can be done in parallel (LoginPage and RegisterPage)
- Tasks 3.2 and 3.4 can be done in parallel (JWT verifier and database migration)
- Tasks 4.1 and 4.2 can be done in parallel (frontend and backend tests)
