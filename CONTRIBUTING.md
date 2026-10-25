# Keeping the samples exact

Each file here is copied from the AAC source repository after review, where a
test validates it against the control plane's registration schema. Changes
therefore start there, not here: a correction to a sample is a correction to
the canonical copy, and the reviewed copy lands here afterwards.

What a pull request here can do: fix a README sentence, add a placeholder
explanation, or report (in an issue) a sample that no longer registers. What
it cannot do: change a sample's shape or add a provider; those arrive with the
AAC release that supports them.

Rules every file follows:

* Placeholders are written `<UPPER_SNAKE_CASE>` and every one is explained in
  the directory's README.
* A sample never carries a real identifier, key or secret.
* A sample uses the provider's OpenID Connect discovery; none carries static
  keys.
