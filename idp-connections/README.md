# Identity-provider connection samples

Each file is a complete input for `aac sso register-idp --file`: the
connection between one AAC tenant and the identity provider its people sign
in with. Copy the file for your provider, replace every `<PLACEHOLDER>` with
the value from your provider's console, and register it. The
[CLI guide](https://docs.cascadeauth.com/cli/) walks through each provider's
console settings; `aac sso register-idp --help` lists every field.

| File | Provider | Placeholders |
|---|---|---|
| `entra.json` | Microsoft Entra ID | `ENTRA_DIRECTORY_ID` (Directory (tenant) ID), `ENTRA_APPLICATION_CLIENT_ID` (Application (client) ID), `ENTRA_ADMIN_GROUP_OBJECT_ID` (Object ID of the security group holding your AAC administrators) |
| `okta.json` | Okta (Org Authorization Server) | `OKTA_ORG` (your Okta subdomain), `OKTA_CLIENT_ID` (Client ID of the Native application), `OKTA_ADMIN_GROUP_NAME` (name of the Okta group holding your AAC administrators) |

Rules that hold for every file:

- The placeholders are the only values to change. Every other field is the
  shape AAC expects for that provider.
- `role_map` grants AAC roles to the groups in the identity token. The four
  roles are `tenant-admin`, `key-admin`, `policy-admin` and `auditor-read`;
  a person with none of the mapped groups cannot sign in.
- Do not add `jwks_static`. AAC performs OpenID Connect discovery on the
  issuer to obtain signing keys and sign-in endpoints; static keys are a local
  test facility and disable interactive sign-in.

These files are reviewed copies of the canonical ones kept beside the AAC
source, where a test validates each against the control plane's registration
schema. See [CONTRIBUTING.md](../CONTRIBUTING.md) before proposing a change.
