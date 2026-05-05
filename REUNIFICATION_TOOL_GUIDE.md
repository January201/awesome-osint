# Humanitarian Reunification Tool Guide
## Top 10 OSINT Tools: Exact Output Examples for Finding Lost Family

> **Note:** All examples below are simulated outputs demonstrating how these tools reveal connections in a humanitarian context.  
> **Safety Warning:** Never expose real data of vulnerable refugees in public logs or unsecured channels.

---

## 1️⃣ **SHERLOCK** - Username Search (Non-API)

**Use Case:** Finding displaced persons who created new social media accounts in host countries using old usernames.

### **Input:**
```bash
sherlock "ahmed_hassan_95"
```

### **Output You Get:**
```
[*] Checking username ahmed_hassan_95 on 300+ sites...

✓ FOUND on Facebook:
   https://facebook.com/ahmed.hassan.95 
   Profile Picture: [Matches uploaded photo]
   Location: Berlin, Germany
   Bio: "Syrian refugee. Looking for family from Homs."
   Last Active: 2 days ago

✓ FOUND on WhatsApp:
   Number Linked: +49-151-XXXX-XXXX
   Profile Pic: [Same as Facebook]
   Status: "Alive and safe in Berlin. Contact Red Cross."

✓ FOUND on Telegram:
   https://t.me/ahmed_h_95 
   Groups: "Syrians in Berlin", "Homs Missing Persons"
   Last Seen: Recently

✓ FOUND on Ukraine Refugees Support Forum:
   Thread: "Looking for siblings - Ahmed Hassan"
   Posted: 2024-01-15
   Contact Email: a.hassan.temp@protonmail.com

✗ NOT FOUND on: Instagram, TikTok, Twitter

SUMMARY:
Total Sites Checked: 300+
Accounts Found: 4
Time Taken: 14.2 seconds
ACTION: Contact via Telegram or Red Cross intermediary.
```

### **File Output:**
- `ahmed_hassan_95.txt` - List of found profiles with URLs
- `ahmed_hassan_95.csv` - Structured data for case management

---

## 2️⃣ **TINEYE** - Reverse Image Search (Non-API / Freemium)

**Use Case:** Matching photos of lost children against news articles, NGO reports, and "found person" databases.

### **Input:**
```
Upload: lost_child_photo.jpg
Search: Internet-wide (News, Social, Archives)
```

### **Output You Get:**
```
🖼️ REVERSE IMAGE SEARCH RESULTS

MATCH STATISTICS:
├─ Total Matches Found: 12
├─ Oldest Match: 2022-05-10 (Original Upload)
├─ Newest Match: 2024-03-01
└─ Domains: 8

TOP MATCHES:

1. [EXACT MATCH 100%]
   URL: https://unhcr.org/stories/found-children-may-2022 
   Context: UNHCR Article "Children Reunited at Border"
   Date: 2022-05-15
   Caption: "Child identified as A.H. reunited with aunt in Poland."
   Significance: CONFIRMS SURVIVAL & LOCATION

2. [CROPPED MATCH 95%]
   URL: https://facebook.com/PolandRefugeeSupport/posts/12345 
   Context: Volunteer Group Post
   Date: 2022-05-12
   Caption: "Found child at border checkpoint, looking for family."
   Comments: 45 (Includes potential witness contacts)

3. [SIMILAR 85%]
   URL: https://icrc.org/restoring-family-links 
   Context: ICRC Database Thumbnail (Access Restricted)
   Note: Requires caseworker login to view full details.

USAGE ANALYSIS:
├─ News Articles: 2 instances
├─ NGO Reports: 1 instance
├─ Social Media: 8 instances
└─ Forums: 1 instance

COPYRIGHT/PRIVACY:
⚠️ Image appears in restricted ICRC database.
ACTION: Contact ICRC Restoring Family Links with Case Ref: POL-2022-889
```

### **File Output:**
- `tineye_report.html` - Visual report with thumbnails
- `matches.csv` - URLs and dates for case file

---

## 3️⃣ **PHONEINFOGA** - Phone Intelligence (Non-API / Local)

**Use Case:** Checking if a lost relative's old phone number is still active, ported, or linked to a new identity.

### **Input:**
```bash
phoneinfoga scan -n +380671234567
```

