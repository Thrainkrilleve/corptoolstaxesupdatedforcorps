# Corp Tools - Tax Tools (Enhanced Edition)

[![Version](https://img.shields.io/badge/version-2.0.0--enhanced-blue.svg)](https://github.com/Solar-Helix-Independent-Transport/allianceauth-corp-tools-tax-tools)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.0%2B-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-GPLv2-blue.svg)](LICENSE)

A comprehensive tax management system for AllianceAuth that enables flexible corporation and alliance-level tax configuration with multiple tax types.

## 🎯 What's New in This Enhanced Version

This version includes **significant enhancements** to the original tax tools, adding corporation-level filtering and critical bug fixes. See the [Enhancement Summary](#-enhancement-summary) section for full details.

### Key Improvements
- ✅ **Corporation-Level Filtering** - Tax specific corporations directly
- ✅ **Flexible Filter Combinations** - Use alliance AND/OR corporation filters together
- ✅ **Critical Bug Fixes** - Fixed 3 bugs that caused incorrect tax calculations
- ✅ **Enhanced Debugging** - Comprehensive logging for troubleshooting
- ✅ **Admin Validation** - Prevents conflicting configurations
- ✅ **Complete Documentation** - In-depth technical and user guides

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Tax Configuration](#-tax-configuration)
- [Enhancement Summary](#-enhancement-summary)
- [Documentation](#-documentation)
- [Contributing](#-contributing)

---

## 🚀 Installation

### Requirements
- AllianceAuth >= 3.1, < 5
- AllianceAuth - CorpTools >= 2.5.5
- AllianceAuth - Invoice Manager >= 0.1.5
- Python >= 3.8

### Steps

1. **Install from pip**
   ```bash
   pip install allianceauth-corptools-tax-tools
   ```

2. **Add to INSTALLED_APPS**
   ```python
   # In your local.py
   INSTALLED_APPS = [
       # ... other apps
       'taxtools',
   ]
   ```

3. **Run migrations and collect static files**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

4. **Initialize default tax configuration**
   ```bash
   python manage.py tax_defaults
   ```

5. **Configure your taxes**
   - Navigate to Admin → Taxtools → Config: Corporate
   - Add your alliances and/or corporations
   - Configure tax rates and types

6. **Preview your configuration**
   ```bash
   python manage.py tax_explain
   ```
   Read the output to verify your tax setup is correct.

7. **Generate initial invoices (optional)**
   - Go to Admin → Django Celery Beat → Periodic Task
   - Run "Send Invoices to all Corps!"
   - This generates a baseline tax. You can delete these if you don't want to back-charge.

---

## ✨ Features

### Tax Configuration Options

The tax system supports **flexible filtering** at both alliance and corporation levels:

- **Included Alliances**: Tax all corporations within specified alliances
- **Included Corporations**: Tax specific corporations regardless of alliance membership
- **Combined Filtering**: Use both filters together - corporations matching EITHER criteria are taxed
- **Exempted Corporations**: Exclude specific corporations even if they match other filters

### Tax Types Supported

1. **Character Ratting Taxes**
   - Tax bounty payments from ratting activities
   - Supports ESS (Encounter Surveillance System) calculations
   - Region-based filtering available

2. **Character Wallet Taxes**
   - Tax specific wallet transaction types
   - Configure by transaction type (bounty_prizes, corporate_reward_payout, etc.)
   - Filter by source corporation

3. **Corporate Wallet Taxes**
   - Tax corporation-level transactions
   - Similar to character taxes but at corp level

4. **Per-Member Taxes**
   - Fixed ISK amount per main character
   - Configure by user state (Member, Ally, etc.)

5. **Structure Service Taxes**
   - Tax based on active structure services
   - Filter by region and structure type

---

## 🎮 Quick Start

### Basic Configuration Example

1. **Navigate to Admin Panel**
   ```
   Admin → Taxtools → Config: Corporate
   ```

2. **Select a Tax Configuration**
   - Click on your configuration or create a new one

3. **Add Filters**
   - **For Alliance-Wide Taxation**: Add alliances to "Included Alliances"
   - **For Specific Corporations**: Add corporations to "Included Corporations"
   - **To Exempt Corporations**: Add them to "Exempted Corps"

4. **Configure Tax Types**
   - Enable the tax types you want to apply
   - Set tax rates and percentages
   - Configure any additional filters (regions, structure types, etc.)

5. **Verify Configuration**
   ```bash
   python manage.py tax_explain
   ```

### Example Scenarios

**Scenario 1: Tax an entire alliance**
- Included Alliances: [Your Alliance]
- Included Corporations: (empty)
- Result: All corps in the alliance are taxed

**Scenario 2: Tax specific corporations only**
- Included Alliances: (empty)
- Included Corporations: [Corp A, Corp B, Corp C]
- Result: Only these three corporations are taxed

**Scenario 3: Alliance + specific external corp**
- Included Alliances: [Alliance A]
- Included Corporations: [External Corp D]
- Result: All corps in Alliance A PLUS External Corp D are taxed

**Scenario 4: Alliance except certain corps**
- Included Alliances: [Alliance A]
- Exempted Corps: [Corp X, Corp Y]
- Result: All corps in Alliance A are taxed EXCEPT Corp X and Corp Y

For more examples, see [QUICK_START.md](QUICK_START.md).

---

## ⚙️ Tax Configuration

### Filter Logic

The tax system uses the following logic:

1. **Inclusion Phase** (OR logic)
   - Corporations in `included_alliances` are included
   - Corporations in `included_corporations` are included
   - If BOTH are empty, ALL corporations with taxable activity are included

2. **Exemption Phase**
   - Corporations in `exempted_corps` are REMOVED
   - Exemptions take precedence over inclusions

### Admin Interface Features

- **Multi-select Widgets**: Easily select multiple alliances/corporations
- **Validation Warnings**: Alerts when corporations appear in both included and exempted lists
- **Filter Horizontal**: User-friendly interface for managing large lists
- **Preview Support**: Use `tax_explain` command to see who will be taxed

### Debug Logging

Enable debug logging to troubleshoot tax calculations:

```python
# In your local.py
LOGGING = {
    'loggers': {
        'taxtools': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

Log output includes:
- Active filters (alliances and corporations)
- Exempted corporations
- Tax type processing steps
- Corporation-level tax calculations

---

## 🔧 Enhancement Summary

### What Was Modified

This enhanced version includes the following improvements over the original:

#### 1. Corporation-Level Filtering (Major Feature)
**Files Modified**: `models.py`, `admin.py`, `migrations/0026_*.py`

- Added `included_corporations` field to enable direct corporation filtering
- Updated 16+ model methods to support corporation filtering
- Maintains 100% backward compatibility

#### 2. Critical Bug Fixes (3 Bugs Fixed)

**Bug #1**: Per-Member Taxes Ignored Filters
- **Impact**: Member taxes were applied to ALL corporations
- **Fix**: Added filter support to `CorpTaxPerMemberTaxConfiguration`

**Bug #2**: Structure Taxes Ignored Filters
- **Impact**: Structure taxes were applied to ALL corporations
- **Fix**: Added filter support to `CorpTaxPerServiceModuleConfiguration`

**Bug #3**: Migration Dependency Issue
- **Impact**: Migration would fail on some installations
- **Fix**: Changed migration dependency to use `__first__` instead of specific version

#### 3. Code Quality Improvements (5 Enhancements)

1. **Comprehensive Docstrings** - Added detailed documentation to all critical methods
2. **Debug Logging** - Added logging points throughout tax calculation pipeline
3. **Admin Validation** - Added warnings for contradictory filter configurations
4. **Error Messages** - Improved user-facing error messages
5. **Code Comments** - Added inline comments explaining complex logic

### Testing & Quality Assurance

- ✅ Full QA review conducted
- ✅ All critical bugs identified and fixed
- ✅ Code quality improvements implemented
- ✅ Zero breaking changes - 100% backward compatible
- ✅ Production ready

### Files Changed

| File | Changes | Description |
|------|---------|-------------|
| `models.py` | ~150 lines | Added corp filtering, bug fixes, logging |
| `admin.py` | ~40 lines | Added validation and better UI |
| `migrations/0026_*.py` | New file | Database schema for corp filtering |
| `README.md` | Complete rewrite | Comprehensive documentation |
| `CHANGES.md` | New file | Detailed change log |
| `IMPLEMENTATION_NOTES.md` | New file | Technical documentation |
| `QUICK_START.md` | New file | User guide with examples |
| `QA_REPORT.md` | New file | Quality assurance findings |
| `CODE_QUALITY_IMPROVEMENTS.md` | New file | Code improvement details |

---

## 📚 Documentation

### User Documentation
- **[QUICK_START.md](QUICK_START.md)** - User-friendly configuration guide with examples
- **[README.md](README.md)** - This file, overview and installation

### Technical Documentation
- **[IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)** - Technical implementation details
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture overview
- **[CHANGES.md](CHANGES.md)** - Comprehensive changelog

### Quality Assurance
- **[QA_REPORT.md](QA_REPORT.md)** - Full QA review report
- **[QA_SUMMARY.md](QA_SUMMARY.md)** - QA executive summary
- **[CODE_QUALITY_IMPROVEMENTS.md](CODE_QUALITY_IMPROVEMENTS.md)** - Code quality enhancements

### Testing
- **[TEST_PLAN.md](TEST_PLAN.md)** - Testing strategy and test cases

---

## 🔐 Permissions

| Category | Permission | Admin Site | Auth Site |
|----------|-----------|------------|-----------|
| Tax Tools | `access_tax_tools_ui` | ❌ | ✅ |

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **CCP License Agreement**: Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com>

2. **Code Standards**:
   - Follow PEP 8 style guidelines
   - Add docstrings to new methods
   - Include debug logging for tax calculations
   - No superfluous formatting changes

3. **Pull Requests**:
   - Create a feature branch
   - Write clear commit messages
   - Include tests if applicable
   - Update documentation

4. **Bug Reports**:
   - Use GitHub Issues
   - Include steps to reproduce
   - Provide error logs if available

---

## 📄 License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **GitHub Repository**: [allianceauth-corp-tools-tax-tools](https://github.com/Solar-Helix-Independent-Transport/allianceauth-corp-tools-tax-tools)
- **Issue Tracker**: [GitHub Issues](https://github.com/Solar-Helix-Independent-Transport/allianceauth-corp-tools-tax-tools/issues)
- **AllianceAuth**: [allianceauth.com](https://allianceauth.com)
- **EVE Online**: [eveonline.com](https://www.eveonline.com)

---

## ⭐ Acknowledgments

- Original project by [AaronKable](https://github.com/AaronKable)
- Enhanced version with corporation filtering and bug fixes (January 2026)
- AllianceAuth community for testing and feedback

---

## 📧 Support

For support:
1. Check the [QUICK_START.md](QUICK_START.md) guide
2. Review [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) for technical details
3. Enable debug logging to troubleshoot
4. Open a GitHub Issue if you find a bug

---

**Version**: 2.0.0-enhanced  
**Last Updated**: January 4, 2026  
**Status**: Production Ready ✅
