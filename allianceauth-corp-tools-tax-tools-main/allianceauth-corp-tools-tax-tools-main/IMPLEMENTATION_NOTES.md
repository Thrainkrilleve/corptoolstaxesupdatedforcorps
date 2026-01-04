# Tax Tools Corporation-Level Filtering Implementation

## Summary

Successfully added corporation-level filtering alongside the existing alliance-level filtering system. The tax system now supports both alliance and corporation filtering simultaneously, giving administrators maximum flexibility in tax configuration.

## Changes Made

### 1. Models (taxtools/models.py)

#### CorpTaxConfiguration Model
- **Added Field**: `included_corporations` - ManyToManyField to EveCorporationInfo
- **Modified Field**: `exempted_corps` - Added `related_name='tax_exemptions'` to avoid conflicts
- **Updated Methods**:
  - `calculate_tax()` - Now accepts `corp_filter` parameter
  - `get_invoice_data()` - Extracts both alliance and corp filters, passes both to calculate_tax
  - `rerun_taxes()` - Now accepts `corp_filter` parameter

#### CharacterRattingTaxConfiguration Model
Updated all methods to support `corp_filter` parameter:
- `get_payment_data()`
- `get_payment_data_from_ids()`
- `get_character_aggregates()`
- `get_character_aggregates_id()`
- `get_character_aggregates_corp_level()`
- `get_character_aggregates_corp_level_id()`

#### CharacterPayoutTaxConfiguration Model
Updated all methods to support `corp_filter` parameter:
- `get_payment_data()`
- `get_payment_data_from_ids()`
- `get_character_aggregates()`
- `get_character_aggregates_ids()`
- `get_character_aggregates_corp_level()`
- `get_character_aggregates_corp_level_id()`

#### CorpTaxPayoutTaxConfiguration Model
Updated methods to support `corp_filter` parameter:
- `get_payment_data()` - Added corp_filter logic with proper query filtering
- `get_aggregates()` - Passes corp_filter to get_payment_data

### 2. Admin Interface (taxtools/admin.py)

- **CorpTaxConfigurationAdmin**: Added `included_corporations` to `filter_horizontal` list
- This enables the multi-select widget for choosing corporations in the admin panel

### 3. Database Migration (taxtools/migrations/0026_corptaxconfiguration_included_corporations.py)

Created new migration that:
- Alters `exempted_corps` field to add `related_name='tax_exemptions'`
- Adds `included_corporations` field with `related_name='tax_inclusions'`

### 4. Documentation (README.md)

Updated with comprehensive information about:
- New corporation-level filtering feature
- How alliance and corporation filtering work together
- Configuration instructions
- Explanation of all supported tax types

## How It Works

### Filtering Logic

The system uses an **OR** logic for included filters:
```
IF included_alliances.count() > 0:
    Apply alliance filter
    
IF included_corporations.count() > 0:
    Apply corporation filter
    
Result: Corps matching EITHER alliance OR corporation criteria are taxed
```

Exemptions are applied AFTER filtering:
```
excluded_cids = exempted_corps.all()
# Corps in excluded_cids are skipped even if they match alliance/corp filters
```

### Query Flow Example

For Character Ratting Taxes:
```python
query = CharacterWalletJournalEntry.objects.filter(...)

if alliance_filter:
    query = query.filter(
        character__character__character_ownership__user__profile__main_character__alliance_id__in=alliance_filter)

if corp_filter:
    query = query.filter(
        character__character__character_ownership__user__profile__main_character__corporation_id__in=corp_filter)
```

## Use Cases

### 1. Alliance-Only Taxation (Original Behavior)
- Set `included_alliances`: [My Alliance]
- Leave `included_corporations`: empty
- Result: Taxes all corps in the alliance

### 2. Corporation-Only Taxation (New Feature)
- Leave `included_alliances`: empty
- Set `included_corporations`: [Corp A, Corp B, Corp C]
- Result: Taxes only those specific corps

### 3. Mixed Taxation (New Feature)
- Set `included_alliances`: [Alliance A]
- Set `included_corporations`: [Corp X, Corp Y]
- Result: Taxes all corps in Alliance A + Corp X + Corp Y (even if X and Y aren't in Alliance A)

### 4. Global Taxation with Exemptions
- Leave both `included_alliances` and `included_corporations` empty
- Set `exempted_corps`: [Corp Z]
- Result: Taxes ALL corps with data except Corp Z

## Migration Path

To upgrade to this version:

1. **Backup your database** (always!)
2. Pull the updated code
3. Run migrations:
   ```bash
   python manage.py migrate taxtools
   ```
4. The new `included_corporations` field will be available in admin
5. Existing configurations will continue to work unchanged

## Testing Recommendations

1. **Test alliance-only filtering** (ensure backward compatibility)
2. **Test corp-only filtering** (new feature)
3. **Test mixed filtering** (alliance + specific corps)
4. **Test exemptions** (ensure they work with both filter types)
5. **Test with empty filters** (should process all corps)

## API Endpoints

All existing API endpoints continue to work without changes. The filtering is transparent to API consumers as it's handled within the model methods.

## Notes

- **Backward Compatible**: Existing tax configurations will work exactly as before
- **No Breaking Changes**: All existing method signatures remain compatible (corp_filter is optional)
- **HTML/CSS Unchanged**: Frontend code remains untouched as requested
- **Database Performance**: Added filters use indexed foreign keys, minimal performance impact

## Future Enhancements (Optional)

Possible future improvements:
1. Add AND logic option (tax only corps in BOTH alliance AND corp list)
2. Add corporation exclusions from specific tax types
3. Add tax rate overrides per corporation
4. Add detailed logging of which filter matched each corporation
