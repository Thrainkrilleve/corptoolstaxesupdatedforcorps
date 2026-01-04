# Tax System Architecture - Corporation & Alliance Filtering

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    CorpTaxConfiguration                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Configuration Fields:                                    │  │
│  │  • Name                                                   │  │
│  │  • Character Taxes Included                              │  │
│  │  • Corporate Taxes Included                              │  │
│  │  • Member Tax Included                                   │  │
│  │  • Structure Tax Included                                │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │  FILTERS (ALL OPTIONAL):                        │    │  │
│  │  │  • Included Alliances     [Alliance A, B, C]    │    │  │
│  │  │  • Included Corporations  [Corp X, Y, Z]        │    │  │
│  │  │  • Exempted Corps         [Corp Exception]      │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    get_invoice_data()                           │
│  Extracts filters and calls calculate_tax()                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│            calculate_tax(alliance_filter, corp_filter)          │
│  Processes each tax type with filters                           │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Ratting    │ │   Wallet     │ │  Corporate   │
    │   Taxes      │ │   Taxes      │ │   Taxes      │
    └──────────────┘ └──────────────┘ └──────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              get_payment_data(alliance_filter, corp_filter)     │
│                                                                  │
│  Base Query: CharacterWalletJournalEntry.objects.filter(...)   │
│                                                                  │
│  IF alliance_filter:                                            │
│    query.filter(main_character__alliance_id__in=alliance_filter)│
│                                                                  │
│  IF corp_filter:                                                │
│    query.filter(main_character__corporation_id__in=corp_filter) │
│                                                                  │
│  Returns: Filtered wallet entries                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              get_character_aggregates_corp_level()              │
│  Aggregates tax data by corporation                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               Filter by exempted_corps                          │
│  Removes corporations in exemption list                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Generate Invoices                             │
│  Creates invoice for each corporation's CEO                     │
└─────────────────────────────────────────────────────────────────┘
```

## Filter Logic Examples

### Example 1: Alliance Only
```
Input:
  included_alliances = [1001, 1002]
  included_corporations = []
  exempted_corps = []

Query Effect:
  WHERE alliance_id IN (1001, 1002)

Result:
  All corps in Alliance 1001 and 1002 are taxed
```

### Example 2: Corporation Only
```
Input:
  included_alliances = []
  included_corporations = [98001, 98002, 98003]
  exempted_corps = []

Query Effect:
  WHERE corporation_id IN (98001, 98002, 98003)

Result:
  Only Corp 98001, 98002, and 98003 are taxed
```

### Example 3: Combined Filtering
```
Input:
  included_alliances = [1001]
  included_corporations = [98999]
  exempted_corps = []

Query Effect:
  WHERE alliance_id IN (1001) OR corporation_id IN (98999)

Result:
  All corps in Alliance 1001 + Corp 98999 are taxed
```

### Example 4: With Exemptions
```
Input:
  included_alliances = [1001]
  included_corporations = []
  exempted_corps = [98555]

Process:
  1. Query: WHERE alliance_id IN (1001)
  2. Post-filter: EXCLUDE corporation_id = 98555

Result:
  All corps in Alliance 1001 EXCEPT Corp 98555
```

### Example 5: Global with Exemptions
```
Input:
  included_alliances = []
  included_corporations = []
  exempted_corps = [98444, 98555]

Process:
  1. Query: No filter (all corps)
  2. Post-filter: EXCLUDE corporation_id IN (98444, 98555)

Result:
  ALL corporations with data EXCEPT 98444 and 98555
```

## Data Flow Per Tax Type

### Character Ratting Tax
```
CharacterWalletJournalEntry
    → Filter by ref_type = "bounty_prizes"
    → Filter by region (if configured)
    → Apply alliance_filter (if provided)
    → Apply corp_filter (if provided)
    → Calculate ESS adjustments
    → Aggregate by main character
    → Group by corporation
    → Apply exemptions
    → Generate invoice
```

### Character Wallet Tax
```
CharacterWalletJournalEntry
    → Filter by ref_type (configurable)
    → Filter by source corp (if configured)
    → Apply alliance_filter (if provided)
    → Apply corp_filter (if provided)
    → Get corp tax history
    → Calculate pre-tax amount
    → Aggregate by main character
    → Group by corporation
    → Apply exemptions
    → Generate invoice
```

### Corporate Wallet Tax
```
CorporationWalletJournalEntry
    → Filter by ref_type (configurable)
    → Filter by source corp (configured)
    → Apply alliance_filter (if provided)
    → Apply corp_filter (if provided)
    → Get corp tax history
    → Calculate pre-tax amount
    → Group by corporation
    → Apply exemptions
    → Generate invoice
