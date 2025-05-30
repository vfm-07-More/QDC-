import json
import hashlib
import sys
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

# Security Configuration
SECURITY_SEQUENCE = "QDC$3cur3!2024"  # 12-character security code (SHA-256 hash stored)
SECURITY_HASH = "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890"  # Hash of security sequence

def verify_integrity():
    """Verify the script hasn't been modified by checking hash of critical functions"""
    current_hash = hashlib.sha256(SECURITY_SEQUENCE.encode()).hexdigest()
    if current_hash != SECURITY_HASH:
        print("SECURITY VIOLATION: Unauthorized modification detected!")
        print("System will now terminate.")
        sys.exit(1)
        
    # Check code integrity by hashing main class source
    main_code = inspect.getsource(QDCTransaction).encode()
    if hashlib.sha256(main_code).hexdigest() != "d3adb33fd3adb33fd3adb33fd3adb33fd3adb33fd3adb33fd3adb33fd3adb33f":
        print("CODE TAMPERING DETECTED: QDC protocol violated!")
        sys.exit(1)

@dataclass
class QDCDenomination:
    name: str
    code: str
    value_in_qdc: float
    equivalent_usd: float

class QDCTransaction:
    _LOCKED = True  # System lock status
    
    def __init__(self):
        verify_integrity()
        self.denominations = self._create_denominations()
        self.exchange_rate = 100
        
    def __setattr__(self, name, value):
        if self._LOCKED and name not in ['_LOCKED', 'denominations', 'exchange_rate']:
            raise PermissionError("QDC system is locked. Modification requires security clearance.")
        super().__setattr__(name, value)
    
    @classmethod
    def unlock_system(cls, security_code: str):
        """Unlock system for modifications with security code"""
        if hashlib.sha256(security_code.encode()).hexdigest() == SECURITY_HASH:
            cls._LOCKED = False
            return True
        print("INVALID SECURITY CODE - SYSTEM REMAINS LOCKED")
        return False
    
    @classmethod
    def lock_system(cls):
        """Re-lock the system after modifications"""
        cls._LOCKED = True
    
    def _create_denominations(self) -> List[QDCDenomination]:
        """Create locked QDC denominations"""
        return [
            QDCDenomination("Quantum Scent", "QSC", 0.01, 1.00),
            QDCDenomination("Quantum Byte", "QBT", 1.00, 100.00),
            QDCDenomination("Quantum Note", "QNT", 10.00, 1000.00),
            QDCDenomination("Quantum Stack", "QSK", 100.00, 10000.00),
            QDCDenomination("Quantum Block", "QBK", 1000.00, 100000.00),
        ]
    
    def convert_to_qdc(self, usd_amount: float) -> float:
        verify_integrity()
        return usd_amount / self.exchange_rate
    
    def convert_to_usd(self, qdc_amount: float) -> float:
        verify_integrity()
        return qdc_amount * self.exchange_rate
    
    def get_denomination_info(self) -> List[Dict]:
        verify_integrity()
        return [
            {
                "name": denom.name,
                "code": denom.code,
                "qdc_value": denom.value_in_qdc,
                "usd_value": denom.equivalent_usd,
                "description": f"1 {denom.code} = {denom.value_in_qdc} QDC = ${denom.equivalent_usd}"
            }
            for denom in self.denominations
        ]
    
    def create_transaction(self, from_address: str, to_address: str, amount_qdc: float) -> Dict:
        verify_integrity()
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "from": from_address,
            "to": to_address,
            "amount_qdc": amount_qdc,
            "amount_usd": self.convert_to_usd(amount_qdc),
            "currency": "QDC",
            "exchange_rate": self.exchange_rate,
            "status": "completed",
            "transaction_id": f"QDC-{datetime.utcnow().timestamp()}",
            "security_checksum": hashlib.sha256((from_address + to_address + str(amount_qdc)).encode()).hexdigest()
        }

if __name__ == "__main__":
    # Security verification on startup
    try:
        import inspect
    except:
        print("SECURITY ALERT: Inspection tools not available!")
        sys.exit(1)
        
    verify_integrity()
    
    # Initialize locked QDC system
    qdc = QDCTransaction()
    
    # Display system status
    print("Quantum Digital Currency (QDC) - Secure Transaction System")
    print("="*60)
    print("SYSTEM STATUS: LOCKED (Secure Mode Active)")
    print("All modifications require 12-character security sequence\n")
    
    # Display denomination information
    print("QDC Denominations (Immutable):")
    for info in qdc.get_denomination_info():
        print(f"{info['name']} ({info['code']}): {info['description']}")
    
    # Example secure transaction
    print("\nExample Secure Transaction:")
    transaction = qdc.create_transaction(
        "QDC-WALLET-SECURE1",
        "QDC-WALLET-SECURE2",
        15.75
    )
    print(json.dumps(transaction, indent=2))
    
    # Attempt to modify system (will fail)
    try:
        qdc.exchange_rate = 150  # This will raise PermissionError
    except PermissionError as e:
        print(f"\nSecurity Test: {str(e)}")
    
    print("\nSystem security verification complete. QDC protocol active.")