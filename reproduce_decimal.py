
try:
    from bson.decimal128 import Decimal128
    from decimal import Decimal
    
    val = Decimal128(Decimal("10.50"))
    qty = 2
    
    print(f"Value: {val} (type: {type(val)})")
    
    try:
        res = val * qty
        print(f"Direct multiplication success: {res} (type: {type(res)})")
    except Exception as e:
        print(f"Direct multiplication failed: {e}")

    try:
        res = float(str(val)) * qty
        print(f"Float conv multiplication success: {res} (type: {type(res)})")
    except Exception as e:
        print(f"Float conv multiplication failed: {e}")

except ImportError:
    print("pymongo/bson not installed, cannot test Decimal128 directly.")
