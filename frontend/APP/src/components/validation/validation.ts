export class Validator {
    static noSpecSymbolReg: String = '^[-a-zA-Z0-9_]{1,30}$';
    static noCommsymbolReg: String = '^[-a-zA-Z0-9_]{1,256}$';
    static includeChineseReg: String = '[\u4e00-\u9fa5]';
    static regTest(reg: any, value: any) {
        let regInstance = new RegExp(reg);
        return regInstance.test(value);
    }
    static noSpecSymbol(param: any): boolean {
        if (Validator.regTest(Validator.noSpecSymbolReg, param)) {
            return true;
        } else {
            return false;
        }
    }
    static notNullCheck(param: any) {
        if (param && param.trim()) {
            return true;
        } else {
            return false;
        }
    }
    static noCommsymbol(param: any) {
        if (Validator.regTest(Validator.noCommsymbolReg, param)) {
            return true;
        } else {
            return false;
        }
    }
    static includeChinese(param: any) {
        if (Validator.regTest(Validator.includeChineseReg, param)) {
            return true;
        } else {
            return false;
        }
    }
}
