# Implementation Plan - Fix Vercel Deployment Error

The Vercel deployment is failing because the project contains over **66,000 files** in the `games/` directory. Vercel has a hard limit of **15,000 files** per deployment.

We will resolve this by zipping the Lua files into a single archive and updating the Flask app to serve from that archive.

## Proposed Changes

### 1. File Architecture
- **[NEW]** `games.zip`: A compressed archive containing all files from the `games/` directory.
- **[MODIFY]** `.vercelignore`: Add `games/` to prevent Vercel from trying to upload the 66k individual files.

### 2. Application Logic
- **[MODIFY] [app.py](file:///d:/webserver2/app.py)**:
    - Update `serve_lua` to open `games.zip` and read the requested file.
    - Update `check_availability` to check within the zip file.
    - Implement a small caching mechanism for the zip file handle for performance.

### 3. Automation (GitHub Actions)
- **[MODIFY] [.github/workflows/generate-index.yml](file:///d:/webserver2/.github/workflows/generate-index.yml)**:
    - Add a step to create/update `games.zip` after generating the index.
    - Include `games.zip` in the auto-commit.
- **[MODIFY] [.github/workflows/update-games.yml](file:///d:/webserver2/.github/workflows/update-games.yml)**:
    - Ensure `games.zip` is part of the committed patterns.

## User Review Required

> [!IMPORTANT]
> **Performance Impact**: Serving from a zip file is slightly slower than direct filesystem access, but given the files are small text files, the impact will be negligible (~1-5ms extra per request).
>
> **GitHub Repo Size**: The `games.zip` will be added to your repository (~18MB). This is necessary for Vercel to access the data without the 66k file overhead.

## Verification Plan

### Automated Tests
- Run a local test script to verify:
    - `app.py` successfully serves a sample Lua file from `games.zip`.
    - `app.py` correctly returns 404 for missing files in the zip.
    - `app.py` health check and other endpoints still work.

### Manual Verification
- Deploy to Vercel after the changes and verify the build completes successfully.
- Verify the admin panel still shows the games correctly.
