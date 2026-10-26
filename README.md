# AAC identity-provider connection examples

Ready-to-edit input files for the [Agent Authority Cloud](https://cascadeauth.com/)
(AAC) command-line tool. Each sample is complete except for the
`<PLACEHOLDER>` values you replace with your own identifiers.

| Directory | What the files are | Used by |
|---|---|---|
| [`idp-connections/`](idp-connections/) | One connection file per identity provider a tenant can bring, with a console walkthrough beside it: Microsoft Entra ID, Okta, Auth0, Google Workspace. | `aac sso register-idp --file <file>` |

How to use a sample:

```bash
curl -fsSLO https://raw.githubusercontent.com/CascadeAuth/aac-idp-connection-examples/main/idp-connections/okta.json
# replace every <PLACEHOLDER>, then
aac sso register-idp --profile prod --tenant-id '<TENANT_ID>' --file okta.json
```

The [AAC CLI guide](https://docs.cascadeauth.com/cli/) explains each
provider's console settings and the registration ceremony; the
[command reference](https://docs.cascadeauth.com/cli/reference/) lists every
field. Questions and corrections: open an issue here, or write to
support@cascadeauth.com.

The canonical copies of these files live beside the AAC source, where a test
validates each against the control plane's registration schema on every
change. Files here are reviewed copies of those; a difference between the two
is a defect, not a local customization.
