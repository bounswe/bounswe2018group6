import { getCookie, TOKEN_COOKIE } from "./cookies.js";

const Configuration = {
    API_URL: process.env.REACT_APP_API_URL,
    HTTP_TIMEOUT_MS: 40000 /* 40 sec */
};

class HttpService {
    fetch(requestOptions) {
        return new Promise((resolve, reject) => {
            const url = this._createUrl(requestOptions);
            const overriddenHeaders = requestOptions.headers || {};
            const sendToken = requestOptions.sendToken || false;
            const processedRequestOptions = {
                ...requestOptions,
                body: JSON.stringify(requestOptions.body),
                headers: {
                    "Content-Type": "application/json",
                    Authorization:
                        typeof sendToken === "undefined"
                            ? "JWT " + getCookie(TOKEN_COOKIE)
                            : sendToken === false
                            ? null
                            : "JWT " + getCookie(TOKEN_COOKIE),
                    ...overriddenHeaders
                },
                timeout: Configuration.HTTP_TIMEOUT_MS,
            };

            let fetchStatus = null;

            fetch(url, processedRequestOptions)
                .then(fetchRes => {
                    fetchStatus = fetchRes.status;
                    //console.log("#request", processedRequestOptions);
                    //console.log("#response", fetchRes);
                    return fetchRes.json();
                })
                .then(res => {
                    const response = {
                        status: fetchStatus,
                        responseBody: res
                    };
                    resolve(response);
                    return response;
                })
                .catch(err => {
                    console.log("HttpService.js:", err);
                    reject({
                        detail: "Something wrong happened when try to fetch data. Code-API"
                    });
                });
        });
    }

    _createUrl(requestOptions) {
        let url = requestOptions.apiPath || Configuration.API_URL;
        url = requestOptions.path ? url + requestOptions.path : url;
        return url;
    }
}

export default new HttpService();