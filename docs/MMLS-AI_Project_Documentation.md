# MMLS-AI — Military Medical Logistics System (AI)
## Complete Project Documentation

---

## Table of Contents

1. [What Is MMLS-AI?](#1-what-is-mmls-ai)
2. [Who Uses It — Roles & Login](#2-who-uses-it--roles--login)
3. [Dashboard Overview — The KPI Bar](#3-dashboard-overview--the-kpi-bar)
4. [Tab 1: Inventory](#4-tab-1-inventory)
5. [Tab 2: Medicine Search & Registration](#5-tab-2-medicine-search--registration)
6. [Tab 3: XGBoost AI Demand Forecast](#6-tab-3-xgboost-ai-demand-forecast)
7. [Tab 4: LSTM Surge Trend Model](#7-tab-4-lstm-surge-trend-model)
8. [Tab 5: Hours of Supply](#8-tab-5-hours-of-supply)
9. [Tab 6: Cross-Echelon Map](#9-tab-6-cross-echelon-map)
10. [Tab 7: Validation Scenarios](#10-tab-7-validation-scenarios)
11. [Tab 8: Audit Log](#11-tab-8-audit-log)
12. [Tab 9: Digital Twin (LSCO)](#12-tab-9-digital-twin-lsco)
13. [Hours-of-Supply Tier System](#13-hours-of-supply-tier-system)
14. [Behind the Scenes — The API](#14-behind-the-scenes--the-api)
15. [Real-Life Medical Scenarios](#15-real-life-medical-scenarios)
16. [Known Limitations](#16-known-limitations)

---

## 1. What Is MMLS-AI?

MMLS-AI is a **military medical supply chain management system** that uses AI to track, predict, and plan the consumption of medical consumables across a multi-echelon battlefield medical network.

It is designed for **Large-Scale Combat Operations (LSCO)** — the kind of sustained, high-casualty environment where knowing exactly how many tourniquets, blood units, or anaesthetic sets you have left is the difference between saving and losing lives.

### What problem does it solve?

In a combat medical setting, supplies flow through a chain of care:

```
National Warehouse (WH) → Theatre Depot (DEP) → Role 3 Hospital (R3)
   → Role 2 Enhanced Forward Surgical Team (R2E) → Role 1 Battalion Aid Station (R1)
```

- **Role 1 (R1):** Front-line battalion aid station — medics apply tourniquets, dressings, basic life-saving interventions.
- **Role 2E (R2E):** Forward surgical team — emergency surgeries, blood transfusions, anaesthesia.
- **Role 3 (R3):** Combat support hospital — definitive surgery, intensive care, larger stockholdings.

MMLS-AI tracks every item at every echelon, logs who used what and when, uses AI to predict future demand, and runs a digital-twin simulation to test whether your supply plan will survive a 30-day combat scenario with casualty surges, depot losses, and cold-chain failures.

### What are the main features?

| Feature | What it does |
|---|---|
| **Live Inventory** | Real-time stock levels for every medical item, with AI-calculated hours-of-supply and low-stock alerts |
| **Item Search & Registration** | Search for an item by name, auto-look it up in BST NSN catalog / FDA / Wikipedia, and register new items into the system |
| **Usage Recording** | Log every time an item is used — decrements stock, writes an audit entry, fires low-stock alerts |
| **XGBoost Forecast** | AI demand prediction per item based on operational tempo and triage mix (T1/T2/T3 casualty ratios) |
| **LSTM Surge Detection** | Deep learning model that detects consumption trend spikes (MASCAL / mass-casualty surges) over 48 hours |
| **Hours of Supply** | Color-coded dashboard showing how many hours each item will last at current consumption rates |
| **Cross-Echelon Map** | Geographic view of the supply chain nodes and resupply pipeline |
| **Validation Scenarios** | Automated tests that verify low-stock alerts, surge detection, and controlled-drug auditing work correctly |
| **Audit Log** | Full audit trail of every usage event — who, what, when, how much — with CSV export for controlled-drug accountability |
| **Digital Twin (LSCO)** | A 30-day synthetic simulation comparing static vs dynamic resupply policies, with casualty surges, cold-chain failures, blood spoilage, depot strikes, and DDIL (Degraded, Disrupted, Interrupted, and Limited) logistics loss |

---

## 2. Who Uses It — Roles & Login

### Login Screen

When you open the dashboard, you see:

- The **BST logo** on the left and **Code:Black AI logo** on the right
- Title: **"🏥 MMLS-AI — Military Medical Logistics System"**
- A login card with **Username** and **Password** fields
- A green **"🔐 Secure Login"** button

### The Three Roles

The system has three user roles, each with different access levels:

| Role | Username | Password | Echelon | What they see |
|---|---|---|---|---|
| **Medic (Role 1)** | `medic01` | `medic123` | Role1 | 5 tabs: Inventory, Search, Hours of Supply, Audit Log, Digital Twin |
| **FST Surgeon (Role 2)** | `surgeon01` | `surgeon123` | Role2 | 7 tabs: adds XGBoost Forecast + LSTM Trend |
| **Logistician (Role 3)** | `logistic01` | `admin123` | Role3 | All 9 tabs: adds Cross-Echelon Map + Validation |

**Why different roles?** A frontline medic should see what they have in their aid station. A surgeon at the forward surgical team needs demand forecasts. The logistician at the Role 3 hospital needs the full picture — every echelon, the map, and validation tools.

### How role filtering works

- **Medics (Role 1):** Only see inventory items assigned to Role 1
- **Surgeons (Role 2):** Only see inventory items assigned to Role 2
- **Logisticians (Role 3):** See everything — all echelons, all items

### Login / Logout Flow

**To log in:**
1. Enter your username and password
2. Click **"🔐 Secure Login"**
3. If correct: you enter the dashboard
4. If wrong: you see **"Invalid username or password"** in red

**To log out:**
1. Click the **"Logout"** button in the top-right card (shows "Logged in as {username}" with a colored role badge)
2. You return to the login screen

**What you see after login:** The dashboard header shows your username with a colored badge (green for Medic, blue for Surgeon, gold for Logistician) and a Logout button.

---

## 3. Dashboard Overview — The KPI Bar

At the top of the dashboard (after login), you see four KPI (Key Performance Indicator) cards. These give you an instant snapshot of the supply situation:

| Card | Icon | Color Logic | What It Means |
|---|---|---|---|
| **TOTAL ITEMS** | 📦 | Blue | Total number of items in your echelon's inventory |
| **LOW STOCK** | 📉 | Red if >0, Green if 0 | How many items have dropped to or below their alert threshold — items that need resupply soon |
| **EXPIRY WARNING** | ⏳ | Amber if >0, Green if 0 | How many items expire within 30 days — items that need to be used first or replaced |
| **CONTROLLED** | 🔒 | Purple | How many items are controlled drugs (e.g., morphine, ketamine, fentanyl) — these require strict audit logging |

**Real-life meaning:** A medic opens the dashboard and sees LOW STOCK = 3 in red. That means three types of medical consumables are running low. They should check the Inventory tab to see which ones and arrange resupply before the next casualty arrives.

---

## 4. Tab 1: 📦 Inventory

### Purpose

Shows the complete, live inventory of medical consumables for your echelon. Every item's stock level, hours-of-supply tier, category, NSN (National Stock Number), and clinical reference is displayed in one table.

### Buttons

| Button | What It Does | When to Use It |
|---|---|---|
| **🔄 Refresh** | Reloads the inventory from the API. The data is always live, so this just pulls the latest state. | After recording usage on another tab or if you suspect the data is stale. |
| **🗑️ Delete Items** | Toggles delete mode on/off. When on, checkboxes appear next to each row and a red "Confirm Deletion" button appears. | When an item has been removed from the system entirely (e.g., discontinued, wrong entry). Mainly used by logisticians. |

### What You See — Normal Mode

A styled table with these columns:

| Column | Meaning |
|---|---|
| **Cat #** | Catalog number |
| **CATEGORY** | Type of item (e.g., Analgesia, Dressing, Blood, Haemorrhage Control) |
| **ITEM / DESCRIPTION** | Full name of the medical item |
| **NSN** | NATO Stock Number — the unique identifier for this item in the NATO supply system |
| **UNIT** | Unit of measure (ea, ml, etc.) |
| **Role 1 (BAS)** | Standard quantity for a Battalion Aid Station |
| **Role 2 (FSE)** | Standard quantity for a Forward Surgical Element |
| **Role 2+ (E-FST)** | Enhanced quantity for an Enhanced Forward Surgical Team |
| **FST** | Forward Surgical Team quantity |
| **Role 3 (CSH)** | Standard quantity for a Combat Support Hospital |
| **FSC** | Federal Supply Class |
| **CONTENTS / SPECIFICATION** | What's in the package |
| **CoTCCC / Clinical Ref** | Committee on Tactical Combat Casualty Care reference |
| **Sterile?** | Whether the item is sterile |
| **NOTES / PROCUREMENT** | Procurement notes, including AI metrics like "[🔴 LOW STOCK \| HoS: 12.3h (GREEN) \| 🔒 Controlled]" |
| **HoS Tier** | Hours-of-Supply tier — color-coded (see Section 13) |

**What the AI metrics appended to notes mean:**

- 🔴 **LOW STOCK** — the item has dropped to or below its alert threshold
- **HoS: 12.3h (GREEN)** — the item will last 12.3 hours at current consumption rate, which is in the GREEN tier (safe)
- 🔒 **Controlled** — the item is a controlled drug requiring audit logging

### What You See — Delete Mode

When you click **"🗑️ Delete Items"**:

1. A yellow warning appears: **"⚠️ DELETE MODE ACTIVE: Check the boxes of items to delete."**
2. The table changes to an editable mode with a **"Select"** checkbox column.
3. A red **"🚨 Confirm Deletion"** button appears below the table.

**To delete items:**
1. Check the boxes next to items you want to remove
2. Click **"🚨 Confirm Deletion"**
3. You see: **"✅ Successfully deleted N items!"**
4. Delete mode turns off and the table refreshes

**If you click Confirm with nothing selected:** You see **"No items selected."**

**Real-life scenario:** A logistician discovers that item ITM016 (Cric Kit) has been replaced by a newer version with a different NSN. They enter delete mode, check the old item, confirm deletion, and then use the Medicine Search tab to register the new version.

---

## 5. Tab 2: 🔍 Medicine Search & Registration

### Purpose

This is the core operational tool. You use it to:
1. **Search** for an item already in inventory and record usage
2. **Look up** an item not yet in inventory (searches BST NSN catalog, FDA databases, Wikipedia)
3. **Register** a new item into the inventory

### Layout

The tab has a two-column layout. The left column is for searching, and the right column shows results and the registration form.

### Step 1: Convert to FDA Name (Medicines Only)

**When to use:** When you know a drug by its common/brand name but need the FDA generic name for accurate cataloging.

| Input | What It Does |
|---|---|
| Radio: **💊 Medicine / 🩺 Medical Equipment** | Selects the item type. Medicine enables the FDA conversion step; Equipment skips it. |
| Text: **"Generic / Brand name"** | Type a drug name like "paracetamol" or "adrenaline" |
| Button: **"🔄 Convert"** | Converts the name to the FDA standard generic name |

**How conversion works:**
- First checks a local map (e.g., paracetamol → acetaminophen, adrenaline → epinephrine)
- If not found locally, queries the **NLM RxNorm API** (National Library of Medicine)
- Result shown in a green box: **"FDA Name (source): acetaminophen"**
- Source badge shows: "Local conversion map", "RxNorm Database", or "No conversion found — using as-is"

**Real-life scenario:** A medic types "adrenaline" and clicks Convert. The system shows "FDA Name (RxNorm Database): epinephrine". This ensures the item is cataloged under the correct FDA name, which matters for procurement and interoperability with NATO systems.

### Step 2: Search & Look Up

| Input | What It Does |
|---|---|
| Text: **"Item name or ID"** | Type an item name or item ID (auto-filled with the FDA name if you converted in Step 1) |
| Button: **"🔍 Search & Look Up"** | Searches the inventory first, then external databases if not found |

### Output — Item Found in Inventory

If the item exists in MMLS-AI inventory, you see:

- A green box: **"✅ Already in MMLS-AI Inventory"** showing:
  - Item name, ID, category, echelon
  - Current stock level
  - Alert threshold
  - Hours-of-supply (color-coded by tier)

**Then a usage recording form appears:**

| Input/Button | What It Does |
|---|---|
| **"Quantity Used"** (number, 1–50) | How many units of this item were consumed |
| **"User ID"** (text, defaults to your username) | Who used the item |
| **"✅ Record Usage"** button | Logs the usage — decrements stock, writes audit entry, fires alert if low |
| **"✖ Clear"** button | Clears the match and resets the form |

**What happens when you click "✅ Record Usage":**
- If stock drops to or below the alert threshold: **"⚠️ LOW STOCK: {item name} → {new stock} left"** (red error)
- If stock is still above threshold: **"✅ Recorded — New stock: {new stock}"** (green success)

**Real-life scenario:** A medic treats a casualty with a tourniquet (ITM004). They open the Search tab, type "tourniquet", find it in inventory showing 15 in stock, enter Quantity Used = 1, and click Record Usage. The system shows "✅ Recorded — New stock: 14". Later, when stock drops to 5 (the alert threshold), they'll see "⚠️ LOW STOCK: CAT Tourniquet → 5 left".

### Output — Item Not Found in Inventory

If the item is NOT in the MMLS-AI inventory:

1. An amber box appears: **"⚠️ Not found in inventory. Searching BST NSN Catalog and online databases…"**
2. The system searches in this order:
   - **BST NSN Excel Catalog** — the local medical consumables database with NATO stock numbers
   - **FDA Drug Label API** (for medicines) or **FDA Device Classification API** (for equipment)
   - **Wikipedia REST API** — for general information
   - **Manual entry** — if all else fails, you fill in the details yourself
3. Found information is shown in a blue box: **"🌐 Info Found Online"** with a source badge

**Then a registration form appears:**

### Registration Form — "Add to MMLS-AI Inventory"

| Field | What to Enter |
|---|---|
| **NSN** | NATO Stock Number (auto-suggested as ITM{next number} or extracted from search) |
| **ITEM / DESCRIPTION** | Full item name |
| **CATEGORY** | Select from ~17 categories (Analgesia, Antibiotic, Blood, Dressing, Haemorrhage Control, etc.) |
| **UNIT** | Unit of measure (ea, ml, etc.) |
| **FSC** | Federal Supply Class |
| **CoTCCC / Clinical Ref** | TCCC clinical reference |
| **Sterile?** | Whether the item is sterile |
| **Role 1 (BAS)** | Standard Role 1 quantity |
| **Role 2 (FSE)** | Standard Role 2 quantity |
| **Role 2+ (E-FST)** | Enhanced Role 2 quantity |
| **FST** | FST quantity |
| **Role 3 (CSH)** | Role 3 quantity |
| **Assign AI Echelon** | Which echelon this item belongs to (Role1/Role2/Role3) |
| **Initial AI Stock** | Starting stock quantity (1–1000) |
| **CONTENTS / SPECIFICATION** | What's in the package |
| **NOTES / PROCUREMENT** | Procurement and usage notes |

| Button | What It Does |
|---|---|
| **"💾 Add to Inventory"** | Registers the item in the database |
| **"✖ Cancel"** | Clears the form |

**What happens when you click "💾 Add to Inventory":**
- Success: **🎉 Balloons** + **"✅ {item name} added to MMLS-AI inventory!"** + blue line showing "Last registered: {item name}"
- Item already exists: **"⚠️ Item ID {nsn} already exists"**
- Error: red error message

**Real-life scenario:** A forward surgical team receives a new type of haemostatic dressing not yet in the system. The surgeon opens the Search tab, types the dressing name, it's not in inventory, so the system looks it up in the BST NSN catalog and finds the NSN. The surgeon fills in the echelon (Role2), initial stock (50), and clicks Add to Inventory. The item now appears in the Inventory tab.

---

## 6. Tab 3: 🤖 XGBoost AI Demand Forecast

### Who Can Access: Surgeons (Role 2) and Logisticians (Role 3) only

### Purpose

Uses a trained **XGBoost machine learning model** to predict how fast each medical consumable will be consumed, based on the expected operational situation. This helps you plan resupply before you run out.

### Inputs (Sliders)

| Slider | Range | Default | What It Controls |
|---|---|---|---|
| **Operational Tempo** | 0.1 – 1.0 | 0.5 | Overall intensity of operations. 0.1 = low-intensity (patrol), 1.0 = high-intensity combat. Higher tempo = faster consumption. |
| **T1 Severe** | 0.0 – 0.5 | 0.2 | Fraction of casualties who are T1 (immediate, life-threatening). These need the most supplies per casualty. |
| **T2 Moderate** | 0.0 – 0.4 | 0.2 | Fraction of T2 casualties (urgent but not immediate). |
| **T3 Minor** | 0.0 – 0.4 | 0.1 | Fraction of T3 casualties (minor injuries, can wait). |

**What the triage mix means in practice:**
- **T1 (Immediate):** Life-threatening bleeding, airway obstruction, tension pneumothorax — needs tourniquets, chest seals, blood, TXA
- **T2 (Urgent):** Serious but not immediately fatal — needs IV fluids, splints, antibiotics
- **T3 (Minor):** Minor wounds — needs simple dressings, analgesia

### Button

| Button | What It Does |
|---|---|
| **"🤖 Run XGBoost Forecast"** | Sends the slider values to the API, which runs the XGBoost model on every inventory item and returns predicted consumption rates |

### Output

After clicking **"🤖 Run XGBoost Forecast"**, you see three things:

**1. Horizontal Bar Chart — "Predicted Consumption"**
- One bar per item, showing the predicted consumption rate (units/hour)
- Bars are color-coded by hours-of-supply tier (GREEN/TEAL/AMBER/RED/PURPLE)
- Chart title shows the parameters used: "Predicted Consumption — Tempo:0.5 T1:0.2 T2:0.2 T3:0.1"
- **How to read it:** Longer bars = faster consumption = will run out sooner. Red/Purple bars are the most urgent.

**2. Feature Importance Image**
- Displays `feature_importance.png` — a chart showing which factors the XGBoost model considers most important for predicting demand
- If the image is missing: "💡 Run train_model.py to generate feature_importance.png"

**3. Results Table**

| Column | Meaning |
|---|---|
| **ID** | Item ID |
| **Name** | Item name |
| **Stock** | Current stock level |
| **Rate (u/hr)** | Predicted consumption rate in units per hour |
| **HoS (hrs)** | Hours of supply = stock ÷ rate. How long the item will last. |
| **Tier** | Color-coded hours-of-supply tier |

**Real-life scenario:** A surgeon is planning for a planned offensive. They set Operational Tempo to 0.8 (high-intensity combat) and T1 to 0.3 (expecting more severe casualties). They click Run XGBoost Forecast. The chart shows BLOOD_UNIT in red with a predicted rate of 8.5 units/hour and only 50 units in stock — that's about 6 hours of supply (AMBER tier). They alert the logistician to arrange a blood resupply immediately.

---

## 7. Tab 4: 📈 LSTM Surge Trend Model

### Who Can Access: Surgeons (Role 2) and Logisticians (Role 3) only

### Purpose

Shows a pre-trained **LSTM (Long Short-Term Memory) neural network** model that predicts consumption trends over 48 hours and highlights where a **MASCAL (Mass Casualty) surge** occurs. This helps you recognize when a sudden spike in demand is coming so you can pre-position supplies.

### What You See (No Buttons — Auto-Loaded)

**1. Line Chart — "LSTM: 48-Hour Consumption Trend — CAT Tourniquet (MASCAL surge at H+24)"**
- Blue solid line: **Actual** consumption over 48 hours
- Red dashed line: **LSTM Predicted** consumption
- A dotted vertical line at hour 24 labeled **"MASCAL Surge →"** — this is where the model detects a sudden spike in demand
- **How to read it:** Before hour 24, consumption is steady and low. At hour 24, a mass-casualty event occurs and consumption spikes dramatically. The LSTM model's predicted line closely tracks the actual line, showing it can detect the surge.

**2. Three Metric Cards**

| Card | What It Shows |
|---|---|
| **LSTM R²** | R-squared score — how well the LSTM predictions match the actual data (1.0 = perfect, 0.0 = no better than average) |
| **LSTM MSE** | Mean Squared Error — average prediction error (lower is better) |
| **Purpose** | "Surge Detection" |

**3. Info Box**
- "💡 LSTM tracks consumption trends over time. XGBoost predicts per-item demand. Together they provide complete AI coverage."

**If the data files are missing:** "⚠️ LSTM files not found. Make sure lstm_actual.npy, lstm_preds.npy, lstm_hours.npy are in the mmsai folder."

**Real-life scenario:** A logistician is reviewing the LSTM chart and sees that the model successfully predicted a consumption spike at hour 24. This tells them that if a MASCAL event happens, they can expect tourniquet usage to triple within hours. They use this insight to pre-position extra tourniquets at Role 1 stations before an operation.

---

## 8. Tab 5: ⏱️ Hours of Supply

### Who Can Access: All roles

### Purpose

Shows a live, color-coded view of how many hours of supply remain for every item. This is the fastest way to see what's running critically low.

### What You See (No Buttons — Auto-Loaded)

**1. Five Tier-Count Cards**

| Card | Color | Meaning |
|---|---|---|
| **GREEN** | Green | Items with 24+ hours of supply — safe |
| **TEAL** | Teal | Items with 12–24 hours — draft resupply |
| **AMBER** | Amber/Orange | Items with 6–12 hours — escalate to commander |
| **RED** | Red | Items with 2–6 hours — emergency resupply needed |
| **PURPLE** | Purple | Items with less than 2 hours — critical, commander alert |

Each card shows how many items fall into that tier.

**2. Horizontal Bar Chart — "Hours of Supply per Item"**
- One bar per item, showing hours of supply
- Bars colored by tier (GREEN/TEAL/AMBER/RED/PURPLE)
- Three dashed vertical reference lines:
  - **Red dashed line at 2h** labeled "Critical 2h" — anything left of this is PURPLE
  - **Amber dashed line at 6h** labeled "AMBER 6h"
  - **Green dashed line at 24h** labeled "GREEN 24h"
- Text labels on each bar showing the exact hours (e.g., "12.3h")

**Real-life scenario:** A medic opens the Hours of Supply tab and sees the PURPLE card shows 2 — two items have less than 2 hours of supply. Looking at the chart, they see Morphine (0.5h) and Ketamine (1.2h) in purple. Both are critical pain medications. They immediately request resupply from the forward surgical team.

---

## 9. Tab 6: 🗺️ Cross-Echelon Map

### Who Can Access: Logisticians (Role 3) only

### Purpose

Shows a geographic view of the supply chain — where the medical facilities are, their supply status, and what resupply is in transit.

### What You See (No Buttons — Auto-Loaded)

**Left Side: Geographic Map**
- A world map with three markers:
  - **R1-ALPHA** (Role 1 — front line) — colored by its average hours-of-supply tier
  - **R2-BRAVO** (Role 2 — forward surgical team) — colored by its tier
  - **R3-CHARLIE** (Role 3 — combat support hospital) — colored by its tier
- Grey lines connecting the nodes, showing the supply chain flow
- Hover over a marker to see: node name, role, average hours of supply, tier

**Right Side: Node Status Cards**
- One card per node, with a colored left border matching the tier
- Shows the node's role, average HoS, and tier

**Below: Resupply Pipeline**
- Shows items currently in transit between nodes, e.g.:
  - "🚛 In Transit IV Fluids x50 R3-CHARLIE → R2-BRAVO · ETA: 2h"
  - "📦 Packed Tourniquets x20 R2-BRAVO → R1-ALPHA · ETA: 45min"

**Note:** The map uses hardcoded coordinates and randomly generated HoS values. The values change each time you refresh the page. This tab is a visualization concept — it shows what the supply chain map would look like when connected to live data.

**Real-life scenario:** A logistician checks the map and sees R1-ALPHA in red (critical supply level). The resupply pipeline shows tourniquets are in transit from R2-BRAVO with a 45-minute ETA. They verify the resupply will arrive in time, but also check if they need to expedite additional supplies.

---

## 10. Tab 7: ✅ Validation Scenarios

### Who Can Access: Logisticians (Role 3) only

### Purpose

Automated test scenarios that verify the system's alerts, AI predictions, and audit logging work correctly. Think of it as a built-in quality check.

### Three Sub-Tabs

#### Scenario 1: Low Stock Alert

**Button:** **"▶️ Run Scenario 1"**

**What it does:** Simulates 12 tourniquet uses (item ITM004, CAT Tourniquet) by repeatedly calling the /scan endpoint. A progress bar shows the simulation running.

**Output:**
- A results table showing each use:
  - Use # (1–12)
  - Stock After (decreasing from current stock)
  - Alert (True/False — becomes True when stock hits the threshold)
  - Message (shows the alert message when it triggers)
- **PASS** (green): "✅ PASS — LOW STOCK alert fired correctly" — if the alert triggered at some point
- **Warning** (amber): "Stock still above threshold…" — if stock never hit the threshold

**Real-life meaning:** This confirms that when a critical item like a tourniquet runs low, the system will alert you. If this test fails, there's a bug in the alert logic that could cause you to miss a critical shortage.

#### Scenario 2: MASCAL Surge

**Inputs:** Four sliders (same as XGBoost Forecast): Operational Tempo, T1 Severe, T2 Moderate, T3 Minor

**Button:** **"▶️ Run MASCAL Forecast"**

**What it does:** Runs the XGBoost forecast with the given parameters, then checks if any items are predicted to enter RED or PURPLE tiers.

**Output:**
- Horizontal bar chart of all items, colored by tier
- If items are in RED/PURPLE: **"⚠️ N items in RED/PURPLE — emergency resupply needed!"** (red error) + table of those items
- **"✅ PASS — Surge correctly detected and tiered"** (green success) — confirms the AI can identify critical shortages during a surge

**Real-life meaning:** This verifies that when you set high operational tempo and triage ratios, the AI correctly identifies which items will run critically low. If this test passes, you can trust the XGBoost forecast during real operations.

#### Scenario 3: Controlled Drug Audit

**Button:** **"▶️ Run Scenario 3"**

**What it does:** Simulates 5 morphine uses (ITM001, Morphine 10mg/ml) by 5 different named clinicians, then checks the audit log to verify all uses were recorded.

**Output:**
- A results table:
  - # (1–5)
  - Clinician (name of the person who used the morphine)
  - Stock After (decreasing)
- Then it fetches the audit log, filters for morphine entries, and shows:
  - Count of morphine audit entries
  - Table of entries (first 10)
  - **"✅ PASS — All N morphine uses recorded in audit log"** (green success)

**Real-life meaning:** Morphine is a controlled drug. In military medicine, every dose must be accounted for — who gave it, who received it, when, and how much. This test confirms the system maintains a complete, traceable audit trail. If it fails, there's a gap in controlled-drug accountability.

---

## 11. Tab 8: 📋 Audit Log

### Who Can Access: All roles

### Purpose

Shows the complete audit trail of every usage event in the system. This is essential for controlled-drug accountability (morphine, ketamine, fentanyl) and for reconstructing what happened during an operation.

### Buttons

| Button | What It Does |
|---|---|
| **🔄 Refresh** | Reloads the audit log from the API |
| **"📥 Download CSV"** (green) | Downloads the audit log as a CSV file named `audit_log.csv` |

### What You See

A table showing the last 100 audit events, sorted by most recent first:

| Column | Meaning |
|---|---|
| **event_type** | Type of event (SCAN for usage logging, or a clinical event type like GSW, BLAST) |
| **item_id** | The item's unique ID |
| **item_name** | The item's name |
| **qty_used** | How many units were used |
| **timestamp** | When the event occurred (YYYY-MM-DD HH:MM:SS) |
| **user** | Who logged the event |
| **controlled** | Whether the item is a controlled drug (True/False) |

Below the table: **"Total events: {n}"**

**If empty:** "No events logged yet."

**Real-life scenario:** After a firefight, the medical unit needs to account for all controlled drugs used. The logistician opens the Audit Log tab, sees 8 morphine uses by 3 different medics over 2 hours, and clicks Download CSV to attach to the after-action report. The CSV shows exactly who used what and when.

---

## 12. Tab 9: 🪖 Digital Twin (LSCO)

### Who Can Access: All roles

### Purpose

The Digital Twin is a **synthetic simulation** that models a 30-day Large-Scale Combat Operation. It compares two resupply strategies — **static** (fixed-order, pre-planned) and **dynamic** (AI-predicted, adaptive) — to show which one keeps more supplies flowing to casualties.

The simulation includes realistic disruptions:
- Mass-casualty surges (sudden spike in casualties)
- Cold-chain failures (blood and temperature-sensitive drugs spoil)
- Theatre depot strikes (the main supply depot is destroyed)
- Walking blood bank operations (fresh blood from walking donors)
- DDIL order loss (communications disrupted, orders don't go through)

### Section A: Scenario Controls & Simulation

**Header:** "Large-Scale Combat Operations Digital Twin"

**Controls:**

| Control | Type | Range | Default | What It Means |
|---|---|---|---|---|
| **Casualties per day** | Number input | 100–10,000 | 2,000 | How many casualties arrive per day in the theatre of operations |
| **Simulation days** | Number input | 1–60 | 30 | How many days to simulate |
| **Evacuation delay multiplier** | Slider | 0–5 | 1.0 | Multiplier for how long it takes to evacuate casualties from Role 1 to Role 2/3. Higher = slower evacuation = more demand piles up at front line. |
| **Resupply delay multiplier** | Slider | 0–5 | 1.0 | Multiplier for how long resupply orders take to arrive. Higher = slower resupply = more stockouts. |
| **National stock (days)** | Slider | 0–365 | 30 | How many days of stock the national warehouse starts with |
| **Orders lost % (DDIL)** | Slider | 0–100 | 0 | Percentage of resupply orders that are lost due to Degraded, Disrupted, Interrupted, and Limited communications |
| **Mass-casualty surge** | Selectbox | None / At hour 72 / At hour 240 | At hour 72 | When a mass-casualty surge occurs (2.5× casualty rate) |
| **Cold-chain failure at Role 2E (hour 120)** | Checkbox | — | Off | If checked, the cold storage at all Role 2E facilities fails at hour 120, destroying all blood and temperature-sensitive items there |
| **Walking blood bank (units/day per R2E)** | Slider | 0–120 | 0 | How many fresh blood units per day each Role 2E receives from walking donors |
| **Theatre depot struck (hour 168)** | Checkbox | — | Off | If checked, the theatre depot is destroyed at hour 168, cutting off the main supply line |
| **Enable ABO/Rh blood group constraints** | Checkbox | — | Off | Would limit walking blood bank output by blood type compatibility (see Known Limitations) |
| **Enable donor pool attrition** | Checkbox | — | Off | Would model donor loss from casualties, rotation, and illness over time (see Known Limitations) |

**Button:**

| Button | What It Does |
|---|---|
| **"Run static vs dynamic simulation"** | Sends all parameters to the API and runs both policies through the hourly simulation engine |

**Output after clicking "Run static vs dynamic simulation":**

1. **Classification disclaimer:** "synthetic scenario result; not real-demand evidence"

2. **Scenario assumptions caption:** Shows casualties/day, triage mix (20% T1 / 30% T2 / 50% T3), days, and planning basis

3. **Daily demand cross-check table:** "Planned daily consumption at this casualty rate" — shows how many units per day each item category needs. At 2,000 casualties/day:
   - THEATRE_PACK: 1,660/day
   - ANAES_SET: 1,440/day
   - BLOOD_UNIT: 4,000/day
   - HAEM_SET: 1,000/day
   - ANTIBIOTIC: 1,000/day
   - ANALGESIA: 2,000/day
   - DRESSING: 2,000/day

4. **Grouped bar chart — "Demand fill rate by item"**: Shows fill rate percentage (how much demand was met) for each item, grouped by policy (static vs dynamic). Higher bars = better. Dynamic should generally outperform static.

5. **First stock-out day table**: Shows which day each item runs out for each policy. Lower numbers = sooner = worse. This tells you when to expect supply failures.

6. **Bar chart — "Dynamic-policy fill rate by echelon"**: Shows fill rate by role (R1, R2E, R3). Helps you see which echelon is struggling most.

**Real-life scenario:** A logistician wants to test whether their current supply plan will hold up during a planned 30-day operation with 2,000 casualties/day and a surge at hour 72. They set the parameters and click Run. The simulation shows that blood units stock out on day 2 under the static policy but the dynamic policy maintains a 99.7% fill rate. They also enable the cold-chain failure at hour 120 and re-run — now the dynamic policy also shows blood stockouts, suggesting they need a backup blood supply plan.

### Section B: Hours-of-Supply Snapshot

**Header:** "Synthetic Hours-of-Supply by node (simulator)"

| Control | Type | What It Does |
|---|---|---|
| **Snapshot hour** | Slider (0–719) | Which hour of the simulation to view (default 96 = day 4) |
| **Echelon** | Selectbox (All/R1/R2E/R3) | Filter by echelon level |

**Button:**

| Button | What It Does |
|---|---|
| **"Load HoS snapshot"** | Shows the hours-of-supply for every node and item at the selected hour |

**Output:**
- A table with columns: **node, level, item, stock, hos (hours of supply), tier**
- Sorted by hos ascending (worst first)
- A caption summarizing tier counts with actions, e.g.: "Tiers per PID §9.3 · PURPLE: 8 (Commander alert; lateral redistribution) · RED: 5 (Emergency resupply; Role 3 CO alerted) · AMBER: 12 (Escalate to FST commander / MO)"

**If no data at that hour:** "No forward demand at this hour for the selected echelon."

**Real-life scenario:** A logistician sets the snapshot to hour 120 (when the cold-chain failure happens) and selects R2E. The table shows blood units at 0.0 hours of supply (PURPLE) at multiple R2E nodes — confirming the cold-chain failure destroyed the blood supply. They now know they need the walking blood bank activated before hour 120.

### Section C: Live Forecast for Current Inventory

**Header:** "Dynamic forecast for current inventory"

This section auto-loads when you open the Digital Twin tab — no button needed.

| Control | Type | Options | Default |
|---|---|---|---|
| **Forecast horizon (hours)** | Select slider | 6, 12, 24, 48, 72, 168 | 24 |

**How it works:** The system looks at your real inventory (from MongoDB) and the last 72 hours of usage events (from the audit log). It uses a dual EWMA (Exponentially Weighted Moving Average) model to predict future consumption — if there's been a recent spike in usage, the forecast adjusts upward; if usage has been quiet, it falls back to the baseline rate.

**Output:**
- Caption showing generation timestamp and classification
- A table sorted worst-first (lowest hours of supply at top):

| Column | Meaning |
|---|---|
| **item_id** | Item ID |
| **item_name** | Item name |
| **current_stock** | Current stock level |
| **predicted_rate** | Predicted consumption rate (units/hour) |
| **expected_qty** | Expected quantity needed in the forecast horizon |
| **hours_of_supply** | How many hours the item will last |
| **hos_tier** | Color-coded tier |
| **observed_consumption_72h** | Actual usage in the last 72 hours |
| **source** | "recent_audit_activity" (if there's recent usage data) or "inventory_baseline" (if no recent usage, using baseline rate) |

- A caption listing the tier actions and naming the lowest item

**Real-life scenario:** A medic opens the Digital Twin tab and the live forecast auto-loads. They see that Morphine has 8 hours of supply (AMBER tier) with a predicted rate of 0.5 units/hour and 4 units used in the last 72 hours. The source says "recent_audit_activity" — meaning the forecast is based on real recent usage, not just a default rate. They know to request more morphine soon.

### Section D: Monte Carlo Validation

**Header:** "Monte Carlo Validation (Nye blood model benchmark)"

**Controls:**

| Control | Type | What It Does |
|---|---|---|
| **Number of runs** | Slider (10–200) | How many simulation iterations to run (default 50) |
| **Policy** | Selectbox (dynamic/static) | Which policy to test |

**Button:**

| Button | What It Does |
|---|---|
| **"Run Monte Carlo validation"** | Runs the simulation N times with different random seeds to see how stable the results are |

**Output after clicking "Run Monte Carlo validation":**

**Notice — free-tier run cap:** Because the app runs on free hosting with limited compute, the server automatically caps the number of runs to stay within time limits. For example, requesting 50 runs may complete only 20. You will see an info banner:
> "ℹ run count capped to fit free-tier compute limits: requested 50 runs, completed 20 to stay within free-hosting time limits."

This is expected behavior — the results are still statistically valid.

**1. Three Metric Cards**

| Card | Example Value | What It Means |
|---|---|---|
| **Median Fill Rate** | 99.6% (p5: 99.6% – p95: 99.7%) | Across all simulation runs, the median percentage of demand that was met. The p5–p95 range shows how much it varies. |
| **Blood Stock-out Day (median)** | 2.0 (p5: 2.0 – p95: 3.1) | The median day when blood units run out across all runs. p5 and p95 show the range of outcomes. |
| **First Stock-out Day (median)** | 1.0 (p5: 1.0 – p95: 1.1) | The median day when any item first runs out. |

**2. Fill Rate Distribution Histogram**
- Title: "Monte Carlo distribution of fill rate (N runs, dynamic policy)"
- Blue bars showing how many runs fell into each fill-rate bucket
- A red dashed vertical **Median** line
- X-axis: Fill rate (%), Y-axis: Count
- **How to read it:** A tight cluster of bars near 99.6% means the results are consistent and reliable across different random seeds.

**3. Blood Stock-out Day Distribution Histogram**
- Title: "Distribution of first blood stock-out day across runs"
- Red bars showing which day blood units ran out in each simulation run
- **How to read it:** If most bars are at day 2, blood consistently runs out on day 2 regardless of randomness — that's a robust finding.

**4. Validation Interpretation**
- ✅ **Robust finding** (green): "Day-2.0 blood stock-out is a robust finding: 95% of runs stock out by day 3.1. This validates the PID §4.2 blood constraint." — shown when p5 ≤ 2 and median ≤ 4
- ⚠️ **Warning** (amber): shown when blood stock-out timing is variable across runs

**5. Results Table**
- Shows first 20 individual runs with columns: blood_stockout_day, first_stockout_day, overall_fill_rate_pct, run

**Real-life meaning:** The Monte Carlo validation proves that the day-2 blood stockout finding is not a one-off result — it's a reliable prediction that holds up across many different random scenarios. A logistician can trust the simulation's warning that blood will run critically low by day 2 and plan accordingly.

---

## 13. Hours-of-Supply Tier System

The tier system is the backbone of the entire application. Every item at every echelon is assigned a tier based on how many hours of supply remain:

| Tier | Hours of Supply | Color | What It Means | Recommended Action |
|---|---|---|---|---|
| **GREEN** | 24+ hours (or unlimited) | 🟢 Green | Safe — plenty of supply | Monitor (full readiness) |
| **TEAL** | 12–24 hours | 🔵 Teal | Adequate but watch | Draft resupply for logistician review (12–24h) |
| **AMBER** | 6–12 hours | 🟠 Amber/Orange | Getting low | Escalate to FST commander / Medical Officer (6–12h) |
| **RED** | 2–6 hours | 🔴 Red | Critical — will run out soon | Emergency resupply; Role 3 CO alerted (2–6h) |
| **PURPLE** | Less than 2 hours | 🟣 Purple | Almost out | Commander alert; lateral redistribution (<2h) |

### How it's calculated

```
Hours of Supply = Current Stock ÷ Consumption Rate (units per hour)
```

If the consumption rate is 0 (item not being used), HoS = 999 (GREEN — unlimited).

The consumption rate comes from either:
- The item's `avg_consumption_per_hour` baseline (stored in the database)
- The XGBoost model's prediction (when using the Forecast tab)
- The EWMA model's prediction (when using the Live Forecast)

---

## 14. Behind the Scenes — The API

The Flask API (`app.py`) runs on Render and provides all the data. Here's what each endpoint does:

| Endpoint | Method | What It Does | Used By |
|---|---|---|---|
| `/` | GET | Health check — returns `{"status":"MMLS-AI API running","version":"2.0"}` | Render health check |
| `/inventory` | GET | Returns all items with live HoS, tier, alert status, and expiry warning | Inventory tab, Search tab |
| `/scan` | POST | Records item usage — decrements stock, writes audit entry | Search tab "Record Usage", Validation scenarios |
| `/clinical_event` | POST | Records a clinical event (e.g., GSW, BLAST) — auto-decrements multiple items | Not exposed in dashboard (API only) |
| `/forecast` | GET | Runs XGBoost prediction with given tempo/triage parameters | XGBoost Forecast tab, Validation Scenario 2 |
| `/hours_of_supply` | GET | Returns HoS for every item | Hours of Supply tab |
| `/audit_log` | GET | Returns last 100 audit events | Audit Log tab, Validation Scenario 3 |
| `/register_item` | POST | Registers a new item in inventory | Search tab "Add to Inventory" |
| `/delete_items` | POST | Deletes items by ID | Inventory tab "Delete Items" |
| `/reset` | POST | Wipes all inventory and audit data | Not exposed in dashboard (API only) |
| `/twin/simulate` | GET | Runs the 30-day static vs dynamic simulation | Digital Twin tab Section A |
| `/twin/hos` | GET | Returns HoS snapshot at a specific simulation hour | Digital Twin tab Section B |
| `/twin/live-forecasts` | GET | Returns live demand forecast from real inventory + recent usage | Digital Twin tab Section C |
| `/twin/monte-carlo` | GET | Runs the simulation N times with different seeds and returns fill rate distribution, blood stock-out statistics, and validation result | Digital Twin tab Section D |

### The Clinical Event Map

The `/clinical_event` endpoint maps clinical events to the medical items they consume. This is how the system would auto-decrement inventory when a specific type of casualty arrives:

| Event | Items Consumed |
|---|---|
| **GSW** (Gunshot Wound) | 2× Tourniquet, 1× TXA, 2× IV Cannula, 1× Chest Seal |
| **BLAST** | 3× Tourniquet, 2× TXA, 1× IV Fluid, 1× ETT |
| **HAEMORRHAGE** | 2× Tourniquet, 1× TXA, 1× pRBC |
| **INTUBATION** | 1× ETT, 1× IV Cannula, 1× Syringe 10ml |
| **BURN_MINOR** | 2× Burn Dressing, 1× Decomp Needle |
| **BURN_MAJOR** | 4× Burn Dressing, 2× Decomp Needle, 1× IV Fluid |
| **FRACTURE** | 1× Splint, 1× Decomp Needle, 1× IV Cannula |
| **CARDIAC** | 1× IV Fluid, 2× IV Cannula, 1× Syringe 2ml |
| **ANAPHYLAXIS** | 1× IV Fluid, 1× Syringe 2ml |
| **CRUSH** | 2× Tourniquet, 1× IV Fluid, 2× IV Cannula |
| **AMPUTATION** | 3× Tourniquet, 2× TXA, 1× pRBC |
| **CHEST_TRAUMA** | 1× Chest Seal, 1× Blood Giving Set, 1× IV Cannula |
| **TBI** | 1× IV Fluid, 2× IV Cannula, 1× Syringe 2ml |
| **CBRN** | 2× Decomp Needle, 2× IV Cannula, 1× IV Fluid |
| **POLYTRAUMA** | 3× Tourniquet, 2× TXA, 1× pRBC, 1× IV Fluid |

---

## 15. Real-Life Medical Scenarios

### Scenario 1: Frontline Tourniquet Usage

**Situation:** A medic at a Role 1 Battalion Aid Station treats a casualty with a severed femoral artery from an IED blast.

**Steps in MMLS-AI:**
1. **Login** as `medic01` / `medic123`
2. Go to **🔍 Medicine Search** tab
3. Type "tourniquet" and click **"🔍 Search & Look Up"**
4. System finds CAT Tourniquet (ITM004) in inventory — shows current stock = 20, HoS = GREEN
5. Enter **Quantity Used = 1**, User ID defaults to "medic01"
6. Click **"✅ Record Usage"**
7. System shows: **"✅ Recorded — New stock: 19"**
8. An audit entry is written: event_type=SCAN, item_id=ITM004, qty=1, user=medic01, timestamp=now

**What happens behind the scenes:**
- Stock decreases from 20 to 19
- Audit log records: who (medic01), what (tourniquet), when (timestamp), how much (1)
- If stock drops to the alert threshold (e.g., 5), the system shows "⚠️ LOW STOCK"
- The Live Forecast in the Digital Twin tab will pick up this usage event and adjust the demand prediction

### Scenario 2: Surge Planning Before an Offensive

**Situation:** A surgeon at a Role 2 Forward Surgical Team is planning for an upcoming offensive expected to generate 500 casualties/day with heavy T1 (severe) cases.

**Steps in MMLS-AI:**
1. **Login** as `surgeon01` / `surgeon123`
2. Go to **🤖 XGBoost Forecast** tab
3. Set **Operational Tempo = 0.8** (high-intensity combat)
4. Set **T1 Severe = 0.35** (expecting many life-threatening casualties)
5. Set **T2 Moderate = 0.25**, **T3 Minor = 0.15**
6. Click **"🤖 Run XGBoost Forecast"**

**What you see:**
- Bar chart shows BLOOD_UNIT in red (predicted rate: 6.2 u/hr, HoS: 8 hours = AMBER)
- THEATRE_PACK in amber (predicted rate: 2.1 u/hr, HoS: 10 hours = AMBER)
- Feature importance image shows that operational_tempo and T1 are the most important factors

**Action taken:** The surgeon alerts the logistician that blood and theatre packs will run critically low within 8–10 hours of the offensive starting. The logistician arranges emergency resupply.

### Scenario 3: Mass-Casualty Event Detection

**Situation:** During sustained operations, a mass-casualty event occurs at hour 24 of an operation. Multiple casualties arrive simultaneously.

**What MMLS-AI shows:**
1. Go to **📈 LSTM Trend** tab
2. The chart shows consumption was steady at ~5 units/hour for the first 24 hours
3. At hour 24, the "MASCAL Surge →" marker appears — actual consumption spikes to 25+ units/hour
4. The LSTM predicted line (red dashed) closely tracks the actual spike, showing the model detected the surge
5. The R² metric shows the model's prediction accuracy

**Action taken:** The LSTM confirms the surge pattern. The logistician now knows to watch for this pattern in live data — if the Live Forecast's predicted rate suddenly exceeds 2× the baseline, a MASCAL event may be happening.

### Scenario 4: Cold-Chain Failure During Operations

**Situation:** A generator failure at a Role 2E facility destroys all stored blood at hour 120 of a 30-day operation.

**Steps in MMLS-AI:**
1. Go to **🪖 Digital Twin** tab
2. Set casualties/day = 2000, days = 30
3. Check **"Cold-chain failure at Role 2E (hour 120)"**
4. Set **Walking blood bank = 40 units/day** (to compensate)
5. Click **"Run static vs dynamic simulation"**

**What you see:**
- The daily demand table shows 4,000 blood units needed per day
- The fill-rate chart shows blood fill rate dropping after hour 120 under the static policy
- The dynamic policy recovers faster because it adjusts order rates
- The first stock-out table shows blood stockouts occur earlier under both policies
- The echelon chart shows R2E has the lowest fill rate (it lost its blood supply)

**Action taken:** The logistician realizes that 40 units/day from the walking blood bank isn't enough to fully compensate for the cold-chain failure. They plan to pre-position additional cold storage backup at R2E facilities and arrange emergency blood airlift.

### Scenario 5: Controlled Drug Accountability

**Situation:** After a 12-hour operation, the medical unit must account for all controlled drugs used.

**Steps in MMLS-AI:**
1. **Login** as `logistic01` / `admin123` (Logistician, full access)
2. Go to **📋 Audit Log** tab
3. Click **"🔄 Refresh"** to get the latest entries
4. The table shows all events, including morphine, ketamine, and fentanyl uses
5. Filter visually for controlled = True entries
6. Click **"📥 Download CSV"** to export the full audit trail

**What the CSV contains:**
- Every event with timestamp, user, item, quantity
- The medical officer can verify that every dose of morphine was used by an authorized clinician
- Any discrepancy (e.g., a dose with no corresponding patient record) would be flagged for investigation

### Scenario 6: Registering a New Medical Item

**Situation:** A forward surgical team receives a new type of haemostatic dressing (e.g., QuikClot Combat Gauze) that isn't in the system yet.

**Steps in MMLS-AI:**
1. Go to **🔍 Medicine Search** tab
2. Select **"🩺 Medical Equipment"** radio button
3. Type "QuikClot" in the search box
4. Click **"🔍 Search & Look Up"**
5. System doesn't find it in inventory — searches BST NSN catalog
6. Finds QuikClot in the BST catalog with NSN and specifications
7. Blue box shows: "🌐 Info Found Online" with source badge "BST NSN Database"
8. Registration form auto-fills with the found data
9. Fill in: **Assign AI Echelon = Role2**, **Initial AI Stock = 30**, **Category = Haemorrhage Control**
10. Click **"💾 Add to Inventory"**
11. System shows: 🎉 + **"✅ QuikClot Combat Gauze added to MMLS-AI inventory!"**

**What happened:** The item is now in the database with its NSN, specifications, echelon assignment, and initial stock. It will appear in the Inventory tab and be included in all forecasts and the live digital twin forecast.

---

## 16. Known Limitations

These are important to know so you don't rely on features that don't work as expected:

1. **Monte Carlo run count is capped on free hosting.** The `/twin/monte-carlo` endpoint works correctly, but Render's free tier has limited compute time. If you request more runs than the server can complete within its time budget, it automatically reduces the run count and shows an info banner (e.g., "requested 50 runs, completed 20"). Results are still statistically valid — just with a smaller sample.

2. **Blood grouping and donor attrition checkboxes have no effect.** The "Enable ABO/Rh blood group constraints" and "Enable donor pool attrition" checkboxes are sent to the API, but the backend silently ignores them. The simulator has no blood-grouping or donor-attrition logic implemented yet.

3. **No camera/QR scanning.** Despite the module docstring mentioning "Real QR camera scanner", the search box is a manual text entry field. There is no camera integration or barcode scanning.

4. **Cross-Echelon Map uses random data.** The map tab generates random hours-of-supply values each time the page loads. It is not connected to live inventory data. Values will change on every refresh.

5. **LSTM view is static.** The LSTM tab loads pre-computed `.npy` data files (actual values, predictions, timestamps). It does not run the LSTM model live — it displays a fixed example of a MASCAL surge detection. The `lstm_model.keras` file exists but is not loaded by the dashboard.

6. **`/reset` and `/clinical_event` are not accessible from the dashboard.** These API endpoints exist but no button in the dashboard UI calls them. They are only reachable via direct API calls.

7. **No server-side authentication.** The login is client-side only (the `USERS` dictionary in the dashboard). The API endpoints have no authentication — anyone who can reach the API URL can read or modify inventory, including the destructive `/reset` endpoint.

8. **All simulation outputs are synthetic.** The digital twin uses placeholder casualty-to-consumption factors from BST PID v0.2. They are not validated clinical planning factors. The outputs are for planning exploration only, not operational decisions.

---

## Appendix: The 20 Standard Medical Items

The system ships with these items pre-loaded in the inventory:

| ID | Item | Category | Controlled? |
|---|---|---|---|
| ITM001 | Morphine 10mg/ml | Analgesia | Yes |
| ITM002 | Ketamine 500mg | Analgesia | Yes |
| ITM003 | Fentanyl 100mcg | Analgesia | Yes |
| ITM004 | CAT Tourniquet | Haemorrhage Control | No |
| ITM005 | Chest Seal (Vented) | Resuscitation | No |
| ITM006 | TXA 1g/10ml | Haemorrhage Control | No |
| ITM007 | pRBC O-Negative | Blood | No |
| ITM008 | IV Fluid 500ml | Resuscitation | No |
| ITM009 | IV Cannula 18G | Resuscitation | No |
| ITM010 | ETT Size 7.0 | Airway | No |
| ITM011 | Blood Giving Set | Blood | No |
| ITM012 | Syringe 10ml | General | No |
| ITM013 | Syringe 2ml | General | No |
| ITM014 | Surgical Gloves | General | No |
| ITM015 | Decomp Needle 14G | Resuscitation | No |
| ITM016 | Cric Kit | Airway | No |
| ITM017 | QuikClot Dressing | Haemorrhage Control | No |
| ITM018 | Burn Dressing (Large) | Burn Care | No |
| ITM019 | Eye Shield | General | No |
| ITM020 | Sam Splint | Orthopaedic | No |

Each item has a corresponding QR code image in the `qr_codes/` folder, though the QR scanning feature is not implemented (see Known Limitations).

---

*This documentation is based on the MMLS-AI v2.0 codebase as deployed at https://mmls-ai-dashboard.onrender.com. The system is a proof-of-concept for military medical logistics AI and should not be used as the sole source of operational planning decisions.*
