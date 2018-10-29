import httpService from "services/HttpService";

class api {
    doLogin = (username, password) => {
        return httpService.fetch({
            path: "auth/",
            method: "POST",
            body: {
                username,
                password
            },
            sendToken: false
        });
    };
    
    doRegister = (first_name, last_name,  username, email, birth_date, password, 
        is_corporate_user, corporate_profile) => {
        return httpService.fetch({
            path: "signup/",
            method: "POST",
            body: {
                first_name,
                last_name,
                birth_date,
                username,
                email,
                password,
                is_corporate_user,
                corporate_profile,
            },
            sendToken: false
        });
    };

    doLogout = () => {

    }
}

export default new api();
