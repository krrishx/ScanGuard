# ScanGuard – Secure QR & Barcode Scanner

ScanGuard is a real-time QR and barcode scanning application built using Python and computer vision.  
It follows a security-first design by verifying scanned QR content before executing links, helping reduce risks from malicious or scam QR codes.

---

## 📌 Features

- Real-time QR and barcode scanning via webcam  
- Visual bounding box overlay on detected codes  
- Rule-based scam detection for scanned QR content  
- Classification of scanned data as **SAFE**, **SUSPICIOUS**, or **SCAM**  
- Automatic link opening only for **SAFE** URLs  
- Prevention of repeated or unintended link execution  
- Stable camera handling and clean shutdown on Windows  

---

## 🛠 Tech Stack

**Language**
- Python  

**Libraries**
- OpenCV  
- pyzbar  

**Concepts Used**
- Computer Vision  
- Real-time video processing  
- QR-based security risks  
- Rule-based URL verification  

---

## 🚀 How ScanGuard Works

- Captures live video frames from the webcam  
- Detects QR codes and barcodes in real time  
- Draws bounding boxes around detected codes  
- Analyzes scanned content using predefined security rules  
- Opens links automatically only when verified as **SAFE**  
- Blocks unsafe or suspicious QR content from execution  

---

## 🎯 Learning Outcomes

- Practical experience with real-time computer vision  
- Understanding of QR-code-based attack vectors  
- Handling webcam stability and backend issues on Windows  
- Writing event-driven, security-aware Python applications  
- Applying cybersecurity principles to everyday tools  

---

## 🔮 Future Enhancements

- GUI-based interface for improved usability  
- Advanced scam detection using threat intelligence APIs  
- Scan history and logging  
- Configurable auto-open and verification settings  
- Cross-platform optimization  