### **Output You Get:**
```
📞 PHONE NUMBER ANALYSIS: +380-67-123-4567

BASIC INFORMATION:
├─ Country: Ukraine
├─ Carrier: Kyivstar (Original)
├─ Line Type: Mobile
└─ Valid: Yes

CURRENT STATUS:
├─ Active: ✓ Yes
├─ Roaming: ✓ Yes (Country: Poland)
├─ Ported: ✓ Yes (New Carrier: Orange PL)
└─ Last Activity: 2024-04-01

GEOLOCATION:
├─ Current Network: Poland
├─ Timezone: Europe/Warsaw
└─ Approximate Location: Warsaw Metro Area

SOCIAL MEDIA LINKS:
✓ Found on WhatsApp (Profile Pic Updated: 2 weeks ago)
✓ Found on Telegram (Username: @lena_k_ua)
✗ Not found on Viber

ADDITIONAL INFO:
├─ Number Age: ~6 years
└─ Port Date: 2022-03-10 (Likely fled conflict)

RECOMMENDATION:
Number is ACTIVE in Poland.
DO NOT call directly (security risk).
Send WhatsApp message via Red Cross intermediary.
```

---

## 4️⃣ **EXIFTOOL** - Metadata Extractor (Non-API / Local)

**Use Case:** Extracting GPS coordinates and device info from the last known photo of a missing person.

### **Input:**
```bash
exiftool last_seen_photo.jpg
```

### **Output You Get:**
```
File Name                       : last_seen_photo.jpg
Date/Time Original              : 2022:02:24 09:15:33
Make                            : Samsung
Camera Model                    : Galaxy S10

GPS LOCATION (CRITICAL):
├─ GPS Latitude                 : 50° 27' 12.4" N
├─ GPS Longitude                : 30° 31' 24.8" E
├─ GPS Altitude                 : 150 m
└─ Location: Kyiv, Ukraine (Specific District: Podilskyi)

SOFTWARE:
├─ Software                     : Android 11
└─ Modified                     : No (Original File)

USER INFO:
├─ Artist                       : Olena Kovalenko
└─ Copyright                    : © 2022 OK

ACTION:
Coordinates place subject in Kyiv at time of photo.
Cross-reference with evacuation routes from Podilskyi district on 2022-02-24.
```

> **Warning:** Strip GPS data before sharing photos publicly to prevent tracking by hostile actors.

---

## 5️⃣ **MALTEGO** - Visual Intelligence (API Required)

**Use Case:** Mapping relationships between family members, NGOs, and locations.

### **Input:**
```
Target: "Kovalenko Family"
Transforms: Person → Social Networks, Location → Facilities
```

### **Output You Get:**
```
VISUAL GRAPH showing:

👥 ENTITIES DISCOVERED:
├─ Person: Olena Kovalenko (Missing)
│  ├─ Last Known: Kyiv, Ukraine
│  ├─ Phone: +380-67-XXX-XXXX
│  └─ Social: Facebook, WhatsApp
├─ Person: Dmitro Kovalenko (Brother)
│  ├─ Location: Warsaw, Poland
│  └─ Social: Facebook (Active)
├─ Organization: ICRC Warsaw
│  ├─ Case Number: POL-2022-889
│  └─ Contact: caseworker@icrc.org
├─ Location: Shelter #4, Lviv
│  └─ Connection: Transfer record to Warsaw
└─ Document: Refugee Registration #UA-998877
   └─ Status: Approved

RELATIONSHIPS:
Olena → [Sibling] → Dmitro
Olena → [Registered At] → ICRC Warsaw
Olena → [Transferred From] → Shelter #4
```

### **File Output:**
- `family_graph.mtgx` - Maltego graph file
- `case_summary.pdf` - Relationship map for caseworkers

---

## 6️⃣ **SPIDERFOOT** - Automated OSINT (API/Local Hybrid)

**Use Case:** Running a comprehensive scan on a name/email to find all digital footprints across 200+ modules.

### **Input:**
```
Target: olena.kovalenko@example.com
Scan Type: All Modules (Safe Mode)
```

### **Output You Get:**
```
SCAN RESULTS - 200+ Modules Executed:

📧 EMAIL ADDRESSES (3 found):
olena.kovalenko@example.com (Personal)
o.kovalenko@redcross.org.ua (Volunteer Record)
olena.k@protonmail.com (New Account - 2022)

📱 PHONE NUMBERS (2 found):
+380-67-123-4567 (Ukraine - Roaming PL)
+48-501-XXX-XXX (Poland - New SIM)

🌐 DOMAINS & USER NAMES (5 found):
Facebook: olena.kovalenko.90
Telegram: @lena_k_ua
ProtonMail: olena.k

👤 PEOPLE (2 found):
Olena Kovalenko (DOB: 1990-05-15)
Dmitro Kovalenko (Associate/Sibling)

📄 LEAKED CREDENTIALS (0 found):
No breaches detected.

📡 TECHNOLOGIES DETECTED:
Email Provider: ProtonMail (Secure)
Device: Samsung Galaxy (from metadata)

⚠️ SECURITY ISSUES:
[INFO] Subject using secure email (Good)
[INFO] Phone roaming in safe country (Good)

SUMMARY:
Subject is alive, in Poland, using secure comms.
Contact via ProtonMail or Telegram.
```

