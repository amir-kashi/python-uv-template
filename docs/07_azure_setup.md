# Azure Infrastructure Setup for Container Deployment

This guide explains how to set up the Azure infrastructure required to deploy a containerized application via CI/CD. The architecture consists of:

- **Azure Container Registry (ACR)** – to store Docker images
- **Azure Web App for Containers** – to run the containerized application
- **Managed Identity + RBAC** – to allow the Web App to securely pull images from ACR

This setup works well with CI/CD pipelines (e.g., GitHub Actions) that build and push Docker images to ACR and then deploy them to the Web App.

---

# Architecture Overview

```

GitHub CI/CD
│
│  push Docker image
▼
Azure Container Registry (ACR)
│
│  pull image
▼
Azure Web App for Containers
│
▼
Public HTTPS Endpoint

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

# 2. Create Web App for Containers

Azure Web App for Containers runs Docker containers without needing Kubernetes.

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

During Web App creation, configure the container source.

Choose:

| Setting | Value |
|------|------|
| Image Source | Azure Container Registry |
| Registry | Select your ACR |
| Image | Your repository name |
| Tag | `latest` (can be updated via CI/CD later) |

Complete the creation.

---

# 4. Enable Managed Identity for Web App

Instead of storing registry credentials in the Web App, use **Managed Identity**.

### Enable Identity

1. Open the **Web App**
2. Navigate to **Identity**
3. Under **System Assigned**, enable **On**
4. Click **Save**

Azure will create a managed identity for the application.

---

# 5. Grant Web App Permission to Pull Images

Now grant the Web App permission to pull images from ACR.

### Steps

1. Go to **Azure Container Registry**
2. Select **Access Control (IAM)**
3. Click **Add Role Assignment**

Configure:

| Field | Value |
|------|------|
| Role | **AcrPull** |
| Assign access to | Managed Identity |
| Identity | Select your Web App |

Click **Save**.

Now the Web App can securely pull images from ACR.

---

# 6. Configure Application Settings

Your container may require environment variables.

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

You may also add custom variables, for example:

```
WEBSITES_PORT=8000
ENVIRONMENT=production
```

`WEBSITES_PORT` must match the port your container listens on.

---

# 7. Verify Container Deployment

Before deployment, ensure the required GitHub repository secrets are configured, especially the ACR and Azure secrets listed under **CD Secrets** in [CI/CD](06_cicd.md) setup. 

Once a container image exists in ACR:

1. Go to **Web App**
2. Navigate to **Deployment Center**
3. Confirm container image and tag
4. Restart the Web App

Then open:

```
https://<web-app-name>.azurewebsites.net
```

If the application loads, the infrastructure is correctly configured.

---

# Final Infrastructure

Your Azure resources should look like:

```
Resource Group
├── Container Registry (ACR)
└── App Service
└── Web App (Linux Container)
```

The Web App pulls images from ACR using Managed Identity and serves the application over HTTPS.
