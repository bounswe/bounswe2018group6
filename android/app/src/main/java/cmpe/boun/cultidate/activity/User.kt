package cmpe.boun.cultidate.activity


class User {
    // val oldunca sorun çıkıyor
    var firstname: String = ""
    var lastname: String = ""
    var username :String = ""
    var email :String = ""
    var password: String = ""
    var passwordconfirm: String =""

    constructor(firstname_:String, lastname_: String, username_: String, email_: String, password_: String, passwordconfirm_: String) {
        this.firstname = firstname_
        this.lastname = lastname_
        this.username  = username_
        this.email = email_
        this.password = password_
        this.passwordconfirm = passwordconfirm_
    }
}