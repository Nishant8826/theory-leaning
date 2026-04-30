# 🔐 Authentication and Authorization

## 📌 Topic Name
Jenkins Security: SSO, RBAC, and Matrix-Based Authorization

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Logging into Jenkins with your company email and only seeing the jobs you are allowed to see.
*   **Expert**: Jenkins separates **Authentication** (AuthN - Who are you?) from **Authorization** (AuthZ - What can you do?). AuthN is typically delegated to enterprise IdPs via **OIDC (OpenID Connect) or SAML**, allowing Jenkins to remain stateless regarding user passwords. AuthZ is managed via the **Matrix-based Security** or **Role-Based Access Control (RBAC)** plugins. A Staff engineer architects this to prevent **Privilege Escalation** (where a user with 'Build' access modifies a job to grant themselves 'Admin' access) and ensures strict multi-tenant isolation.

## 🏗️ Mental Model
Think of Jenkins Security as a **Corporate Office Building**.
- **Authentication (SAML/OIDC)**: The security guard at the front door checking your ID badge. If you are not in the corporate directory, you cannot enter the lobby.
- **Authorization (RBAC)**: Your ID badge is swiped at the elevator. The elevator only allows you to go to the 3rd floor (Frontend Team). It denies access to the 5th floor (DevOps/Admin).
- **The Vulnerability**: If you can edit the blueprints of the building (edit a Jenkinsfile), you might be able to rewire the elevator to take you to the 5th floor.

## ⚡ Actual Behavior
- **Global vs Item Level**: Roles can be defined Globally (e.g., "Can view the dashboard") or at the Item level (e.g., "Can build jobs inside the `frontend/` folder").
- **Job/Configure is Root**: In Jenkins, granting a user `Job/Configure` access is essentially granting them Root/Admin access. If they can configure a job, they can inject malicious shell scripts or Groovy code that executes with the permissions of the Jenkins Controller.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **SecurityRealm**: The Java interface Jenkins uses for Authentication (e.g., `HudsonPrivateSecurityRealm` for local users, `SamlSecurityRealm` for Okta/Entra ID).
2.  **AuthorizationStrategy**: The Java interface for Authorization. Every time a user clicks a button, Stapler checks `Jenkins.instance.hasPermission()`.
3.  **Project-Based Matrix Authorization**: Stores an Access Control List (ACL) directly inside the `config.xml` of every folder or job.

## 🔁 Execution Flow (OIDC Login)
1.  **User**: Navigates to `jenkins.corp.com`.
2.  **Jenkins**: Detects no session cookie. Redirects browser to `login.microsoftonline.com` (Entra ID).
3.  **IdP**: User authenticates with MFA. Entra ID redirects back to Jenkins with a JWT/SAML token.
4.  **Jenkins AuthN**: Validates the JWT signature. Extracts username and group claims (e.g., `group: frontend-devs`).
5.  **Jenkins AuthZ**: User clicks "Build" on `App-A`.
6.  **Validation**: Jenkins checks if the role assigned to `frontend-devs` has the `Item/Build` permission on `App-A`. (Grants or Denies).

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **LDAP Thrashing**: If Jenkins uses an old LDAP integration without caching, every page load triggers a synchronous LDAP query to the domain controller, hanging the UI threads and creating massive network traffic.
- **Matrix Calculation**: In a system with 50,000 jobs and complex inherited ACLs, calculating a user's permissions when rendering the dashboard consumes significant CPU.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ USER ] --- (1. Login Request) ---> [ JENKINS (SecurityRealm) ]
                                          |
                               (2. Redirect to SSO)
                                          v