---

## 7️⃣ **THEHARVESTER** - Email/Domain Harvester (Non-API)

**Use Case:** Finding email addresses associated with a specific NGO shelter or camp domain.

### **Input:**
```bash
theHarvester -d shelter4.lviv.ua -b all
```

### **Output You Get:**
```
[*] Searching in 30+ sources...

📧 EMAILS FOUND (12):
admin@shelter4.lviv.ua
caseworker1@shelter4.lviv.ua
caseworker2@shelter4.lviv.ua
volunteer_maria@shelter4.lviv.ua
...

🌐 HOSTS/SUBDOMAINS (4):
www.shelter4.lviv.ua
mail.shelter4.lviv.ua
registry.shelter4.lviv.ua (Internal?)

👤 PEOPLE/NAMES (8):
Maria Ivanova (Volunteer Coordinator)
Dmytro Petrov (Director)
...

ACTION:
Contact caseworker emails directly for inmate lists.
Do not scrape internal registry subdomain.
```

---

## 8️⃣ **HUNTER.IO** - Email Finder (API Required)

**Use Case:** Finding contact emails for NGO caseworkers when only names are known.

### **Input:**
```
Domain: icrc.org
Name: "Anna Schmidt" (Caseworker)
```

### **Output You Get:**
```json
{
  "emails_found": 3,
  "results": [
    {
      "email": "anna.schmidt@icrc.org",
      "first_name": "Anna",
      "last_name": "Schmidt",
      "position": "Family Links Caseworker",
      "department": "Warsaw Office",
      "verification": {
        "status": "valid",
        "smtp_check": true
      },
      "sources": ["LinkedIn", "ICRC Staff Directory"]
    }
  ]
}
```

### **Action:**
Email verified. Send formal reunification request with case details.

---

## 9️⃣ **AMASS** - Subdomain Enumeration (Non-API / Local)

**Use Case:** Discovering hidden portals or databases run by aid organizations (e.g., refugee registration portals).

### **Input:**
```bash
amass enum -d gov.ua
```

### **Output You Get:**
```
SUBDOMAINS DISCOVERED:
...
refugees.gov.ua (Registration Portal)
find-your-own.gov.ua (Missing Persons DB)
shelter-registry.gov.ua (Camp Locations)
...
```

### **Action:**
Direct family to `find-your-own.gov.ua` for official search.

---

## 🔟 **SHODAN** - IoT Search Engine (API Required)

**Use Case:** *Rarely used for people*, but can verify infrastructure of refugee camps (e.g., network availability, security cameras).

### **Input:**
```bash
shodan search "org:UNHCR"
```

### **Output You Get:**
```json
{
  "devices": [
    {
      "ip": "192.0.2.1",
      "location": "Warsaw, Poland",
      "org": "UNHCR Poland",
      "services": ["HTTP", "SSH"],
      "vulnerabilities": []
    }
  ]
}
```

### **Action:**
Verify network presence of aid organization in target region.

---

## 📊 SUMMARY TABLE - TOOL CLASSIFICATION

| Tool | API Required? | Best For | Safety Level |
|------|---------------|----------|--------------|
| **Sherlock** | ❌ No | Username tracking | High |
| **TinEye** | ❌ No (Web) | Photo matching | Medium (Privacy Risk) |
| **PhoneInfoga** | ❌ No | Phone status | High |
| **ExifTool** | ❌ No | GPS from photos | High (Local Only) |
| **Maltego** | ✅ Yes | Relationship mapping | Medium (Data Cloud) |
| **SpiderFoot** | ⚠️ Hybrid | Comprehensive scan | Medium |
| **theHarvester** | ❌ No | NGO contact discovery | High |
| **Hunter.io** | ✅ Yes | Email verification | High |
| **Amass** | ❌ No | Finding gov portals | High |
| **Shodan** | ✅ Yes | Infrastructure check | Low (Not for people) |

> **Recommendation:** Prioritize **Non-API** tools for field work where internet is unstable or operational security is critical. Use **API** tools only from secure locations with proper data handling agreements.
