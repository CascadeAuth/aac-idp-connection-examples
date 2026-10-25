# Microsoft Entra ID: configure the application, then register the connection

What you end up with: an Entra application registration your people sign in
to with the AAC command-line tool, a security group whose members get AAC
roles, and the three values that complete [`entra.json`](entra.json).

## 1. Record the two directory values

In the Microsoft Entra admin center, App registrations → New registration:
single-tenant ("Accounts in this organizational directory only"), any name.
On its Overview page record the **Application (client) ID** (the
`ENTRA_APPLICATION_CLIENT_ID` placeholder) and the **Directory (tenant) ID**
(the `ENTRA_DIRECTORY_ID` placeholder, used twice: in the issuer URL and in
`binding_claims.tid`). Both are GUIDs; label them as you copy. The audience
must be the client ID GUID, never the application's display name.

## 2. Enable the sign-in flows

Under Authentication: set **Allow public client flows** to Yes (the device
flow). For the browser flow, add a platform **Mobile and desktop
applications** with the redirect URI exactly `http://127.0.0.1/callback`, no
port: Entra accepts any loopback port but compares the path.

## 3. Put the group into the ID token

Create a security group (Groups → New group, type Security), add the people
who should administer the tenant, and record the group's **Object ID**: that
is the `ENTRA_ADMIN_GROUP_OBJECT_ID` placeholder. On the application: Token
configuration → Add groups claim → Security groups, Group ID in the ID token.
Save. A token without a mapped group cannot obtain an AAC role.

## 4. Register and sign in

Fill the three placeholders in `entra.json`, then, with a tenant-admin
session or during the onboarding ceremony:

```bash
aac sso register-idp --profile prod --tenant-id '<TENANT_ID>' --file entra.json
aac sso login --profile prod --tenant-id '<TENANT_ID>' \
  --idp-url 'https://login.microsoftonline.com/<ENTRA_DIRECTORY_ID>/v2.0'
aac sso whoami --profile prod --output table
```

Use your exact directory issuer, never `common`, `organizations` or
`consumers`; AAC refuses those at registration. Both the device flow and
`--flow pkce` work with Entra.

## If something fails

| You see | Cause | Fix |
|---|---|---|
| `AADSTS700016` application not found | Audience is the display name, not the GUID | Step 1 |
| `AADSTS50011` redirect URI mismatch | Redirect URI without `/callback`, or wrong platform type | Step 2 |
| Device flow refused | Public client flows off | Step 2 |
| AAC STS: `invalid_grant` | Wrong directory id, wrong audience, or no mapped group in the token | Steps 1 and 3 |
| Sign-in blocked by security defaults (`AADSTS530035`) | The directory's own policy, before AAC sees a token | Entra ID → Properties → Manage security defaults, or complete MFA registration |
