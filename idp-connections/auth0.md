# Auth0: configure the application, then register the connection

What you end up with: an Auth0 application your people sign in to with the
AAC command-line tool, an Auth0 role whose holders get AAC roles, a post-login
Action that puts the role names into the ID token, and the three values that
complete [`auth0.json`](auth0.json). Verified on 2026-10-25 with a free Auth0
tenant and AAC CLI 0.2.16.

## 1. Create the application

Applications → Applications → Create Application: any name, application type
**Native**. On its Settings tab record the **Domain** (for example
`acme.us.auth0.com`; a custom domain works too) and the **Client ID**.

- The Domain is the `AUTH0_DOMAIN` placeholder. The issuer AAC registers is
  `https://<AUTH0_DOMAIN>/` with the trailing slash, exactly as Auth0's
  discovery document declares it.
- The Client ID is the `AUTH0_CLIENT_ID` placeholder.

Scroll to Advanced Settings → Grant Types and tick **Device Code** (keep
Authorization Code; Refresh Token is not needed, AAC sessions do not
refresh). Under the OAuth tab, **OIDC Conformant** stays on. Save. Leave
Allowed Callback URLs empty: AAC signs in with the device flow, which uses no
redirect. Auth0 matches callback URLs exactly and the CLI's browser flow picks
its port at run time, so `--flow pkce` does not work with Auth0.

## 2. Create the role and assign it

User Management → Roles → Create Role. Name it, for example
`aac-tenant-admins`, and add the people who should administer the tenant
(Users tab → Add Users). The role name is the `AUTH0_ADMIN_ROLE_NAME`
placeholder: AAC maps the name to AAC roles.

## 3. Put the role names into the ID token

Auth0 ID tokens carry no groups or roles by default. Actions → Library →
Build from scratch: any name, trigger **Login / Post Login**, runtime Node.
Replace the code with:

```js
exports.onExecutePostLogin = async (event, api) => {
  if (event.authorization) {
    api.idToken.setCustomClaim("https://cascadeauth.com/roles", event.authorization.roles);
  }
};
```

Deploy it, then Actions → Triggers → post-login: drag the Action into the
flow and Apply. The claim name is the sample's `groups_claim`; any other
namespace works as long as both say the same thing (Auth0 rejects its own
domains as namespaces). Without this step the token carries no roles and AAC
refuses the sign-in with "no roles derivable".

## 4. Register and sign in

Fill the three placeholders in `auth0.json`, then, with a tenant-admin
session or during the onboarding ceremony:

```bash
aac sso register-idp --profile prod --tenant-id '<TENANT_ID>' --file auth0.json
aac sso login --profile prod --tenant-id '<TENANT_ID>' --idp-url 'https://<AUTH0_DOMAIN>/'
aac sso whoami --profile prod --output table
```

The sign-in prints a code and an Auth0 activation link; open the link,
confirm the code, sign in, and the CLI caches the session. Approve promptly:
Auth0's device code expires after a few minutes by default (a tenant setting
under Settings → Advanced → Device User Code). `--idp-url` accepts the issuer
with or without its trailing slash.

## If something fails

| You see | Cause | Fix |
|---|---|---|
| Device code refused (`unauthorized_client`) | Device Code grant off | Step 1 |
| AAC STS: `invalid_grant`, no roles derivable | The Action is not in the Login flow, the person holds no role, or `role_map` key differs from the role name | Steps 2 and 3; compare the names exactly |
| Registration: discovery failed or issuer mismatch | Issuer without the trailing slash, or the wrong domain | Step 1 |
| Auth0 403: Callback URL mismatch | `--flow pkce` was used | Use the device flow |
| CLI: the device code expired | The code was approved too late | Run the sign-in again and approve at once |
