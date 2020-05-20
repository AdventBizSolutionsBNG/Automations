import enum

import enum


class Modules(enum.Enum):
    ACTPBL = ('ACTPBL', 'ACCOUNT PAYABLES')
    ACTRBL = ('ACTRBL', 'ACCOUNT RECEIVABLES')
    RECO = ('RECO', 'RECONCILIATIONS')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class EnvTypes(enum.Enum):
    DEV = ('DEV', 'Development')
    QA = ('QA', 'QA or SIT')
    UAT = ('UAT', 'UAT')
    PROD = ('PROD', 'Production')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class CompanyCategories(enum.Enum):
    PROP = ('PROP', 'Proprietorship')
    OPC = ('OPC', 'One Person Company')
    PTNR = ('PTNR', 'Traditional Partnership')
    LLP = ('LLLP', 'Limited Liability Partnership (LLP)')
    PVT = ('PVT', 'Private Limited Company')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class CompanySubCategories(enum.Enum):
    PROP = ('PROP', 'Proprietorship')
    OPC = ('OPC', 'One Person Company')
    PTNR = ('PTNR', 'Traditional Partnership')
    LLP = ('LLLP', 'Limited Liability Partnership (LLP)')
    PVT = ('PVT', 'Private Limited Company')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class CompanyClass(enum.Enum):
    L = ('L', 'Listed')
    U = ('U', 'Unlisted')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class CompanyTypes(enum.Enum):
    L = ('L', 'Listed')
    U = ('U', 'Unlisted')

    @classmethod
    def get_value(cls, member):
        return member.value[0]

class ProcessingEngines(enum.Enum):
    PE = ('PE', 'ProductEngine')
    CE = ('CE', 'CoreEngine')
    EE = ('EE', 'ETLEngine')
    KE = ('KE', 'KPIEngine')
    QE = ('QE', 'QueryEngine')
    UI = ('UI', 'WEB UI ENGINE')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class Editions (enum.Enum):
    BSC = ('BE', 'Basic')
    STD = ('STD', 'Standard')
    ENT = ('ENT', 'Enterprise')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class LicensingTypes(enum.Enum):
    SUBCRPTN = ('SUBCRPTN', 'Subscription Based')
    PRPTL = ('PRPTL', 'Perpetual')
    EVAL = ('EVAL', 'Evaluation')

    @classmethod
    def get_value(cls, member):
        return member.value[0]

class AddressTypes(enum.Enum):
    H = ('H', 'Home')
    O = ('O', 'Office')

    @classmethod
    def get_value(cls, member):
        return member.value[0]

class Categories(enum.Enum):
    PROP = ('PROP', 'Proprietorship')
    OPC = ('OPC', 'One Person Company')
    PTNR = ('PTNR', 'Traditional Partnership')
    LLP = ('LLLP', 'Limited Liability Partnership (LLP)')
    PVT = ('PVT', 'Private Limited Company')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class EntityTypes(enum.Enum):
    LE = ('LE', 'Legal Entity')
    BU = ('BU', 'Business Unit')
    BR = ('BR', 'Branch Office')


    @classmethod
    def get_value(cls, member):
        return member.value[0]


