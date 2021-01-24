# Changelog
All notable changes in **python-transip** are documented below.

## [Unreleased]

## [0.4.0] (2021-01-24)
### Added
- This `CHANGELOG.md` file to be able to list all notable changes for each version of **python-transip**.
- The `transip.TransIP.api_test` service to allow calling the test resource to make sure everything is working.
- The option to list all invoices attached to your TransIP account from the `transip.TransIP.invoices` service.
- The option to save an invoice as PDF file from `transip.v6.objects.Invoice` object.
- The option to list all products available in TransIP from the `transip.TransIP.products` service.
- The option to update a single SSH key from `transip.v6.objects.SshKey` object.
- The option to update the content of a single DNS record from the `transip.v6.objects.Domain.dns` service, as well as from the `transip.v6.objects.DnsEntry` object.
- The option to replace all existing DNS records of a single domain at once from the `transip.v6.objects.Domain.dns` service.

[Unreleased]: https://github.com/roaldnefs/python-transip/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/roaldnefs/python-transip/compare/v0.3.0...v0.4.0
