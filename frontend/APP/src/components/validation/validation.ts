export class Validator {
    // need modify noSpecSymbolReg
    static noSpecSymbolReg: RegExp = /[\x00-\xff]+/;
    static noCommsymbolReg: RegExp = /[\x00-\xff]+/;
    static oidReg: RegExp = /^[1-9]+(\.[1-9]+)*$/;
    static numReg: RegExp = /[0-9]/;
    static xOffsetReg: RegExp = /^-?[1-9]\d*$/;
    static offsetReg: RegExp = /^-?[0-9]\d*$/;
    static regTest(reg: any, value?: any) {
        if (value) {
            let regInstance = new RegExp(reg);
            return regInstance.test(value);
        } else {
            try {
                let regInstance = new RegExp(reg);
                return true;
            } catch (e) {
                return false;
            }
        }
    }
    static noSpecSymbol(param: any): boolean {
        if (Validator.regTest(Validator.noSpecSymbolReg, param)) {
            return true;
        } else {
            return false;
        }
    }
    static notNullCheck(param: any) {
        if (param && param.toString().trim()) {
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
    static oidRegCheck(param: any) {
        if (Validator.regTest(Validator.oidReg, param)) {
            return true;
        } else {
            return false;
        }
    }
    static numRegCheck(param: any) {
        if (Validator.regTest(Validator.numReg, param)) {
            return true;
        } else {
            return false;
        }
    }
    static xOffsetCheck(param: any) {
        if (Validator.regTest(Validator.xOffsetReg, param)) {
            return true;
        } else {
            return false;
        }
    }
    static offsetCheck(param: any) {
        if (Validator.regTest(Validator.offsetReg, param)) {
            return true;
        } else {
            return false;
        }
    }
}
