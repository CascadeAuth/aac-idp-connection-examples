# Okta: configure the application, then register the connection

What you end up with: an Okta application your people sign in to with the
AAC command-line tool, a group whose members get AAC roles, and the three
values that complete [`okta.json`](okta.json). Verified on 2026-10-25 with an
Okta trial org and AAC CLI 0.2.15.

## 1. Find your org URL

In the Admin Console the address bar reads `https://<org>-admin.okta.com/…`.
Your org URL is that host without `-admin`, for example
`https://trial-9948518.okta.com`. It is the `OKTA_ORG` placeholder's host and
the issuer AAC registers. Keep it exact: no trailing slash, no path.

## 2. Create the group

Directory → Groups → Add group. Name it, for example `aac-tenant-admins`,
and add the people who should administer the tenant. The name is the
`OKTA_ADMIN_GROUP_NAME` placeholder: Okta puts group names, not ids, into the
token, and AAC maps the name to roles.

## 3. Create the application

Applications → Applications → Create App Integration:

- Sign-in method **OIDC - OpenID Connect**, application type **Native
  Application**.
- Grant type: keep **Authorization Code** and tick **Device Authorization**
  (under Advanced). Leave Refresh Token off; AAC sessions do not refresh.
- Leave **Require Demonstrating Proof of Possession (DPoP)** unchecked; the
  CLI sends no DPoP proof.
- Leave the sign-in redirect URI as Okta's default. AAC signs in with the
  device flow, which uses no redirect. Okta requires a fixed port in a
  loopback redirect URI, and the CLI's browser flow picks its port at run
  time, so `--flow pkce` does not work with Okta.
- Controlled access: **Limit access to selected groups** and pick the group
  from step 2.

Save. The General tab shows the **Client ID** (it starts with `0oa`): that is
the `OKTA_CLIENT_ID` placeholder.

## 4. Put the group names into the ID token

Open the application's **Sign On** tab.

- In the **OpenID Connect ID Token** card, Issuer must be *Okta URL
  (https://<org>.okta.com)*, not Dynamic. New applications already have it.
- Scroll to the **Token claims** card and expand **Show legacy
  configuration**. In **Group Claims**, click Edit: Groups claim type
  **Filter**; Groups claim filter: name `groups`, operator **Matches regex**,
  value `.*` (or **Starts with** and a prefix such as `aac-`). Save.

Without this, the token carries no groups and AAC refuses the sign-in with
"no roles derivable".

## 5. Register and sign in

Fill the three placeholders in `okta.json`, then, with a tenant-admin
session or during the onboarding ceremony:

```bash
aac sso register-idp --profile prod --tenant-id '<TENANT_ID>' --file okta.json
aac sso login --profile prod --tenant-id '<TENANT_ID>' --idp-url 'https://<org>.okta.com'
aac sso whoami --profile prod --output table
```

The sign-in prints a code and an Okta activation link; open the link, confirm
the code, and the CLI caches the session. The CLI asks Okta for the `groups`
scope by itself. If you registered a Custom Authorization Server
(`https://<org>.okta.com/oauth2/<id>`) instead of the org URL, configure its
`groups` claim there and sign in with `--scope 'openid profile email'`.

## If something fails

| You see | Cause | Fix |
|---|---|---|
| Device code refused (`invalid_grant`, `unauthorized_client`) | Device Authorization grant off | Step 3 |
| Okta says you are not assigned to the application | Controlled access excludes you | Step 3, add your group |
| AAC STS: `invalid_grant`, no roles derivable | No `groups` claim, or `role_map` key differs from the group name | Step 4; compare the names exactly |
| Okta 400: redirect_uri must be a Login redirect URI | `--flow pkce` was used | Use the device flow |
| Registration: discovery failed | The `-admin` host or a trailing slash in the issuer | Step 1 |
