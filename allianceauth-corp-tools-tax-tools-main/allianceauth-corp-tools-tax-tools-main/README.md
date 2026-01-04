
# Corp Tools - Tax Tools

## Installation

Requires AllianceAuth - CorpTools and AllianceAuth - Invoice Manager

1. Install from pip `pip install allianceauth-corptools-tax-tools`
2. Add `'taxtools'` to INSTALLED_APPS in local.py
3. Run Migrations, collectstatic
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```
4. `python manage.py tax_defaults`
5. Configure taxes as wanted
    Add Alliances and/or Corporations and Taxes to `admin/taxtools/corptaxconfiguration/`
6. `python manage.py tax_explain`. Read it to see if you are happy.
7. Run `Send Invoices to all Corps!` on `admin/django_celery_beat/periodictask/` to generate a base level tax. If you dont want to back-charge people you can delete them.

## Features

### Tax Configuration Options

The tax system now supports **both Alliance-level and Corporation-level filtering**:

- **Included Alliances**: Tax all corporations within specified alliances
- **Included Corporations**: Tax specific corporations regardless of alliance membership
- **Combined Filtering**: You can use both filters together - the system will tax corporations that match either criteria
- **Exempted Corporations**: Exclude specific corporations from taxation even if they match alliance/corp filters

### Tax Types Supported

1. **Character Ratting Taxes** - Tax bounty payments from ratting activities
   - Supports ESS (Encounter Surveillance System) calculations
   - Region-based filtering available
   
2. **Character Wallet Taxes** - Tax specific wallet transaction types
   - Configure by transaction type (bounty_prizes, corporate_reward_payout, etc.)
   - Filter by source corporation
   
3. **Corporate Wallet Taxes** - Tax corporation-level transactions
   - Similar to character taxes but at corp level
   
4. **Per-Member Taxes** - Fixed ISK amount per main character
   - Configure by user state (Member, Ally, etc.)
   
5. **Structure Service Taxes** - Tax based on active structure services
   - Filter by region and structure type

### How to Configure

1. Go to Admin → Taxtools → Config: Corporate
2. Select your tax configuration
3. Under **Included Alliances**: Add any alliances you want to tax
4. Under **Included Corporations**: Add any specific corporations you want to tax
5. Under **Exempted Corps**: Add any corporations that should be excluded
6. Select which tax types to apply (Character Ratting, Character Wallet, Corporate Wallet, etc.)

**Note**: If neither alliances nor corporations are specified, the system will process ALL corporations with tracked data.

## Permissions

Category | Perm | Admin Site | Auth Site
--- | --- | --- | ---
Tax Tools | access_tax_tools_ui | ❌ | ✅

## Contributing

Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
