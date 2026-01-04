# Quick Start Guide: Corporation-Level Tax Filtering

## What Changed?

You can now configure taxes for **specific corporations** in addition to alliance-based taxation. Both options work together!

## Configuration Steps

### 1. Access Admin Panel
Navigate to: **Admin → Taxtools → Config: Corporate**

### 2. Choose Your Filtering Strategy

#### Option A: Alliance-Based (Original Way)
- **Included Alliances**: Select your alliance(s)
- **Included Corporations**: Leave empty
- **Result**: Taxes all corporations in the selected alliance(s)

#### Option B: Corporation-Based (New!)
- **Included Alliances**: Leave empty
- **Included Corporations**: Select specific corps
- **Result**: Taxes only the selected corporations

#### Option C: Combined Filtering (New!)
- **Included Alliances**: Select alliance(s)
- **Included Corporations**: Also select specific corps
- **Result**: Taxes corporations in the alliance(s) PLUS the specific corps you selected

#### Option D: Tax Everyone with Exemptions
- **Included Alliances**: Leave empty
- **Included Corporations**: Leave empty
- **Exempted Corps**: Select corps to exclude
- **Result**: Taxes ALL corporations except those in exempted list

### 3. Configure Tax Types
Select which taxes to apply:
- ☑️ Character Ratting Taxes
- ☑️ Character Wallet Taxes
- ☑️ Corporate Wallet Taxes
- ☑️ Per-Member Taxes
- ☑️ Structure Service Taxes

### 4. Save and Test
1. Click **Save**
2. Run: `python manage.py tax_explain`
3. Review the output to ensure correct corporations are included
4. When ready, trigger invoice generation

## Examples

### Example 1: Small Corp Tax System
**Scenario**: You only want to tax 3 specific corporations

**Configuration**:
- Included Alliances: (empty)
- Included Corporations: Corp A, Corp B, Corp C
- Exempted Corps: (empty)

**Result**: Only Corps A, B, and C are taxed

---

### Example 2: Alliance Tax with Special Addition
**Scenario**: Tax your alliance + one friendly corp from another alliance

**Configuration**:
- Included Alliances: Your Alliance
- Included Corporations: Friendly Corp
- Exempted Corps: (empty)

**Result**: All corps in your alliance + Friendly Corp are taxed

---

### Example 3: Alliance Tax with Exemption
**Scenario**: Tax your alliance but exclude your newbie training corp

**Configuration**:
- Included Alliances: Your Alliance
- Included Corporations: (empty)
- Exempted Corps: Training Corp Name

**Result**: All corps in alliance except Training Corp

---

### Example 4: Everything Except Specific Corps
**Scenario**: You manage multiple alliances and want to tax everyone except a few special cases

**Configuration**:
- Included Alliances: (empty)
- Included Corporations: (empty)
- Exempted Corps: Special Corp 1, Special Corp 2

**Result**: ALL corporations with tracked data are taxed except those exempted

## Tips

✅ **Use Alliance Filtering** when you want to tax entire alliances  
✅ **Use Corporation Filtering** for granular control of specific corps  
✅ **Use Both Together** to cover your alliance plus external partners  
✅ **Use Exemptions** to exclude specific corps from any taxation  
✅ **Leave Both Empty** to tax everyone (global taxation)  

## Troubleshooting

**Q: I added a corporation but it's not being taxed**  
A: Check if it's in the "Exempted Corps" list

**Q: A corporation in my exempted list is still being taxed**  
A: Exemptions are checked during invoice generation. Make sure to regenerate invoices after changing exemptions

**Q: How do I know which corporations will be taxed?**  
A: Run `python manage.py tax_explain` to see a detailed breakdown

**Q: Can I set different tax rates per corporation?**  
A: Currently, tax rates are set per tax type configuration, not per corporation. All corporations matching your filters use the same rates.

**Q: What if a corporation is in multiple alliances?**  
A: Characters are associated with their main character's corporation. The system uses the main character's corp/alliance membership for filtering.

## After Configuration

Remember to:
1. ✅ Run migrations if upgrading: `python manage.py migrate`
2. ✅ Test your configuration: `python manage.py tax_explain`
3. ✅ Review generated invoices before they go out
4. ✅ Set up the periodic task for automated invoice generation

## Need Help?

Check the full documentation in README.md or IMPLEMENTATION_NOTES.md for technical details.
