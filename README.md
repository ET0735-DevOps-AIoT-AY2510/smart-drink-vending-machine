### **Smart Drink Vending Machine Overview**

Smart vending machine functionalities, covering user interactions, payments, monitoring, security, and admin interface.

---

### **Main Menu & Payment**

* **Home Screen:** Displays "Welcome, please select a drink" on startup.  
* **Drink Selection:** Users enter drink number and confirm with '#'. System validates availability.  
* **Barcode Scanning:** Pressing '#' without entering a number activates barcode scanning. Users can redeem drinks purchased online, and admins can scan a barcode to unlock the door.  
* **Payment Options:** Card or QR Code.  
* **Cancel & Return:** Pressing '*' at any point returns the machine to the home screen.  
* **Inactivity Timeout:** Returns to home screen after 15 seconds.

---

### **Payment Processing**

* **Card Payment:** Tap card; success or decline shown.  
* **QR Code Payment:** Scan valid QR code to pay; invalid codes give feedback.

---

### **Dispensing & Stock Management**

* **Dispensing:** Shows "Dispensing" after payment and releases drink.  
* **Stock Tracking:** Internal inventory updated automatically; ultrasonic sensor verifies stock.  
* **Discrepancy & Low Stock Alerts:** Email alerts for jams, extra dispenses, or stock below five units.

---

### **Environmental & Security Monitoring**

* **Temperature Control:** Alerts above 10°C; machine goes "Out of order" at 20°C with warnings.  
* **Liquid Leakage:** Moisture sensor triggers alert and machine goes "Out of order".  
* **Burglar Detection:** IR sensor/accelerometer triggers alarm, LED, and camera email.  
* **Graceful Handling:** Ongoing transactions complete before "Out of order" state.

---

### **Admin & Maintenance**

* **Admin Passcode:** Disables alarm and unlocks door; alarm reactivates on closing.  
* **Door Open Alert:** Buzzer sounds if door remains open 3–20 minutes; duration adjustable by admin. Silenced by closing door or pressing any key.

---

### **User & Admin Web API**

* **User Functions:** Account management, view menu, online purchase generates redeemable code/barcode. If the machine is "Out of order", the barcode will show a cross and indicate that redemption is currently unavailable.  
* **Admin Dashboard:** Monitor and adjust stock, view temporary passcode, manage alert emails.

---

### **Database**

* **Admin Credentials:** Predefined login details for authorized personnel.  
* **User Credentials:** Stores registered user accounts.  
* **Reserved Stock:** Tracks paid but uncollected drinks.  
* **Physical Stock:** Records actual drink inventory inside the machine.

---

### Running with Docker

1. **Build the Docker Image**
```bash
docker compose build
````

2. **Run the Interactive Docker Shell**

```bash
docker run -it \
  --privileged \
  --device=/dev/* \
  -v /run/udev:/run/udev:ro \
  -p 5000:5000 \
  dcpe_2a_01_group2-vending-machine sh
```

### Once in the shell

1. **Initialise the database (once)**

```bash
python3 database_setup.py
```

2. **Run the main Python script in background**

```bash
python3 F123456789.py &
```

3. **Change the mock temperature for testing purposes**

```bash
python3 settemp.py <value>
```

---

### Google Drive for Demo Video

[https://drive.google.com/drive/folders/1g4HWi8hh0Cg1HQ0AUzOtiVWKkkE3ZSNq](https://drive.google.com/drive/folders/1g4HWi8hh0Cg1HQ0AUzOtiVWKkkE3ZSNq)

### Contributions

**Nathan:** Responsible for F1, F4, F5, and F9. Completed PyTests for F1, F2, F4, F5, F7, and F9, SRS documentation and flowcharts, integration of F1, F4, and F5, and preparation of Excel sheets for PyTest results and physical test cases.  
*GitHub:* `FootOfTheFoot`, `FootOfTheFoot-Project`  

**Terence:** Responsible for F3, F6, and F8. Completed PyTests for F3, F6, and F8, SRS documentation and flowcharts, integration of all other functionalities, and created the files for containerisation, database, and admin dashboard.  
*GitHub:* `T3rrybl3`, `terence-tng`  

**Mark:** Responsible for F7 and SRS flowcharts.  
*GitHub:* `bununu2`  

**Zayan:** Responsible for F2, user API design, and SRS flowcharts.  
*GitHub:* `zayanfm`