[ SSO PROVIDER ] --- (3. Valid Token + Groups) ---> [ JENKINS ]
   (Okta/Azure)                           |
                               (4. Check AuthorizationStrategy)
                                          v
                              +-------------------------+
                              | ROLE: 'frontend-dev'    |
                              | - Overall/Read          |
                              | - Job/Read (Folder A)   |
                              | - Job/Build (Folder A)  |
                              +-------------------------+
                                          |
                               (5. Grant UI Access)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```yaml
# JCasC snippet configuring OIDC and Matrix Authorization
jenkins:
  securityRealm:
    oic:
      clientId: "${OIDC_CLIENT_ID}"
      clientSecret: "${OIDC_CLIENT_SECRET}"
      wellKnownOpenIDConfigurationUrl: "https://login.microsoftonline.com/.../v2.0/.well-known/openid-configuration"
      groupsClaimFieldName: "roles"

  authorizationStrategy:
    projectMatrix:
      permissions:
        - "Overall/Administer:admin-group"
        - "Overall/Read:authenticated"
        # Danger: Never give configure rights to regular users
        # - "Job/Configure:dev-group" 
```

## 💥 Production Failures
1.  **The "Configure" Privilege Escalation**: An admin grants a junior developer `Job/Configure` access to a Sandbox job. The developer modifies the job to execute a system Groovy script that grants their user account `Overall/Administer`. They now own the Jenkins server. **Solution**: Use Jenkinsfiles (Configuration as Code) and disable UI-based job configuration entirely for non-admins.
2.  **The Anonymous Admin**: A misconfiguration in JCasC accidentally grants `Overall/Administer` to the `Anonymous` user. Anyone on the internet can now execute code.
3.  **IdP Lockout**: The SSO provider goes down, or the Client Secret expires. No one can log into Jenkins to fix the configuration. **Solution**: Always maintain an emergency "Local Admin" backdoor account or rely on JCasC to push fixes via Git.

## 🧪 Real-time Q&A
*   **Q**: What is the difference between `Job/Build` and `Job/Configure`?
*   **A**: `Build` allows a user to click the "Build Now" button. `Configure` allows them to change *what* the build does. In CI/CD, configuring a job is equivalent to root access.
*   **Q**: How do I secure Jenkinsfiles from malicious developers?
*   **A**: You cannot secure a Jenkinsfile if the developer has push access to the repository. If they can edit the Jenkinsfile, they can execute code on your Jenkins agents. Security must be enforced at the SCM layer (e.g., Pull Request approvals required before merging to `main` where the production Jenkinsfile runs).

## ⚠️ Edge Cases
*   **API Tokens**: Users can generate API tokens that bypass SSO MFA. If a developer's API token is leaked, an attacker has permanent access to Jenkins until the token is manually revoked.

## 🏢 Best Practices
1.  **SSO Only**: Disable local user database. Use SAML/OIDC and rely on your company's IdP for MFA, lifecycle management, and offboarding.
2.  **Folders for Multi-Tenancy**: Group jobs into Folders (e.g., `/Frontend`, `/Backend`). Apply Role-Based Access Control to the Folder, not individual jobs, to maintain sanity.
3.  **Read-Only UI**: Transition the organization to GitOps. Developers should not configure jobs in the UI; they should commit Jenkinsfiles. The UI should be Read/Build only.

## ⚖️ Trade-offs
*   **Granular ACLs vs Maintainability**: Defining permissions down to the individual job level provides perfect least-privilege, but becomes impossible to audit or maintain. Folder-level RBAC is the industry standard compromise.

## 💼 Interview Q&A
*   **Q**: A security audit reveals that 50 developers have `Job/Configure` access in Jenkins. The security team demands this be revoked, but developers say they need it to modify their build steps. How do you resolve this?
*   **A**: I would transition the teams from "Freestyle" jobs to **Pipeline (Jenkinsfile)** jobs. By defining the build steps in a `Jenkinsfile` stored in their Git repository, developers can modify their build process by opening a Pull Request. We can then revoke `Job/Configure` access in the Jenkins UI, reducing the Jenkins attack surface, while maintaining developer velocity and adding SCM peer-review security to pipeline changes.

## 🧩 Practice Problems
1.  Review the Matrix Authorization configuration in your Jenkins instance. Identify exactly which group has the `Overall/Administer` permission.
2.  Create a test folder and apply a local matrix authorization strategy that denies `Job/Read` to the `authenticated` group, but grants it to a specific user. Log in as a different user and verify the folder disappears from the dashboard.

---
Prev: [05_Network_Latency_Impact.md](../Distributed/05_Network_Latency_Impact.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [02_Credentials_Management.md](../Security/02_Credentials_Management.md)
---