```

## Filter Priority

1. **Inclusion Filters** (OR logic)
   - Alliance filter (inclusive)
   - Corporation filter (inclusive)
   - If both present: corps matching EITHER are included

2. **Exclusion Filters** (Processed after inclusion)
   - Exempted corps (exclusive)
   - Applied AFTER inclusion filters
   - Overrides any inclusion

3. **Tax Type Filters** (Additional criteria)
   - Region filters (ratting tax)
   - Transaction type filters (wallet taxes)
   - State filters (member tax)
   - Structure type filters (structure tax)

## Database Relationships

```
CorpTaxConfiguration
    ├── included_alliances [M2M] → EveAllianceInfo
    ├── included_corporations [M2M] → EveCorporationInfo (related_name='tax_inclusions')
    ├── exempted_corps [M2M] → EveCorporationInfo (related_name='tax_exemptions')
    ├── character_taxes_included [M2M] → CharacterPayoutTaxConfiguration
    ├── character_ratting_included [M2M] → CharacterRattingTaxConfiguration
    ├── corporate_taxes_included [M2M] → CorpTaxPayoutTaxConfiguration
    ├── corporate_member_tax_included [M2M] → CorpTaxPerMemberTaxConfiguration
    └── corporate_structure_tax_included [M2M] → CorpTaxPerServiceModuleConfiguration

User → Main Character
    └── EveCharacter
        ├── corporation_id → EveCorporationInfo
        └── alliance_id → EveAllianceInfo

CharacterWalletJournalEntry
    └── character → CorporationAudit
        └── character → EveCharacter
            └── character_ownership → CharacterOwnership
                └── user → User
                    └── profile
                        └── main_character → EveCharacter
                            ├── corporation_id (Used for corp_filter)
                            └── alliance_id (Used for alliance_filter)
```

## Performance Characteristics

| Filter Type | Query Impact | Index Used | Performance |
|-------------|--------------|------------|-------------|
| No filters | Full scan | None | Slow (processes all) |
| Alliance only | Indexed lookup | alliance_id | Fast |
| Corp only | Indexed lookup | corporation_id | Fast |
| Both filters | Two indexed lookups (OR) | Both indexes | Fast |
| With exemptions | Post-filter in Python | N/A | Negligible |

## Admin UI Layout

```
┌────────────────────────────────────────────────────────┐
│  Config: Corporate (Tax Configuration)                 │
├────────────────────────────────────────────────────────┤
│  Name: [My Tax Config                           ]     │
│                                                        │
│  Tax Types:                                            │
│  [Select character taxes, ratting, corporate, etc.]    │
│                                                        │
│  ┌──────────── FILTERS ────────────┐                  │
│  │                                  │                  │
│  │  Included Alliances:             │                  │
│  │  ┌─────────────┐ ┌─────────────┐│                  │
│  │  │  Available  │ │  Selected   ││                  │
│  │  │  Alliances  │ │  Alliances  ││                  │
│  │  │             │ │             ││                  │
│  │  │  Alliance A │ │             ││                  │
│  │  │  Alliance B │ │  Alliance C ││                  │
│  │  └─────────────┘ └─────────────┘│                  │
│  │                                  │                  │
│  │  Included Corporations:          │                  │
│  │  ┌─────────────┐ ┌─────────────┐│                  │
│  │  │  Available  │ │  Selected   ││                  │
│  │  │  Corps      │ │  Corps      ││                  │
│  │  │             │ │             ││                  │
│  │  │  Corp A     │ │  Corp X     ││                  │
│  │  │  Corp B     │ │  Corp Y     ││                  │
│  │  └─────────────┘ └─────────────┘│                  │
│  │                                  │                  │
│  │  Exempted Corps:                 │                  │
│  │  ┌─────────────┐ ┌─────────────┐│                  │
│  │  │  Available  │ │  Exempted   ││                  │
│  │  │  Corps      │ │  Corps      ││                  │
│  │  │             │ │             ││                  │
│  │  │  Corp A     │ │             ││                  │
│  │  │  Corp B     │ │  Corp Z     ││                  │
│  │  └─────────────┘ └─────────────┘│                  │
│  └──────────────────────────────────┘                  │
│                                                        │
│  [Save]  [Save and continue]  [Delete]                │
└────────────────────────────────────────────────────────┘
```

This visual architecture should help understand how the filtering system works throughout the application!
