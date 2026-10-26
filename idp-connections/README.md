# Identity-provider connection samples

Each file is a complete input for `aac sso register-idp --file`: the
connection between one AAC tenant and the identity provider its people sign
in with. Copy the file for your provider, replace every `<PLACEHOLDER>` with
the value from your provider's console, and register it. Each provider's
walkthrough page (next to its file) shows the console settings that produce
those values; the [CLI guide](https://docs.cascadeauth.com/cli/guide/) covers
the registration ceremony and `aac sso register-idp --help` lists every field.

| File | Provider | Console walkthrough | Placeholders |
|---|---|---|---|
| `entra.json` | Microsoft Entra ID | [entra.md](entra.md) | `ENTRA_DIRECTORY_ID` (Directory (tenant) ID), `ENTRA_APPLICATION_CLIENT_ID` (Application (client) ID), `ENTRA_ADMIN_GROUP_OBJECT_ID` (Object ID of the security group holding your AAC administrators) |
| `okta.json` | Okta (Org Authorization Server) | [okta.md](okta.md) | `OKTA_ORG` (your Okta subdomain), `OKTA_CLIENT_ID` (Client ID of the Native application), `OKTA_ADMIN_GROUP_NAME` (name of the Okta group holding your AAC administrators) |
| `auth0.json` | Auth0 | [auth0.md](auth0.md) | `AUTH0_DOMAIN` (the application's Domain, for example `acme.us.auth0.com`, or your custom domain; the issuer keeps the trailing slash Auth0 declares), `AUTH0_CLIENT_ID` (Client ID of the Native application), `AUTH0_ADMIN_ROLE_NAME` (name of the Auth0 role held by your AAC administrators; a post-login Action copies role names into the `https://cascadeauth.com/roles` claim) |
| `google-workspace.json` | Google Workspace (or a Cloud Identity organization) | [google-workspace.md](google-workspace.md) | `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` (the Desktop-app OAuth client in your own Google Cloud project; Google's token endpoint requires the secret even from this public client and documents it as non-confidential), `WORKSPACE_DOMAIN` (your organization's primary domain, the `hd` claim Google puts in your people's tokens), `ADMIN_EMAIL` (the Google-verified address of an AAC administrator; add one entry per person) |

Rules that hold for every file:

- The placeholders are the only values to change; the one structural edit is
  adding `role_map` entries (Google Workspace: one per administrator). Every
  other field is the shape AAC expects for that provider.
- `role_map` grants AAC roles to the groups in the identity token. The four
  roles are `tenant-admin`, `key-admin`, `policy-admin` and `auditor-read`;
  a person with none of the mapped groups cannot sign in. Google tokens
  carry no groups, so the Google Workspace file keys roles by each person's
  Google-verified email address instead, under the organization-domain pin.
- Do not add `jwks_static`. AAC performs OpenID Connect discovery on the
  issuer to obtain signing keys and sign-in endpoints; static keys are a local
  test facility and disable interactive sign-in.

These files are reviewed copies of the canonical ones kept beside the AAC
source, where a test validates each against the control plane's registration
schema. See [CONTRIBUTING.md](../CONTRIBUTING.md) before proposing a change.
