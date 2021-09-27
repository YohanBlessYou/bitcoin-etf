import Foundation

enum SystemError: Error {
	case ReadLineError
	case UndefinedError
}

struct ContactBookManager {
    private var contactBook: ContactBook = ContactBook()
	
    mutating func runManager() {
        while true {
			do{
				let menu = try receiveMenuFromCLI()
				if menu == "0" {
					print("\n[프로그램 종료]\n")
					return
				}
				if isValidMenu(menu: menu) == false {
					print("메뉴입력이 잘못되었습니다")
					continue
				}
				try playMenu(menu: menu)
			} catch SystemError.ReadLineError {
				print("ReadLine Error")
				return
			} catch {
				print("UndefinedError")
				return
			}
        }
    }

    private func receiveMenuFromCLI() throws -> String {
        print("1) 연락처 추가 2) 연락처 목록보기 3) 연락처 검색 x) 종료")
        print("메뉴를 선택해주세요 : ", terminator: "")
		
        if let menu = readLine() {
			return menu
		} else { 
			throw SystemError.ReadLineError 
		}
    }
	
	private func isValidMenu(menu: String) -> Bool {
		if menu == "1" || menu == "2" || menu == "3" {
			return true
		} else {
			return false
		}
	}
	
	private mutating func playMenu(menu: String) throws {
		switch menu {
		case "1": try contactBook.addContact()
		// case "2": try contactBook.showAllContacts()
		// case "3": try contactBook.searchAllInBook()
		default: throw SystemError.UndefinedError
		}
	}
}

struct ContactBook {
	private(set) var contactList: [ContactInfo] = []
	
	enum UserInputError: Error {
		case EmptyInput
		case WrongSeperatorUsage
		case WrongNameInput
		case WrongAgeInput
		case WrongPhoneNumberInput
	}
	
	mutating func addContact() throws {
		do {
			let rawString = try receiveContactInfoFromCLI() //공백 제거 기능 포함
			if rawString == "" { throw UserInputError.EmptyInput }
			
			let contactInfoArray = rawString.components(separatedBy: "/")
			if contactInfoArray.count != 3 { throw UserInputError.WrongSeperatorUsage }

			//영어는 전부 소문자로 변환하여 저장
			let name = try extractName(rawName: contactInfoArray[0])
			let age = try extractAge(rawAge: contactInfoArray[1]) 
			// let phoneNumber = try extractPhoneNumber(rawPhoneNumber: contactInfoArray[2])

			// let newContactInfo = ContactInfo(name: name, age: age, phoneNumber: phoneNumber)
			// self.contactList.append(newContactInfo)
			// print("입력한 정보는 \(newContactInfo.age)세 \(newContactInfo.name)(\(newContactInfo.phoneNumber))입니다.")
			// print("")
			
		} catch UserInputError.EmptyInput {
			print("아무것도 입력되지 않았습니다. 입력 형식을 확인해주세요.")
            return
		} catch UserInputError.WrongSeperatorUsage {
			print("슬래시(/) 사용이 잘못되었습니다. 입력 형식을 확인해주세요.")
            return
		} catch SystemError.ReadLineError {
			print("ReadLine Error")
			return
		} catch {
			print("UndefinedError")
			return
		}
	}
	
	private func receiveContactInfoFromCLI() throws -> String {
		print("연락처 정보를 입력해주세요 : ", terminator: "")
		if let contactInfo = readLine() {
			return contactInfo.replacingOccurrences(of: " ", with: "")
		} else { 
			throw SystemError.ReadLineError 
		}
	}

	private func extractName(rawName: String) throws -> String {
        if isValidName(rawName: rawName) == false { throw UserInputError.WrongNameInput }
        return rawName.lowercased()
    }
	private func extractAge(rawAge: String) throws -> Int {
		if isValidAge(rawAge: rawAge) == false { throw UserInputError.WrongAgeInput }
		
		guard let integerAge = Int(age) else { throw SystemError.UndefinedError }
		
		return integerAge
	}
	
    private func isValidName(rawName: String) -> Bool {
        for character in rawName {
            if isKoreanOrEnglish(character: character) == false { return false }
        }
        return true
    }
    private func isKoreanOrEnglish(character: Character) -> Bool {
        switch character {
        case "A"..."Z", "a"..."z", "가"..."힣": return true
        default: return false
        }
    }

