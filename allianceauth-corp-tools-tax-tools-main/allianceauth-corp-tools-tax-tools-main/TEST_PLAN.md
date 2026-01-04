# Test Plan - Corporation-Level Filtering

## Test Environment Setup

### Prerequisites
- AllianceAuth installation with CorpTools
- Multiple test corporations in database
- Test alliances with corporations
- Test characters with main characters set
- Invoice manager installed

### Test Data Required
```python
Test Alliance A (ID: 99001)
  ├─ Corp A1 (ID: 98001) - 10 members, 5 structures
  └─ Corp A2 (ID: 98002) - 15 members, 3 structures

Test Alliance B (ID: 99002)
  ├─ Corp B1 (ID: 98003) - 8 members, 2 structures
  └─ Corp B2 (ID: 98004) - 12 members, 0 structures

Independent Corps (No Alliance)
  ├─ Corp X (ID: 98005) - 5 members, 1 structure
  └─ Corp Y (ID: 98006) - 20 members, 8 structures
```

---

## Test Suite 1: Alliance-Only Filtering (Backward Compatibility)

### Test 1.1: Single Alliance Filter - Character Ratting
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = [Alliance A]
  included_corporations = []
  character_ratting_included = [10% Ratting Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1 receives ratting tax invoice
- ✅ Corp A2 receives ratting tax invoice
- ❌ Corp B1 does NOT receive invoice
- ❌ Corp B2 does NOT receive invoice
- ❌ Corp X does NOT receive invoice

**Verification Query**:
```sql
SELECT corporation_id, SUM(amount) 
FROM invoices 
WHERE ref LIKE 'Alliance Taxes%'
GROUP BY corporation_id;
```

---

### Test 1.2: Multiple Alliance Filter - Member Tax
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = [Alliance A, Alliance B]
  included_corporations = []
  corporate_member_tax_included = [10M per member]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1: Invoice for 50M (5 members × 10M)
- ✅ Corp A2: Invoice for 150M (15 members × 10M)
- ✅ Corp B1: Invoice for 80M (8 members × 10M)
- ✅ Corp B2: Invoice for 120M (12 members × 10M)
- ❌ Corp X: No invoice
- ❌ Corp Y: No invoice

---

### Test 1.3: Alliance Filter with Exemption
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = [Alliance A]
  included_corporations = []
  exempted_corps = [Corp A2]
  character_ratting_included = [10% Ratting Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1 receives invoice
- ❌ Corp A2 does NOT receive invoice (exempted)
- ❌ Other corps do NOT receive invoices

---

## Test Suite 2: Corporation-Only Filtering (New Feature)

### Test 2.1: Single Corporation Filter - Wallet Tax
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = []
  included_corporations = [Corp X]
  character_taxes_included = [5% Wallet Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp X receives wallet tax invoice
- ❌ All other corps do NOT receive invoices

---

### Test 2.2: Multiple Corporation Filter - Structure Tax
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = []
  included_corporations = [Corp X, Corp Y]
  corporate_structure_tax_included = [50M per structure]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp X: Invoice for 50M (1 structure × 50M)
- ✅ Corp Y: Invoice for 400M (8 structures × 50M)
- ❌ Corp A1: No invoice (even though it has structures)
- ❌ Other corps: No invoices

---

### Test 2.3: Corporation from Different Alliances
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = []
  included_corporations = [Corp A1, Corp B1, Corp X]
  corporate_member_tax_included = [10M per member]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1 (Alliance A): Invoice
- ✅ Corp B1 (Alliance B): Invoice
- ✅ Corp X (No alliance): Invoice
- ❌ Corp A2 (same alliance as A1): No invoice
- ❌ Other corps: No invoices

---

## Test Suite 3: Combined Filtering (Alliance + Corporation)

### Test 3.1: Alliance Plus Additional Corporation
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = [Alliance A]
  included_corporations = [Corp X]
  character_ratting_included = [10% Ratting Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1 receives invoice (matched by alliance)
- ✅ Corp A2 receives invoice (matched by alliance)
- ✅ Corp X receives invoice (matched by corporation)
- ❌ Corp B1 does NOT receive invoice
- ❌ Corp Y does NOT receive invoice

**Verification**: Ensure Corp X gets invoice even though it's not in Alliance A

---

### Test 3.2: Overlapping Filters (Corp in Alliance)
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = [Alliance A]
  included_corporations = [Corp A1]  # Corp A1 is already in Alliance A
  character_taxes_included = [5% Wallet Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1 receives ONE invoice (not duplicated)
- ✅ Corp A2 receives invoice
- ❌ Other corps do NOT receive invoices

**Verification**: Check that Corp A1 is not double-taxed

---

### Test 3.3: Combined with Exemptions
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = [Alliance A]
  included_corporations = [Corp X, Corp Y]
  exempted_corps = [Corp A1, Corp Y]
  character_ratting_included = [10% Ratting Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ❌ Corp A1: No invoice (exempted, even though in included alliance)
- ✅ Corp A2: Invoice (in alliance, not exempted)
- ✅ Corp X: Invoice (in corporations, not exempted)
- ❌ Corp Y: No invoice (exempted, even though in included corporations)

---

## Test Suite 4: Edge Cases

### Test 4.1: Empty Filters (Global Taxation)
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = []
  included_corporations = []
  exempted_corps = []
  character_ratting_included = [10% Ratting Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ ALL corporations with ratting data receive invoices

---

### Test 4.2: Empty Filters with Exemptions
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = []
  included_corporations = []
  exempted_corps = [Corp A1, Corp B1]
  corporate_member_tax_included = [10M per member]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ All corps EXCEPT Corp A1 and Corp B1 receive invoices

---

### Test 4.3: Corporation with No Alliance
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = [Alliance A]
  included_corporations = []
  character_ratting_included = [10% Ratting Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1, Corp A2 receive invoices
- ❌ Corp X (no alliance) does NOT receive invoice
- ❌ Corp Y (no alliance) does NOT receive invoice

---

### Test 4.4: Non-Existent Corporation ID
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = []
  included_corporations = [999999]  # Non-existent corp
  character_ratting_included = [10% Ratting Tax]
```

**Execute**: Generate invoices

**Expected Results**:
- ❌ No invoices generated
- ✅ No errors or exceptions
- ✅ System logs "No corporations matched filters"

---

## Test Suite 5: Tax Type Specific Tests

### Test 5.1: Ratting Tax with Region Filter + Corp Filter
**Setup**:
```python
CharacterRattingTaxConfiguration:
  region_filter = [Delve]
  
CorpTaxConfiguration:
  included_corporations = [Corp A1]
  character_ratting_included = [Above config]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1 receives invoice ONLY for Delve ratting
- ❌ Corp A1 ratting in other regions NOT taxed
- ❌ Other corps not taxed

---

### Test 5.2: Wallet Tax with Transaction Type + Alliance Filter
**Setup**:
```python
CharacterPayoutTaxConfiguration:
  wallet_transaction_type = "bounty_prizes,corporate_reward_payout"
  
CorpTaxConfiguration:
  included_alliances = [Alliance B]
  character_taxes_included = [Above config]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Alliance B corps taxed on bounties and rewards
- ❌ Alliance B corps NOT taxed on other transaction types
- ❌ Other alliances not taxed

---

### Test 5.3: Multiple Tax Types with Different Filters
**Setup**:
```python
CorpTaxConfiguration:
  included_alliances = [Alliance A]
  included_corporations = [Corp X]
  character_ratting_included = [10% Ratting]
  corporate_member_tax_included = [10M per member]
  corporate_structure_tax_included = [50M per structure]
```

**Execute**: Generate invoices

**Expected Results**:
- ✅ Corp A1: Ratting + Member + Structure taxes
- ✅ Corp A2: Ratting + Member + Structure taxes
- ✅ Corp X: Ratting + Member + Structure taxes
- ❌ Other corps: No taxes

**Verification**: Check each corp receives COMBINED invoice with all tax types

---

## Test Suite 6: Migration Tests

### Test 6.1: Fresh Installation Migration
**Setup**: Clean database, fresh AllianceAuth install

**Execute**:
```bash
python manage.py migrate taxtools
```

**Expected Results**:
- ✅ All migrations apply successfully
- ✅ No dependency errors
- ✅ Database schema created correctly

---

### Test 6.2: Upgrade from Previous Version
**Setup**: Database with existing tax configurations

**Execute**:
```bash
python manage.py migrate taxtools
```

**Expected Results**:
- ✅ Migration 0026 applies successfully
- ✅ Existing `exempted_corps` data preserved
- ✅ New `included_corporations` field added (empty)
- ✅ Existing tax configurations still work

---

### Test 6.3: Rollback Migration
**Execute**:
```bash
python manage.py migrate taxtools 0025
```

**Expected Results**:
- ✅ Migration 0026 rolled back
- ✅ `included_corporations` field removed
- ✅ `exempted_corps` reverted to original state
- ✅ No data loss

---

## Test Suite 7: Performance Tests

### Test 7.1: Large Corporation List
**Setup**:
```python
included_corporations = [100+ corporation IDs]
```

**Execute**: Generate invoices

**Metrics to Measure**:
- Query execution time < 5 seconds
- Memory usage reasonable
- No N+1 query issues

---

### Test 7.2: Large Alliance with Many Corps
**Setup**:
```python
included_alliances = [Alliance with 50+ corporations]
```

**Execute**: Generate invoices

**Metrics to Measure**:
- All corps processed
- Query execution time acceptable
- No timeout errors

---

## Test Suite 8: Admin Interface Tests

### Test 8.1: Add Corporation Filter via Admin
**Steps**:
1. Login to admin
2. Navigate to Taxtools → Config: Corporate
3. Select configuration
4. Use "Included Corporations" widget
5. Add 2-3 corporations
6. Save

**Expected Results**:
- ✅ Corporations saved correctly
- ✅ Widget shows selected corporations
- ✅ Configuration loads correctly on page reload

---

### Test 8.2: Filter Horizontal Widget Functionality
**Steps**:
1. Open tax configuration
2. Move corporations between Available/Selected
3. Use search/filter in widget
4. Save configuration

**Expected Results**:
- ✅ Widget responsive and functional
- ✅ Search works correctly
- ✅ Multiple selections possible
- ✅ Changes persist after save

---

## Test Suite 9: Logging and Debugging

### Test 9.1: Verify Filter Debug Logging
**Setup**: Enable DEBUG logging

**Execute**: Generate invoices

**Expected in Logs**:
```
TAXTOOLS: Starting calculate_tax
TAXTOOLS: Starting character_ratting_included
TAXTOOLS: Starting character_taxes_included
TAXTOOLS: Starting corporate_taxes_included
TAXTOOLS: Starting corporate_member_tax_included
TAXTOOLS: Starting corporate_structure_tax_included
TAXTOOLS: Done corporate_structure_tax_included
```

---

### Test 9.2: Tax Explanation Command
**Execute**:
```bash
python manage.py tax_explain
```

**Expected Results**:
- ✅ Shows which corporations will be taxed
- ✅ Shows which filters are active
- ✅ Shows tax amounts per corporation
- ✅ Output is readable and accurate

---

## Automated Test Script Template

```python
# test_corp_filtering.py

from django.test import TestCase
from taxtools.models import CorpTaxConfiguration
from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo

class CorporationFilteringTests(TestCase):
    
    def setUp(self):
        # Create test alliances and corps
        self.alliance_a = EveAllianceInfo.objects.create(...)
        self.corp_a1 = EveCorporationInfo.objects.create(...)
        # ... setup test data
        
    def test_alliance_only_filter(self):
        config = CorpTaxConfiguration.objects.create(...)
        config.included_alliances.add(self.alliance_a)
        
        # Generate and verify invoices
        result = config.calculate_tax()
        
        self.assertIn(self.corp_a1.corporation_id, result['taxes'])
        self.assertNotIn(self.corp_b1.corporation_id, result['taxes'])
        
    def test_corp_only_filter(self):
        config = CorpTaxConfiguration.objects.create(...)
        config.included_corporations.add(self.corp_x)
        
        result = config.calculate_tax()
        
        self.assertIn(self.corp_x.corporation_id, result['taxes'])
        self.assertNotIn(self.corp_a1.corporation_id, result['taxes'])
        
    def test_combined_filters(self):
        config = CorpTaxConfiguration.objects.create(...)
        config.included_alliances.add(self.alliance_a)
        config.included_corporations.add(self.corp_x)
        
        result = config.calculate_tax()
        
        # Both alliance corps AND specific corp should be taxed
        self.assertIn(self.corp_a1.corporation_id, result['taxes'])
        self.assertIn(self.corp_x.corporation_id, result['taxes'])
        
    def test_exemptions_override_filters(self):
        config = CorpTaxConfiguration.objects.create(...)
        config.included_alliances.add(self.alliance_a)
        config.exempted_corps.add(self.corp_a1)
        
        result = config.calculate_tax()
        
        # Corp A1 should NOT be taxed (exempted)
        self.assertNotIn(self.corp_a1.corporation_id, result['taxes'])
        # But Corp A2 should be taxed
        self.assertIn(self.corp_a2.corporation_id, result['taxes'])
```

---

## Test Execution Checklist

- [ ] All Test Suite 1 tests pass (Alliance-only)
- [ ] All Test Suite 2 tests pass (Corporation-only)
- [ ] All Test Suite 3 tests pass (Combined)
- [ ] All Test Suite 4 tests pass (Edge cases)
- [ ] All Test Suite 5 tests pass (Tax types)
- [ ] All Test Suite 6 tests pass (Migrations)
- [ ] All Test Suite 7 tests pass (Performance)
- [ ] All Test Suite 8 tests pass (Admin UI)
- [ ] All Test Suite 9 tests pass (Logging)
- [ ] Manual smoke test completed
- [ ] Production deployment approved

---

## Sign-Off

**Tester**: _______________  
**Date**: _______________  
**Status**: _______________  
**Notes**: _______________
