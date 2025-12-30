# DevOps Dashboard

**Category:** Web
**Difficulty:** Easy
**Points:** 100
**Author:** CTF Admin

---

## Backstory

TechStart Inc. is a fast-growing startup that just closed their Series A funding round. With investors breathing down their necks, the development team had to rush their internal DevOps dashboard to production before the big demo.

Jake, the junior developer, was tasked with deploying the dashboard. In his rush to meet the deadline, he may have cut a few corners on the deployment configuration. The CTO is confident their admin panel is secure since it requires authentication.

Your task: As part of a penetration test engagement, you've been given access to their DevOps dashboard. Find a way to access the admin panel and retrieve the sensitive API key.

---

## Challenge Info

**URL:** `http://localhost:8080`

**Objective:** Retrieve the flag from the admin panel.

---

## Hints

<details>
<summary>Hint 1 (Free)</summary>
Developers sometimes forget to clean up after themselves when deploying...
</details>

<details>
<summary>Hint 2 (-25 points)</summary>
What version control system do most developers use? Is it accessible?
</details>

<details>
<summary>Hint 3 (-50 points)</summary>
Try accessing /.git/ on the web server. Tools like git-dumper can help reconstruct the repository.
</details>

---

## Deployment

```bash
cd challenge
docker-compose up --build -d
```

The challenge will be available at `http://localhost:8080`

To stop:
```bash
docker-compose down
```

---

## Files Provided to Players

- Challenge URL only (no source code)