    private func isValidAge(rawAge: String) -> Bool {
        if rawAge.count > 3 { return false }
        for character in rawAge {
            if isNumber(character: character) == false { return false }
        }
        return true
    }
    private func isNumber(character: Character) -> Bool {
        switch character {
        case "0"..."9": return true
        default: return false
        }
    }
    
	
}

struct ContactInfo {
    let name: String
    let age: Int
    let phoneNumber: String
}

// struct ContactInformationDictionary {
//     private(set) var contactInformationList: [ContactInformation] = []


//     mutating func sortList() {
//         self.contactInformationList.sort { $0.name < $1.name }
//     }

//     mutating func showAll() {
//         sortList()
//         self.contactInformationList.sort { $0.name < $1.name }
//         for eachInformation in self.contactInformationList {
//             print("- \(eachInformation.name) / \(eachInformation.age) / \(eachInformation.phoneNumber)")
//         }
//         print("")
//     }

//     mutating func searchAllInList() {
//         sortList()
//         while true {
//             print("연락처에서 찾을 이름을 입력해주세요 : ", terminator: "")
//             guard let name = readLine() else {
//                 print("알 수 없는 오류발생 : failed to run readline()")
//                 return
//             }
            
//             if ContactInformation.isValidName(string: name) == false {
//                 print("입력한 이름정보가 잘못되었습니다. 입력 형식을 확인해주세요.")
//                 continue
//             }

//             var existFlag = false
//             for eachInformation in self.contactInformationList {
//                 if eachInformation.name == name {
//                     print("- \(eachInformation.name) / \(eachInformation.age) / \(eachInformation.phoneNumber)")
//                     existFlag = true
//                 }
//             }
//             if existFlag == false {
//                 print("연락처에 \(name)이 없습니다.")
//             }
//             print("")
//             return
//         }
//     }

// }

// struct ContactInformation {
//     let name: String
//     let age: Int
//     let phoneNumber: String




//     private static func getAge(stringList: [String?]) -> Int? {
//         guard let age = stringList[1] else { 
//             print("알 수없는 오류발생")
//             return nil 
//         }

//         if isValidAge(string: age) == false { return nil }

//         guard let integerAge = Int(age) else { 
//             print("알 수없는 오류발생")
//             return nil 
//         }
//         return integerAge
//     }
//     private static func isValidAge(string age: String) -> Bool {
//         if age.count > 3 { return false }
//         for character in age {
//             if isNumber(character: character) == false { return false }
//         }
//         return true
//     }
//     private static func isNumber(character: Character) -> Bool {
//         switch character {
//         case "0"..."9": return true
//         default: return false
//         }
//     }
    
//     private static func getPhoneNumber(stringList: [String?]) -> String? {
//         guard let phoneNumber = stringList[2] else { 
//             print("알 수없는 오류발생")
//             return nil 
//         }
//         if isValidPhoneNumber(string: phoneNumber) == false { return nil }
//         return phoneNumber
//     }
//     private static func isValidPhoneNumber(string phoneNumber: String) -> Bool {
//         let splitPhoneNumber: [String?] = phoneNumber.split(separator: "-").map{ return String($0) }
//         if splitPhoneNumber.count != 3 { return false }

//         guard let firstNumbers = splitPhoneNumber[0], 
//             let secondNumbers = splitPhoneNumber[1], 
//             let thirdNumbers = splitPhoneNumber[2] else { 
//                 print("알 수없는 오류발생")
//                 return false
//             }

//         if firstNumbers.count != 2 && firstNumbers.count != 3 { return false }
//         for character in firstNumbers {
//             if isNumber(character: character) == false {  return false }
//         }
  
//         if secondNumbers.count != 3 && secondNumbers.count != 4 {  return false }
//         for character in firstNumbers {
//             if isNumber(character: character) == false {  return false }
//         }

//         if thirdNumbers.count != 4 {  return false }
//         for character in firstNumbers {
//             if isNumber(character: character) == false {  return false }
//         }

//         return true
//     }

// }




var contactBookManager = ContactBookManager()
contactBookManager.runManager()