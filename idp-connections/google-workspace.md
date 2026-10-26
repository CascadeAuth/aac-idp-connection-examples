# Google Workspace: create the OAuth client, then register the connection

What you end up with: an OAuth client in your own Google Cloud project that
your people sign in to with the AAC command-line tool, your organization's
domain pinned on the connection so only your accounts can use it, and the
four values that complete [`google-workspace.json`](google-workspace.json).
This applies to a Google Workspace subscription and to a Cloud Identity
organization: what matters is that your accounts belong to a Google
organization with a verified domain.

Google Workspace is the same identity provider as personal Google accounts.
AAC tells your organization's sign-ins apart by two facts in the token: the
OAuth client it was issued to (yours, from step 2) and the `hd` claim, the
domain of the organization the account belongs to (step 3). With an Internal
consent screen Google itself turns away accounts from outside your
organization; AAC's `hd` check is the second layer, and it still holds if the
screen is ever switched to External.

## 1. Pick or create the Google Cloud project

Open the [Google Cloud console](https://console.cloud.google.com/) signed in
as an administrator of your organization and select a project under your
organization (the project picker lists the organization above its projects).
A new project named, for example, `aac-sign-in` is fine; no API needs enabling.

## 2. Configure the consent screen and create the Desktop client

APIs & Services → OAuth consent screen (on newer consoles: Google Auth
Platform → **Get started**, later **Audience**): user type **Internal**.
Internal means only accounts of your organization can sign in and Google asks
for no app verification; the option exists only when the project sits under
an organization. Under Branding, give the app a name your people will
recognize on the sign-in page, such as `AAC command-line tool`, and your
support email. Save.

APIs & Services → Credentials → Create credentials → **OAuth client ID**,
application type **Desktop app**, any name. Google shows the **Client ID**
and **Client secret**; copy the secret now, because newer consoles show it
only at creation (if it is lost, add a new secret on the client and use that):

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
Google puts the organization's domain into the ID token of every account that
belongs to an organization, as the `hd` claim, and AAC refuses tokens that do
not carry exactly this value.

Google tokens carry no groups, so AAC maps each administrator's
Google-verified email address to AAC roles. Put one `role_map` entry per
person; the `ADMIN_EMAIL` placeholder is the first. Write the address in
lowercase, as Google returns it, and use the person's primary address, not an
alias; the tool's default sign-in scope already requests the email. The
person's identity in AAC remains Google's stable account id, never the
address; the address is only the key that grants roles, so renaming or
reassigning an address means editing the connection.

## 4. Register and sign in

Fill the four placeholders in `google-workspace.json` (the filled file holds
the client secret; non-confidential by Google's definition, but keep it out
of public repositories anyway), then, with a tenant-admin session or during
the onboarding ceremony:

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
| Google: `Error 403: org_internal` (access blocked for accounts outside the organization) | The account is not in your organization | Sign in with an account from your domain |
| Google: `Error 400: redirect_uri_mismatch` | The OAuth client is a Web application, not a Desktop app | Step 2: create a Desktop app client |
| Google: `invalid_request` (`client_secret is missing`) | `public_client_secret` was left out of the file | Step 2; correct the connection with `aac sso replace-idp` |
| Google: `invalid_client` | The secret belongs to another client or was mistyped | Step 2; correct the connection with `aac sso replace-idp` |
| AAC STS: `invalid_grant` (tenant-binding claim `hd` mismatch) | The account belongs to another Google organization or is a personal account, or `WORKSPACE_DOMAIN` is mistyped or not the primary domain | Step 3 |
| AAC STS: `invalid_grant`, no roles derivable | The address is not a `role_map` key (lowercase, primary address) | Step 3 |
| AAC STS: `invalid_grant`, email is not verified | Google did not mark the account's address verified, or the token carries no email | Step 3; sign in with a managed account of the organization |
| Registration: `binding_claims 'hd' pin` required | `binding_claims` was removed | Keep `{"hd": "<WORKSPACE_DOMAIN>"}` |
