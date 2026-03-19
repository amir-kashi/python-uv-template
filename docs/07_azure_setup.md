# Azure Infrastructure Setup for Container Deployment

This guide explains how to set up the Azure infrastructure required to deploy a containerized application via CI/CD. The architecture consists of:

- **Azure Container Registry (ACR)** – to store Docker images
- **Two Azure Web Apps for Containers** – one for Streamlit UI and one for FastAPI API
- **Managed Identity + RBAC** – to allow each Web App to securely pull images from ACR

This setup works well with CI/CD pipelines (e.g., GitHub Actions) that build and push Docker images to ACR and then deploy them to two Web Apps.

---

# Architecture Overview

```

GitHub CI/CD
│
│  push Docker images
▼
Azure Container Registry (ACR)
│
├── pull Streamlit image ──► Azure Web App (Streamlit)
│
└── pull FastAPI image ─────► Azure Web App (FastAPI)

```

Key advantages:

- Fully managed PaaS
- No Kubernetes required
- Secure container access using Managed Identity
- Versioned deployments using container tags

---

# 1. Create Azure Container Registry

Azure Container Registry (ACR) stores Docker images built by your CI pipeline.

### Steps

1. Go to **Azure Portal**
2. Search for **Container Registries**
3. Click **Create**

Fill the form:

| Setting | Value |
|------|------|
| Subscription | Your subscription |
| Resource Group | Create or select existing |
| Registry Name | Unique name (e.g., `myprojectacr`) |
| Region | Same region as Web App |
| SKU | **Basic** (sufficient for most projects) |

Click **Review + Create** → **Create**

---

### Enable Admin Access (Optional)

If your CI pipeline authenticates using username/password:

1. Open the registry
2. Go to **Access keys**
3. Enable **Admin user**

You will see:

```
Login server: myprojectacr.azurecr.io
Username
Password
```

**Important:** Save these values (`ACR_LOGIN_SERVER`, `ACR_USERNAME`, and `ACR_PASSWORD`) as GitHub Action secrets in your repository settings (see **CD Secrets** section in [06_cicd.md](06_cicd.md) for detailed instructions on all required secrets for deployment). After adding the secrets, run the CI/CD pipeline for the first time to build and push the Docker image to your Azure Container Registry. This initial image push is required before proceeding to the next steps, as your Web App for Containers will need the image to be available in the ACR.

---

# 2. Create Two Web Apps for Containers

Azure Web App for Containers runs Docker containers without needing Kubernetes.
Create one Web App for Streamlit and one Web App for FastAPI.

### Steps

1. Go to **Azure Portal**
2. Search **App Services**
3. Click **Create**

Configuration:

| Setting | Value |
|------|------|
| Publish | Docker Container |
| Operating System | Linux |
| Region | Same as ACR |

---

### Configure App Service Plan

Create a new plan.

Recommended tiers:

| Environment | Suggested Tier |
|-------------|---------------|
| Development | B1 |
| Production | P1v3 |

Avoid **Free tier** for containers.

---

# 3. Configure Container Settings

During each Web App creation, configure the container source.

Choose:

| Setting | Value |
|------|------|
| Image Source | Azure Container Registry |
| Registry | Select your ACR |
| Image | Streamlit image for Streamlit app, FastAPI image for FastAPI app |
| Tag | `latest` (can be updated via CI/CD later) |

Complete the creation.

---

# 4. Enable Managed Identity for Both Web Apps

Instead of storing registry credentials in each Web App, use **Managed Identity**.

### Enable Identity

1. Open the **Web App**
2. Navigate to **Identity**
3. Under **System Assigned**, enable **On**
4. Click **Save**

Azure will create a managed identity for the application.
Repeat for both Web Apps.

---

# 5. Grant Both Web Apps Permission to Pull Images

Now grant each Web App permission to pull images from ACR.

### Steps

1. Go to **Azure Container Registry**
2. Select **Access Control (IAM)**
3. Click **Add Role Assignment**

Configure:

| Field | Value |
|------|------|
| Role | **AcrPull** |
| Assign access to | Managed Identity |
| Identity | Select each Web App (Streamlit and FastAPI) |

Click **Save**.

Now both Web Apps can securely pull images from ACR.

---

# 6. Configure Application Settings

Each container may require environment variables.

Open:

```
Web App → Settings → Environment Variables
```

You may notice that these variables are injected as environment variables into the container at runtime:

```
DOCKER_REGISTRY_SERVER_PASSWORD
DOCKER_REGISTRY_SERVER_USERNAME
DOCKER_REGISTRY_SERVER_URL
```

For the Streamlit Web App, set:

```
WEBSITES_PORT=8501
ENVIRONMENT=production
```

For the FastAPI Web App, set:

```
WEBSITES_PORT=8000
ENVIRONMENT=production
```

`WEBSITES_PORT` must match the port each container listens on.

---

# 7. Verify Container Deployment

Before deployment, ensure the required GitHub repository secrets are configured, especially the ACR and Azure secrets listed under **CD Secrets** in [CI/CD](06_cicd.md) setup.

Once container images exist in ACR:

1. Go to **Streamlit Web App**
2. Navigate to **Deployment Center**
3. Confirm Streamlit image and tag
4. Restart the Streamlit Web App
5. Repeat for the **FastAPI Web App**

Then open:

```
https://<streamlit-web-app-name>.azurewebsites.net

and

https://<fastapi-web-app-name>.azurewebsites.net
```

If the application loads, the infrastructure is correctly configured.

---

# Final Infrastructure

Your Azure resources should look like:

```
Resource Group
├── Container Registry (ACR)
├── App Service Plan
├── Web App (Linux Container - Streamlit)
└── Web App (Linux Container - FastAPI)
```

Both Web Apps pull images from ACR using Managed Identity and serve the application over HTTPS.