class EntitySubTypes(enum.Enum):
    HO = ('HO', 'Head Office')
    DIV = ('DIV', 'Division')
    WH = ('WH', 'Warehouse')
    DC = ('DC', 'Distribution Center')
    RO = ('RO', 'Regional Office')
    MO = ('MO', 'Marketing Office')
    SO = ('SO', 'Sales Office')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class Regions(enum.Enum):
    EUR = ('EUR','Europe')
    APAC = ('APAC', 'Asia Pacific')
    NA = ('NA', 'North America')
    SA = ('SA', 'South America')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class OrgHieararchyTypes(enum.Enum):
    SE = ('SE', 'SingleEntity')
    SD = ('SD', 'SingleEntity With Division')
    ME = ('ME' , 'MultiEntity')
    MD = ('MD', 'MultiEntity with Division')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class CalenderTypes(enum.Enum):
    G = ('G', 'Gregorian')
    J = ('J' , 'Julian')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class DateHierarchy(enum.Enum):
    YQMD = ('YQMD', 'YEAR - QUARTER - MONTH - DAY')
    YMD = ('YMD', 'YEAR - MONTH - DAY')
    YMWD = ('YMDW', 'YEAR - MONTH - WEEK - DAY')
    YMDH = ('ME' , 'YEAR - MONTH - DAY - HOUR')
    YQMDH = ('YQMDH', 'YEAR - QUARTER - MONTH - DAY - HOUR')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class ObjectClass(enum.Enum):
    E = ('E', 'Event Based (Time Series)')
    M = ('M' , 'Master Data')
    P = ('P', 'Persona/Entity Based')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class AttributeType(enum.Enum):
    COL = ('COL', 'Column')
    DC = ('DC', 'Derived Column')
    CNST = ('CONSTANT', 'Constant')
    DCF = ('DCF', 'Derived Column using Function')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class DataTypes(enum.Enum):
    S = ('S', 'String')
    I = ('I', 'Inter')
    DICT = ('D', 'Dictionary')
    F = ('F', 'Float')
    SET = ('SET', 'Set')
    B = ('B', 'Boolean')
    D = ('D', 'Date')
    DT = ('DT', 'Date Time')
    A = ('A', 'Array')
    BYT = ('BYT', 'Bytes' )

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class InbuiltDataFormats(enum.Enum):
    EMAIL = ('EMAIL', 'Email')
    GSTIN = ('GSTIN', 'GSTIN')
    PAN = ('PAN', 'PANCARD')
    SSN = ('SSN', 'SSN')
    HSN = ('HSN', 'HSN')
    CUR = ('CUR', 'CURRENCY')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class PIITypes(enum.Enum):
    N = ('N', 'None')
    W = ('W', 'Weak')
    M = ('M', 'Medium')
    S = ('S', 'Strong')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class DimensionTypes(enum.Enum):
    D = ('D', 'By Date')
    V = ('V', 'By Value')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class MeasureTypes(enum.Enum):
    V = ('V', 'By Value')
    C = ('C', 'By Count')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class MeasureOperators(enum.Enum):
    S = ('S', 'SUM')
    C = ('C', 'COUNT')
    MIN = ('MIN', 'MIN')
    MAX = ('MAX','MAX')
    AVG = ('AVG','AVG')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class SourceConnectors(enum.Enum):
    DFILE = ('DFILE', 'Delimited Flat File')
    XLS = ('XLS', 'EXCEL FILE')
    MYSQL = ('MYSQL', 'MYSQL Database')
    HIVE = ('HIVE', 'HIVE Database')
    MONGO = ('MONGO',' MONGO Database')
    KQ = ('KQ', 'KAFKA QUEUE')
    S3 = ('S3', 'S3 Connector')
    BLB = ('BLB', 'AZURE BLOB')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class DestinationConnectors(enum.Enum):
    DFILE = ('DFILE', 'Delimited Flat File')
    MYSQL = ('MYSQL', 'MYSQL Database')
    HIVE = ('HIVE', 'HIVE Database')
    MONGO = ('MONGO',' MONGO Database')
    KQ = ('KQ', 'KAFKA QUEUE')
    S3 = ('S3', 'S3 Connector')
    BLB = ('BLB', 'AZURE BLOB')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class ContainerCategories(enum.Enum):
    G = ('G', 'Generic')
    U = ('U', 'User Defined')

    @classmethod
    def get_value(cls, member):
        return member.value[0]

class ContainerTypes(enum.Enum):
    T = ('T', 'Time Series')
    E = ('E', 'Entity Based')

    @classmethod
    def get_value(cls, member):
        return member.value[0]

class Operators(enum.Enum):
    SUM = ('SUM', 'SUM')
    MAX = ('MAX', 'MAX')
    MIN = ('MIN', 'MIN')
    AVG = ('AVG','AVG')
    COUNT  = ('COUNT','COUNT')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class KPIType(enum.Enum):
    P = ('P', 'Pre Populated KPI')
    R = ('R', 'Run Time KPI')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class ComponentType(enum.Enum):
    T = ('T', 'Time Series')
    V = ('V', 'Value Based')

    @classmethod
    def get_value(cls, member):
        return member.value[0]


class ComponentDisplayType(enum.Enum):
    W = ('W', 'Widget')
    T = ('T', 'Tabular')
    S = ('S', 'Singular')

    @classmethod
    def get_value(cls, member):
        return member.value[0]

