export class Validator {
    // full-width and half-width without space, comma , quotes and double quotes
    static fullWithoutSpecialReg: RegExp = /^(?!.*[, \'\"])/;
    // full-width with space, comma , quotes and double quotes
    static halfWithoutSpecialReg: RegExp = /[^\x00-\xff]|[\x22|\x20|\x27\x2c]/;
    // only half-width
    static halfReg: RegExp = /[^\x00-\xff]/;
    // static oidReg: RegExp = /^[1-9](\.(?!0+)\d+)*$/;
    // static oidReg: RegExp = /^1(\.(?!0)\d+)*$/;
    // static oidReg: RegExp = /^1(\.(?!0+)\d+)*$/;
    static oidReg: RegExp = /^1(\.\d+)*$/;
    // static numReg: RegExp = /^\+?[1-9]\d*$/;
    static numReg: RegExp = /^(0|[1-9]+\d*)$/;
    static xOffsetReg: RegExp = /^-?[1-9]\d*$/;
    static offsetReg: RegExp = /^-?[0-9]\d*$/;
    static portReg: RegExp = /^([0-9]|[1-9]\\d|[1-9]\\d{2}|[1-9]\\d{3}|[1-5]\\d{4}|6[0-4]\\d{3}|65[0-4]\\d{2}|655[0-2]\\d|6553[0-5])$/;
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
    static fullWithoutSpecial(param: any): boolean {
        if (Validator.regTest(Validator.fullWithoutSpecialReg, param)) {
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
    static halfWithoutSpecial(param: any) {
        if (Validator.regTest(Validator.halfWithoutSpecialReg, param)) {
            return false;
        } else {
            return true;
        }
    }
    static halfWidthReg(param: any) {
        if (Validator.regTest(Validator.halfReg, param)) {
            return false;
        } else {
            return true;
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
    static portCheck(param: any) {
        if (Validator.regTest(Validator.portReg, param)) {
            return true;
        } else {
            return false;
        }
    }
}
