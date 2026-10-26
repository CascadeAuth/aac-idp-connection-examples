# Google Workspace: create the OAuth client, then register the connection

What you end up with: an OAuth client in your own Google Cloud project that
your people sign in to with the AAC command-line tool, your organization's
domain pinned on the connection so only your accounts can use it, and the
four values that complete [`google-workspace.json`](google-workspace.json).
This works for a Google Workspace subscription and for a Cloud Identity
organization (including the free edition): what matters is that your accounts
belong to a Google organization with a verified domain.

Google Workspace is the same identity provider as personal Google accounts.
AAC tells your organization's sign-ins apart by two facts in the token: the
OAuth client it was issued to (yours, from step 2) and the `hd` claim, your
organization's primary domain (step 3). A personal account, or an account from
another organization, is refused even when Google signs it in.

## 1. Pick or create the Google Cloud project

Open the [Google Cloud console](https://console.cloud.google.com/) signed in
as an administrator of your organization and select a project under your
organization (IAM & Admin → Settings shows the parent). A new project named,
for example, `aac-sign-in` is fine; no API needs enabling.

## 2. Configure the consent screen and create the Desktop client

APIs & Services → OAuth consent screen (Google auth platform → Branding on
newer consoles): user type **Internal**. Internal means only accounts of your
organization can sign in and Google asks for no app verification. Give the
app a name your people will recognize on the sign-in page, such as
`AAC command-line tool`, and your support email. Save.

APIs & Services → Credentials → Create credentials → **OAuth client ID**,
application type **Desktop app**, any name. Google shows the **Client ID**
and **Client secret**:

- The Client ID is the `GOOGLE_CLIENT_ID` placeholder.
- The Client secret is the `GOOGLE_CLIENT_SECRET` placeholder. Google
  requires it when the command-line tool redeems a sign-in, and documents
  it as non-confidential for Desktop clients; AAC stores it with the
  connection and hands it to the tool at sign-in.

No redirect URI is configured: Desktop clients accept the loopback address
and any port the tool picks.

## 3. Note your domain and the administrators

The `WORKSPACE_DOMAIN` placeholder is your organization's primary domain as
the Admin console shows it (Account → Domains), for example `acme.com`.
Google puts it in every token as the `hd` claim and AAC refuses tokens that
do not carry exactly this value.

Google tokens carry no groups, so AAC maps each administrator's
Google-verified email address to AAC roles. Put one `role_map` entry per
person; the `ADMIN_EMAIL` placeholder is the first. The person's identity in
AAC remains Google's stable account id, never the address; the address is
only the key that grants roles, so renaming or reassigning an address means
editing the connection.

## 4. Register and sign in

Fill the four placeholders in `google-workspace.json`, then, with a
tenant-admin session or during the onboarding ceremony:

```bash
aac sso register-idp --profile prod --tenant-id '<TENANT_ID>' --file google-workspace.json
aac sso login --profile prod --tenant-id '<TENANT_ID>' --idp google
aac sso whoami --profile prod --output table
```

Sign-in opens Google in your browser and returns to the tool on the loopback
address (the browser PKCE flow; Google's device flow does not serve Desktop
clients). `--idp google` selects your own Google Workspace connection; the
shared developer Google sign-in is picked only when the tenant has no Google
connection of its own.

## If something fails

| You see | Cause | Fix |
|---|---|---|
| Google: `Error 403: org_internal` or "This app is restricted to users within its organization" | The account is not in your organization | Sign in with an account from your domain |
| Google: `client_secret is missing` or `invalid_client` | The secret was left out of the file or copied wrong | Step 2; re-register with `aac sso replace-idp` |
| AAC STS: `invalid_grant` (tenant-binding claim `hd` mismatch) | The account belongs to another Google organization or is a personal account | Step 3 |
| AAC STS: `invalid_grant`, no roles derivable | The address is not in `role_map` | Step 3; compare the address exactly |
| Registration: `binding_claims 'hd' pin` required | `binding_claims` was removed | Keep `{"hd": "<WORKSPACE_DOMAIN>"}` |
