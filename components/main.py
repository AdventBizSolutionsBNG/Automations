from core.coreEngine import CoreEngine
from product.ProductEngine import ProductEngine
def main():
    for arg in sys.argv[1:]:
        c = CoreEngine()
        p = ProductEngine
        print(c.constants["CODE"]["dataType"])

if __name__=="__main__":
    main()